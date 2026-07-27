import os
import re

catalog_path = r"D:\Deepseek\camstar\CamstarOntology\scenarios_catalog.md"
with open(catalog_path, "r", encoding="utf-8") as f:
    content = f.read()

pattern = r"### 📌 (SC_\d+): ([^\n]+)\n\n-\s+\*\*本体模型映射\*\*:\s+`([^`]+)`\n-\s+\*\*业务痛点 \(Pain Point\)\*\*:\s+([^\n]+)\n-\s+\*\*数字化映射方案 \(Digital Solution\)\*\*:\s+([^\n]+)\n-\s+\*\*客户易懂价值 \(Value to Client\)\*\*:\s+([^\n]+)"
matches = re.findall(pattern, content)
for m in matches:
    if m[0] == "SC_291":
        print("Match details for SC_291:")
        print("ID:", m[0])
        print("Title:", m[1].encode('gbk', 'ignore').decode('gbk')) # avoid print encoding issue
        print("Pain:", m[3][:50])
        print("Solution:", m[4][:50])
