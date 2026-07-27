"""
QA Engine – Orchestrates Graph + Vector hybrid RAG
──────────────────────────────────────────────────
1. Extract entities from the user question (via keyword matching + LLM)
2. Parallel retrieval: Neo4j graph + ChromaDB vector
3. Assemble prompt with conversation history
4. Stream response from DeepSeek
"""
import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv
from src.qa.graph_retriever import search_graph, format_graph_context, get_all_class_names
from src.qa.prompt_builder import build_prompt, format_vector_results
from src.qa.logger import ChatTrace, CHAT_LOG_ENABLED
import glob

# Dynamically loaded Chinese to English class name mappings
CN_MAP = {}

def _load_cn_map():
    global CN_MAP
    CN_MAP.clear()
    
    CN_MAP.update({
        "工艺路线": "Workflow", "流程": "Workflow",
        "步骤": "WorkflowStep", "工段": "Operation",
        "规范": "Spec", "指令": "Spec", "rework": "Rework",
        "物料": "Product", "设备": "Resource",
        "任务列表": "TaskList", "批次": "Container",
        "工单": "MfgOrder", "在制品": "Container",
        "警报": "AlarmDef", "挂起": "HoldReason",
        "工作中心": "WorkCenter", 
        "派工": "DispatchRule", "排程": "DispatchRule",
        "认证": "Skill", "资质": "Skill",
        "保养": "Resource", "校准": "Resource",
        "集团": "Enterprise", "园区": "Site", "车间": "Factory", "厂房": "Factory",
        "洁净室": "ManufacturingArea", "区域": "ManufacturingArea",
        "生产线": "ProductionLine", "排班": "ShiftPattern", "轮班": "ShiftPattern",
        "在制品消息": "WipMessage",
    })
    
    # Dynamically extract chineseName from ontology JSONs to auto-map new objects
    kb_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ontology", "wiki_kb")
    for file_path in glob.glob(os.path.join(kb_path, "*_ontology.json")):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for cls in data.get("classes", []):
                    cname = cls.get("chineseName")
                    ename = cls.get("className")
                    if cname and ename:
                        CN_MAP[cname] = ename
        except Exception as e:
            print(f"Error loading {file_path} for CN_MAP: {e}")

_load_cn_map()

load_dotenv(override=True)

# DeepSeek client
_llm_client = None
_async_llm_client = None
_class_names = None


def _get_llm():
    global _llm_client
    if _llm_client is None:
        _llm_client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
            timeout=float(os.getenv("LLM_TIMEOUT", "120")),
        )
    return _llm_client


def _get_async_llm():
    global _async_llm_client
    if _async_llm_client is None:
        from openai import AsyncOpenAI
        _async_llm_client = AsyncOpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
            timeout=float(os.getenv("LLM_TIMEOUT", "120")),
        )
    return _async_llm_client


def _get_class_names():
    global _class_names
    if _class_names is None:
        _class_names = get_all_class_names()
    return _class_names


def extract_keywords(question: str) -> list[str]:
    """
    Extract relevant ontology keywords from the user question.
    Uses a two-pronged approach:
      1. Direct matching against known class names
      2. Chinese keyword heuristics
    """
    keywords = []
    class_names = _get_class_names()

    # Direct match: check if any known class name appears in the question
    q_lower = question.lower()
    for name in class_names:
        if name.lower() in q_lower:
            keywords.append(name)

    # Use globally loaded CN_MAP (populated dynamically from ontology JSONs + aliases)
    for cn, en in CN_MAP.items():
        if cn in question:
            keywords.append(en)

    # Deduplicate and return
    return list(dict.fromkeys(keywords)) or ["Workflow"]  # fallback


async def query(
    question: str,
    history: list[dict] | None = None,
    vector_collection=None,
    product_line: str = "general",
) -> str:
    """
    Non-streaming query: returns complete answer string.
    """
    chunks = []
    async for chunk in query_stream(question, history, vector_collection, product_line=product_line):
        if isinstance(chunk, str):
            chunks.append(chunk)
    return "".join(chunks)


async def query_stream(
    question: str,
    history: list[dict] | None = None,
    vector_collection=None,
    trace: ChatTrace | None = None,
    product_line: str = "general",
):
    """
    Streaming query: yields answer chunks as they arrive from DeepSeek.
    Pure Graph RAG strategy: Graph + Vector + LLM streaming.
    If 'trace' is provided, each step's timing and metadata are logged.
    """
    # 1. Extract entities/keywords
    step_kw = trace.add_step("关键词提取") if trace else None
    keywords = extract_keywords(question)
    if step_kw:
        step_kw.done(output={"keywords": keywords})

    # 2. Graph retrieval
    step_graph = trace.add_step("图谱检索") if trace else None
    graph_data = search_graph(keywords)
    graph_context = format_graph_context(graph_data)
    if step_graph:
        step_graph.done(output={
            "matched_classes": len(graph_data.get("matched_classes", [])),
            "relationships": len(graph_data.get("relationships", [])),
            "properties": len(graph_data.get("properties", [])),
        })

    # 3. Vector retrieval (supplementary context)
    step_vec = trace.add_step("向量检索") if trace else None
    vector_context = "未配置向量检索。"
    if vector_collection is not None:
        try:
            results = vector_collection.query(
                query_texts=[question],
                n_results=3,
            )
            vector_context = format_vector_results(results)
            if step_vec:
                chunks_count = len(results.get("documents", [[]])[0]) if results.get("documents") else 0
                step_vec.done(output={"chunks_retrieved": chunks_count})
        except Exception as e:
            vector_context = f"向量检索错误: {e}"
            if step_vec:
                step_vec.fail(str(e))
    else:
        if step_vec:
            step_vec.done(output={"chunks_retrieved": 0})

    # 4. Build prompt
    step_prompt = trace.add_step("提示词构建") if trace else None
    messages = build_prompt(question, graph_context, vector_context, history, product_line=product_line)
    if step_prompt:
        step_prompt.done(output={
            "system_tokens": len(messages[0]["content"]) // 3 if messages else 0,
            "history_turns": len(history) if history else 0,
        })

    # 5. Stream from DeepSeek
    step_llm = trace.add_step("LLM调用") if trace else None
    client = _get_async_llm()
    model = os.getenv("LLM_MODEL", "deepseek-v4-flash")

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            temperature=0.3,
            max_tokens=4096,
        )

        full_answer = ""
        async for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                token = chunk.choices[0].delta.content
                full_answer += token
                yield token

        if step_llm:
            step_llm.done(output={
                "model": model,
                "answer_length": len(full_answer),
                "answer_tokens_estimate": len(full_answer) // 2,
            })
    except Exception as e:
        if step_llm:
            step_llm.fail(str(e))
        yield f"\n\n❌ LLM 调用失败: {e}"


def extract_class_links(answer: str) -> list[str]:
    """Extract [[ClassName]] markers from the answer text."""
    return re.findall(r'\[\[(\w+)\]\]', answer)
