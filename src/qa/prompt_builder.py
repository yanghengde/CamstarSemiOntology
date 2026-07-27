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
) -> list[dict]:
    """
    Build the complete message list for the LLM API call.
    Uses compact context to reduce token count and latency.
    """
    show_cn_alias = os.getenv("SHOW_CN_ALIAS", "false").lower() == "true"
    
    if show_cn_alias:
        system_prompt = (
            "你是 Opcenter EX CR 建模助手。基于给定上下文用中文简洁回答。\n\n"
            "规则：\n"
            "1. 只基于上下文，不编造。提及本体类名用[[英文类名]]（中文名称）标记，例如：[[Workflow]]（工艺路线）、[[Spec]]（工序规范）。\n"
            "2. 多对象用表格，步骤用编号。上下文不足时说明。\n"
            "3. 严格只回答用户提出的问题，不要自行补充额外内容、不要主动生成后续建议或追问。\n"
            "4. 以用户的问题为主，用户问什么答什么，不做多余延伸。"
        )
    else:
        system_prompt = (
            "你是 Opcenter EX CR 建模助手。基于给定上下文用中文简洁回答。\n\n"
            "规则：\n"
            "1. 只基于上下文，不编造。提及本体类名用[[英文类名]]标记，例如：[[Workflow]]。\n"
            "2. 多对象用表格，步骤用编号。上下文不足时说明。\n"
            "3. 严格只回答用户提出的问题，不要自行补充额外内容、不要主动生成后续建议或追问。\n"
            "4. 以用户的问题为主，用户问什么答什么，不做多余延伸。"
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
    if graph_context:
        parts.append(f"## 图谱\n{graph_context}")
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
