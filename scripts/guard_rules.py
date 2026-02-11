#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import re
from pathlib import Path


PROTECTED_FILES = [
    "standards/MDS_v1.md",
    "standards/QC.md",
]

REQUIRED_HEADER_KEYS = [
    "Status:",
    "Introduced in:",
    "Last updated in:",
]


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    raise SystemExit(2)


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return p.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    root = Path(__file__).resolve().parents[1]

    for rel in PROTECTED_FILES:
        p = root / rel
        if not p.exists():
            fail(f"Missing protected file: {rel}")

        txt = read_text(p)

        # Minimal drift guard: ensure standard headers exist
        for k in REQUIRED_HEADER_KEYS:
            if k not in txt:
                fail(f"{rel}: missing required header key '{k}'")

        # Guard against forbidden external markdown links to modules-docs (same policy style)
        # Allow plain text and code blocks; forbid markdown links like [](...modules-docs...)
        forbidden = re.search(r"\]\([^)]+modules-docs[^)]*\)", txt)
        if forbidden:
            fail(f"{rel}: forbidden markdown link to modules-docs (use plain text or code block)")

    print("PASS: guard_rules checks succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
