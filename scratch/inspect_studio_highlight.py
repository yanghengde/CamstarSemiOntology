with open("web/static/studio.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
# Find updateGraphHighlight definition
pos = html.find("function updateGraphHighlight")
if pos != -1:
    print("Found updateGraphHighlight:")
    print(html[pos:pos+1500])
else:
    print("updateGraphHighlight not found.")
