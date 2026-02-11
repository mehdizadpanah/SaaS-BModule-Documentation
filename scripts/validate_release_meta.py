#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    raise SystemExit(2)


def read_text(p: Path) -> str:
    if not p.exists():
        fail(f"Missing file: {p}")
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return p.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    root = Path(__file__).resolve().parents[1]

    # SSoT in modules-docs: standards/MDS_v1.md header lines
    p_ssot = root / "standards" / "MDS_v1.md"
    p_readme = root / "README.md"
    p_changelog = root / "CHANGELOG.md"

    ssot = read_text(p_ssot)
    readme = read_text(p_readme)
    changelog = read_text(p_changelog)

    m_ver = re.search(r"Introduced in:\s*([0-9]+\.[0-9]+\.[0-9]+)", ssot)
    m_date = re.search(r"Last updated in:\s*([0-9]+\.[0-9]+\.[0-9]+)", ssot)
    if not m_ver or not m_date:
        fail("standards/MDS_v1.md: cannot parse Introduced in / Last updated in as x.y.z (SemVer).")

    # For modules-docs we treat Introduced in as current release version
    ssot_version = m_ver.group(1)

    # README expects explicit version + date
    m_r_ver = re.search(r"^\s*-\s*Current version:\s*`([0-9]+\.[0-9]+\.[0-9]+)`\s*$", readme, re.M)
    m_r_date = re.search(r"^\s*-\s*Release date:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})\s*$", readme, re.M)
    if not m_r_ver or not m_r_date:
        fail("README.md: cannot parse Current version / Release date (expected English lines).")

    readme_version = m_r_ver.group(1)
    readme_date = m_r_date.group(1)

    if readme_version != ssot_version:
        fail(f"README version mismatch: README={readme_version} vs SSoT(MDS Introduced in)={ssot_version}")

    # CHANGELOG must have: ## [x.y.z] - YYYY-MM-DD
    header_re = rf"^##\s*\[{re.escape(ssot_version)}\]\s*-\s*([0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}})\s*$"
    hm = re.search(header_re, changelog, re.M)
    if not hm:
        fail(f"CHANGELOG missing release entry: expected '## [{ssot_version}] - YYYY-MM-DD'")

    ch_date = hm.group(1)
    if ch_date != readme_date:
        fail(f"CHANGELOG date mismatch: CHANGELOG={ch_date} vs README={readme_date}")

    # Enforce Keep-a-Changelog structure for this release section
    section_re = re.compile(
        rf"^##\s*\[{re.escape(ssot_version)}\]\s*-\s*{re.escape(readme_date)}\s*$"
        r"([\s\S]*?)(?=^##\s*\[\d+\.\d+\.\d+\]\s*-\s*\d{4}-\d{2}-\d{2}\s*$|\Z)",
        re.M,
    )
    sm = section_re.search(changelog)
    if not sm:
        fail(f"CHANGELOG cannot extract section for [{ssot_version}] - {readme_date}")

    section = sm.group(1)
    has_heading = any(h in section for h in ["### Added", "### Changed", "### Fixed"])
    if not has_heading:
        fail(f"CHANGELOG structure invalid for [{ssot_version}]: missing '### Added/Changed/Fixed' headings")

    if not re.search(r"^\s*-\s+\S+", section, re.M):
        fail(f"CHANGELOG structure invalid for [{ssot_version}]: no bullet items found under headings")

    print("PASS: Release meta is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
