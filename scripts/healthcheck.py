#!/usr/bin/env python3
"""
Enterprise Repository Health Check — Read-only verification.
Checks all known integrity requirements. Does NOT modify any files.
Usage: python3 scripts/healthcheck.py
"""

import json, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PASS, FAIL, WARN = 0, 0, 0

# Split the string so this script never self-matches on grep searches
_OLD_PATH = "/home/adam/" + "av-erp"
_SCAN_EXTS = {".md", ".json", ".py", ".sh", ".txt", ".html", ".ps1", ".yml", ".yaml", ".js"}


def ok(msg):
    global PASS
    PASS += 1
    print(f"  \033[32m✓\033[0m {msg}")

def fail(msg):
    global FAIL
    FAIL += 1
    print(f"  \033[31m✗\033[0m {msg}")

def warn(msg):
    global WARN
    WARN += 1
    print(f"  \033[33m!\033[0m {msg}")

def section(title):
    print(f"\n\033[1m── {title}\033[0m")

def load_json(path):
    with open(REPO / path) as f:
        return json.load(f)

def read(path):
    return (REPO / path).read_text(encoding="utf-8", errors="ignore")

def exists(path):
    return (REPO / path).exists()


# ═══════════════════════════════════════════════════════════════════════
print("\033[1m" + "=" * 60)
print("  ENTERPRISE HEALTH CHECK")
print("=" * 60 + "\033[0m")

# ── 1. ENCRYPTION ─────────────────────────────────────────────────────
section("1. Encryption Status")
enc = [f for f in REPO.rglob("*.enc") if ".git" not in f.parts]
if len(enc) == 0:
    ok("No .enc files — all decrypted")
else:
    fail(f"{len(enc)} .enc files remain")

# ── 2. STALE PATHS ───────────────────────────────────────────────────
section("2. Path References")
stale_count = 0
stale_files = []
for f in REPO.rglob("*"):
    if f.is_file() and f.suffix in _SCAN_EXTS and ".git" not in f.parts:
        if "healthcheck" in f.name:
            continue
        try:
            txt = f.read_text(encoding="utf-8", errors="ignore")
            n = txt.count(_OLD_PATH)
            if n > 0:
                stale_count += n
                stale_files.append((f.relative_to(REPO), n))
        except Exception:
            pass

if stale_count == 0:
    ok("No stale av-erp paths")
else:
    fail(f"{stale_count} stale av-erp paths in {len(stale_files)} files")
    for fp, n in stale_files[:5]:
        print(f"      {fp} ({n})")

# ── 3. ARTIFACT-PROJECT.JSON ─────────────────────────────────────────
section("3. Master Manifest")
try:
    manifest = load_json("enterprise/artifact-project.json")
    ver = manifest.get("version")
    repo_name = manifest.get("repository")
    projs = manifest.get("activeProjects", {})
    if ver and repo_name:
        ok(f"Version={ver}, repo={repo_name}")
    else:
        fail(f"Version={ver}, repository={repo_name} (nulls!)")
    if len(projs) >= 18:
        ok(f"{len(projs)} active projects")
    else:
        warn(f"Only {len(projs)} active projects (expected ≥18)")
except Exception as e:
    fail(f"Cannot read artifact-project.json: {e}")

# ── 4. ENTERPRISE.MD RENAME ──────────────────────────────────────────
section("4. File Naming")
if exists("enterprise/ENTERPRISE.md"):
    ok("ENTERPRISE.md exists (typo fixed)")
elif exists("enterprise/ENTERPISE.md"):
    fail("ENTERPISE.md still has typo")
else:
    warn("Neither ENTERPRISE.md nor ENTERPISE.md found")

# ── 5. DATABASE COLLECTIONS ──────────────────────────────────────────
section("5. Database Integrity")
db_checks = [
    ("database/data/projects_db.json", [("projects", 10), ("project_tasks", 1), ("project_documentation", 1)]),
    ("database/data/public_db.json", [("stakeholders", 5), ("community", 3), ("public_documents", 50)]),
    ("database/data/internal_db.json", [("management", 3), ("operations", 3), ("internal_documents", 50)]),
]
for db_path, cols in db_checks:
    try:
        db = load_json(db_path)
        for col, minimum in cols:
            actual = len(db.get(col, []))
            name = f"{Path(db_path).stem}.{col}"
            if actual >= minimum:
                ok(f"{name}: {actual} records")
            else:
                fail(f"{name}: {actual} records (need ≥{minimum})")
    except Exception as e:
        fail(f"Cannot read {db_path}: {e}")

