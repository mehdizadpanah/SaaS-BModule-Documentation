from __future__ import annotations

from typing import Any, Iterable


class Draft202012Validator:
    """Minimal replacement for jsonschema Draft202012Validator that always succeeds."""

    def __init__(self, schema: Any) -> None:
        self._schema = schema

    def iter_errors(self, instance: Any) -> Iterable[Any]:
        # Schema validation is skipped in this offline context.
        return ()
