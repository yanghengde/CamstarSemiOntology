import os
import json

path = r"D:\Deepseek\camstar\CamstarOntology\src\ontology\scenarios\general\scenario_SC_291.json"
print("File exists:", os.path.exists(path))
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print("Name in file:", data.get("name"))
