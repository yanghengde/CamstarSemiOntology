import os
import glob
import json
from functools import lru_cache
from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from web.shared import driver, _classify_module, _get_vector_collection, PROJECT_ROOT

class ScenarioCache:
    def __init__(self):
        self._cache = {}  # {(industry, scenario_id): scenario_data}
        self.is_loaded = False

    def load_all(self):
        import glob
        import json
        scenarios_dir = os.path.join(PROJECT_ROOT, "src", "ontology", "scenarios")
        new_cache = {}
        if os.path.exists(scenarios_dir):
            for ind in os.listdir(scenarios_dir):
                dir_path = os.path.join(scenarios_dir, ind)
                if not os.path.isdir(dir_path):
                    continue
                files = glob.glob(os.path.join(dir_path, "*.json"))
                for f in files:
                    try:
                        with open(f, "r", encoding="utf-8") as file:
                            data = json.load(file)
                            sid = str(data.get("scenario_id"))
                            new_cache[(ind.lower(), sid)] = data
                    except Exception as e:
                        print(f"[Cache] Error loading {f}: {e}")
        self._cache = new_cache
        self.is_loaded = True
        print(f"[Cache] Loaded {len(self._cache)} scenarios into memory.")

    def get(self, scenario_id: str, industry: str = "general"):
        if not self.is_loaded:
            self.load_all()
        val = self._cache.get((industry.lower(), scenario_id))
        if val is None and industry.lower() != "general":
            val = self._cache.get(("general", scenario_id))
        return val

    def get_all(self, industry: str = "general"):
        if not self.is_loaded:
            self.load_all()
        return [data for (ind, sid), data in self._cache.items() if ind == industry.lower()]

    def set(self, industry: str, scenario_id: str, data: dict):
        if not self.is_loaded:
            self.load_all()
        self._cache[(industry.lower(), scenario_id)] = data

    def delete(self, industry: str, scenario_id: str):
        if not self.is_loaded:
            self.load_all()
        self._cache.pop((industry.lower(), scenario_id), None)
        self._cache.pop(("general", scenario_id), None)

# Trigger hot-reload for LLM model update to deepseek-chat
scenario_cache = ScenarioCache()
scenario_cache.load_all()

router = APIRouter()

class GraphResolveRequest(BaseModel):
    twins: list[str]


class PlanRequest(BaseModel):
    message: str
    history: list[dict] = []
    current_scenario: str | None = None


class StepModel(BaseModel):
    step: str
    desc: str
    twins: list[str]
    rels: list[str]
    code: str


class SaveScenarioRequest(BaseModel):
    scenario_id: str
    industry: str = "general"
    name: str
    description: str
    steps: list[StepModel]


def get_ontology_and_path_context(message: str, current_scenario: str | None) -> str:
    # 1. Extract keywords from message
    from src.qa.engine import extract_keywords
    keywords = extract_keywords(message)
    
    # 2. Extract classes from current_scenario
    current_classes = []
    if current_scenario and current_scenario.strip():
        try:
            import re
            json_text = current_scenario.strip()
            json_match = re.search(r'```(?:json)?\s*([\s\S]+?)\s*```', json_text)
            if json_match:
                json_text = json_match.group(1).strip()
            parsed = json.loads(json_text)
            if "steps" in parsed:
                for step in parsed["steps"]:
                    if "twins" in step:
                        for tw in step["twins"]:
                            if tw not in current_classes:
                                current_classes.append(tw)
        except Exception:
            pass
            
    # Combine search targets
    search_classes = list(dict.fromkeys(keywords + current_classes))
    if not search_classes:
        return ""
        
    # Get graph context via search_graph
    from src.qa.graph_retriever import search_graph, format_graph_context
    try:
        graph_data = search_graph(search_classes)
        graph_context = format_graph_context(graph_data)
    except Exception as e:
        print(f"Error in search_graph: {e}")
        graph_context = ""
        
    # Get path context between classes using Dijkstra pathfinder
    path_context = ""
    if len(search_classes) >= 2:
        paths = []
        from src.qa.graph_retriever import find_reasonable_path
        keywords_set = set(search_classes)
        for i in range(len(search_classes)):
            for j in range(i + 1, len(search_classes)):
                c1, c2 = search_classes[i], search_classes[j]
                try:
                    p_nodes, p_rels = find_reasonable_path(c1, c2, keywords_set)
                    if p_nodes and len(p_nodes) > 1:
                        path_str = p_nodes[0]
                        for idx in range(len(p_rels)):
                            path_str += f" -[{p_rels[idx]}]-> {p_nodes[idx+1]}"
                        paths.append(path_str)
                except Exception:
                    pass
        if paths:
            path_context = "### 真实类间关联链路参考：\n" + "\n".join(f"- {p}" for p in paths)
            
    parts = []
    if graph_context:
        parts.append(f"## 涉及的真实本体类及字段/关系定义：\n{graph_context}")
    if path_context:
        parts.append(path_context)
        
    return "\n\n".join(parts)


