from __future__ import annotations

import sys
from pathlib import Path

import shutil
from typing import Dict, List

_repo_root = Path(__file__).resolve().parents[1]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from scripts.lib.catalog_loader import load_categories, load_registry, module_root_from_registry_entry, repo_root


REQUIRED_DOC_FILES = [
    "00_overview.md",
    "01_scope_personas_usecases.md",
    "02_domain_model.md",
    "03_business_logic_and_rules.md",
    "04_ui_specifications.md",
    "05_api_contracts.md",
    "06_events_and_realtime.md",
    "07_data_model_and_migrations.md",
    "08_integrations.md",
    "09_operations_observability.md",
    "10_qc_and_acceptance.md",
]


def safe_slug(module_code: str) -> str:
    return module_code.replace(".", "_")


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for p in src.rglob("*"):
        if p.is_dir():
            continue
        rel = p.relative_to(src)
        out = dst / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, out)


def read_module_category(module_root: Path) -> str:
    import yaml

    p = module_root / "module.yaml"
    if not p.exists():
        return "uncategorized"
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    if isinstance(data, dict) and data.get("category"):
        return str(data["category"])
    return "uncategorized"


def main() -> int:
    root = repo_root()
    build_docs = root / ".build" / "docs"
    build_docs.mkdir(parents=True, exist_ok=True)

    cats = load_categories(root)
    reg = load_registry(root)

    # 1) Aggregate modules docs + assets
    modules_out = build_docs / "modules"
    if modules_out.exists():
        shutil.rmtree(modules_out)
    modules_out.mkdir(parents=True, exist_ok=True)

    module_nav_by_cat: Dict[str, List[dict]] = {}
    errors = 0

    for entry in reg:
        mroot = module_root_from_registry_entry(entry, root)
        docs_src = mroot / "docs"
        assets_src = mroot / "assets"

        slug = safe_slug(entry.module_code)
        m_out = modules_out / slug
        docs_out = m_out / "docs"
        assets_out = m_out / "assets"

        # copy docs
        if docs_src.exists():
            copy_tree(docs_src, docs_out)
        # copy assets
        if assets_src.exists():
            copy_tree(assets_src, assets_out)

        # ensure required docs exist (if module is registered)
        missing = [f for f in REQUIRED_DOC_FILES if not (docs_out / f).exists()]
        if missing:
            errors += 1
            print(f"ERROR BUILD.MODULE_DOCS_MISSING [{entry.module_code}]: {', '.join(missing)}")

        # write module index page
        idx = docs_out / "index.md"
        if not idx.exists():
            idx.write_text(
                "\n".join(
                    [
                        "---",
                        f"title: {entry.module_code}",
                        f"status: {entry.status or 'n/a'}",
                        f"owner: {entry.owner or 'n/a'}",
                        "---",
                        f"# {entry.module_code}",
                        "",
                        f"- Path: `{entry.path}`",
                        "",
                        "## Docs",
                        "",
                        "- Overview: 00_overview.md",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

        cat_key = read_module_category(mroot)

        module_nav_by_cat.setdefault(cat_key, []).append(
            {"title": entry.module_code, "path": f".build/docs/modules/{slug}/docs/index.md"}
        )

    if errors:
        return 2

    # 2) Global modules index
    modules_index = build_docs / "modules_index.md"
    lines = ["# Modules Index\n", "\n", "> Generated file. Do not edit manually.\n\n"]
    if not reg:
        lines.append("_No modules registered yet._\n")
    else:
        for m in reg:
            lines.append(f"- `{m.module_code}` ({m.status or 'n/a'}) -- `{m.path}`\n")
    modules_index.write_text("".join(lines), encoding="utf-8")

    # 3) Generate mkdocs_generated.yml (Option B)
    gen = root / "mkdocs_generated.yml"
    nav_lines = [
        "site_name: Business Modules Docs (MDS)\n",
        "site_description: Module Docs Standard (MDS) v1\n",
        "theme:\n  name: mkdocs\n",
        "nav:\n",
        "  - Home: README.md\n",
        "  - Standard:\n",
        "      - MDS v1: standards/MDS_v1.md\n",
        "  - Catalogs:\n",
        "      - Categories: catalogs/categories.yaml\n",
        "      - Modules Registry: catalogs/modules_registry.yaml\n",
        "  - Ideas:\n",
        "      - Inbox: ideas/inbox.md\n",
        "  - Generated:\n",
        "      - Modules Index: .build/docs/modules_index.md\n",
        "  - Modules:\n",
    ]

    # group by cat_key (MVP)
    for cat_key, items in module_nav_by_cat.items():
        nav_lines.append(f"      - {cat_key}:\n")
        for it in items:
            nav_lines.append(f"          - {it['title']}: {it['path']}\n")

    gen.write_text("".join(nav_lines), encoding="utf-8")
    print(f"Generated: {gen}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
