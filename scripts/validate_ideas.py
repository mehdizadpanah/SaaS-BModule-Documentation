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

IDEA_HEADER_RE = re.compile(r"^- \[[ xX]\]\s+(MI-\d{4})\b")
FIELD_RE = re.compile(r"^\s*-\s+([a-z0-9_]+)\s*:\s*(.*)$")
SNAKE_CASE_RE = re.compile(r"^[a-z0-9]+(_[a-z0-9]+)*$")


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    raise SystemExit(2)


def warn(msg: str) -> None:
    print(f"WARN: {msg}")


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


def _parse_list_value(raw: str) -> list[str] | None:
    m = re.fullmatch(r"\[(.*)\]", raw.strip())
    if not m:
        return None
    inner = m.group(1).strip()
    if not inner:
        return []
    parts = [p.strip() for p in inner.split(",")]
    if any(p == "" for p in parts):
        return []
    return parts


def _check_applicable_business_segments(path: Path) -> None:
    lines = _read_utf8(path).splitlines()
    headers: list[tuple[int, str]] = []
    for idx, line in enumerate(lines):
        m = IDEA_HEADER_RE.match(line)
        if m:
            headers.append((idx, m.group(1)))

    for i, (start, idea_id) in enumerate(headers):
        end = headers[i + 1][0] if i + 1 < len(headers) else len(lines)
        found_value: str | None = None
        found_category: str | None = None
        found_line = start + 1

        for j in range(start + 1, end):
            m = FIELD_RE.match(lines[j])
            if not m:
                continue
            if m.group(1) == "proposed_category":
                found_category = m.group(2).strip()
            if m.group(1) == "applicable_business_segments":
                found_value = m.group(2).strip()
                found_line = j + 1

        if found_value is None:
            fail(
                f"{path.as_posix()}: {idea_id} missing required field "
                f"'applicable_business_segments:' (near line {start+1})"
            )

        if found_value == "all":
            if found_category == "commerce":
                warn(
                    f"{path.as_posix()}: {idea_id} uses applicable_business_segments=all "
                    f"with proposed_category=commerce (line {found_line}). "
                    "Consider using a segment-specific list."
                )
            continue

        values = _parse_list_value(found_value)
        if values is None:
            fail(
                f"{path.as_posix()}: {idea_id} has invalid applicable_business_segments "
                f"'{found_value}' at line {found_line}. Use 'all' or [item1, item2]."
            )

        if not values:
            fail(
                f"{path.as_posix()}: {idea_id} applicable_business_segments list must be non-empty "
                f"(line {found_line})"
            )

        for seg in values:
            if not SNAKE_CASE_RE.fullmatch(seg):
                fail(
                    f"{path.as_posix()}: {idea_id} segment '{seg}' must be lowercase_snake_case "
                    f"(line {found_line})"
                )

        if len(set(values)) != len(values):
            fail(
                f"{path.as_posix()}: {idea_id} applicable_business_segments has duplicate values "
                f"(line {found_line})"
            )


def main() -> int:
    root = Path(__file__).resolve().parents[1]

    # Validate core idea inbox
    inbox = root / "ideas" / "inbox.md"
    if inbox.exists():
        _check_notes_bullets(inbox)
        _check_applicable_business_segments(inbox)

    print("PASS: validate_ideas checks succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
