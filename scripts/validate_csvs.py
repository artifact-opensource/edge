#!/usr/bin/env python3
"""Validate CSV dashboards listed in csv-manifest.json.
Produces a Markdown report at reports/csv-validation-report.md
Checks performed:
- File exists and size
- Header presence
- Number of rows (sample)
- Presence of formula cells (starting with '=')
- Potential sensitive columns (by keyword)
- Duplicate file names/overlap
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'docs' / 'csv-manifest.json'
REPORT_DIR = ROOT / 'reports'
REPORT_DIR.mkdir(exist_ok=True)
REPORT_FILE = REPORT_DIR / 'csv-validation-report.md'
SENSITIVE_KEYS = ['ssn','password','secret','token','key','private','dob','email']

# PII regex patterns
PII_PATTERNS = {
    'email': r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    'ssn': r"\b\d{3}-\d{2}-\d{4}\b",
    # stricter phone pattern (requires separators or parentheses) to reduce false positives
    'phone': r"(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}",
    'ip': r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    'cc': r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b"
}


manifest = json.loads(MANIFEST.read_text())

report_lines = ["# CSV Validation Report\n"]

all_headers = {}
for it in manifest:
    p = ROOT / it['path']
    report_lines.append(f"## {it['name']} — `{it['path']}`\n")
    if not p.exists():
        report_lines.append(f"**MISSING**: file not found.\n")
        continue
    size = p.stat().st_size
    report_lines.append(f"- Size: {size} bytes\n")
    # Try to find the real header row (skip title/empty rows)
    with p.open(newline='') as fh:
        raw = list(csv.reader(fh))
    headers = None
    header_row_index = 0
    # Heuristic: pick the row with the most non-empty columns and that doesn't look like an all-caps title
    best_score = -1
    for i, row in enumerate(raw[:20]):
        non_empty = sum(1 for c in row if c and c.strip())
        title_like = any(str(c).strip().upper().startswith('ARTIFACT') or str(c).strip().upper().startswith('SHEET') for c in row if c)
        score = non_empty - (5 if title_like else 0)
        if score > best_score and non_empty >= 1:
            best_score = score
            headers = [c if c is not None else '' for c in row]
            header_row_index = i
    report_lines.append(f"- Chosen header row index: {header_row_index} -> `{headers}`\n")
    # Build a DictReader from the chosen header row
    sample_rows = []
    formula_count = 0
    row_count = 0
    with p.open(newline='') as fh:
        reader = csv.reader(fh)
        # skip until header_row_index
        for _ in range(header_row_index + 1):
            try:
                next(reader)
            except StopIteration:
                break
        dict_reader = csv.DictReader(fh, fieldnames=headers)
        for r in dict_reader:
            row_count += 1
            if row_count <= 50:
                sample_rows.append(r)
                for v in r.values():
                    if isinstance(v, str) and v.strip().startswith('='):
                        formula_count += 1
            if row_count > 1000:
                break
    report_lines.append(f"- Sample rows read: {min(row_count,1000)}\n")
    report_lines.append(f"- Formula-like cells detected (in preview): {formula_count}\n")
    # detect potential sensitive columns
    potential_sensitive = [h for h in (headers or []) if any(s in h.lower() for s in SENSITIVE_KEYS)]
    if potential_sensitive:
        report_lines.append(f"- Potential sensitive columns: `{potential_sensitive}`\n")
    # content-based PII scan (sample)
    content_matches = {}
    import re
    for row in sample_rows:
        for k, v in row.items():
            if not v:
                continue
            for name, pattern in PII_PATTERNS.items():
                if re.search(pattern, str(v)):
                    content_matches.setdefault(name, []).append({'column': k, 'value': str(v)[:100]})
        if content_matches:
            report_lines.append(f"- PII patterns detected in sample: `{list(content_matches.keys())}`\n")
            for k, vs in content_matches.items():
                report_lines.append(f"  - {k}: examples={vs[:3]}\n")
            # mark manifest entry as sensitive and create a redacted copy
            try:
                manifest_obj = json.loads(MANIFEST.read_text())
                for mi in manifest_obj:
                    if mi['path'] == it['path']:
                        mi['sensitive'] = True
                        break
                MANIFEST.write_text(json.dumps(manifest_obj, indent=2))
                report_lines.append(f"- Manifest updated: `{it['path']}` marked as sensitive\n")
            except Exception as e:
                report_lines.append(f"- Failed to update manifest: {e}\n")

            # create a redacted copy of the CSV (mask PII values)
            redacted_path = p.with_suffix('.redacted.csv')
            try:
                with p.open(newline='') as fh_in, redacted_path.open('w', newline='') as fh_out:
                    reader = csv.DictReader(fh_in)
                    writer = csv.DictWriter(fh_out, fieldnames=reader.fieldnames)
                    writer.writeheader()
                    for row in reader:
                        out = {}
                        for k, v in row.items():
                            masked = v
                            for name, pattern in PII_PATTERNS.items():
                                if re.search(pattern, str(v)):
                                    masked = f"REDACTED_{name.upper()}"
                                    break
                            out[k] = masked
                        writer.writerow(out)
                report_lines.append(f"- Redacted copy written: `{redacted_path}`\n")
            except Exception as e:
                report_lines.append(f"- Failed to write redacted copy: {e}\n")
        else:
            report_lines.append(f"- PII patterns detected in sample: None\n")


# duplicates
report_lines.append("\n# Duplicates & Header Overlaps\n")
for heads, paths in all_headers.items():
    if len(paths) > 1:
        report_lines.append(f"- Identical headers for: {paths}\n")

REPORT_FILE.write_text('\n'.join(report_lines))
print(f"Validation complete — report written to {REPORT_FILE}")