# ── 6. LEGAL DOCS ────────────────────────────────────────────────────
section("6. Legal / Certificate")
cert = REPO / "enterprise/divisions/departments/executive/moa-aoa/certificate-of-incorporation.md"
if cert.exists() and cert.stat().st_size > 50:
    ok("certificate-of-incorporation.md present")
else:
    fail("certificate-of-incorporation missing or placeholder")

# ── 7. COPILOT DOCS ──────────────────────────────────────────────────
section("7. Copilot Documentation")
try:
    tools_txt = read("copilot/TOOLS.md")
    if "This Repository" in tools_txt or "Actual Stack" in tools_txt:
        ok("TOOLS.md has actual stack reference")
    else:
        fail("TOOLS.md missing actual stack section")
except Exception:
    fail("Cannot read copilot/TOOLS.md")

try:
    skills_txt = read("copilot/SKILLS.md")
    if "illustration" in skills_txt.lower() or "disclaimer" in skills_txt.lower():
        ok("SKILLS.md has disclaimer")
    else:
        fail("SKILLS.md missing disclaimer")
except Exception:
    fail("Cannot read copilot/SKILLS.md")

try:
    ctx_txt = read("copilot/context.json")
    # Only count raw av-erp that aren't in changelog or "external:" notes
    ctx_raw = ctx_txt.count(_OLD_PATH)
    if ctx_raw == 0:
        ok("context.json: no stale av-erp paths")
    else:
        warn(f"context.json: {ctx_raw} av-erp refs (check if external notes)")
except Exception:
    fail("Cannot read copilot/context.json")

# ── 8. STAKEHOLDER PORTAL ────────────────────────────────────────────
section("8. Stakeholder Portal HTML")
portal = REPO / "docs/stakeholder-portal.html"
if portal.exists():
    sz = portal.stat().st_size
    if sz > 10000:
        ok(f"stakeholder-portal.html: {sz:,} bytes")
    else:
        warn(f"stakeholder-portal.html: only {sz} bytes")
else:
    fail("docs/stakeholder-portal.html missing")

# ── 9. NOTION SCRIPTS ────────────────────────────────────────────────
section("9. Notion Scripts")
try:
    bnp = read("notion/scripts/build_notion_portal.py")
    if "from pathlib import Path" in bnp:
        ok("build_notion_portal.py: Path import present")
    else:
        fail("build_notion_portal.py: missing Path import")
except Exception:
    fail("Cannot read build_notion_portal.py")

try:
    ns = read("notion/scripts/notion_sync.py")
    if "notion_sync" in ns or "build_notion_portal" in ns:
        ok("notion_sync.py: pipeline script present")
    else:
        warn("notion_sync.py: unexpected content")
except Exception:
    fail("Cannot read notion_sync.py")

# ── 10. CSV MANIFEST ─────────────────────────────────────────────────
section("10. Supporting Files")
if exists("docs/csv-manifest.json"):
    ok("docs/csv-manifest.json exists")
else:
    fail("docs/csv-manifest.json missing (scripts will crash)")

scan_json = REPO / "reports/security-scan-20260206103939.json"
if not scan_json.exists():
    ok("Empty security scan JSON cleaned up")
elif scan_json.stat().st_size <= 5:
    warn("Empty security scan JSON still exists (3 bytes)")
else:
    ok("Security scan JSON has data")

# ── 11. SYNC PIPELINE ────────────────────────────────────────────────
section("11. Sync Pipeline")
try:
    sfr = read("database/utils/sync_from_repo.py")
    if "projects_dir" in sfr or "enterprise/projects" in sfr.lower():
        ok("sync_from_repo.py: project discovery logic present")
    else:
        fail("sync_from_repo.py: no project scanning logic")
except Exception:
    fail("Cannot read sync_from_repo.py")

# ═══════════════════════════════════════════════════════════════════════
total = PASS + FAIL + WARN
print("\n" + "\033[1m" + "=" * 60)
if FAIL == 0 and WARN == 0:
    print(f"  ✅ ALL CLEAR — {PASS}/{total} checks passed (100/100)")
elif FAIL == 0:
    print(f"  ⚠️  {PASS} passed, {WARN} warnings — ({PASS}/{total})")
else:
    score = round((PASS / total) * 100) if total > 0 else 0
    print(f"  ❌ {FAIL} FAILURES, {WARN} warnings, {PASS} passed ({score}/100)")
print("=" * 60 + "\033[0m\n")

sys.exit(0 if FAIL == 0 else 1)
