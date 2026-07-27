import os
import re

catalog_path = r"D:\Deepseek\camstar\CamstarOntology\scenarios_catalog.md"
with open(catalog_path, "r", encoding="utf-8") as f:
    content = f.read()

pattern = r"### 📌 (SC_\d+): ([^\n]+)\n\n-\s+\*\*本体模型映射\*\*:\s+`([^`]+)`\n-\s+\*\*业务痛点 \(Pain Point\)\*\*:\s+([^\n]+)\n-\s+\*\*数字化映射方案 \(Digital Solution\)\*\*:\s+([^\n]+)\n-\s+\*\*客户易懂价值 \(Value to Client\)\*\*:\s+([^\n]+)"
matches = re.findall(pattern, content)
ids = [m[0] for m in matches]
print("Is SC_291 matched?", "SC_291" in ids)
print("Total IDs matched:", len(ids))
# Print count of each ID to see if there are duplicates in the catalog
from collections import Counter
counts = Counter(ids)
dupes = {k: v for k, v in counts.items() if v > 1}
print("Duplicates in catalog matches:", dupes)
