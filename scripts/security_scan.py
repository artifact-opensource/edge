#!/usr/bin/env python3
"""Simple local security scanner for common secret patterns.
Produces JSON and Markdown reports under reports/security-scan-<timestamp>.*
"""
import re
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'reports'
REPORTS.mkdir(exist_ok=True)

PATTERNS = {
    'private_key': re.compile(r'-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----'),
    'aws_access_key': re.compile(r'AKIA[0-9A-Z]{16}'),
    'aws_secret_key': re.compile(r'(?i)aws(.{0,20})?(secret|secret_access_key).{0,50}=[ \t\"\']?([A-Za-z0-9/+=]{40})'),
    'slack_token': re.compile(r'xox[baprs]-[0-9A-Za-z-]+'),
    'jwt_token': re.compile(r'eyJ[0-9A-Za-z-_]+\.[0-9A-Za-z-_]+\.[0-9A-Za-z-_]+'),
    'github_token': re.compile(r'gh[pousr]_[0-9A-Za-z_]{36}'),
    'azure_key': re.compile(r'(?i)azure(.{0,20})?key.{0,50}=[ \t\"\']?([A-Za-z0-9-_]{32,64})')
}

EXCLUDE_DIRS = ['.git', 'backups', 'node_modules', '.artifact_shield']

results = []
for p in ROOT.rglob('*'):
    if not p.is_file():
        continue
    rel = p.relative_to(ROOT)
    if any(part in EXCLUDE_DIRS for part in rel.parts):
        continue
    try:
        text = p.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    for name, pat in PATTERNS.items():
        for m in pat.finditer(text):
            snippet = text[m.start(): m.end()+80].splitlines()[0][:200]
            results.append({'path': str(rel), 'pattern': name, 'match': m.group(0)[:200], 'snippet': snippet})

now = datetime.utcnow().strftime('%Y%m%d%H%M%S')
json_out = REPORTS / f'security-scan-{now}.json'
md_out = REPORTS / f'security-scan-{now}.md'
json_out.write_text(json.dumps(results, indent=2))

md_lines = [f"# Security Scan Report — {now}", f"Found {len(results)} possible findings", '']
for r in results:
    md_lines.append(f"- **{r['pattern']}** in `{r['path']}` -> `{r['match']}`")
md_out.write_text('\n'.join(md_lines))
print(f"Security scan complete — {len(results)} findings (report: {md_out})")
