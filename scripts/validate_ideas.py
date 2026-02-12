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
NOTES_ITEM_RE = re.compile(r"^\s*-\s+(EN|FA)\s*:\s*")

REQUIRED_FIELDS = (
    "candidate_module_code",
    "proposed_category",
    "priority",
    "dependencies",
    "created_at",
    "applicable_business_segments",
    "notes",
)


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    raise SystemExit(2)


def warn(msg: str) -> None:
    print(f"WARN: {msg}")


def _read_utf8(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _line_indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _idea_blocks(lines: list[str]) -> list[tuple[int, int, str]]:
    headers: list[tuple[int, str]] = []
    for idx, line in enumerate(lines):
        m = IDEA_HEADER_RE.match(line)
        if m:
            headers.append((idx, m.group(1)))

    blocks: list[tuple[int, int, str]] = []
    for i, (start, idea_id) in enumerate(headers):
        end = headers[i + 1][0] if i + 1 < len(headers) else len(lines)
        blocks.append((start, end, idea_id))
    return blocks


def _parse_fields(lines: list[str], start: int, end: int) -> dict[str, tuple[str, int, int]]:
    fields: dict[str, tuple[str, int, int]] = {}
    for j in range(start + 1, end):
        m = FIELD_RE.match(lines[j])
        if not m:
            continue
        key = m.group(1)
        value = m.group(2).strip()
        fields[key] = (value, j + 1, _line_indent(lines[j]))
    return fields


def _check_required_structure(path: Path) -> None:
    lines = _read_utf8(path).splitlines()
    for start, end, idea_id in _idea_blocks(lines):
        fields = _parse_fields(lines, start, end)
        missing = [k for k in REQUIRED_FIELDS if k not in fields]
        if missing:
            fail(
                f"{path.as_posix()}: {idea_id} missing required field(s): "
                f"{', '.join(missing)} (near line {start+1})"
            )

        has_notes = "notes" in fields
        has_lang_bullets = False
        for j in range(start + 1, end):
            stripped = lines[j].lstrip(" ")
            if NOTES_ITEM_RE.match(stripped):
                has_lang_bullets = True
                break
        if has_lang_bullets and not has_notes:
            fail(
                f"{path.as_posix()}: {idea_id} has '- EN:'/'- FA:' bullets without a 'notes:' block "
                f"(near line {start+1})"
            )

        notes_value, notes_line, notes_indent = fields["notes"]
        if notes_value:
            fail(
                f"{path.as_posix()}: {idea_id} notes must be a block ('notes:' with empty value), "
                f"found inline value at line {notes_line}"
            )

        notes_idx = notes_line - 1
        notes_children: list[tuple[str, int, int]] = []
        j = notes_idx + 1
        while j < end:
            line = lines[j]
            if line.strip() == "":
                j += 1
                continue
            indent = _line_indent(line)
            if indent <= notes_indent:
                break
            stripped = line.lstrip(" ")
            if re.match(r"^(EN|FA)\s*:\s*", stripped):
                fail(
                    f"{path.as_posix()}: {idea_id} notes language lines must be bulleted "
                    f"('- EN:' / '- FA:') at line {j+1}"
                )
            m_lang = NOTES_ITEM_RE.match(stripped)
            if m_lang:
                notes_children.append((m_lang.group(1), j + 1, indent))
            j += 1

        if len(notes_children) != 2:
            fail(
                f"{path.as_posix()}: {idea_id} notes must contain exactly two bullets: "
                f"'- EN:' and '- FA:' (notes line {notes_line})"
            )

        langs = {lang for lang, _, _ in notes_children}
        if langs != {"EN", "FA"}:
            fail(
                f"{path.as_posix()}: {idea_id} notes must contain both '- EN:' and '- FA:' "
                f"(notes line {notes_line})"
            )

        expected_indent = notes_indent + 2
        for lang, lang_line, lang_indent in notes_children:
            if lang_indent != expected_indent:
                fail(
                    f"{path.as_posix()}: {idea_id} '{lang}' bullet has invalid nesting at line {lang_line}; "
                    f"expected indent {expected_indent} spaces under 'notes:'"
                )


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
    for start, end, idea_id in _idea_blocks(lines):
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
                    "Commerce ideas should rarely be 'all'; please specify segments unless truly universal."
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
        _check_required_structure(inbox)
        _check_applicable_business_segments(inbox)

    print("PASS: validate_ideas checks succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
