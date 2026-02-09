from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass(frozen=True)
class RegistryModule:
    module_code: str
    path: str
    status: Optional[str] = None
    owner: Optional[str] = None


def repo_root() -> Path:
    # scripts/lib/catalog_loader.py -> scripts/lib -> scripts -> repo root
    return Path(__file__).resolve().parents[2]


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(str(path))
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def load_categories(root: Optional[Path] = None) -> List[Dict[str, Any]]:
    root = root or repo_root()
    data = load_yaml(root / "catalogs" / "categories.yaml")
    cats = data.get("categories", [])
    if not isinstance(cats, list):
        raise ValueError("categories must be a list in catalogs/categories.yaml")
    return cats


def load_registry(root: Optional[Path] = None) -> List[RegistryModule]:
    root = root or repo_root()
    data = load_yaml(root / "catalogs" / "modules_registry.yaml")
    mods = data.get("modules", [])
    if not isinstance(mods, list):
        raise ValueError("modules must be a list in catalogs/modules_registry.yaml")
    out: List[RegistryModule] = []
    for i, m in enumerate(mods):
        if not isinstance(m, dict):
            raise ValueError(f"registry.modules[{i}] must be a mapping")
        out.append(
            RegistryModule(
                module_code=str(m.get("module_code", "")).strip(),
                path=str(m.get("path", "")).strip(),
                status=(str(m["status"]).strip() if "status" in m else None),
                owner=(str(m["owner"]).strip() if "owner" in m else None),
            )
        )
    return out


def module_root_from_registry_entry(entry: RegistryModule, root: Optional[Path] = None) -> Path:
    root = root or repo_root()
    return (root / entry.path).resolve()
