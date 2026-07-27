"""
Wiki Manager – Relationship Wiki Knowledge Base Engine
──────────────────────────────────────────────────────
Manages per-product-line Markdown wiki files for each ontology relationship.
Supports:
  • Read / Write / Update individual wiki files
  • Batch generation via LLM (DeepSeek)
  • Product-line isolation
  • Collect all relationships from ontology JSONs
"""
import os
import json
import glob
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=True)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WIKI_KB_PATH = os.path.join(PROJECT_ROOT, "src", "ontology", "wiki_kb")
RELATIONSHIPS_DIR = os.path.join(WIKI_KB_PATH, "relationships")
PRODUCT_LINES_FILE = os.path.join(WIKI_KB_PATH, "product_lines.json")

# LLM config
API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")
LLM_TIMEOUT = float(os.getenv("LLM_TIMEOUT", "120"))

# Wiki review flag (for future use)
WIKI_REVIEW_REQUIRED = os.getenv("WIKI_REVIEW_REQUIRED", "false").lower() == "true"

_llm_client = None


def _get_llm():
    global _llm_client
    if _llm_client is None:
        from openai import OpenAI
        _llm_client = OpenAI(api_key=API_KEY, base_url=BASE_URL, timeout=LLM_TIMEOUT)
    return _llm_client


# ══════════════════════════════════════════════════════
#  Product Line Helpers
# ══════════════════════════════════════════════════════

def load_product_lines() -> list[dict]:
    """Load all product line definitions from product_lines.json."""
    try:
        with open(PRODUCT_LINES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("product_lines", [])
    except Exception as e:
        print(f"[WikiManager] Error loading product lines: {e}")
        return [{"id": "general", "name": "通用", "description": "", "icon": "📦", "color": "#009999"}]


def save_product_lines(product_lines: list[dict]) -> bool:
    """Save all product line definitions to product_lines.json."""
    try:
        with open(PRODUCT_LINES_FILE, "w", encoding="utf-8") as f:
            json.dump({"product_lines": product_lines}, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"[WikiManager] Error saving product lines: {e}")
        return False


def get_product_line_info(product_line_id: str) -> dict:
    """Get a single product line's info by ID."""
    for pl in load_product_lines():
        if pl["id"] == product_line_id:
            return pl
    return {"id": product_line_id, "name": product_line_id, "description": "", "icon": "📦", "color": "#999"}


# ══════════════════════════════════════════════════════
#  Relationship Collection
# ══════════════════════════════════════════════════════

def collect_all_relationships() -> list[dict]:
    """
    Scan all *_ontology.json files (including cross_module_ontology.json)
    and return a unified list of relationships.
    Each item: { fromClass, toClass, relationName, cardinality, description, source_file }
    """
    relationships = []
    seen_keys = set()

    json_files = glob.glob(os.path.join(WIKI_KB_PATH, "*_ontology.json"))
    for file_path in json_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            source = os.path.basename(file_path)
            for rel in data.get("relationships", []):
                key = f"{rel['fromClass']}_{rel['relationName']}_{rel['toClass']}"
                if key not in seen_keys:
                    seen_keys.add(key)
                    relationships.append({
                        "fromClass": rel["fromClass"],
                        "toClass": rel["toClass"],
                        "relationName": rel["relationName"],
                        "cardinality": rel.get("cardinality", ""),
                        "description": rel.get("description", ""),
                        "source_file": source,
                    })
        except Exception as e:
            print(f"[WikiManager] Error reading {file_path}: {e}")

    return relationships


# ══════════════════════════════════════════════════════
#  Wiki File Path Helpers
# ══════════════════════════════════════════════════════

def _wiki_filename(from_class: str, rel_name: str, to_class: str) -> str:
    """Generate wiki filename: {From}_{Rel}_{To}.md"""
    return f"{from_class}_{rel_name}_{to_class}.md"


def _wiki_filepath(product_line: str, from_class: str, rel_name: str, to_class: str) -> str:
    """Full filesystem path for a wiki file."""
    filename = _wiki_filename(from_class, rel_name, to_class)
    return os.path.join(RELATIONSHIPS_DIR, product_line, filename)


def _ensure_product_dir(product_line: str):
    """Ensure the product line directory exists."""
    dirpath = os.path.join(RELATIONSHIPS_DIR, product_line)
    os.makedirs(dirpath, exist_ok=True)


# ══════════════════════════════════════════════════════
#  Wiki CRUD Operations
# ══════════════════════════════════════════════════════

def read_wiki(product_line: str, from_class: str, rel_name: str, to_class: str) -> dict:
    """
    Read a wiki file. Returns:
      { found: bool, content: str, path: str, metadata: dict }
    """
    filepath = _wiki_filepath(product_line, from_class, rel_name, to_class)

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract metadata from YAML-like header if present
        metadata = _extract_metadata(content)
        
        # Check review status
        if WIKI_REVIEW_REQUIRED and metadata.get("status") != "approved":
            return {
                "found": False,
                "content": "",
                "path": filepath,
                "metadata": metadata,
                "reason": "pending_review",
            }

        return {
            "found": True,
            "content": content,
            "path": filepath,
            "metadata": metadata,
        }

    return {
        "found": False,
        "content": "",
        "path": filepath,
        "metadata": {},
    }


def save_wiki(product_line: str, from_class: str, rel_name: str, to_class: str,
              content: str, editor: str = "system") -> dict:
    """
    Save/update a wiki file. Used by both LLM generation and manual editing.
    Adds/updates metadata header with edit history.
    """
    _ensure_product_dir(product_line)
    filepath = _wiki_filepath(product_line, from_class, rel_name, to_class)

    # Track edit history in a companion JSON file
    history_path = filepath.replace(".md", ".meta.json")
    history = _load_history(history_path)

    history["edits"].append({
        "editor": editor,
        "timestamp": datetime.now().isoformat(),
        "content_length": len(content),
    })
    history["last_modified"] = datetime.now().isoformat()
    history["last_editor"] = editor

    # If review is required, newly generated content starts as "draft"
    if WIKI_REVIEW_REQUIRED and editor == "llm":
        history["status"] = "draft"
    else:
        history["status"] = "approved"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    return {"saved": True, "path": filepath, "history": history}


def _load_history(history_path: str) -> dict:
    """Load or create edit history metadata."""
    if os.path.exists(history_path):
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "created": datetime.now().isoformat(),
        "last_modified": datetime.now().isoformat(),
        "last_editor": "system",
        "status": "approved",
        "edits": [],
    }


