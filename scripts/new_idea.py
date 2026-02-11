#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from typing import Iterable, List

import yaml

_repo_root = Path(__file__).resolve().parents[1]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from scripts.lib.catalog_loader import repo_root


ID_PATTERN = re.compile(r"MI-(\d{4})")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_category_keys(root: Path) -> set[str]:
    data = yaml.safe_load(_read_text(root / "catalogs" / "categories.yaml")) or {}
    cats = data.get("categories", [])
    if not isinstance(cats, list):
        raise ValueError("categories must be a list in catalogs/categories.yaml")
    keys = {str(c.get("key")).strip() for c in cats if isinstance(c, dict) and c.get("key")}
    return keys


def _collect_ids(paths: Iterable[Path]) -> List[int]:
    out: List[int] = []
    for p in paths:
        if not p.exists():
            continue
        for match in ID_PATTERN.findall(_read_text(p)):
            try:
                out.append(int(match))
            except ValueError:
                continue
    return out


def _next_id(root: Path) -> str:
    paths = [
        root / "ideas" / "inbox.md",
        root / "ideas" / "backlog.md",
        root / "ideas" / "archived.md",
    ]
    ids = _collect_ids(paths)
    next_num = max(ids) + 1 if ids else 1
    return f"MI-{next_num:04d}"


def _format_dependencies(raw: str | None) -> str:
    if not raw:
        return "[]"
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if not parts:
        return "[]"
    return f"[{', '.join(parts)}]"


def _render_template(template_text: str, replacements: dict[str, str]) -> str:
    rendered = template_text
    for token, value in replacements.items():
        rendered = rendered.replace(token, value)
    return rendered


def _insert_into_inbox(inbox_path: Path, item_text: str) -> None:
    lines = _read_text(inbox_path).splitlines()
    try:
        idx = next(i for i, line in enumerate(lines) if line.strip() == "## Items")
    except StopIteration:
        raise ValueError("Missing '## Items' section in ideas/inbox.md")

    insert_pos = idx + 1
    new_lines = lines[:insert_pos]

    if insert_pos < len(lines) and lines[insert_pos].strip() != "":
        new_lines.append("")

    block_lines = item_text.strip("\n").splitlines()
    new_lines.extend(block_lines)
    new_lines.append("")
    new_lines.extend(lines[insert_pos:])

    inbox_path.write_text("\n".join(new_lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True, help="Short idea title")
    ap.add_argument("--proposed-category", required=True, help="Category key from catalogs/categories.yaml")
    ap.add_argument("--candidate-module-code", default="TBD", help="Candidate module code")
    ap.add_argument("--priority", choices=["P1", "P2", "P3"], default="P2")
    ap.add_argument("--dependencies", default="", help="Comma-separated list, e.g. core-platform,auth")
    ap.add_argument("--platform-compatibility", default="unknown")
    ap.add_argument("--target-persona", default="admin")
    ap.add_argument("--core-dependency-risk", choices=["yes", "no"], default="no")
    ap.add_argument("--created-at", default=date.today().isoformat())
    ap.add_argument("--notes", default="...")
    args = ap.parse_args()

    root = repo_root()
    cat_keys = _load_category_keys(root)
    if args.proposed_category not in cat_keys:
        print(
            f"ERROR: proposed_category '{args.proposed_category}' not found in catalogs/categories.yaml",
            file=sys.stderr,
        )
        return 2

    template_path = root / "standards" / "templates" / "ideas" / "idea_item.md"
    if not template_path.exists():
        print("ERROR: Missing template standards/templates/ideas/idea_item.md", file=sys.stderr)
        return 2

    new_id = _next_id(root)
    dependencies = _format_dependencies(args.dependencies)
    template_text = _read_text(template_path)
    item_text = _render_template(
        template_text,
        {
            "MI-0000": new_id,
            "<short title>": args.title,
            "<placeholder>": args.candidate_module_code,
            "<category_key>": args.proposed_category,
            "P1|P2|P3": args.priority,
            "admin|end_user|...": args.target_persona,
            "yes|no": args.core_dependency_risk,
            "YYYY-MM-DD": args.created_at,
            "dependencies: []": f"dependencies: {dependencies}",
            "platform_compatibility: unknown": f"platform_compatibility: {args.platform_compatibility}",
            "notes: ...": f"notes: {args.notes}",
        },
    )

    inbox_path = root / "ideas" / "inbox.md"
    if not inbox_path.exists():
        print("ERROR: Missing ideas/inbox.md", file=sys.stderr)
        return 2

    _insert_into_inbox(inbox_path, item_text)
    print(f"Added {new_id} to ideas/inbox.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
