from __future__ import annotations

import sys
from pathlib import Path

import json

_repo_root = Path(__file__).resolve().parents[1]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from scripts.lib.catalog_loader import load_categories, load_registry, repo_root


def main() -> int:
    root = repo_root()
    out_dir = root / ".build" / "exports"
    out_dir.mkdir(parents=True, exist_ok=True)

    categories = load_categories(root)
    registry = [m.__dict__ for m in load_registry(root)]

    (out_dir / "categories.json").write_text(
        json.dumps(categories, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "modules_registry.json").write_text(
        json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Minimal MD exports (human-readable)
    md = ["# Catalog Export\n", "## Categories\n"]
    for c in categories:
        md.append(f"- `{c.get('key')}`: {c.get('title')} - {c.get('description')}\n")
    md.append("\n## Modules\n")
    for m in registry:
        md.append(f"- `{m.get('module_code')}` -> `{m.get('path')}`\n")

    (out_dir / "catalog.md").write_text("".join(md), encoding="utf-8")
    print(f"Exported catalogs to: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