def _extract_metadata(content: str) -> dict:
    """Extract simple metadata from wiki content (first few lines with > markers)."""
    metadata = {}
    for line in content.split("\n")[:10]:
        line = line.strip()
        if line.startswith("> **") and "**:" in line:
            try:
                key = line.split("**")[1].rstrip(":")
                value = line.split("**:")[-1].strip()
                metadata[key] = value
            except Exception:
                pass
    return metadata


# ══════════════════════════════════════════════════════
#  Wiki Statistics
# ══════════════════════════════════════════════════════

def get_wiki_stats(product_line: str = None) -> dict:
    """
    Get wiki coverage statistics.
    If product_line is specified, stats for that line only.
    Otherwise, stats for all lines.
    """
    all_rels = collect_all_relationships()
    total = len(all_rels)
    product_lines = load_product_lines()

    if product_line:
        product_lines = [pl for pl in product_lines if pl["id"] == product_line]

    stats = {}
    for pl in product_lines:
        pl_id = pl["id"]
        pl_dir = os.path.join(RELATIONSHIPS_DIR, pl_id)
        existing = 0
        if os.path.isdir(pl_dir):
            existing = len([f for f in os.listdir(pl_dir) if f.endswith(".md")])
        stats[pl_id] = {
            "name": pl["name"],
            "total_relationships": total,
            "wiki_count": existing,
            "coverage": round(existing / total * 100, 1) if total > 0 else 0,
        }

    return {"product_lines": stats, "total_relationships": total}


# ══════════════════════════════════════════════════════
#  Wiki Search (for QA — wiki-first before LLM)
# ══════════════════════════════════════════════════════

def search_wiki(question: str, keywords: list[str], product_line: str = "general", top_k: int = 3) -> list[dict]:
    """
    Search relationship wiki files in the active product line (falling back to general)
    for content matching the user question.
    Returns list of {product_line, relationship, content, score} sorted by relevance.
    """
    results = []
    question_lower = question.lower()

    if not os.path.isdir(RELATIONSHIPS_DIR):
        return results

    # Only scan the selected product line and fall back to general
    dirs_to_scan = [product_line]
    if product_line != "general" and "general" not in dirs_to_scan:
        dirs_to_scan.append("general")

    for pl_dir in dirs_to_scan:
        pl_path = os.path.join(RELATIONSHIPS_DIR, pl_dir)
        if not os.path.isdir(pl_path):
            continue

        for filename in os.listdir(pl_path):
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(pl_path, filename)
            fname_lower = filename.lower()

            # Score: keyword matches in filename + content
            score = 0
            for kw in keywords:
                if kw.lower() in fname_lower:
                    score += 3  # filename match is strong signal
                if kw.lower() in question_lower:
                    score += 1

            # Also check partial class name matches
            for kw in keywords:
                parts = kw.replace("_", " ").split()
                for part in parts:
                    if len(part) >= 3 and part.lower() in fname_lower:
                        score += 1

            if score == 0:
                continue  # skip irrelevant files

            # Boost score for matches in the active product line folder
            if pl_dir == product_line:
                score += 5

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Boost score if question terms appear in content
                content_lower = content.lower()
                for kw in keywords:
                    if kw.lower() in content_lower:
                        score += 2

                # Parse relationship from filename: {From}_{Rel}_{To}.md
                import re
                rel_name = filename.replace(".md", "")
                match_rel = re.match(r'^([A-Z][a-zA-Z0-9]+)_([A-Z0-9_]+)_([A-Z][a-zA-Z0-9]+)$', rel_name)
                if match_rel:
                    rel_display = f"{match_rel.group(1)} → {match_rel.group(2)} → {match_rel.group(3)}"
                else:
                    parts = rel_name.split("_", 2)
                    if len(parts) >= 3:
                        rel_display = f"{parts[0]} → {parts[1]} → {parts[2]}"
                    else:
                        rel_display = rel_name

                results.append({
                    "product_line": pl_dir,
                    "relationship": rel_display,
                    "filename": filename,
                    "content": content,
                    "score": score,
                })
            except Exception:
                continue

    # Sort by score descending, take top_k
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


