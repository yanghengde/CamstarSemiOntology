import requests
import json

base_url = "http://127.0.0.1:5050"

payload = {
    "scenario_id": "99",
    "industry": "general",
    "name": "Test SPC quality control scenario",
    "description": "An optimized automated test checking SPC limits and quality constraints",
    "steps": [
        {
            "step": "Step 1: Ingestion",
            "desc": "Mock test ingestion step",
            "twins": ["Container"],
            "rels": [],
            "code": "SELECT * FROM Container;"
        }
    ]
}

# 1. Post to save scenario
print("Sending save scenario request via IPv4...")
save_res = requests.post(f"{base_url}/api/scenarios/save", json=payload)
print(f"Save Status Code: {save_res.status_code}")
print(f"Save Response: {save_res.text}")

# 2. Query search RAG
print("\nQuerying search API via IPv4...")
search_res = requests.get(f"{base_url}/api/scenarios/search", params={"query": "optimized automated test"})
print(f"Search Status Code: {search_res.status_code}")
print(f"Search Response:")
print(json.dumps(search_res.json(), indent=2, ensure_ascii=False))
