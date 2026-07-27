with open("web/static/planner.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    line_lower = line.lower()
    if any(k in line_lower for k in ["reset", "clear", "history"]):
        print(f"Line {i+1}: {line.strip()}")
