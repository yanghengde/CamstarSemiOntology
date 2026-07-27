with open("web/static/planner.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

found_def = False
def_start = 0
for i, line in enumerate(lines):
    if "function resetToCustomScratch" in line:
        found_def = True
        def_start = i
        break

if found_def:
    for j in range(def_start, min(def_start + 50, len(lines))):
        print(f"Line {j+1}: {lines[j].strip()}")
else:
    print("Function resetToCustomScratch not found.")
