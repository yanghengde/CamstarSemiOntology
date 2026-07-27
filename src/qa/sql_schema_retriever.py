"""Read-only physical schema context for the Camstar SQL assistant.

The ontology intentionally hides some infrastructure fields. SQL generation
must instead see the authoritative CSV rows, including primary keys and exact
foreign-key columns.
"""

from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TABLES_CSV = PROJECT_ROOT / "docs" / "Database_Tables.csv"
FIELDS_CSV = PROJECT_ROOT / "docs" / "Database_Fields.csv"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


@lru_cache(maxsize=1)
def _schema():
    tables = {
        row["CDOName"]: row
        for row in _read_csv(TABLES_CSV)
        if row.get("CDOName")
    }
    fields_by_table: dict[str, list[dict[str, str]]] = {}
    for row in _read_csv(FIELDS_CSV):
        if row.get("CDOName") and row.get("FieldName"):
            fields_by_table.setdefault(row["CDOName"], []).append(row)
    return tables, fields_by_table


def build_sql_schema_context(
    class_names: list[str],
    *,
    question: str = "",
    max_tables: int = 8,
    max_fields: int = 560,
) -> str:
    """Format exact physical tables, fields, PKs and FKs for an LLM prompt."""
    tables, fields_by_table = _schema()
    requested = list(class_names)
    from src.qa.sql_domain_context import (
        HISTORY_MAINLINE_TABLES,
        history_mainline_companion_tables,
    )

    history_domain_tables = {"HistoryMainline"}
    for companion_group in HISTORY_MAINLINE_TABLES.values():
        history_domain_tables.update(companion_group)
    if history_domain_tables.intersection(requested):

        # HistoryMainline may be appended after many persisted selections.
        # Prioritize the active transaction domain so the six-table cap cannot
        # discard the table the user is currently asking about.
        requested = (
            ["HistoryMainline"]
            + history_mainline_companion_tables(question)
            + [name for name in requested if name != "HistoryMainline"]
        )

    selected = []
    for name in requested:
        if name in tables and name not in selected:
            selected.append(name)
        if len(selected) >= max_tables:
            break

    if not selected:
        return "未匹配到物理表。不得猜测表名或字段名，应要求用户指定表或在图中选择节点。"

    lines = [
        "以下内容直接来自 Database_Tables.csv 与 Database_Fields.csv；字段名区分大小写按原样输出。",
    ]
    remaining = max_fields
    for table_name in selected:
        table = tables[table_name]
        fields = fields_by_table.get(table_name, [])
        lines.append(
            f"\n### 物理表 [{table_name}] "
            f"(CDODefId={table.get('CDODefId', '')}, Workspace={table.get('Workspace', '')})"
        )

        # Put PK/FK rows first so join evidence is retained if the context cap
        # is reached, then keep the CSV order for ordinary fields.
        ordered = sorted(
            enumerate(fields),
            key=lambda item: (
                item[1].get("IsPrimaryKey", "").lower() != "true",
                item[1].get("IsForeignKey", "").lower() != "true",
                item[0],
            ),
        )
        for _, field in ordered[:remaining]:
            flags = []
            if field.get("IsPrimaryKey", "").lower() == "true":
                flags.append("PK")
            if field.get("IsCandidateKey", "").lower() == "true":
                flags.append("候选键")
            if field.get("IsList", "").lower() == "true":
                flags.append("List")
            if (
                field.get("IsForeignKey", "").lower() == "true"
                and field.get("FKTableName")
            ):
                flags.append(
                    f"FK→[{field['FKTableName']}].[{field.get('FKFieldName') or '?'}]"
                )
            flag_text = f" | {'; '.join(flags)}" if flags else ""
            lines.append(
                f"- [{field['FieldName']}] "
                f"(DataTypeCode={field.get('DataType', '')}, "
                f"Precision={field.get('Precision', '')}, "
                f"Scale={field.get('Scale', '')}{flag_text})"
            )
        remaining -= min(len(fields), remaining)
        if remaining <= 0:
            lines.append("- ……字段上下文达到上限；未显示的字段不得猜测。")
            break

    return "\n".join(lines)
