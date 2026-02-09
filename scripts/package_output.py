from __future__ import annotations

import argparse
import subprocess
from datetime import datetime, timezone
from uuid import uuid4
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


EXCLUDE_PREFIXES = (
    ".build/",
    "site/",
    "dist/",
    ".git/",
    ".vscode/",
    ".venv/",
)

EXCLUDE_DIR_NAMES = {
    "__pycache__",
}

EXCLUDE_SUFFIXES = (
    ".pyc",
)


def should_exclude(rel_path: str) -> bool:
    if any(rel_path.startswith(prefix) for prefix in EXCLUDE_PREFIXES):
        return True
    if rel_path.endswith(EXCLUDE_SUFFIXES):
        return True
    if any(part in EXCLUDE_DIR_NAMES for part in rel_path.split("/")):
        return True
    return False


def git_changed_files() -> list[str]:
    r = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if r.returncode != 0:
        return []
    files: list[str] = []
    for line in r.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip()
        path = path.split(" -> ")[-1].strip()  # rename support
        if should_exclude(path):
            continue
        if Path(path).is_dir():
            continue
        files.append(path)

    seen = set()
    out: list[str] = []
    for f in files:
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out


def all_project_files(root: Path, zip_name: str) -> list[str]:
    files: list[str] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if rel == zip_name:
            continue
        if should_exclude(rel):
            continue
        files.append(rel)
    return files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["changed", "all"], default="changed")
    args = ap.parse_args()

    root = Path(".").resolve()
    _ = datetime.now(timezone.utc)
    zip_name = f"{uuid4().hex}.zip"
    zip_path = root / zip_name

    if args.mode == "all":
        files = all_project_files(root, zip_name)
        if not files:
            print("WARN: No files detected in project. ZIP will not be generated.")
            return 2
    else:
        files = git_changed_files()
        if not files:
            print("WARN: No changed files detected via git. ZIP will not be generated.")
            return 2

    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as z:
        for f in files:
            p = root / f
            if p.exists() and p.is_file():
                z.write(p, arcname=f)

    print(f"ZIP generated: {zip_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
