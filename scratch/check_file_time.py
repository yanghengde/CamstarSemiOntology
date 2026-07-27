import os
import time

path = r"D:\Deepseek\camstar\CamstarOntology\src\ontology\scenarios\general\scenario_SC_291.json"
mtime = os.path.getmtime(path)
print("File modification time:", time.ctime(mtime))
print("Current time:", time.ctime())
