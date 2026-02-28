#!/usr/bin/env python3
"""Generate csv-manifest.json by scanning repo for CSV files.
- Populates id, name, path, department, size, headers (preview), and sensitive:false by default.
"""
import json
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'csv-manifest.json'

entries = []
for p in sorted(ROOT.rglob('*.csv')):
    rel = p.relative_to(ROOT).as_posix()
    # ignore backups
    if '/backups/' in rel:
        continue
    # determine department from path
    parts = rel.split('/')
    dept = parts[1] if len(parts) > 1 else 'root'
    # peek headers
    with p.open(newline='') as fh:
        try:
            reader = csv.reader(fh)
            headers = next(reader)
        except StopIteration:
            headers = []
    entries.append({
        'id': Path(rel).stem.lower().replace('.', '_').replace(' ', '_'),
        'name': Path(rel).stem,
        'path': rel,
        'department': dept,
        'size': p.stat().st_size,
        'headers_preview': headers[:10],
        'sensitive': False
    })

OUT.write_text(json.dumps(entries, indent=2))
print(f"Wrote {OUT} with {len(entries)} entries")
