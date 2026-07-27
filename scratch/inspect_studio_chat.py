with open("web/static/studio.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
scripts = re.findall(r'<script[^>]*src="([^"]+)"', html)
print("Scripts found in studio.html:", scripts)

for line in html.splitlines():
    if "chat" in line.lower() or "qa" in line.lower():
        # Clean line to print without emojis or non-ascii
        clean_line = "".join(c for c in line if ord(c) < 128)
        if len(clean_line.strip()) > 0:
            print("Line:", clean_line.strip()[:100])
