from src.qa.sql_entity_resolver import (
    recent_selected_classes,
    resolve_sql_entities,
)
from src.qa.sql_schema_retriever import (
    build_physical_join_plan,
    build_sql_schema_context,
)
from src.qa.sql_validator import validate_sql_answer
from src.qa.prompt_builder import build_prompt


CLASSES = {
    "Container",
    "CurrentStatus",
    "HistoryMainline",
    "MfgOrder",
    "MoveHistory",
    "Product",
    "ProductFamily",
    "ThruputHistory",
    "Workflow",
}

CN_MAP = {
    "产品": "Product",
    "产品族": "ProductFamily",
    "批次": "Container",
    "工单": "MfgOrder",
}


def test_longest_entity_match_does_not_expand_product_family_to_product():
    result = resolve_sql_entities(
        "查询 ProductFamily 的配置",
        CLASSES,
        CN_MAP,
    )

    assert result == ["ProductFamily"]


def test_longest_chinese_alias_does_not_expand_product_family_to_product():
    result = resolve_sql_entities(
        "查询产品族配置",
        CLASSES,
        CN_MAP,
    )

    assert result == ["ProductFamily"]


def test_move_intent_adds_verified_history_domain_objects():
    result = resolve_sql_entities(
        "增加 Container 在产线上的 move 记录信息",
        CLASSES,
        CN_MAP,
    )

    assert result == ["Container", "HistoryMainline", "MoveHistory"]


def test_engine_entity_space_includes_physical_only_tables(monkeypatch):
    from src.qa import engine
    from src.qa import sql_schema_retriever

    monkeypatch.setattr(
        engine,
        "_get_class_names",
        lambda: ["Container", "HistoryMainline"],
    )
    monkeypatch.setattr(
        sql_schema_retriever,
        "_schema",
        lambda: (
            {
                "Container": {},
                "HistoryMainline": {},
                "MoveHistory": {},
            },
            {},
        ),
    )

    assert engine.extract_keywords(
        "查询 Container 的 move 记录",
        fallback=False,
    ) == ["Container", "HistoryMainline", "MoveHistory"]


def test_throughput_intent_adds_history_tables():
    result = resolve_sql_entities(
        "查询今日工单产出",
        CLASSES,
        CN_MAP,
    )

    assert result == ["MfgOrder", "HistoryMainline", "ThruputHistory"]


def test_unresolved_question_has_no_arbitrary_workflow_fallback():
    result = resolve_sql_entities(
        "帮我查一下今天的数据",
        CLASSES,
        CN_MAP,
    )

    assert result == []


def test_history_fallback_reads_only_last_user_selection():
    history = [
        {
            "role": "user",
            "content": "查询批次",
            "selected_classes": ["Container"],
        },
        {
            "role": "assistant",
            "content": "也可以使用 [[Product]] 和 [[Workflow]]",
        },
    ]

    assert recent_selected_classes(history) == ["Container"]


def test_direct_join_plan_uses_exact_physical_fk():
    plan = build_physical_join_plan(["Workflow", "ERPRoute"])

    assert plan["tables"] == ["Workflow", "ERPRoute"]
    assert plan["joins"] == [
        {
            "from_table": "Workflow",
            "from_field": "ERPRouteId",
            "to_table": "ERPRoute",
            "to_field": "ERPRouteId",
        }
    ]


def test_move_join_plan_uses_history_mainline_as_verified_bridge():
    plan = build_physical_join_plan(
        ["Container", "HistoryMainline", "MoveHistory"]
    )

    assert plan["tables"] == [
        "Container",
        "HistoryMainline",
        "MoveHistory",
    ]
    assert {
        (
            edge["from_table"],
            edge["from_field"],
            edge["to_table"],
            edge["to_field"],
        )
        for edge in plan["joins"]
    } == {
        ("HistoryMainline", "ContainerId", "Container", "ContainerId"),
        (
            "MoveHistory",
            "HistoryMainlineId",
            "HistoryMainline",
            "HistoryMainlineId",
        ),
    }


def test_schema_context_exposes_join_plan_before_fields():
    context = build_sql_schema_context(
        ["Container", "HistoryMainline", "MoveHistory"],
        question="查询 Container 的 move 记录",
    )

    assert "### 已验证物理 JOIN 路径" in context
    assert (
        "[MoveHistory].[HistoryMainlineId] = "
        "[HistoryMainline].[HistoryMainlineId]"
    ) in context
    assert context.index("### 已验证物理 JOIN 路径") < context.index(
        "### 物理表 [HistoryMainline]"
    )
    assert "[MoveInHistory].[HistoryMainlineId]" in context
    assert "[ThruputHistory].[HistoryMainlineId]" not in context
    assert "[A_TrackInLotHistory].[HistoryMainlineId]" not in context


