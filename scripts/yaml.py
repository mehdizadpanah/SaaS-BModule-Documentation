from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

def safe_load(stream: str) -> Dict[str, Any]:
    """Minimal YAML loader for the small catalog files used by doctor."""
    lines = stream.splitlines()
    parsed = _parse_lines(lines)
    if not isinstance(parsed, dict):
        raise ValueError("YAML root must be mapping")
    return parsed

def safe_load_all(stream: str) -> List[Any]:
    return [safe_load(part) for part in stream.split("\n---\n") if part.strip()]


def _parse_lines(lines: List[str]) -> Any:
    root: Dict[str, Any] = {}
    stack: List[Tuple[int, Any]] = [(-1, root)]

    def _next_significant_line(idx: int) -> Optional[Tuple[int, str]]:
        for j in range(idx + 1, len(lines)):
            ln = lines[j]
            if not ln.strip() or ln.lstrip().startswith("#"):
                continue
            return j, ln
        return None

    for idx, raw in enumerate(lines):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        stripped = raw.lstrip()

        if stripped.startswith("- "):
            if not isinstance(parent, list):
                raise ValueError("List entry without list container")
            entry = stripped[2:].strip()
            if entry:
                if ":" in entry:
                    key, value, has_value = _parse_key_value(entry)
                    if not has_value:
                        entry_value: Dict[str, Any] = {key: {}}
                        parent.append(entry_value)
                        stack.append((indent, entry_value[key]))
                        continue
                    entry_value = {key: value}
                else:
                    entry_value = _parse_scalar(entry)
                parent.append(entry_value)
                if isinstance(entry_value, dict):
                    stack.append((indent, entry_value))
            else:
                obj: Dict[str, Any] = {}
                parent.append(obj)
                stack.append((indent, obj))
            continue

        key, value, has_value = _parse_key_value(stripped)
        if not isinstance(parent, dict):
            raise ValueError("Mapping key found outside of mapping container")

        if has_value:
            parent[key] = value
            continue

        next_line = _next_significant_line(idx)
        container: Any = {}
        if next_line:
            next_indent, next_raw = next_line
            if next_indent > indent and next_raw.lstrip().startswith("- "):
                container = []
        parent[key] = container
        stack.append((indent, container))

    return root


def _parse_key_value(text: str) -> Tuple[str, Optional[Any], bool]:
    if ":" not in text:
        raise ValueError(f"Invalid key-value line: {text}")
    key, rest = text.split(":", 1)
    key = key.strip()
    value = rest.strip()
    if value == "":
        return key, None, False
    return key, _parse_scalar(value), True


def _parse_scalar(value: str) -> Any:
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    lowered = value.lower()
    if lowered == "null" or lowered == "none":
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value