@router.post("/api/scenarios/plan")
async def plan_scenario(req: PlanRequest):
    message = req.message.strip()
    history = req.history

    if not message:
        return JSONResponse(status_code=400, content={"error": "message is required"})

    from src.qa.engine import _get_llm
    client = _get_llm()
    model = os.getenv("LLM_MODEL", "deepseek-chat")

    system_prompt = (
        "你是一个专业的西门子 Opcenter MES 数字化映射与业务场景规划专家顾问（Intelligent Scenario Planner Agent）。\n"
        "你的任务是帮助用户梳理、设计、并优化其 MES 自定义业务流程场景。\n\n"
        "请遵循以下设计与工程原则：\n"
        "1. 术语标准化：必须使用 exact、大小写敏感的西门子 Opcenter 物理表名（CDO 类名），例如：Container (在制品/容器)、Spec (工序规范)、Resource (机台/物理资源)、Workflow (工艺路线)、BOM (物料清单)、DataCollectionDef (数据采集组)、AlarmDef (警报定义)、Event (品质事件) 等。\n"
        "2. 紧凑与聚焦：设计的场景要简明清晰，本体图不应过于复杂。只设计该业务场景实际需要的实体，排除无关的辅助实体以防子图杂乱。\n"
        "3. 规范的 2 步法流程结构：\n"
        "   - 步骤 1 必须命名为『Step 1: 触发 - [业务事件名称]』，例如“Step 1: 触发 - 在制品MoveOut事件”。在此步骤中，对应的 twins 应当仅包含触发状态相关的实体（如 Container、Carrier、MfgOrder、BOM），并配合 SELECT 的 SQL 代码表示读取初始状态。\n"
        "   - 步骤 2 必须命名为『Step 2: 校验 - [业务事件名称]』，例如“Step 2: 校验 - 规则校验与动作拦截”。在此步骤中，对应的 twins 应当包含判定规则与后置处理相关的动作实体（如 Resource、BusinessRule、AlarmDef、HoldReason、ReworkReason），并配合 UPDATE 或 INSERT 的 SQL 代码表示规则判定及拦截动作。\n"
        "4. 输出结构化 JSON 提案：在你的对话结尾，除了文字说明外，必须给出一个包裹在 ```json ... ``` 块内的结构化提案，作为前端重绘数字化蓝图与高亮本体图的唯一依据。JSON 必须符合以下 Schema：\n"
        "{\n"
        "  \"name\": \"SC_XXX. 场景中文名称\",\n"
        "  \"description\": \"场景的简要核心业务描述\",\n"
        "  \"steps\": [\n"
        "    {\n"
        "      \"step\": \"Step 1: 触发 - 具体的业务触发动作\",\n"
        "      \"desc\": \"本步骤所对应的物理业务触发与状态检索说明\",\n"
        "      \"twins\": [\"Container\", \"BOM\"],\n"
        "      \"code\": \"SELECT ...\"\n"
        "    },\n"
        "    {\n"
        "      \"step\": \"Step 2: 校验 - 具体的规则校验与动作拦截\",\n"
        "      \"desc\": \"本步骤所对应的校验控制逻辑以及挂起、拦截、警报触发说明\",\n"
        "      \"twins\": [\"Resource\", \"HoldReason\", \"AlarmDef\"],\n"
        "      \"code\": \"UPDATE ...\"\n"
        "    }\n"
        "  ]\n"
        "}"
    )

    # ── Retrieve RAG context to help LLM reason about true database connections ──
    try:
        rag_context = get_ontology_and_path_context(message, req.current_scenario)
    except Exception as re_err:
        print(f"[Plan Server] RAG context retrieval failed: {re_err}")
        rag_context = ""

    if rag_context:
        system_prompt += (
            f"\n\n⚠️【本地方案对应的真实 Neo4j 本体图谱关系（Graph RAG）】\n"
            f"为了使你设计的数字化场景能够100%连接（不产生孤立子图），请参考以下物理数据库中的真实类定义、字段与关系链路设计你的提案：\n"
            f"\"\"\"\n{rag_context}\n\"\"\"\n"
            f"如果你提议的 twins 之间存在没有直接关系的情况，必须通过上述真实的中间类（如 Resource, Spec, WipMessageDefMgr）进行连接/桥接，并将中间桥接类一起列入 twins 列表中！"
        )

    if req.current_scenario and req.current_scenario.strip():
        system_prompt += (
            f"\n\n⚠️【核心协同资产：当前蓝图场景定义（JSON格式）】\n"
            f"以下是当前用户工作台上已加载/生成的数字化映射蓝图拓扑方案内容：\n"
            f"\"\"\"\n{req.current_scenario}\n\"\"\"\n"
            f"请仔细阅读上述场景中的步骤、描述与实体。用户接下来的输入是针对此方案进行的优化、新增、删除或调整修正要求。\n"
            f"请理解用户的修改意图，并在您的回复结尾重新给出完整的、更新后的场景 JSON 代码块（包裹在 ```json ... ``` 内）。这是将微调结果重画至前端卡片与本体子图的唯一依据！"
        )

    messages = [{"role": "system", "content": system_prompt}]
    
    for turn in history:
        messages.append({"role": turn["role"], "content": turn["content"]})
        
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
            max_tokens=4096,
        )
        answer = response.choices[0].message.content
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"LLM 调用失败: {e}"})