# ══════════════════════════════════════════════════════
#  LLM Wiki Generation
# ══════════════════════════════════════════════════════

WIKI_GENERATE_PROMPT = """你是一个 Siemens Opcenter (Camstar) MES 领域专家。
当前产品线: {product_line_name} ({product_line_desc})

请为以下本体关系(Relationship)生成详细的知识库文档：

关系: {from_class} --[{rel_name}]--> {to_class}
基数: {cardinality}
现有描述: {description}

请按以下 Markdown 格式生成内容（直接输出 Markdown，不要包裹在代码块中）：

# {from_class} → {rel_name} → {to_class}

> **产品线**: {product_line_name}
> **基数**: {cardinality}
> **生成时间**: {date}
> **来源**: LLM 自动生成

## 关系说明

（这个关系的含义，在 {product_line_name} 场景中的具体含义，2-3 段）

## 业务场景

### 何时需要配置此关系？
（列出 2-3 个具体的 {product_line_name} 业务场景）

### {product_line_name} 典型示例
（具体的操作示例，包含步骤和参数）

## 配置要点
（5-8 个关键注意事项，条目格式）

## 常见问题 FAQ

**Q: 问题1**
A: 回答1

**Q: 问题2**
A: 回答2

**Q: 问题3**
A: 回答3

---
要求：
- 内容必须结合 {product_line_name} 的实际生产场景
- 如果是"通用 (无产品线)"，则给出通用 Opcenter 建模指导
- 示例要具体可操作
- 全部用中文撰写，技术术语保留英文
"""


def generate_wiki_for_relationship(
    product_line: str,
    from_class: str,
    rel_name: str,
    to_class: str,
    cardinality: str = "",
    description: str = "",
    overwrite: bool = False,
) -> dict:
    """
    Use LLM to generate a wiki document for a single relationship.
    Returns: { generated: bool, path: str, content: str }
    """
    # Check if already exists
    filepath = _wiki_filepath(product_line, from_class, rel_name, to_class)
    if os.path.exists(filepath) and not overwrite:
        return {"generated": False, "path": filepath, "reason": "already_exists"}

    pl_info = get_product_line_info(product_line)
    today = datetime.now().strftime("%Y-%m-%d")

    prompt = WIKI_GENERATE_PROMPT.format(
        product_line_name=pl_info["name"],
        product_line_desc=pl_info.get("description", ""),
        from_class=from_class,
        rel_name=rel_name,
        to_class=to_class,
        cardinality=cardinality,
        description=description,
        date=today,
    )

    try:
        client = _get_llm()
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "你是 Siemens Opcenter MES 领域专家，请根据要求生成高质量的知识库文档。直接输出 Markdown 内容。"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=4096,
        )
        content = response.choices[0].message.content.strip()

        # Strip wrapping code blocks if LLM adds them
        if content.startswith("```markdown"):
            content = content[len("```markdown"):].strip()
        elif content.startswith("```md"):
            content = content[len("```md"):].strip()
        elif content.startswith("```"):
            content = content[3:].strip()
        if content.endswith("```"):
            content = content[:-3].strip()

        # Save the generated wiki
        save_result = save_wiki(product_line, from_class, rel_name, to_class, content, editor="llm")

        return {"generated": True, "path": filepath, "content": content}

    except Exception as e:
        print(f"[WikiManager] LLM generation failed for {from_class}_{rel_name}_{to_class}: {e}")
        return {"generated": False, "path": filepath, "reason": str(e)}


