from __future__ import annotations

import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


EXCLUDE_PREFIXES = (
    ".build/",
    "site/",
    "dist/",
    "__pycache__/",
    ".venv/",
)


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
        if any(path.startswith(p) for p in EXCLUDE_PREFIXES):
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["changed"], default="changed")
    _ = ap.parse_args()

    root = Path(".").resolve()
    dist = root / "dist"
    dist.mkdir(parents=True, exist_ok=True)

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    zip_path = dist / f"changed_{ts}.zip"

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
