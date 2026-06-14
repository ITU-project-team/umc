#!/usr/bin/env python3
"""Compatibility entrypoint for the UMC report-analysis lag checker."""

from __future__ import annotations

import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_CHECKER = PROJECT_ROOT / "scripts" / "hooks" / "report_analysis_lag_check.py"


def main() -> int:
    if not CANONICAL_CHECKER.exists():
        if "--hook" in sys.argv and "stop" in sys.argv:
            print('{"continue":true}')
            return 0
        print(f"Missing canonical checker: {CANONICAL_CHECKER}", file=sys.stderr)
        return 1

    os.execv(sys.executable, [sys.executable, str(CANONICAL_CHECKER), *sys.argv[1:]])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