async def strip_markdown_code_blocks_stream(async_generator):
    """
    Strips leading and trailing markdown code block markers from an async token stream.
    For example, strips leading ```markdown\n, ```md\n, ```\n
    and trailing ``` or similar if they occur.
    """
    buffer = ""
    header_checked = False
    WINDOW_SIZE = 15
    sliding_buffer = ""

    async for chunk in async_generator:
        if not header_checked:
            buffer += chunk
            stripped = buffer.lstrip()
            if not stripped:
                continue
            if stripped.startswith("`"):
                if not stripped.startswith("```"):
                    if len(stripped) < 3:
                        continue
                if "\n" not in stripped:
                    continue
                lines = stripped.split("\n", 1)
                first_line = lines[0].strip()
                if first_line.startswith("```"):
                    buffer = lines[1] if len(lines) > 1 else ""
            else:
                if "\n" not in buffer and len(buffer) < 25:
                    continue
            header_checked = True
            sliding_buffer = buffer
            buffer = ""
            continue
        
        sliding_buffer += chunk
        if len(sliding_buffer) > WINDOW_SIZE:
            yield_len = len(sliding_buffer) - WINDOW_SIZE
            yield sliding_buffer[:yield_len]
            sliding_buffer = sliding_buffer[yield_len:]
            
    if sliding_buffer:
        cleaned = sliding_buffer.rstrip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].rstrip()
        yield cleaned


async def generate_wiki_for_relationship_stream(
    product_line: str,
    from_class: str,
    rel_name: str,
    to_class: str,
    cardinality: str = "",
    description: str = "",
):
    """
    Use AsyncOpenAI to generate a wiki document for a single relationship,
    yielding content chunks progressively and saving it at completion.
    """
    pl_info = get_product_line_info(product_line)
    today = datetime.now().strftime("%Y-%m-%d")

    prompt = WIKI_GENERATE_PROMPT.format(
        product_line_name=pl_info["name"],
        product_line_desc=pl_info.get("description", ""),
        from_class=from_class,
        rel_name=rel_name,
        to_class=to_class,
        cardinality=cardinality,
        description=description,
        date=today,
    )

    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL, timeout=LLM_TIMEOUT)

    response = await client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "你是 Siemens Opcenter MES 领域专家，请根据要求生成高质量的知识库文档。直接输出 Markdown 内容。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=4096,
        stream=True,
    )

    async def token_generator():
        async for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    clean_generator = strip_markdown_code_blocks_stream(token_generator())

    full_content = ""
    async for token in clean_generator:
        full_content += token
        yield token

    # Save the generated wiki so that it is persisted
    save_wiki(product_line, from_class, rel_name, to_class, full_content.strip(), editor="llm")


def generate_all_wikis(product_line: str, overwrite: bool = False,
                       progress_callback=None) -> dict:
    """
    Batch generate wikis for ALL relationships under a given product line.
    Returns: { total, generated, skipped, failed, details: [...] }
    """
    relationships = collect_all_relationships()
    total = len(relationships)
    generated = 0
    skipped = 0
    failed = 0
    details = []

    for i, rel in enumerate(relationships):
        result = generate_wiki_for_relationship(
            product_line=product_line,
            from_class=rel["fromClass"],
            rel_name=rel["relationName"],
            to_class=rel["toClass"],
            cardinality=rel.get("cardinality", ""),
            description=rel.get("description", ""),
            overwrite=overwrite,
        )

        if result.get("generated"):
            generated += 1
            status = "generated"
        elif result.get("reason") == "already_exists":
            skipped += 1
            status = "skipped"
        else:
            failed += 1
            status = "failed"

        detail = {
            "index": i + 1,
            "total": total,
            "relationship": f"{rel['fromClass']}_{rel['relationName']}_{rel['toClass']}",
            "status": status,
        }
        details.append(detail)

        if progress_callback:
            progress_callback(detail)

        # Rate limiting: small delay between LLM calls
        if result.get("generated"):
            time.sleep(0.5)

    return {
        "product_line": product_line,
        "total": total,
        "generated": generated,
        "skipped": skipped,
        "failed": failed,
        "details": details,
    }


# ══════════════════════════════════════════════════════
#  CLI Entry Point (for manual batch generation)
# ══════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    pl = sys.argv[1] if len(sys.argv) > 1 else "general"
    overwrite = "--overwrite" in sys.argv

    print(f"[WikiManager] Generating wikis for product line: {pl}")
    print(f"[WikiManager] Overwrite: {overwrite}")

    all_rels = collect_all_relationships()
    print(f"[WikiManager] Found {len(all_rels)} relationships")

    def on_progress(detail):
        print(f"  [{detail['index']}/{detail['total']}] {detail['relationship']} → {detail['status']}")

    result = generate_all_wikis(pl, overwrite=overwrite, progress_callback=on_progress)

    print(f"\n[WikiManager] Done! Generated: {result['generated']}, "
          f"Skipped: {result['skipped']}, Failed: {result['failed']}")
