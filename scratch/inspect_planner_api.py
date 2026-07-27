with open("web/static/planner.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

found_line = -1
for i, line in enumerate(lines):
    if "/api/scenarios/plan" in line:
        found_line = i
        break

if found_line != -1:
    for j in range(max(0, found_line - 20), min(len(lines), found_line + 40)):
        print(f"Line {j+1}: {lines[j].strip()}")
else:
    print("API endpoint not found in planner.html.")
