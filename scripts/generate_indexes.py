from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Dict, List

import yaml

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
    for p in src.rglob("*"):
        if p.is_dir():
            continue
        rel = p.relative_to(src)
        out = dst / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, out)


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def read_module_category(module_root: Path) -> str:
    p = module_root / "module.yaml"
    if not p.exists():
        return "uncategorized"
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    if isinstance(data, dict) and data.get("category"):
        return str(data["category"])
    return "uncategorized"


def main() -> int:
    root = repo_root()

    # ------------------------------------------------------------------
    # 1) Clean rebuild: .build/docs becomes the single MkDocs docs_dir
    # ------------------------------------------------------------------
    build_root = root / ".build"
    build_docs = build_root / "docs"

    if build_docs.exists():
        shutil.rmtree(build_docs)
    build_docs.mkdir(parents=True, exist_ok=True)

    # Copy repo-level sources into .build/docs
    # README.md -> .build/docs/README.md
    readme = root / "README.md"
    if readme.exists():
        copy_file(readme, build_docs / "README.md")

    # CONTRIBUTING.md -> .build/docs/CONTRIBUTING.md
    contributing = root / "CONTRIBUTING.md"
    if contributing.exists():
        copy_file(contributing, build_docs / "CONTRIBUTING.md")

    # standards/ -> .build/docs/standards/
    copy_tree(root / "standards", build_docs / "standards")

    # catalogs/ -> .build/docs/catalogs/
    copy_tree(root / "catalogs", build_docs / "catalogs")

    # ideas/ -> .build/docs/ideas/
    copy_tree(root / "ideas", build_docs / "ideas")

    # ------------------------------------------------------------------
    # 2) Aggregate modules docs + assets into .build/docs/modules/<slug>/
    # ------------------------------------------------------------------
    cats = load_categories(root)
    reg = load_registry(root)

    modules_out = build_docs / "modules"
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

        if docs_src.exists():
            copy_tree(docs_src, docs_out)
        if assets_src.exists():
            copy_tree(assets_src, assets_out)

        # Required docs check (registered module must have canonical set)
        missing = [f for f in REQUIRED_DOC_FILES if not (docs_out / f).exists()]
        if missing:
            errors += 1
            print(f"ERROR BUILD.MODULE_DOCS_MISSING [{entry.module_code}]: {', '.join(missing)}")

        # Ensure module docs index exists
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

        # Group by real category from module.yaml
        cat_key = read_module_category(mroot)
        module_nav_by_cat.setdefault(cat_key, []).append(
            {
                "title": entry.module_code,
                # IMPORTANT: nav paths are relative to docs_dir (.build/docs)
                "path": f"modules/{slug}/docs/index.md",
            }
        )

    if errors:
        return 2

    # ------------------------------------------------------------------
    # 3) Global modules index inside docs_dir root
    # ------------------------------------------------------------------
    modules_index = build_docs / "modules_index.md"
    lines = ["# Modules Index\n\n", "> Generated file. Do not edit manually.\n\n"]
    if not reg:
        lines.append("_No modules registered yet._\n")
    else:
        for m in reg:
            lines.append(f"- `{m.module_code}` ({m.status or 'n/a'}) — `{m.path}`\n")
    modules_index.write_text("".join(lines), encoding="utf-8")

    # ------------------------------------------------------------------
    # 4) Generate mkdocs_generated.yml with docs_dir + site_dir
    # ------------------------------------------------------------------
    gen = root / "mkdocs_generated.yml"

    nav_lines = [
        "site_name: Business Modules Docs (MDS)\n",
        "site_description: Module Docs Standard (MDS) v1\n",
        "docs_dir: .build/docs\n",
        "site_dir: site\n",
        "theme:\n  name: mkdocs\n",
        "nav:\n",
        "  - Home: README.md\n",
        "  - Contributing: CONTRIBUTING.md\n",
        "  - Standard:\n",
        "      - MDS v1: standards/MDS_v1.md\n",
        "      - QC Standard: standards/QC.md\n",
        "  - Catalogs:\n",
        "      - Categories: catalogs/categories.yaml\n",
        "      - Modules Registry: catalogs/modules_registry.yaml\n",
        "  - Ideas:\n",
        "      - Inbox: ideas/inbox.md\n",
        "  - Generated:\n",
        "      - Modules Index: modules_index.md\n",
        "  - Modules:\n",
    ]

    # order categories by catalogs/categories.yaml if possible
    cat_order = []
    if isinstance(cats, list):
        for c in cats:
            if isinstance(c, dict) and c.get("key"):
                cat_order.append(str(c["key"]))

    # append uncategorized last
    keys = list(module_nav_by_cat.keys())
    ordered_keys = [k for k in cat_order if k in module_nav_by_cat] + [
        k for k in keys if k not in cat_order and k != "uncategorized"
    ]
    if "uncategorized" in module_nav_by_cat:
        ordered_keys.append("uncategorized")

    for cat_key in ordered_keys:
        items = module_nav_by_cat.get(cat_key, [])
        nav_lines.append(f"      - {cat_key}:\n")
        for it in items:
            nav_lines.append(f"          - {it['title']}: {it['path']}\n")

    gen.write_text("".join(nav_lines), encoding="utf-8")
    print(f"Generated: {gen}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
