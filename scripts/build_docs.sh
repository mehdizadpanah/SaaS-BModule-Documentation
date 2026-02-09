#!/usr/bin/env bash
set -euo pipefail

python3 scripts/validate_docs.py
python3 scripts/export_catalogs.py
python3 scripts/generate_indexes.py

mkdocs build -f mkdocs.yml
