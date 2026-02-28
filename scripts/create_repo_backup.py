#!/usr/bin/env python3
"""Create a zip backup of the repository (excluding .git and backups folder)."""
import zipfile
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / 'backups'
OUTDIR.mkdir(exist_ok=True)
now = datetime.utcnow().strftime('%Y%m%d%H%M%S')
outfile = OUTDIR / f'artifactvirtual-backup-{now}.zip'
exclude_dirs = {'.git', 'backups', 'node_modules', '.artifact_shield'}

with zipfile.ZipFile(outfile, 'w', zipfile.ZIP_DEFLATED) as zf:
    for p in ROOT.rglob('*'):
        try:
            if not p.is_file():
                continue
            rel = p.relative_to(ROOT)
            if any(part in exclude_dirs for part in rel.parts):
                continue
            zf.write(p, rel)
        except Exception:
            continue
print(f'Backup written: {outfile}')
