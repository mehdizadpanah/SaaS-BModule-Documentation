#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd)
    if r.returncode != 0:
        raise SystemExit(r.returncode)


def main() -> int:
    # Fail-fast QC-lite gates
    run([sys.executable, "scripts/guard_rules.py"])
    run([sys.executable, "scripts/doctor.py"])
    print("PASS: validate_docs checks succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
