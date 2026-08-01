"""Reviewed CSV import for the physical Camstar ontology skeleton.

CSV rows are never published directly.  Existing ontology classes are treated
as the reviewed business allow-list; every previously unseen CDO remains an
unchecked candidate until the user explicitly selects it in the settings UI.
"""

from __future__ import annotations

import csv
import io
import json
import os
import re
import tempfile
import threading
import time
import uuid
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from scripts.generate_ontology_batch import relation_name
from scripts.validate_ontology_vs_csv import (
    canonical_physical_fields,
    expected_type,
    normalize_field_name,
)
from web.shared import PROJECT_ROOT, driver


router = APIRouter(prefix="/api/ontology-import", tags=["ontology-import"])

ONTOLOGY_DIR = Path(PROJECT_ROOT) / "src" / "ontology" / "wiki_kb"
IMPORTED_ONTOLOGY = ONTOLOGY_DIR / "csv_business_import_ontology.json"
IMPORT_MANIFEST = Path(PROJECT_ROOT) / "data" / "ontology_import_manifest.json"
DESCRIPTION_TRANSLATION_CACHE = Path(PROJECT_ROOT) / "data" / "import_description_translations.json"
MAX_UPLOAD_BYTES = 40 * 1024 * 1024
SESSION_TTL_SECONDS = 60 * 60

_sessions: dict[str, dict[str, Any]] = {}
_session_lock = threading.RLock()

_TECHNICAL_PATTERNS = (
    (re.compile(r"(?:Changes|Maint|Inquiry|Service)$", re.I), "维护、查询或服务型 CDO"),
    (re.compile(r"(?:HistoryDetails?|Txn|Txns|Map|Mapping|ListItem|Details)$", re.I), "历史明细、事务或桥接型 CDO"),
    (re.compile(r"(?:Enum|Message|QueryDef|InquiryDef)$", re.I), "枚举、消息或查询定义型 CDO"),
)


class ImportApplyRequest(BaseModel):
    importId: str = Field(min_length=1, max_length=80)
    selected: list[str] = Field(default_factory=list, max_length=5000)


def _read_csv_upload(upload: UploadFile, required: set[str]) -> list[dict[str, str]]:
    raw = upload.file.read(MAX_UPLOAD_BYTES + 1)
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail=f"{upload.filename or 'CSV'} 超过 40 MB 限制")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        try:
            text = raw.decode("gb18030")
        except UnicodeDecodeError as exc:
            raise HTTPException(status_code=422, detail=f"{upload.filename or 'CSV'} 不是 UTF-8 或 GB18030 编码") from exc
    reader = csv.DictReader(io.StringIO(text))
    columns = {str(name or "").strip() for name in (reader.fieldnames or [])}
    missing = sorted(required - columns)
    if missing:
        raise HTTPException(status_code=422, detail=f"{upload.filename or 'CSV'} 缺少列：{', '.join(missing)}")
    rows = []
    for row in reader:
        normalized = {str(key or "").strip(): str(value or "").strip() for key, value in row.items()}
        if any(normalized.values()):
            rows.append(normalized)
    return rows