@router.post("/api/scenarios/save")
async def save_scenario(req: SaveScenarioRequest):
    scenario_id = req.scenario_id.strip()
    industry = req.industry.strip().lower() or "general"
    name = req.name.strip()
    description = req.description.strip()
    
    if not scenario_id or not name or not description:
        return JSONResponse(status_code=400, content={"error": "scenario_id, name, and description are required"})
        
    scenario_dir = os.path.join(PROJECT_ROOT, "src", "ontology", "scenarios", industry)
    os.makedirs(scenario_dir, exist_ok=True)
    
    file_path = os.path.join(scenario_dir, f"scenario_{scenario_id}.json")
    
    scenario_data = {
        "scenario_id": scenario_id,
        "industry": industry,
        "name": name,
        "description": description,
        "steps": [s.model_dump() for s in req.steps]
    }
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(scenario_data, f, ensure_ascii=False, indent=4)
            
        # Update in-memory cache
        scenario_cache.set(industry, scenario_id, scenario_data)
            
        vec_col = _get_vector_collection()
        if vec_col is not None:
            doc_text = f"{name} {description}"
            doc_id = f"scenario_id_{scenario_id}"
            metadata = {
                "type": "scenario",
                "scenario_id": scenario_id,
                "name": name,
                "industry": industry
            }
            vec_col.upsert(
                ids=[doc_id],
                documents=[doc_text],
                metadatas=[metadata]
            )
            print(f"[Server] Scenario {scenario_id} ({name}) successfully upserted into ChromaDB.")
            
        return {"status": "saved", "scenario_id": scenario_id, "industry": industry, "file_path": file_path}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to save scenario: {str(e)}"})


@router.get("/api/scenarios")
def list_scenarios(industry: str = "general", product_line: str = None, include_general: bool = True):
    ind = product_line or industry or "general"
    ind_lower = ind.lower()
    scs = scenario_cache.get_all(ind_lower)
    
    if include_general and ind_lower != "general":
        general_scs = scenario_cache.get_all("general")
        seen = set()
        combined = []
        for s in scs:
            sid = s.get("scenario_id")
            if sid not in seen:
                seen.add(sid)
                combined.append(s)
        for s in general_scs:
            sid = s.get("scenario_id")
            if sid not in seen:
                seen.add(sid)
                combined.append(s)
        scs = combined
    elif not scs and ind_lower != "general" and include_general:
        scs = scenario_cache.get_all("general")
        
    res = []
    for data in scs:
        res.append({
            "scenario_id": data.get("scenario_id"),
            "name": data.get("name"),
            "description": data.get("description")
        })
    try:
        res.sort(key=lambda x: int(x.get("scenario_id", "0")))
    except:
        res.sort(key=lambda x: x.get("scenario_id", ""))
    return {"scenarios": res}


