#!/usr/bin/env python3
"""Regenerate every reviewed semiconductor ontology batch in dependency order."""

from pathlib import Path

from generate_ontology_batch import DEFAULT_FIELDS, DEFAULT_ONTOLOGY_DIR, DEFAULT_TABLES, generate


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BATCH_DIR = PROJECT_ROOT / "src" / "ontology" / "batches"


def main() -> int:
    configs = sorted(BATCH_DIR.glob("[0-9][0-9]_*.json"))
    for config in configs:
        ontology_path, modeling_path = generate(
            config,
            DEFAULT_TABLES,
            DEFAULT_FIELDS,
            DEFAULT_ONTOLOGY_DIR,
        )
        print(f"{config.name}: {ontology_path.name}, {modeling_path.name}")
    print(f"generated_batches={len(configs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
