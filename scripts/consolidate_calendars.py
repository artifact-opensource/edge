#!/usr/bin/env python3
"""Consolidate duplicate calendar CSVs into a canonical calendar file.
- Uses `csv-manifest.json` to find calendar-like CSVs (headers containing 'Date').
- Merges rows, dedupes by Date + Primary_Activity, sorts by Date, writes canonical file.
- Backs up source files and updates manifest by marking aliases.
"""
import csv
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'docs' / 'csv-manifest.json'
BACKUP_DIR = ROOT / 'backups'
BACKUP_DIR.mkdir(exist_ok=True)

manifest = json.loads(MANIFEST.read_text())

# find calendar-like entries
cals = [m for m in manifest if Path(m['path']).name.lower().find('calendar')!=-1 or m['id'].lower().find('calendar')!=-1]
if not cals:
    print('No calendar-like CSVs found in manifest')
    raise SystemExit(0)

# prefer enterprise/divisions/departments/executive/ceo/CEO_CALENDAR.csv as canonical if present
canonical = None
for c in cals:
    if 'executive/ceo/CEO_CALENDAR.csv' in c['path']:
        canonical = c
        break
if not canonical:
    # pick first
    canonical = cals[0]

print(f"Canonical: {canonical['path']}")

rows_by_date = {}
headers = None

for c in cals:
    p = ROOT / c['path']
    if not p.exists():
        print(f"Warning: missing file {p}")
        continue
    # backup
    bk = BACKUP_DIR / (Path(c['path']).name + '.' + datetime.utcnow().strftime('%Y%m%d%H%M%S') + '.bak')
    bk.write_bytes(p.read_bytes())
    print(f"Backed up {p} -> {bk}")

    with p.open(newline='') as fh:
        reader = csv.DictReader(fh)
        if headers is None:
            headers = reader.fieldnames
        for r in reader:
            key = (r.get('Date') or r.get('date') or '') + '|' + (r.get('Primary_Activity') or r.get('Primary') or '')
            # use date parsing to normalize
            try:
                d = r.get('Date')
                if d:
                    dd = datetime.fromisoformat(d)
                    r['Date'] = dd.date().isoformat()
            except Exception:
                pass
            rows_by_date.setdefault(key, r)

# write merged canonical file
canon_path = ROOT / canonical['path']
merged_path = canon_path.with_suffix('.merged.csv')
with merged_path.open('w', newline='') as fh:
    writer = csv.DictWriter(fh, fieldnames=headers)
    writer.writeheader()
    for k, r in sorted(rows_by_date.items(), key=lambda x: x[1].get('Date') or ''):
        writer.writerow(r)

# move merged in place (backup original again)
orig_bk = BACKUP_DIR / (Path(canonical['path']).name + '.pre-merge.' + datetime.utcnow().strftime('%Y%m%d%H%M%S') + '.bak')
orig_bk.write_bytes(canon_path.read_bytes())
merged_path.replace(canon_path)
print(f"Merged calendars written to {canon_path}, original backed up to {orig_bk}")

# update manifest: mark other calendars as alias_of canonical
changed = False
for m in manifest:
    if m['id'] != canonical['id'] and (Path(m['path']).name.lower().find('calendar')!=-1 or m['id'].lower().find('calendar')!=-1):
        m['alias_of'] = canonical['id']
        changed = True

if changed:
    MANIFEST.write_text(json.dumps(manifest, indent=2))
    print('Updated csv-manifest.json to mark aliases')
else:
    print('No manifest update needed')
