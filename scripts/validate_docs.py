from __future__ import annotations

import subprocess
import sys


def main() -> int:
    g = subprocess.run([sys.executable, "scripts/guard_rules.py"])
    if g.returncode != 0:
        return g.returncode

    d = subprocess.run([sys.executable, "scripts/doctor.py"])
    return d.returncode


if __name__ == "__main__":
    raise SystemExit(main())
