from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

_repo_root = Path(__file__).resolve().parents[1]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))


def add_dir(z: ZipFile, root: Path, arc_prefix: str) -> None:
    if not root.exists():
        return
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        rel = p.relative_to(root)
        z.write(p, arcname=str(Path(arc_prefix) / rel))


def main() -> int:
    root = Path(".").resolve()
    dist = root / "dist"
    dist.mkdir(parents=True, exist_ok=True)

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_zip = dist / f"mds_artifacts_{ts}.zip"

    meta = {
        "generated_at_utc": ts,
        "includes": ["site/", ".build/exports/", ".build/docs/", "mkdocs_generated.yml"],
    }
    (root / ".build").mkdir(parents=True, exist_ok=True)
    (root / ".build" / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    with ZipFile(out_zip, "w", compression=ZIP_DEFLATED) as z:
        add_dir(z, root / "site", "site")
        add_dir(z, root / ".build" / "exports", ".build/exports")
        add_dir(z, root / ".build" / "docs", ".build/docs")

        gen = root / "mkdocs_generated.yml"
        if gen.exists():
            z.write(gen, arcname="mkdocs_generated.yml")

        z.write(root / ".build" / "meta.json", arcname=".build/meta.json")

    print(f"Artifacts packaged: {out_zip}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
