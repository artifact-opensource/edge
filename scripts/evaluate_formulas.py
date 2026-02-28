#!/usr/bin/env python3
"""Evaluate simple spreadsheet-style formulas embedded in CSV files.
- Supports basic arithmetic with cell refs (e.g., =I6-J6), SUM(A1:A3)
- For each CSV in csv-manifest.json run an evaluation pass and write an evaluated copy
  as <original>.evaluated.csv, backing up originals.
"""
import csv, re, math
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'docs' / 'csv-manifest.json'
BACKUP_DIR = ROOT / 'backups'
BACKUP_DIR.mkdir(exist_ok=True)

manifest = json.loads(MANIFEST.read_text())
col_letter_re = re.compile(r'([A-Za-z]+)(\d+)')

# helpers

def col_letter_to_index(letters):
    letters = letters.upper()
    idx = 0
    for ch in letters:
        idx = idx * 26 + (ord(ch) - ord('A') + 1)
    return idx - 1


def parse_cell_ref(ref):
    m = col_letter_re.match(ref)
    if not m:
        raise ValueError('invalid ref')
    col = col_letter_to_index(m.group(1))
    row = int(m.group(2)) - 1
    return row, col


def evaluate_expr(expr, sheet):
    # simple: replace SUM ranges, replace cell refs with numeric values
    expr = expr.strip().lstrip('=')
    # support SUM(A1:A3)
    sum_matches = re.findall(r'SUM\(([A-Za-z0-9:]+)\)', expr, flags=re.I)
    for sm in sum_matches:
        if ':' in sm:
            a, b = sm.split(':')
            r1, c1 = parse_cell_ref(a)
            r2, c2 = parse_cell_ref(b)
            s = 0
            for rr in range(min(r1, r2), max(r1, r2) + 1):
                for cc in range(min(c1, c2), max(c1, c2) + 1):
                    try:
                        v = float(sheet[rr][cc])
                        s += v
                    except Exception:
                        pass
            expr = expr.replace(f'SUM({sm})', str(s))
    # replace cell refs
    refs = re.findall(r'([A-Za-z]+\d+)', expr)
    for ref in refs:
        try:
            rr, cc = parse_cell_ref(ref)
            v = sheet[rr][cc]
            if v is None or v == '':
                val = '0'
            else:
                val = str(v)
            expr = expr.replace(ref, val)
        except Exception:
            expr = expr.replace(ref, '0')
    # safe eval for basic arithmetic
    try:
        # block anything but numbers and operators
        if re.match(r'^[0-9.+\-*/ ()eE]+$', expr):
            return str(eval(expr, {'__builtins__': None, 'math': math}))
        else:
            return None
    except Exception:
        return None


for m in manifest:
    p = ROOT / m['path']
    if not p.exists():
        continue
    # read raw rows
    with p.open(newline='') as fh:
        reader = csv.reader(fh)
        sheet = [r for r in reader]
    changed = False
    for r_idx, row in enumerate(sheet):
        for c_idx, cell in enumerate(row):
            if isinstance(cell, str) and cell.strip().startswith('='):
                val = evaluate_expr(cell.strip(), sheet)
                if val is not None:
                    row[c_idx] = val
                    changed = True
    if changed:
        out = p.with_suffix('.evaluated.csv')
        # backup
        bk = BACKUP_DIR / (p.name + '.' + 'pre-eval.bak')
        bk.write_bytes(p.read_bytes())
        with out.open('w', newline='') as fh:
            writer = csv.writer(fh)
            writer.writerows(sheet)
        print(f"Wrote evaluated CSV: {out}")
    else:
        print(f"No formulas evaluated for {p}")
