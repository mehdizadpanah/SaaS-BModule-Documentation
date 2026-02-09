from __future__ import annotations

from scripts.lib.catalog_loader import load_categories, load_registry, repo_root


def main() -> int:
    root = repo_root()
    out_dir = root / ".build" / "docs"
    out_dir.mkdir(parents=True, exist_ok=True)

    cats = load_categories(root)
    reg = load_registry(root)

    by_cat = {}
    for m in reg:
        by_cat.setdefault(m.path, m)

    lines = ["# Modules Index\n\n"]
    lines.append("> Generated file. Do not edit manually.\n\n")

    # categories list
    lines.append("## Categories\n\n")
    for c in cats:
        lines.append(f"- `{c.get('key')}`: {c.get('title')} - {c.get('description')}\n")

    # modules list
    lines.append("\n## Modules\n\n")
    if not reg:
        lines.append("_No modules registered yet._\n")
    else:
        for m in reg:
            lines.append(f"- `{m.module_code}` ({m.status or 'n/a'}) - `{m.path}`\n")

    (out_dir / "modules_index.md").write_text("".join(lines), encoding="utf-8")
    print(f"Generated: {out_dir / 'modules_index.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
