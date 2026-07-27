import os
import json
import uuid
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from pydantic import BaseModel
from web.shared import _chat_sessions, _get_vector_collection, PROJECT_ROOT

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    session_id: str | None = None
    product_line: str = "general"
    history: list[dict] | None = None
    assistant_mode: str = "sql"
    selected_classes: list[str] | None = None


class ClearRequest(BaseModel):
    session_id: str


@router.post("/api/chat")
async def chat(req: ChatRequest):
    question = req.question.strip()
    session_id = req.session_id or str(uuid.uuid4())

    if not question:
        return JSONResponse(status_code=400, content={"error": "question is required"})

    if req.history is not None:
        history = req.history
        _chat_sessions[session_id] = history
    else:
        if session_id not in _chat_sessions:
            _chat_sessions[session_id] = []
        history = _chat_sessions[session_id]

    # SQL generation relies on the authoritative physical CSV schema and
    # ontology joins. Skip ChromaDB to reduce latency and avoid irrelevant
    # modeling prose influencing table/column selection.
    vec_col = None if req.assistant_mode == "sql" else _get_vector_collection()

    from src.qa.logger import ChatTrace, CHAT_LOG_ENABLED
    trace = ChatTrace(session_id, question) if CHAT_LOG_ENABLED else None

    async def generate():
        from src.qa.engine import query_stream, extract_keywords, extract_class_links, CN_MAP, _get_class_names
        from src.qa.graph_retriever import search_graph, find_path_highlight
        import re

        # 1. Extract keywords from current question
        selected_classes = req.selected_classes or []
        keywords = list(
            dict.fromkeys(
                selected_classes
                + extract_keywords(question, fallback=not bool(selected_classes))
            )
        )

        # 2. Extract classes from recent history (last 4 turns) to enable follow-ups and pronoun resolution
        history_classes = []
        if history:
            for turn in history[-4:]:
                content = turn.get("content", "") or ""
                # Match [[ClassName]] format
                found = re.findall(r'\[\[(\w+)\]\]', content)
                for f in found:
                    if f not in history_classes:
                        history_classes.append(f)
                # Match Chinese alias and direct name
                for cn, en in CN_MAP.items():
                    if cn in content and en not in history_classes:
                        history_classes.append(en)
                for name in _get_class_names():
                    if name in content and name not in history_classes:
                        history_classes.append(name)

        # Combine, keeping current keywords first
        all_classes = list(dict.fromkeys(keywords + history_classes))

        # 3. Detect if the user is asking about relations (supports Chinese & English)
        is_rel_query = any(k in question.lower() for k in [
            "关系", "关联", "联系", "链路", "流转", "到", "连接", "沟通", "通路", "最短路径",
            "relationship", "relation", "connect", "link", "path", "flow", "between"
        ])

        highlight_data = None
        if len(all_classes) >= 2:
            # Always query relationship paths when multiple classes are active to connect them in multi-turn Q&A
            highlight_data = find_path_highlight(all_classes)
        elif len(all_classes) == 1:
            highlight_data = {"nodes": all_classes, "edges": []}

        full_answer = ""
        error_msg = None
        try:
            async for chunk in query_stream(
                question,
                history,
                vec_col,
                trace=trace,
                product_line=req.product_line,
                assistant_mode=req.assistant_mode,
                selected_classes=req.selected_classes,
            ):
                if isinstance(chunk, dict) and chunk.get("type") == "status":
                    yield f"data: {json.dumps({'type': 'status', 'content': chunk['content']}, ensure_ascii=False)}\n\n"
                else:
                    full_answer += chunk
                    yield f"data: {json.dumps({'type': 'chunk', 'content': chunk}, ensure_ascii=False)}\n\n"
        except Exception as e:
            error_msg = str(e)
            yield f"data: {json.dumps({'type': 'error', 'content': error_msg}, ensure_ascii=False)}\n\n"

        if trace:
            trace.finalize(answer=full_answer, error=error_msg)

        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": full_answer})

        if len(history) > 20:
            _chat_sessions[session_id] = history[-20:]

        class_links = extract_class_links(full_answer)

        yield f"data: {json.dumps({'type': 'done', 'session_id': session_id, 'keywords': keywords, 'class_links': class_links, 'highlight': highlight_data, 'trace_id': trace.trace_id if trace else None}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/api/chat/clear")
async def chat_clear(req: ClearRequest):
    if req.session_id in _chat_sessions:
        del _chat_sessions[req.session_id]
    return {"status": "cleared"}


@router.get("/logs")
def logs_page():
    return FileResponse(os.path.join(PROJECT_ROOT, "web", "static", "logs.html"))


@router.get("/api/logs/dates")
def log_dates():
    from src.qa.logger import list_available_dates
    return {"dates": list_available_dates(), "enabled": True}


@router.get("/api/logs")
def api_list_logs(date: str = None, limit: int = 50, offset: int = 0,
                  keyword: str = None, session_id: str = None):
    from src.qa.logger import list_logs
    result = list_logs(
        date_str=date,
        limit=limit,
        offset=offset,
        keyword=keyword,
        session_id=session_id,
    )
    return result


@router.get("/api/logs/{trace_id}")
def api_get_log(trace_id: str, date: str = None):
    from src.qa.logger import get_log
    rec = get_log(trace_id, date_str=date)
    if rec is None:
        return JSONResponse(status_code=404, content={"error": "Log not found"})
    return rec
