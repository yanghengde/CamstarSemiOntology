"""
Step 3: Prompt Builder
──────────────────────
Merges graph context + vector context + conversation history
into a compact prompt for DeepSeek.
"""

import os

def build_prompt(
    question: str,
    graph_context: str,
    vector_context: str,
    history: list[dict] | None = None,
    product_line: str = "general",
    assistant_mode: str = "sql",
    sql_schema_context: str = "",
) -> list[dict]:
    """
    Build the complete message list for the LLM API call.
    Uses compact context to reduce token count and latency.
    """
    if assistant_mode == "sql":
        system_prompt = (
            "你是 Siemens Opcenter Execution（Camstar）只读 SQL 助手，服务对象是需要查询后台业务数据的 IT 人员。"
            "默认数据库方言为 Microsoft SQL Server T-SQL。\n\n"
            "强制规则：\n"
            "1. 表名、字段名、主键和外键连接条件只能使用“物理数据库架构”中明确出现的内容；"
            "本体 camelCase 属性不能直接当作物理列名。不得猜测任何表或列。SQL、说明和注意事项中都不得"
            "推荐、暗示或举例引用物理上下文之外的表和字段。\n"
            "2. JOIN 必须优先使用上下文明确给出的 FK→目标表.目标字段；没有连接证据时说明缺少依据，"
            "不要用同名字段臆造连接。\n"
            "3. 只生成只读 SELECT 或以 SELECT 结束的 CTE。拒绝生成或改写 INSERT、UPDATE、DELETE、"
            "MERGE、TRUNCATE、DROP、ALTER、CREATE、EXEC 等会修改数据或结构的语句。\n"
            "4. 明细查询默认使用 TOP (100)，除非用户明确指定数量；不要 SELECT *，只选择需要的列。\n"
            "5. 使用方括号包围表名和字段名，使用清晰别名；所有筛选值必须使用 @参数，"
            "即使用户给出了数字或文本值也不能直接写入 SQL 字面量。\n"
            "6. 若需求、时间范围、状态含义或目标表不明确，先给可确认的查询骨架，并明确标出待确认参数；"
            "不得把不确定业务含义说成事实。不得根据 DataTypeCode 猜测业务枚举值，也不得虚构状态值说明。\n"
            "7. 输出固定包含：`### SQL`（sql代码块）、`### 说明`、`### 使用的表与连接`、`### 注意事项`。"
            "提及图谱类名时使用 [[ClassName]]，便于界面定位。\n"
            "8. SQL 仅供审核，不在系统中执行。"
            "9. 输出前逐一自检 SQL 和说明中的表名、字段名；删除所有物理上下文中不存在的对象。"
            "不要主动推荐其他表、事务接口或后续扩展查询。"
            "10. 当用户请求写操作时只简短拒绝，不自动改写成 SELECT，也不提供任何替代修改方案。"
        )
    else:
        show_cn_alias = os.getenv("SHOW_CN_ALIAS", "false").lower() == "true"

        if show_cn_alias:
            system_prompt = (
                "你是 Opcenter EX CR 建模助手。基于给定上下文用中文简洁回答。\n\n"
                "规则：\n"
                "1. 只基于上下文，不编造。提及本体类名用[[英文类名]]（中文名称）标记。\n"
                "2. 多对象用表格，步骤用编号。上下文不足时说明。"
            )
        else:
            system_prompt = (
                "你是 Opcenter EX CR 建模助手。基于给定上下文用中文简洁回答。\n\n"
                "规则：只基于上下文，不编造；提及本体类名用[[英文类名]]标记。"
            )

    if product_line and product_line != "general":
        try:
            from src.ontology.wiki_manager import get_product_line_info
            pl = get_product_line_info(product_line)
            if pl and pl.get("name"):
                system_prompt += f"\n当前行业/产品线: {pl['name']}。请结合该行业/产品线（描述: {pl.get('description', '')}）的特定背景、流程和术语来回答。"
        except Exception:
            pass

    messages = [{"role": "system", "content": system_prompt}]

    # Keep last 10 messages (5 turns) — enough context for multi-turn memory
    if history:
        for turn in history[-10:]:
            clean_turn = {
                "role": turn.get("role"),
                "content": turn.get("content")
            }
            if clean_turn.get("role") and clean_turn.get("content"):
                messages.append(clean_turn)

    # Build user message with compact context
    parts = []
    if assistant_mode == "sql" and sql_schema_context:
        parts.append(f"## 物理数据库架构（唯一SQL事实来源）\n{sql_schema_context}")
    if graph_context:
        parts.append(f"## 业务语义与关系图谱（辅助理解，不能替代物理字段）\n{graph_context}")
    if vector_context and vector_context != "未配置向量检索。":
        parts.append(f"## 文档\n{vector_context}")
    parts.append(f"## 问题\n{question}")

    user_msg = "\n\n".join(parts)
    messages.append({"role": "user", "content": user_msg})

    return messages


def format_vector_results(results: dict) -> str:
    """Format ChromaDB query results into compact context."""
    if not results or not results.get("documents"):
        return "未找到相关文档片段。"

    lines = []
    docs = results["documents"][0] if results["documents"] else []
    metas = results["metadatas"][0] if results["metadatas"] else []

    for i, (doc, meta) in enumerate(zip(docs, metas)):
        chapter = meta.get("chapter", "Unknown")
        page = meta.get("start_page", "?")
        # Tighter truncation: 250 chars per chunk
        text = doc[:250] + "..." if len(doc) > 250 else doc
        lines.append(f"**[{chapter}, P.{page}]**\n{text}")

    return "\n\n".join(lines) if lines else "未找到相关文档片段。"