def test_validator_accepts_verified_oracle_move_query():
    answer = """### SQL
```sql
SELECT
    c.ContainerName,
    hm.TxnDate,
    mh.ToSpecName
FROM Container c
JOIN HistoryMainline hm
    ON hm.ContainerId = c.ContainerId
JOIN MoveHistory mh
    ON mh.HistoryMainlineId = hm.HistoryMainlineId
WHERE c.ContainerName = :container_name
  AND hm.TxnDate >= :start_time
  AND hm.TxnDate < :end_time
FETCH FIRST 100 ROWS ONLY;
```
"""
    result = validate_sql_answer(answer, dialect="oracle")

    assert result.valid is True
    assert result.errors == []


def test_validator_rejects_hallucinated_table_and_column():
    answer = """```sql
SELECT x.NotAField
FROM ContainerMoveHistory x
FETCH FIRST 100 ROWS ONLY;
```"""
    result = validate_sql_answer(answer, dialect="oracle")

    assert result.valid is False
    assert any("物理表不存在" in error for error in result.errors)


def test_validator_rejects_non_fk_join():
    answer = """```sql
SELECT c.ContainerName, mo.MfgOrderName
FROM Container c
JOIN MfgOrder mo ON c.ProductId = mo.MfgOrderId
FETCH FIRST 100 ROWS ONLY;
```"""
    result = validate_sql_answer(answer, dialect="oracle")

    assert result.valid is False
    assert any("不是已登记的物理外键" in error for error in result.errors)


def test_validator_rejects_dialect_mixing():
    answer = """```sql
SELECT TOP (100) [c].[ContainerName]
FROM [Container] AS [c]
WHERE [c].[ContainerName] = @name;
```"""
    result = validate_sql_answer(answer, dialect="oracle")

    assert result.valid is False
    assert any("不能使用 TOP" in error for error in result.errors)
    assert any("方括号标识符" in error for error in result.errors)
    assert any("@参数名" in error for error in result.errors)


def test_validator_rejects_write_statement():
    answer = """```sql
DELETE FROM Container WHERE ContainerId = :container_id;
```"""
    result = validate_sql_answer(answer, dialect="oracle")

    assert result.valid is False
    assert any("非只读" in error for error in result.errors)


def test_validator_allows_clarification_without_sql():
    result = validate_sql_answer(
        "请先指定需要查询的业务对象。",
        dialect="oracle",
    )

    assert result.valid is True
    assert result.sql == ""


def test_validator_accepts_read_only_cte_aliases():
    answer = """```sql
WITH recent_container AS (
    SELECT c.ContainerId, c.ContainerName
    FROM Container c
)
SELECT rc.ContainerName
FROM recent_container rc
FETCH FIRST 100 ROWS ONLY;
```"""
    result = validate_sql_answer(answer, dialect="oracle")

    assert result.valid is True


def test_sql_prompt_does_not_reuse_invalid_assistant_sql():
    history = [
        {"role": "user", "content": "查询批次"},
        {
            "role": "assistant",
            "content": "```sql\nSELECT x.BadField FROM MissingTable x;\n```",
        },
        {"role": "user", "content": "再增加状态"},
    ]
    messages = build_prompt(
        "继续",
        "",
        "",
        history=history,
        assistant_mode="sql",
        sql_schema_context="### 物理表 [Container]",
        sql_dialect="oracle",
    )

    assert not any(
        message["role"] == "assistant"
        for message in messages
    )
    assert any(
        message["role"] == "user"
        and message["content"] == "再增加状态"
        for message in messages
    )


def test_sql_prompt_retains_last_physically_valid_query_for_followup():
    valid_answer = """```sql
SELECT c.ContainerName
FROM Container c
FETCH FIRST 100 ROWS ONLY;
```"""
    messages = build_prompt(
        "增加状态字段",
        "",
        "",
        history=[
            {"role": "user", "content": "查询批次名称"},
            {"role": "assistant", "content": valid_answer},
        ],
        assistant_mode="sql",
        sql_schema_context="### 物理表 [Container]",
        sql_dialect="oracle",
    )

    assert any(
        message["role"] == "assistant"
        and message["content"] == valid_answer
        for message in messages
    )