def _reviewed_class_names() -> set[str]:
    names: set[str] = set()
    for path in ONTOLOGY_DIR.glob("*_ontology.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            continue
        names.update(
            str(item.get("className") or "").strip()
            for item in payload.get("classes", [])
            if item.get("className")
        )
    try:
        from web.routers.graph import _graph_overview_cached

        names.update(str(item.get("id") or "") for item in _graph_overview_cached().get("nodes", []))
    except Exception:
        pass
    return {name for name in names if name}


def _candidate_status(class_name: str, reviewed: set[str]) -> tuple[str, str, bool]:
    if class_name in reviewed:
        return "approved", "当前图谱中已审核的业务对象", True
    for pattern, reason in _TECHNICAL_PATTERNS:
        if pattern.search(class_name):
            return "excluded", reason, False
    return "review", "新发现的 CDO，需要确认是否具有独立业务意义", False


def _purge_expired_sessions() -> None:
    cutoff = time.time() - SESSION_TTL_SECONDS
    for session_id in [key for key, value in _sessions.items() if value["createdAt"] < cutoff]:
        _sessions.pop(session_id, None)


def _designer_description_for(class_name: str, catalog: dict[str, dict[str, str]]) -> str:
    matched = catalog.get(class_name.casefold())
    if not matched and class_name.startswith("A_"):
        matched = catalog.get(class_name[2:].casefold())
    return str((matched or {}).get("description") or "")


def _load_description_cache() -> dict[str, str]:
    cache: dict[str, str] = {}
    if DESCRIPTION_TRANSLATION_CACHE.exists():
        try:
            payload = json.loads(DESCRIPTION_TRANSLATION_CACHE.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                cache.update({str(key): str(value) for key, value in payload.items() if key and value})
        except (OSError, json.JSONDecodeError):
            pass
    try:
        from web.routers.i18n import _load_store

        for value in _load_store()["translations"]["nodeDescriptions"].values():
            english = str(value.get("en") or "").strip()
            chinese = str(value.get("zh") or "").strip()
            if english and chinese:
                cache.setdefault(english, chinese)
    except Exception:
        pass
    return cache


def _save_description_cache(cache: dict[str, str]) -> None:
    DESCRIPTION_TRANSLATION_CACHE.parent.mkdir(parents=True, exist_ok=True)
    temporary = DESCRIPTION_TRANSLATION_CACHE.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(DESCRIPTION_TRANSLATION_CACHE)


def _translate_candidate_descriptions(descriptions: list[str]) -> tuple[dict[str, str], str]:
    """Translate what is not cached; return English unchanged when LLM is unavailable."""
    unique = list(dict.fromkeys(value.strip() for value in descriptions if value.strip()))
    cache = _load_description_cache()
    pending = [value for value in unique if value not in cache]
    if not pending:
        return {value: cache[value] for value in unique}, ""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return {value: cache[value] for value in unique if value in cache}, "未配置大模型，中文描述暂时显示数据库英文原文。"
    try:
        from openai import OpenAI
        from scripts.build_designer_display_translations import translate_batch

        client = OpenAI(
            api_key=api_key,
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
            timeout=float(os.getenv("LLM_TIMEOUT", "120")),
        )
        model = os.getenv("LLM_MODEL", "deepseek-chat")
        batches = [pending[index:index + 35] for index in range(0, len(pending), 35)]
        with ThreadPoolExecutor(max_workers=min(4, max(1, len(batches)))) as executor:
            futures = {executor.submit(translate_batch, client, model, "en_to_zh", batch): batch for batch in batches}
            for future in as_completed(futures):
                batch = futures[future]
                translated = future.result()
                cache.update(zip(batch, translated))
        _save_description_cache(cache)
        return {value: cache[value] for value in unique}, ""
    except Exception as exc:
        if cache:
            _save_description_cache(cache)
        return (
            {value: cache[value] for value in unique if value in cache},
            f"大模型或网络暂时不可用，未翻译的描述显示英文原文：{exc}",
        )


@router.post("/analyze")
def analyze_import(
    tables: UploadFile = File(...),
    fields: UploadFile = File(...),
    database: str = Form(...),
):
    database = database.strip().lower()
    if database not in {"oracle", "sqlserver"}:
        raise HTTPException(status_code=422, detail="数据库类型必须是 Oracle 或 SQL Server")
    table_rows = _read_csv_upload(tables, {"CDODefId", "CDOName", "Workspace"})
    field_rows = _read_csv_upload(
        fields,
        {"CDODefId", "CDOName", "FieldID", "FieldName", "IsForeignKey", "FKTableName", "DataType"},
    )
    table_by_name: dict[str, dict[str, str]] = {}
    duplicates: set[str] = set()
    for row in table_rows:
        name = row.get("CDOName", "")
        if not name:
            continue
        if name in table_by_name:
            duplicates.add(name)
        table_by_name[name] = row
    if duplicates:
        sample = ", ".join(sorted(duplicates)[:10])
        raise HTTPException(status_code=422, detail=f"表 CSV 存在重复 CDOName：{sample}")

    fields_by_class: dict[str, list[dict[str, str]]] = defaultdict(list)
    orphan_fields: set[str] = set()
    for row in field_rows:
        name = row.get("CDOName", "")
        if not name:
            continue
        if name not in table_by_name:
            orphan_fields.add(name)
        fields_by_class[name].append(row)
    if orphan_fields:
        sample = ", ".join(sorted(orphan_fields)[:10])
        raise HTTPException(status_code=422, detail=f"字段 CSV 引用了表 CSV 中不存在的 CDO：{sample}")

    reviewed = _reviewed_class_names()
    description_catalog: dict[str, dict[str, str]] = {}
    description_warning = ""
    try:
        from web.designer_metadata import load_cdo_description_catalog

        description_catalog = load_cdo_description_catalog(database)
    except Exception as exc:
        label = "Oracle" if database == "oracle" else "SQL Server"
        description_warning = f"无法连接 {label} 获取 CDO 描述，候选结构仍可审核：{exc}"
    english_descriptions = {
        name: _designer_description_for(name, description_catalog)
        for name in table_by_name
    }
    translations: dict[str, str] = {}
    if description_catalog:
        translations, translation_warning = _translate_candidate_descriptions(list(english_descriptions.values()))
        if translation_warning:
            description_warning = "；".join(value for value in (description_warning, translation_warning) if value)
    candidates = []
    for name, table in sorted(table_by_name.items(), key=lambda item: item[0].casefold()):
        canonical = canonical_physical_fields(fields_by_class.get(name, []), name)
        status, reason, selected = _candidate_status(name, reviewed)
        relationship_count = sum(
            1
            for field in canonical
            if str(field.get("IsForeignKey", "")).lower() == "true" and field.get("FKTableName")
        )
        candidates.append({
            "className": name,
            "cdoDefId": table.get("CDODefId", ""),
            "workspace": table.get("Workspace", ""),
            "propertyCount": len(canonical),
            "relationshipCount": relationship_count,
            "status": status,
            "reason": reason,
            "selected": selected,
            "descriptionEn": english_descriptions.get(name, ""),
            "descriptionZh": translations.get(english_descriptions.get(name, ""), ""),
        })

    session_id = uuid.uuid4().hex
    with _session_lock:
        _purge_expired_sessions()
        _sessions[session_id] = {
            "createdAt": time.time(),
            "tables": table_by_name,
            "fields": dict(fields_by_class),
            "candidates": {item["className"]: item for item in candidates},
            "reviewed": reviewed,
            "database": database,
        }
    summary = {
        "tables": len(table_by_name),
        "fields": len(field_rows),
        "approved": sum(item["status"] == "approved" for item in candidates),
        "review": sum(item["status"] == "review" for item in candidates),
        "excluded": sum(item["status"] == "excluded" for item in candidates),
        "defaultSelected": sum(item["selected"] for item in candidates),
        "described": sum(bool(item["descriptionEn"]) for item in candidates),
        "translated": sum(bool(item["descriptionZh"]) for item in candidates),
    }
    return {
        "importId": session_id,
        "database": database,
        "summary": summary,
        "descriptionWarning": description_warning,
        "candidates": candidates,
    }


def _property_definition(field: dict[str, str], class_name: str) -> dict[str, Any]:
    name = normalize_field_name(field, class_name)
    item: dict[str, Any] = {
        "name": name,
        "type": expected_type(field),
        "description": "",
        "sourceFieldId": field.get("FieldID", ""),
    }
    if name == "name" or str(field.get("IsPrimaryKey", "")).lower() == "true":
        item["required"] = True
    return item


def _write_imported_ontology(new_classes: list[dict], relationships: list[dict]) -> None:
    existing = {"module": "csv_business_import", "classes": [], "relationships": []}
    if IMPORTED_ONTOLOGY.exists():
        existing = json.loads(IMPORTED_ONTOLOGY.read_text(encoding="utf-8-sig"))
    class_by_name = {item["className"]: item for item in existing.get("classes", [])}
    for item in new_classes:
        class_by_name[item["className"]] = item
    relationship_by_key = {
        (item.get("fromClass"), item.get("toClass"), item.get("relationName")): item
        for item in existing.get("relationships", [])
    }
    for item in relationships:
        relationship_by_key[(item["fromClass"], item["toClass"], item["relationName"])] = item
    payload = {
        "module": "csv_business_import",
        "classes": sorted(class_by_name.values(), key=lambda item: item["className"].casefold()),
        "relationships": sorted(
            relationship_by_key.values(),
            key=lambda item: (item["fromClass"].casefold(), item["toClass"].casefold(), item["relationName"]),
        ),
    }
    IMPORTED_ONTOLOGY.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix="csv-business-import-", suffix=".json", dir=IMPORTED_ONTOLOGY.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary, IMPORTED_ONTOLOGY)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _write_manifest(selected: set[str], source_count: int) -> None:
    current: dict[str, Any] = {"version": 1, "approvedBusinessObjects": []}
    if IMPORT_MANIFEST.exists():
        try:
            current.update(json.loads(IMPORT_MANIFEST.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError):
            pass
    approved = set(current.get("approvedBusinessObjects") or []) | selected
    current.update({
        "approvedBusinessObjects": sorted(approved, key=str.casefold),
        "lastImportAt": int(time.time() * 1000),
        "lastSourceTableCount": source_count,
    })
    IMPORT_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    temporary = IMPORT_MANIFEST.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(IMPORT_MANIFEST)


@router.post("/apply")
def apply_import(request: ImportApplyRequest):
    with _session_lock:
        _purge_expired_sessions()
        session = _sessions.get(request.importId)
    if session is None:
        raise HTTPException(status_code=404, detail="导入分析已过期，请重新选择 CSV")
    selected = {name.strip() for name in request.selected if name.strip()}
    unknown = selected - set(session["candidates"])
    if unknown:
        raise HTTPException(status_code=422, detail=f"包含未知 CDO：{', '.join(sorted(unknown)[:10])}")
    if not selected:
        raise HTTPException(status_code=422, detail="请至少选择一个经过确认的业务对象")

    reviewed: set[str] = set(session["reviewed"])
    allowed_targets = reviewed | selected
    class_batch = []
    property_batch = []
    relationship_batch = []
    new_class_payloads = []
    imported_relationships = []
    seen_relationships: set[tuple[str, str, str]] = set()

    for class_name in sorted(selected, key=str.casefold):
        table = session["tables"][class_name]
        canonical = canonical_physical_fields(session["fields"].get(class_name, []), class_name)
        class_batch.append({"name": class_name, "cdoDefId": table.get("CDODefId", ""), "workspace": table.get("Workspace", "")})
        properties = [_property_definition(field, class_name) for field in canonical]
        for prop in properties:
            property_batch.append({"className": class_name, **prop})
        if class_name not in reviewed:
            new_class_payloads.append({
                "className": class_name,
                "chineseName": "",
                "description": "",
                "sourceCDODefId": table.get("CDODefId", ""),
                "properties": properties,
            })
        for field in canonical:
            target = field.get("FKTableName", "")
            if expected_type(field) != "Navigation" or not target or target not in allowed_targets:
                continue
            name = relation_name(normalize_field_name(field, class_name))
            key = (class_name, target, name)
            if key in seen_relationships:
                continue
            item = {
                "fromClass": class_name,
                "toClass": target,
                "relationName": name,
                "cardinality": "MANY_TO_ONE",
                "description": "",
            }
            relationship_batch.append(item)
            if class_name not in reviewed or target not in reviewed:
                imported_relationships.append(item)
            seen_relationships.add(key)

    try:
        with driver.session() as neo_session:
            neo_session.run("""
                UNWIND $batch AS item
                MERGE (c:OntologyClass {name: item.name})
                ON CREATE SET c.chineseName = '', c.description = '', c.layer = 'Config'
                SET c.sourceCDODefId = item.cdoDefId,
                    c.sourceWorkspace = item.workspace,
                    c.schemaSource = 'CSV',
                    c.schemaImportedAt = timestamp()
            """, batch=class_batch).consume()
            neo_session.run("""
                UNWIND $batch AS item
                MATCH (c:OntologyClass {name: item.className})
                MERGE (p:OntologyProperty {className: item.className, name: item.name})
                ON CREATE SET p.description = ''
                SET p.dataType = item.type,
                    p.required = coalesce(item.required, false),
                    p.sourceFieldId = item.sourceFieldId,
                    p.schemaSource = 'CSV',
                    p.schemaImportedAt = timestamp()
                MERGE (c)-[:HAS_PROPERTY]->(p)
            """, batch=property_batch).consume()
            neo_session.run("""
                UNWIND $batch AS item
                MATCH (source:OntologyClass {name: item.fromClass})
                MATCH (target:OntologyClass {name: item.toClass})
                MERGE (source)-[r:ONTOLOGY_RELATION {name: item.relationName}]->(target)
                ON CREATE SET r.description = ''
                SET r.cardinality = item.cardinality,
                    r.schemaSource = 'CSV',
                    r.schemaImportedAt = timestamp()
            """, batch=relationship_batch).consume()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"写入 Neo4j 失败：{exc}") from exc

    _write_imported_ontology(new_class_payloads, imported_relationships)
    _write_manifest(selected, len(session["tables"]))
    from web.routers.graph import (
        _all_class_details_cached,
        _graph_class_detail_cached,
        _graph_overview_cached,
        _stats_cached,
    )
    from web.routers.i18n import _ontology_catalog

    _graph_overview_cached.cache_clear()
    _graph_class_detail_cached.cache_clear()
    _all_class_details_cached.cache_clear()
    _stats_cached.cache_clear()
    _ontology_catalog.cache_clear()
    with _session_lock:
        _sessions.pop(request.importId, None)
    return {
        "success": True,
        "classes": len(class_batch),
        "newClasses": len(new_class_payloads),
        "properties": len(property_batch),
        "relationships": len(relationship_batch),
    }
