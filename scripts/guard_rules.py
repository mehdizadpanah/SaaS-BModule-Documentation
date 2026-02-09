from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Optional

TARGET = "standards/MDS_v1.md"


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def _extract_version(text: str) -> Optional[str]:
    m = re.search(r"^Version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", text, flags=re.MULTILINE)
    return m.group(1) if m else None


def _has_changelog_entry(text: str, version: str) -> bool:
    m = re.search(r"^##\s+Changelog\s*$", text, flags=re.MULTILINE)
    if not m:
        return False
    start = m.end()
    nxt = re.search(r"^##\s+", text[start:], flags=re.MULTILINE)
    end = start + (nxt.start() if nxt else len(text[start:]))
    section = text[start:end]
    return re.search(rf"^\-\s*{re.escape(version)}(\b|:)", section, flags=re.MULTILINE) is not None


def _file_changed_in_git() -> bool:
    r = _run(["git", "status", "--porcelain", "--", TARGET])
    if r.returncode != 0:
        return False
    return bool((r.stdout or "").strip())


def _git_show_head() -> Optional[str]:
    r = _run(["git", "show", f"HEAD:{TARGET}"])
    if r.returncode != 0:
        return None  # not in HEAD (initial add or no commits)
    return r.stdout


def main() -> int:
    if not _file_changed_in_git():
        return 0  # unchanged

    path = Path(TARGET)
    if not path.exists():
        print(f"ERROR GUARD.MDS_MISSING: '{TARGET}' not found.")
        return 2

    new_text = path.read_text(encoding="utf-8")
    new_ver = _extract_version(new_text)
    if not new_ver:
        print(f"ERROR GUARD.MDS_VERSION_MISSING: '{TARGET}' must contain 'Version: x.y.z'")
        return 2

    old_text = _git_show_head()
    if old_text is None:
        return 0  # initial creation allowed

    old_ver = _extract_version(old_text)
    if old_ver and new_ver == old_ver:
        print(f"ERROR GUARD.MDS_VERSION_NOT_BUMPED: '{TARGET}' changed but Version not bumped (still {new_ver})")
        return 2

    if not _has_changelog_entry(new_text, new_ver):
        print(f"ERROR GUARD.MDS_CHANGELOG_MISSING: '{TARGET}' must include a Changelog entry for version {new_ver}")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
