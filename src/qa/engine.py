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

    # 2. Graph & Scenario retrieval
    step_graph = trace.add_step("图谱与场景检索") if trace else None
    
    # Check if this is a scenario query
    is_scenario_query = any(k in question.lower() for k in ["场景", "用例", "实例", "业务流", "应用", "例", "scenario"])

    # Collect class names from question and history
    history_classes = []
    if history:
        for turn in history[-3:]:
            content = turn.get("content", "") or ""
            # [[ClassName]] format
            found = re.findall(r'\[\[(\w+)\]\]', content)
            for f in found:
                if f not in history_classes:
                    history_classes.append(f)
            # Aliases/direct naming
            for cn, en in CN_MAP.items():
                if cn in content and en not in history_classes:
                    history_classes.append(en)
            for name in _get_class_names():
                if name in content and name not in history_classes:
                    history_classes.append(name)
    all_classes = list(dict.fromkeys(keywords + history_classes))

    # Graph context expansion
    graph_context = ""
    
    if is_scenario_query and len(all_classes) >= 1:
        # Find shortest path or multi-hop path if we have at least 2 classes
        path_data = None
        if len(all_classes) >= 2:
            yield {"type": "status", "content": "正在通过图谱分析多级关系链路，请耐心等待..."}
            from src.qa.graph_retriever import get_shortest_path_details
            path_data = get_shortest_path_details(all_classes[0], all_classes[1])

        # If we have a path, resolve it and generate wikis if missing
        rels_list = []
        path_nodes = all_classes[:2]
        if path_data:
            path_nodes = path_data.get("nodes", all_classes[:2])
            rels_list = path_data.get("relationships", [])
        else:
            # Fallback to 1-hop relationships of all_classes[0] if no path found or only 1 class
            from src.qa.graph_retriever import _get_driver
            driver = _get_driver()
            with driver.session() as session:
                query_cy = """
                MATCH (start:OntologyClass)
                WHERE toLower(start.name) = toLower($c1) OR toLower(start.chineseName) = toLower($c1)
                WITH start LIMIT 1
                MATCH (start)-[r:ONTOLOGY_RELATION]-(end:OntologyClass)
                RETURN start.name as from_name, end.name as to_name, r.name as rel, r.cardinality as cardinality, r.description as description
                LIMIT 5
                """
                try:
                    result = session.run(query_cy, c1=all_classes[0])
                    for rec in result:
                        rels_list.append({
                            "from": rec["from_name"],
                            "to": rec["to_name"],
                            "rel": rec["rel"],
                            "cardinality": rec["cardinality"] or "",
                            "description": rec["description"] or ""
                        })
                except Exception:
                    pass

        # Check and generate wiki for each relationship on the path/list
        if rels_list:
            from src.ontology.wiki_manager import generate_wiki_for_relationship
            import asyncio
            
            for r in rels_list:
                from_c = r["from"]
                to_c = r["to"]
                rel_n = r["rel"]
                card = r.get("cardinality") or ""
                desc_val = r.get("description") or ""
                
                # Check if wiki file exists
                wiki_filename = f"{from_c}_{rel_n}_{to_c}.md"
                wiki_dir_pl = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ontology", "wiki_kb", "relationships", product_line)
                wiki_dir_gen = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ontology", "wiki_kb", "relationships", "general")
                
                pl_exists = os.path.exists(os.path.join(wiki_dir_pl, wiki_filename))
                gen_exists = os.path.exists(os.path.join(wiki_dir_gen, wiki_filename))
                
                if not pl_exists and not gen_exists:
                    yield {"type": "status", "content": f"关系定义尚未生成，正在为您自动分析生成中间关系（{from_c} → {rel_n} → {to_c}）的说明内容，可能需要一些时间，请耐心等待..."}
                    try:
                        loop = asyncio.get_event_loop()
                        # Generate wiki synchronously in thread pool
                        await loop.run_in_executor(
                            None,
                            generate_wiki_for_relationship,
                            product_line,
                            from_c,
                            rel_n,
                            to_c,
                            card,
                            desc_val,
                            False # overwrite
                        )
                    except Exception as ge:
                        print(f"Failed to generate wiki for {from_c}_{rel_n}_{to_c}: {ge}")

        # Now, read wiki contents for context
        relation_wikis_text = ""
        for r in rels_list:
            from_c = r["from"]
            to_c = r["to"]
            rel_n = r["rel"]
            wiki_filename = f"{from_c}_{rel_n}_{to_c}.md"
            
            w_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ontology", "wiki_kb", "relationships", product_line, wiki_filename)
            if not os.path.exists(w_path):
                w_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ontology", "wiki_kb", "relationships", "general", wiki_filename)
                
            if os.path.exists(w_path):
                try:
                    with open(w_path, "r", encoding="utf-8") as wf:
                        relation_wikis_text += f"\n--- 关系文档: {from_c} -> {rel_n} -> {to_c} ---\n"
                        relation_wikis_text += wf.read() + "\n"
                except Exception as we:
                    print(f"Error reading wiki {w_path}: {we}")

        # Search and rank 300 business scenarios
        yield {"type": "status", "content": "正在基于关系上下文匹配最佳业务场景，请耐心等待..."}
        
        # Load scenarios
        scenarios_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ontology", "scenarios")
        scenarios = []
        # General scenarios
        gen_path = os.path.join(scenarios_dir, "general", "*.json")
        for f in glob.glob(gen_path):
            try:
                with open(f, "r", encoding="utf-8") as file:
                    scenarios.append(json.load(file))
            except Exception:
                pass
        # Product line scenarios
        if product_line != "general":
            pl_path = os.path.join(scenarios_dir, product_line, "*.json")
            for f in glob.glob(pl_path):
                try:
                    with open(f, "r", encoding="utf-8") as file:
                        scenarios.append(json.load(file))
                except Exception:
                    pass

        # Deduplicate
        seen_ids = set()
        dedup_scenarios = []
        for s in scenarios:
            sid = s.get("scenario_id")
            if sid not in seen_ids:
                seen_ids.add(sid)
                dedup_scenarios.append(s)

        # Calculate scores
        scores = {}
        vec_matched_ids = {}
        
        # Vector query
        if vector_collection is not None and rels_list:
            query_terms = list(path_nodes)
            for r in rels_list:
                query_terms.append(r.get("rel", ""))
                query_terms.append(r.get("description", ""))
            vec_query = " ".join(filter(None, query_terms))
            try:
                results = vector_collection.query(
                    query_texts=[vec_query],
                    n_results=15,
                    where={"type": "scenario"}
                )
                if results and results.get("metadatas") and results["metadatas"][0]:
                    for idx, meta in enumerate(results["metadatas"][0]):
                        if meta and meta.get("scenario_id"):
                            sid = str(meta.get("scenario_id"))
                            vec_matched_ids[sid] = 15 - idx
            except Exception as e:
                print(f"Vector search failed in engine: {e}")

        # Compute match scores
        for s in dedup_scenarios:
            sid = s.get("scenario_id")
            score = 0
            
            # Twins overlap
            twins = [t.lower() for t in s.get("twins", []) or []]
            for step in s.get("steps", []):
                twins.extend([t.lower() for t in step.get("twins", []) or []])
            twins = set(twins)
            
            matching_nodes_count = 0
            for node in path_nodes:
                if node.lower() in twins:
                    score += 8
                    matching_nodes_count += 1
            if matching_nodes_count == len(path_nodes) and len(path_nodes) > 1:
                score += 15
                
            # Rel overlap
            scenario_rels = []
            for step in s.get("steps", []):
                scenario_rels.extend([r_str.lower() for r_str in step.get("rels", []) or []])
                
            for r in rels_list:
                rel_name = r.get("rel", "").lower()
                for sr in scenario_rels:
                    if rel_name in sr:
                        score += 20
                        break
                        
            # Vector score
            if sid in vec_matched_ids:
                score += vec_matched_ids[sid]
                
            # Text matching
            desc = s.get("description", "").lower()
            name = s.get("name", "").lower()
            for r in rels_list:
                rel_desc = r.get("description", "").lower()
                if rel_desc:
                    words = [w for w in rel_desc.split() if len(w) > 1]
                    for w in words:
                        if w in desc or w in name:
                            score += 2
            scores[sid] = score

        # Top 3 scenarios
        sorted_scenarios = sorted(dedup_scenarios, key=lambda x: scores.get(x.get("scenario_id"), 0), reverse=True)
        matched_scs = sorted_scenarios[:3]

        # Format scenario context
        scenario_context = ""
        if matched_scs:
            scenario_context = "\n以下为检索匹配到的最佳 MES 数字化场景列表（在最终回复中，如果是推荐这几个场景，必须以方括号如 [SC_XXX] 的格式标注场景 ID）：\n"
            for sc in matched_scs:
                scenario_context += f"- 场景 ID: [{sc['scenario_id']}]\n  名称: {sc['name']}\n  描述: {sc['description']}\n"
                scenario_context += "  主要步骤:\n"
                for step in sc.get("steps", []):
                    scenario_context += f"    * {step.get('step')}: {step.get('desc')}\n"

        # Construct final graph_context
        graph_data = search_graph(all_classes)
        graph_context = format_graph_context(graph_data)
        if relation_wikis_text:
            graph_context += f"\n\n### 关联关系详细定义与文档参考：\n{relation_wikis_text}"
        if scenario_context:
            graph_context += f"\n\n### 推荐匹配的业务场景参考：\n{scenario_context}"
            
        if step_graph:
            step_graph.done(output={
                "matched_classes": len(all_classes),
                "path_found": path_data is not None,
                "relationships_checked": len(rels_list),
                "matched_scenarios": len(matched_scs)
            })
    else:
        # Normal Graph RAG Flow
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