@router.get("/api/scenarios/search")
def search_scenarios(query: str):
    collection = _get_vector_collection()
    matched_ids = []
    
    if collection is not None:
        try:
            results = collection.query(
                query_texts=[query],
                n_results=3,
                where={"type": "scenario"}
            )
            if results and results.get("metadatas") and results["metadatas"][0]:
                for meta in results["metadatas"][0]:
                    if meta and meta.get("scenario_id"):
                        matched_ids.append(str(meta.get("scenario_id")))
        except Exception as e:
            print(f"ChromaDB scenario vector search failed: {e}")
            
    # Search in-memory cache instead of scanning disk files
    all_general_scs = scenario_cache.get_all("general")
    keyword_matches = []
    query_lower = query.lower()
    
    for data in all_general_scs:
        sid = str(data.get("scenario_id"))
        name = data.get("name", "")
        desc = data.get("description", "")
        if query_lower in name.lower() or query_lower in desc.lower():
            keyword_matches.append(sid)
            
    all_matches = list(dict.fromkeys(matched_ids + keyword_matches))
    
    res = []
    for sid in all_matches:
        data = scenario_cache.get(sid, "general")
        if data:
            res.append({
                "scenario_id": data.get("scenario_id"),
                "name": data.get("name"),
                "description": data.get("description")
            })
    return {"results": res}


class ScenarioQaRequest(BaseModel):
    question: str
    history: list[dict] = []
    industry: str = "general"
    include_general: bool = True

@router.post("/api/scenarios/qa")
async def qa_scenarios(req: ScenarioQaRequest):
    question = req.question.strip()
    history = req.history
    industry = req.industry.strip().lower() or "general"
    include_general = req.include_general
    
    if not question:
        return JSONResponse(status_code=400, content={"error": "question is required"})
        
    vec_col = _get_vector_collection()
    context = ""
    
    if vec_col is not None:
        try:
            # Query top 10 most relevant chunks in ChromaDB and filter in Python
            results = vec_col.query(
                query_texts=[question],
                n_results=10,
                where={"type": "scenario"}
            )
            if results and results.get("documents") and results["documents"][0]:
                matched_scs = []
                # Determine allowed industries based on include_general
                allowed_inds = [industry]
                if include_general or industry == "general":
                    allowed_inds.append("general")

                for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                    if not meta:
                        continue
                    meta_ind = meta.get("industry", "general").lower()
                    if meta_ind in allowed_inds:
                        matched_scs.append((doc, meta))
                
                if matched_scs:
                    context = "以下为通过 RAG 检索到的最相关的 MES 数字化场景列表，以供参考：\n\n"
                    for doc, meta in matched_scs[:6]:
                        if meta and meta.get("scenario_id"):
                            context += f"- 场景 ID: [{meta['scenario_id']}]\n  名称: {meta.get('name')}\n  核心描述: {doc}\n\n"
        except Exception as e:
            print(f"[QA Server] ChromaDB scenario query failed: {e}")
            
    # Heuristic keyword match fallback if ChromaDB returned nothing or failed
    if not context:
        all_scs = []
        if industry != "general":
            all_scs.extend(scenario_cache.get_all(industry))
        if include_general or industry == "general":
            all_scs.extend(scenario_cache.get_all("general"))
        
        matched_count = 0
        context = "以下为根据关键词匹配到的相关场景，以供参考：\n\n"
        for data in all_scs:
            sid = data.get("scenario_id")
            name = data.get("name", "")
            desc = data.get("description", "")
            if any(kw in name.lower() or kw in desc.lower() for kw in question.lower().split()):
                context += f"- 场景 ID: [{sid}]\n  名称: {name}\n  核心描述: {desc}\n\n"
                matched_count += 1
                if matched_count >= 5:
                    break
                
    from src.qa.engine import _get_async_llm
    client = _get_async_llm()
    model = os.getenv("LLM_MODEL", "deepseek-chat")
    
    system_prompt = (
        "你是一个极其资深、专业的西门子 Opcenter MES 数字化车间场景导航与多轮问答专家（Intelligent Scenario Navigation Agent）。\n"
        "你的任务是根据用户输入的业务诉求、现场痛点、控制规范或设备问题，精准地从已部署 of 300 个数字化场景中检索并导航定位出对应的控制方案。\n\n"
    )

    try:
        from src.ontology.wiki_manager import get_product_line_info
        pl = get_product_line_info(industry)
        if pl and pl.get("name"):
            system_prompt += f"当前问答系统针对的行业/产品线: {pl['name']}（ID: {pl['id']}）。业务场景背景: {pl.get('description', '')}。\n在回答中如果合适，应优先推荐该行业的解决方案，并结合该行业的物理车间工艺流程与术语进行解答，必须紧密贴合该行业背景。\n\n"
    except Exception as e:
        print(f"[QA Server] Failed to inject industry context: {e}")

    system_prompt += (
        "请严格遵循以下规则开展对话与解答：\n"
        "1. 意图穿透与多轮追问：理解用户的核心意图。如果用户的表述较为简短或宽泛，你可以结合上下文进行多轮深入对话，引导式询问用户的具体工艺工序、控制节点或在制品拦截要求，帮助其精确收敛范围。\n"
        "2. 【场景ID高亮规则】：一旦在你的回复中提到了具体的场景 ID，请务必使用方括号包裹，例如：『[SC_281]』，且每次推荐尽量提供其标准名称及控制逻辑概述。这是前端将文本解析为可点击预览卡片的唯一特征！\n"
        "3. 深度解读方案：当为用户锁定特定场景时，用精炼且高度专业的技术语言为他们拆解这一工步：\n"
        "   - 在制品 Container 的状态校验（如 PASSED, Hold, Expired 等）；\n"
        "   - 所关联的本体孪生实体（如 Spec, Resource, DataCollection, Quality 等）；\n"
        "   - 具体的现场控制继电器动作或 Andon 警报逻辑。\n"
        "4. 专业谦逊的态度：语气要严谨、极富西门子工业级水准的专业范式，使用中文回答。"
    )
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # Append conversation history
    for turn in history:
        messages.append({"role": turn["role"], "content": turn["content"]})
        
    # Append current user prompt with formatted RAG search context
    user_content = f"【用户问题】: {question}"
    if context:
        user_content += f"\n\n【RAG 知识库检索参考场景】:\n{context}"
        
    messages.append({"role": "user", "content": user_content})
        
    async def generate_response():
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2,
                max_tokens=4096,
                stream=True
            )
            async for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield f"data: {json.dumps({'type': 'chunk', 'content': chunk.choices[0].delta.content}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        generate_response(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/api/scenarios/{scenario_id}")
