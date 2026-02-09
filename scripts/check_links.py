from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

from scripts.lib.catalog_loader import repo_root


LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def is_external(href: str) -> bool:
    return href.startswith(("http://", "https://", "mailto:"))


def normalize_target(href: str) -> str:
    # drop anchors
    href = href.split("#", 1)[0].strip()
    return unquote(href)


def main() -> int:
    root = repo_root()
    base = root / ".build" / "docs"
    if not base.exists():
        print("WARN: .build/docs not found. Run generate_indexes.py first.")
        return 2

    errors = 0
    for md in base.rglob("*.md"):
        text = md.read_text(encoding="utf-8", errors="ignore")
        for m in LINK_RE.finditer(text):
            href = m.group(1).strip()
            if not href or href.startswith("#") or is_external(href):
                continue
            target = normalize_target(href)
            if not target:
                continue

            # mkdocs relative file resolution
            target_path = (md.parent / target).resolve()
            # only enforce links that point within .build/docs
            if str(base.resolve()) not in str(target_path):
                continue
            if not target_path.exists():
                errors += 1
                print(f"ERROR LINK.MISSING: {md.relative_to(base)} -> {href}")

    if errors:
        print(f"FAIL: {errors} broken internal link(s).")
        return 2

    print("PASS: link checks succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
