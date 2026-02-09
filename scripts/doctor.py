from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml
from jsonschema import Draft202012Validator

from scripts.lib.catalog_loader import (
    load_categories,
    load_registry,
    module_root_from_registry_entry,
    repo_root,
)

REQUIRED_ROOT_DIRS = [
    "scripts",
    "standards",
    "catalogs",
    "ideas",
    "modules",
]

REQUIRED_CATALOG_FILES = [
    "catalogs/categories.yaml",
    "catalogs/modules_registry.yaml",
]

SCHEMA_PATH = "standards/rules/module_manifest.schema.json"


@dataclass
class Finding:
    level: str  # "error" | "warn"
    rule_id: str
    message: str
    module_code: Optional[str] = None
    path: Optional[str] = None


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(_read_text(path))


def _load_yaml(path: Path) -> Dict[str, Any]:
    data = yaml.safe_load(_read_text(path)) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be mapping: {path}")
    return data


def validate_repo_structure(root: Path, findings: List[Finding]) -> None:
    for d in REQUIRED_ROOT_DIRS:
        if not (root / d).exists():
            findings.append(Finding("error", "L1.ROOT_DIR_MISSING", f"Missing required dir: {d}", path=d))
    for f in REQUIRED_CATALOG_FILES:
        if not (root / f).exists():
            findings.append(Finding("error", "L1.CATALOG_FILE_MISSING", f"Missing required file: {f}", path=f))
    if not (root / SCHEMA_PATH).exists():
        findings.append(Finding("error", "L1.SCHEMA_MISSING", f"Missing schema: {SCHEMA_PATH}", path=SCHEMA_PATH))


def validate_registry_and_categories(root: Path, findings: List[Finding]) -> Tuple[List[Dict[str, Any]], List[Any]]:
    cats = load_categories(root)
    keys = [c.get("key") for c in cats if isinstance(c, dict)]
    if len(keys) != len(set(keys)):
        findings.append(Finding("error", "L4.CATEGORY_KEY_NOT_UNIQUE", "Duplicate category key(s) in categories.yaml"))

    registry = load_registry(root)
    module_codes = [m.module_code for m in registry if m.module_code]
    if len(module_codes) != len(set(module_codes)):
        findings.append(Finding("error", "L4.MODULE_CODE_NOT_UNIQUE", "Duplicate module_code(s) in modules_registry.yaml"))

    return cats, registry


def _validator(root: Path) -> Draft202012Validator:
    schema = _load_json(root / SCHEMA_PATH)
    return Draft202012Validator(schema)


def validate_module_manifest(
    module_code: str,
    module_root: Path,
    cats_by_key: set,
    validator: Draft202012Validator,
    findings: List[Finding],
) -> None:
    manifest_path = module_root / "module.yaml"
    if not manifest_path.exists():
        findings.append(Finding("error", "L1.MANIFEST_MISSING", "Missing module.yaml", module_code=module_code, path=str(manifest_path)))
        return

    try:
        manifest = _load_yaml(manifest_path)
    except Exception as e:
        findings.append(Finding("error", "L2.MANIFEST_YAML_INVALID", f"Invalid YAML: {e}", module_code=module_code, path=str(manifest_path)))
        return

    errors = sorted(validator.iter_errors(manifest), key=lambda e: e.path)
    for e in errors:
        findings.append(Finding("error", "L2.MANIFEST_SCHEMA", f"{e.message} (at {list(e.path)})", module_code=module_code, path=str(manifest_path)))

    cat = manifest.get("category")
    if cat and cat not in cats_by_key:
        findings.append(Finding("error", "L3.CATEGORY_INVALID", f"category '{cat}' not found in catalogs/categories.yaml", module_code=module_code, path=str(manifest_path)))

    def _check_rel(p: str, rule_id: str) -> None:
        abs_path = (module_root / p).resolve()
        if not abs_path.exists():
            findings.append(Finding("error", rule_id, f"Referenced path not found: {p}", module_code=module_code, path=str(manifest_path)))

    for ev_field in ("events_published", "events_consumed"):
        items = manifest.get(ev_field) or []
        if isinstance(items, list):
            for it in items:
                if isinstance(it, dict) and "contract" in it:
                    _check_rel(str(it["contract"]), "L3.EVENT_CONTRACT_MISSING")
                if isinstance(it, dict) and "examples" in it:
                    _check_rel(str(it["examples"]), "L3.EVENT_EXAMPLES_MISSING")


def _emit(findings: List[Finding], json_out: Optional[str]) -> int:
    errors = [f for f in findings if f.level == "error"]
    warns = [f for f in findings if f.level == "warn"]

    if errors or warns:
        for f in findings:
            loc = f" [{f.module_code}]" if f.module_code else ""
            p = f" ({f.path})" if f.path else ""
            print(f"{f.level.upper()} {f.rule_id}{loc}: {f.message}{p}")
    else:
        print("PASS: doctor checks succeeded.")

    if json_out:
        out = {
            "errors": [f.__dict__ for f in errors],
            "warnings": [f.__dict__ for f in warns],
        }
        Path(json_out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    return 2 if errors else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", dest="json_out", default=None)
    args = ap.parse_args()

    root = repo_root()
    findings: List[Finding] = []

    validate_repo_structure(root, findings)
    if any(f.level == "error" for f in findings):
        return _emit(findings, args.json_out)

    try:
        cats, registry = validate_registry_and_categories(root, findings)
    except Exception as e:
        findings.append(Finding("error", "L1.CATALOG_PARSE", f"Catalog parse error: {e}"))
        return _emit(findings, args.json_out)

    cats_by_key = {c["key"] for c in cats if isinstance(c, dict) and "key" in c}

    validator = _validator(root)

    for entry in registry:
        if not entry.module_code:
            findings.append(Finding("error", "L1.REGISTRY_MODULE_CODE_EMPTY", "Registry entry has empty module_code"))
            continue
        if not entry.path:
            findings.append(Finding("error", "L1.REGISTRY_PATH_EMPTY", f"Registry entry '{entry.module_code}' has empty path", module_code=entry.module_code))
            continue

        mroot = module_root_from_registry_entry(entry, root)
        if not mroot.exists():
            findings.append(Finding("error", "L1.MODULE_PATH_MISSING", f"Module path not found: {entry.path}", module_code=entry.module_code))
            continue

        validate_module_manifest(entry.module_code, mroot, cats_by_key, validator, findings)

    return _emit(findings, args.json_out)


if __name__ == "__main__":
    raise SystemExit(main())