def get_scenario(scenario_id: str, industry: str = "general"):
    data = scenario_cache.get(scenario_id, industry)
    if not data:
        return JSONResponse(status_code=404, content={"error": f"Scenario {scenario_id} not found."})
    return data


@router.delete("/api/scenarios/{scenario_id}")
async def delete_scenario(scenario_id: str, industry: str = "general"):
    scenario_id = scenario_id.strip()
    industry = industry.strip().lower() or "general"
    
    scenario_dir = os.path.join(PROJECT_ROOT, "src", "ontology", "scenarios", industry)
    file_path = os.path.join(scenario_dir, f"scenario_{scenario_id}.json")
    
    if not os.path.exists(file_path):
        file_path = os.path.join(PROJECT_ROOT, "src", "ontology", "scenarios", "general", f"scenario_{scenario_id}.json")
        
    if not os.path.exists(file_path):
        scenario_cache.delete(industry, scenario_id)
        return JSONResponse(status_code=404, content={"error": f"Scenario {scenario_id} not found."})
        
    try:
        os.remove(file_path)
        
        # Delete from cache
        scenario_cache.delete(industry, scenario_id)
        
        # Remove from ChromaDB vector store
        vec_col = _get_vector_collection()
        if vec_col is not None:
            try:
                doc_id = f"scenario_id_{scenario_id}"
                vec_col.delete(ids=[doc_id])
                print(f"[Server] Scenario {scenario_id} successfully deleted from ChromaDB.")
            except Exception as cv_err:
                print(f"[Server] Failed to delete scenario {scenario_id} from ChromaDB: {cv_err}")
                
        return {"status": "deleted", "scenario_id": scenario_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to delete scenario: {str(e)}"})


def heal_twins(twins: list[str]) -> list[str]:
    if len(twins) <= 1:
        return twins

    with driver.session() as session:
        # Get all valid twins first (check if they exist in Neo4j)
        res = session.run("MATCH (c:OntologyClass) WHERE c.name IN $twins RETURN c.name as name", twins=twins)
        valid_twins = [r["name"] for r in res]
        if not valid_twins:
            return twins
            
        # Get direct relationships
        res = session.run("""
            MATCH (from:OntologyClass)-[:ONTOLOGY_RELATION]-(to:OntologyClass)
            WHERE from.name IN $twins AND to.name IN $twins
            RETURN from.name AS source, to.name AS target
        """, twins=valid_twins)
        
        adj = {node: [] for node in valid_twins}
        for r in res:
            src, tgt = r["source"], r["target"]
            if src in adj and tgt in adj:
                adj[src].append(tgt)
                adj[tgt].append(src)
                
        # Find components
        visited = set()
        components = []
        for node in valid_twins:
            if node not in visited:
                comp = []
                queue = [node]
                visited.add(node)
                while queue:
                    curr = queue.pop(0)
                    comp.append(curr)
                    for neighbor in adj[curr]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                components.append(comp)
                
        if len(components) <= 1:
            return twins
            
        # Heal using find_reasonable_path
        from src.qa.graph_retriever import find_reasonable_path, INFRASTRUCTURE_NODES, TRANSACTION_NODES
        healed = set(components[0])
        
        def get_path_cost(p_nodes):
            if not p_nodes:
                return float('inf')
            cost = 0
            for n in p_nodes[1:-1]:
                if n in INFRASTRUCTURE_NODES:
                    cost += 100
                elif n in TRANSACTION_NODES:
                    cost += 20
                else:
                    cost += 1
            cost += len(p_nodes) - 1
            return cost

        for i in range(1, len(components)):
            comp_i = components[i]
            best_path = None
            best_cost = float('inf')
            keywords_set = healed.union(comp_i)
            
            for a in healed:
                for b in comp_i:
                    try:
                        p_nodes, _ = find_reasonable_path(a, b, keywords_set)
                        if p_nodes and len(p_nodes) > 1:
                            cost = get_path_cost(p_nodes)
                            if cost < best_cost:
                                best_cost = cost
                                best_path = p_nodes
                    except Exception:
                        pass
                        
            if best_path:
                for name in best_path:
                    healed.add(name)
            else:
                for name in comp_i:
                    healed.add(name)
                    
        # Keep any original twins that weren't resolved
        for t in twins:
            if t not in healed:
                healed.add(t)
                
        return list(healed)


@router.post("/api/scenarios/graph")
def resolve_scenario_graph(req: GraphResolveRequest):
    twins_key = tuple(sorted({str(t).strip() for t in req.twins if str(t).strip()}))
    if not twins_key:
        return {"nodes": [], "edges": []}

    return _resolve_scenario_graph_cached(twins_key)


@lru_cache(maxsize=256)
def _resolve_scenario_graph_cached(twins_key: tuple[str, ...]):
    twins = list(twins_key)
    twins = heal_twins(twins)
        
    with driver.session() as session:
        result = session.run("""
            MATCH (c:OntologyClass)
            WHERE c.name IN $twins
            RETURN c.name AS name,
                   c.chineseName AS chineseName,
                   c.description AS description,
                   c.layer AS layer
        """, twins=twins)
        
        nodes = []
        for r in result:
            name = r["name"]
            module = _classify_module(name)
            nodes.append({
                "id": name,
                "data": {
                    "label": name,
                    "chineseName": r["chineseName"] or "",
                    "description": r["description"] or "",
                    "layer": r["layer"] or "Config",
                    "module": module,
                    "type": "class",
                }
            })
            
        result = session.run("""
            MATCH (from:OntologyClass)-[r:ONTOLOGY_RELATION]->(to:OntologyClass)
            WHERE from.name IN $twins AND to.name IN $twins
            RETURN from.name AS source,
                   to.name   AS target,
                   r.name    AS label,
                   r.cardinality AS cardinality,
                   r.description AS description
        """, twins=twins)
        
        edges = []
        for r in result:
            edges.append({
                "source": r["source"],
                "target": r["target"],
                "data": {
                    "label": r["label"] or "",
                    "cardinality": r["cardinality"] or "",
                    "description": r["description"] or "",
                }
            })
            
    return {"nodes": nodes, "edges": edges}




