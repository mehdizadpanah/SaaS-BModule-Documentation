#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Idea doc validations.

Currently enforces a simple formatting rule that prevents inconsistent rendering
and downstream parsing issues:

Rule: Under any "notes:" block in ideas/inbox.md (and other idea markdown files
if added later), language lines must be bullet items, e.g.

  - notes:
    - EN: ...
    - FA: ...

Non-bulleted variants like "EN:" / "FA:" are rejected.
"""

from __future__ import annotations

import re
from pathlib import Path


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    raise SystemExit(2)


def _read_utf8(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _check_notes_bullets(path: Path) -> None:
    txt = _read_utf8(path)
    lines = txt.splitlines()

    i = 0
    while i < len(lines):
        line = lines[i]

        # Match "  - notes:" with any amount of leading whitespace >=2
        m = re.match(r"^(\s*)-\s+notes\s*:\s*$", line)
        if not m:
            i += 1
            continue

        notes_indent = len(m.group(1))
        child_indent_min = notes_indent + 2
        j = i + 1

        while j < len(lines):
            nxt = lines[j]

            if nxt.strip() == "":
                j += 1
                continue

            # Stop when we exit the notes block (indent decreases to notes level or less)
            nxt_indent = len(nxt) - len(nxt.lstrip(" "))
            if nxt_indent <= notes_indent:
                break

            # Only validate immediate note items at/after child indent
            if nxt_indent >= child_indent_min:
                # Reject non-bulleted language tags like "EN:" or "FA:".
                if re.match(r"^\s{0,}EN\s*:\s*", nxt.lstrip()):
                    fail(f"{path.as_posix()}: notes language line must be a bullet: '- EN:' (line {j+1})")
                if re.match(r"^\s{0,}FA\s*:\s*", nxt.lstrip()):
                    fail(f"{path.as_posix()}: notes language line must be a bullet: '- FA:' (line {j+1})")

            j += 1

        i = j


def main() -> int:
    root = Path(__file__).resolve().parents[1]

    # Validate core idea inbox
    inbox = root / "ideas" / "inbox.md"
    if inbox.exists():
        _check_notes_bullets(inbox)

    print("PASS: validate_ideas checks succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
