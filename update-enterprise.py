#!/usr/bin/env python3
"""
Enterprise Update Script — Python entry point.

This wrapper calls scripts/update_engine.py which is the main enterprise
update engine. Use update-enterprise.sh (Bash) or update-enterprise.ps1
(PowerShell) for the recommended entry points.

Usage:
    python update-enterprise.py [--apply] [--skip-db] [--skip-csv]
"""

import subprocess
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent
engine = repo_root / "scripts" / "update_engine.py"

if not engine.exists():
    print(f"Error: Update engine not found at {engine}")
    sys.exit(1)

sys.exit(subprocess.call([sys.executable, str(engine)] + sys.argv[1:]))
