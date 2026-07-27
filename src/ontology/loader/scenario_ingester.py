import os
import sys
import glob
import json

# Ensure project root is in path for 'src' imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from src.qa.vectorizer import get_vector_collection

def ingest_scenarios():
    print("[Ingester] Connecting to ChromaDB...")
    try:
        collection = get_vector_collection()
    except Exception as e:
        print(f"[Ingester] Failed to get vector collection: {e}")
        return

    scenarios_path = os.path.join(PROJECT_ROOT, "src", "ontology", "scenarios", "general")
    files = glob.glob(os.path.join(scenarios_path, "*.json"))
    print(f"[Ingester] Found {len(files)} general scenario files for ingestion.")

    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as file:
                data = json.load(file)
            
            sid = str(data.get("scenario_id"))
            name = data.get("name", "")
            desc = data.get("description", "")
            
            doc_text = f"{name} {desc}"
            doc_id = f"scenario_id_{sid}"
            metadata = {
                "type": "scenario",
                "scenario_id": sid,
                "name": name,
                "industry": "general"
            }
            
            # Upsert into ChromaDB
            print(f"  Ingesting '{name}' (ID: {doc_id}) into ChromaDB...")
            collection.upsert(
                ids=[doc_id],
                documents=[doc_text],
                metadatas=[metadata]
            )
        except Exception as e:
            print(f"[Ingester] Failed to ingest {f}: {e}")

    print(f"[Ingester] Completed. Current ChromaDB collection count: {collection.count()}")

if __name__ == "__main__":
    ingest_scenarios()
