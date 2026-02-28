#!/usr/bin/env python3
"""
Enterprise Update Engine
========================
Central automation script for Artifact Virtual enterprise repository.

Responsibilities:
  1. Sync databases (existing database/update_databases.py)
  2. Regenerate CSV manifest
  3. Scan for drift (moved files, broken internal refs)
  4. Auto-update root README filesystem tree
  5. Refresh CEO/obsidian summary data
  6. Append to monolithic semver changelog
  7. Produce structured terminal report

Design:
  - Dry-run by default: shows planned changes, asks for confirmation
  - All helper scripts stay in /scripts/
  - Changelog lives in /changelog/CHANGELOG.md (append-only)

Usage:
    python scripts/update_engine.py [--apply] [--dry-run] [--skip-db] [--skip-csv]
"""

import argparse
import csv
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import textwrap
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

# ── Constants ────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent
CHANGELOG_DIR = REPO_ROOT / "changelog"
CHANGELOG_FILE = CHANGELOG_DIR / "CHANGELOG.md"
README_FILE = REPO_ROOT / "README.md"
DOCS_DIR = REPO_ROOT / "docs"
CSV_MANIFEST = DOCS_DIR / "csv-manifest.json"
DASHBOARD_HTML = DOCS_DIR / "enterprise-dashboard.html"
OBSIDIAN_DIR = REPO_ROOT / "obsidian"
ADMIN_DIR = REPO_ROOT / "admin"
ENTERPRISE_DIR = REPO_ROOT / "enterprise"
DATABASE_DIR = REPO_ROOT / "database"
SCRIPTS_DIR = REPO_ROOT / "scripts"

# Directories/files to exclude from tree generation
TREE_EXCLUDE = {
    ".git", ".github", "__pycache__", "node_modules", ".bin",
    "copilot-conversations", "copilot-custom-prompts", ".enc",
}

VERSION_FILE = REPO_ROOT / ".enterprise-version"

# ── Utilities ────────────────────────────────────────────────────────────────

_BOLD = "\033[1m"
_GREEN = "\033[92m"
_YELLOW = "\033[93m"
_RED = "\033[91m"
_CYAN = "\033[96m"
_DIM = "\033[2m"
_RESET = "\033[0m"
_BLUE = "\033[94m"


def _ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _header(title: str):
    w = 72
    print()
    print(f"{_CYAN}{'═' * w}{_RESET}")
    print(f"{_CYAN}  {title}{_RESET}")
    print(f"{_CYAN}{'═' * w}{_RESET}")


def _section(title: str):
    print(f"\n{_BOLD}{_BLUE}── {title}{_RESET}")


def _ok(msg: str):
    print(f"  {_GREEN}✓{_RESET} {msg}")


def _warn(msg: str):
    print(f"  {_YELLOW}⚠{_RESET} {msg}")


def _fail(msg: str):
    print(f"  {_RED}✗{_RESET} {msg}")


def _info(msg: str):
    print(f"  {_DIM}ℹ{_RESET} {msg}")


def _file_hash(path: Path) -> str:
    """SHA-256 of file contents."""
    h = hashlib.sha256()
    try:
        h.update(path.read_bytes())
    except OSError:
        return ""
    return h.hexdigest()[:12]


# ── 1. Database Sync ────────────────────────────────────────────────────────

def run_database_sync(dry_run: bool) -> dict:
    """Run the existing database update pipeline."""
    _section("Database Sync")
    result = {"changed": False, "details": []}

    if dry_run:
        _info("Would run database/update_databases.py (sync + index + validate)")
        result["details"].append("database sync (dry-run)")
        return result

    script = DATABASE_DIR / "update_databases.py"
    if not script.exists():
        _fail(f"Database update script not found: {script}")
        result["details"].append("MISSING database/update_databases.py")
        return result

    # Snapshot DB hashes before
    db_dir = DATABASE_DIR / "data"
    before = {}
    if db_dir.exists():
        for p in list(db_dir.glob("*.json")) + list(db_dir.glob("*.db")):
            before[p.name] = _file_hash(p)

    try:
        proc = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True, text=True, timeout=120,
            cwd=str(REPO_ROOT),
        )
        if proc.returncode != 0:
            _fail("Database sync failed")
            for line in proc.stderr.strip().splitlines()[-5:]:
                _fail(f"  {line}")
            result["details"].append("database sync FAILED")
            return result
    except subprocess.TimeoutExpired:
        _fail("Database sync timed out (120s)")
        result["details"].append("database sync TIMEOUT")
        return result

    # Snapshot after
    after = {}
    if db_dir.exists():
        for p in list(db_dir.glob("*.json")) + list(db_dir.glob("*.db")):
            after[p.name] = _file_hash(p)
    changed_dbs = [k for k in after if before.get(k) != after[k]]

    if changed_dbs:
        result["changed"] = True
        for db in changed_dbs:
            _ok(f"Updated {db}")
            result["details"].append(f"updated {db}")
    else:
        _ok("All databases up to date (no changes)")
        result["details"].append("databases unchanged")

    return result


# ── 2. CSV Manifest Regeneration ────────────────────────────────────────────

def regenerate_csv_manifest(dry_run: bool) -> dict:
    """Scan repo for CSV files and regenerate csv-manifest.json."""
    _section("CSV Manifest")
    result = {"changed": False, "details": [], "csvs": []}

    entries = []
    for p in sorted(REPO_ROOT.rglob("*.csv")):
        rel = p.relative_to(REPO_ROOT).as_posix()
        if any(ex in rel for ex in ("/backups/", "node_modules/", ".git/")):
            continue
        # Determine department
        parts = rel.split("/")
        if "departments" in parts:
            idx = parts.index("departments")
            dept = parts[idx + 1] if idx + 1 < len(parts) else "unknown"
        elif "divisions" in parts:
            idx = parts.index("divisions")
            dept = parts[idx + 1] if idx + 1 < len(parts) else "divisions"
        elif "obsidian" in parts:
            dept = "ceo"
        else:
            dept = "root"

        # Read headers
        headers = []
        try:
            with p.open(newline="", errors="replace") as fh:
                reader = csv.reader(fh)
                headers = next(reader, [])
        except Exception:
            pass

        base_id = p.stem.lower().replace(".", "_").replace(" ", "_").replace("-", "_")
        entry_id = f"{dept}_{base_id}" if dept != "root" else base_id

        entries.append({
            "id": entry_id,
            "name": p.stem,
            "path": rel,
            "department": dept,
            "size": p.stat().st_size,
            "headers_preview": headers[:10],
            "sensitive": False,
        })

    result["csvs"] = entries

    if dry_run:
        _info(f"Would write csv-manifest.json with {len(entries)} CSV entries")
        result["details"].append(f"{len(entries)} CSVs found (dry-run)")
        return result

    new_json = json.dumps(entries, indent=2) + "\n"
    old_json = CSV_MANIFEST.read_text() if CSV_MANIFEST.exists() else ""

    if new_json != old_json:
        CSV_MANIFEST.write_text(new_json)
        result["changed"] = True
        _ok(f"Updated docs/csv-manifest.json ({len(entries)} CSVs)")
        result["details"].append(f"csv-manifest.json updated ({len(entries)} entries)")
    else:
        _ok(f"docs/csv-manifest.json unchanged ({len(entries)} CSVs)")
        result["details"].append(f"csv-manifest.json unchanged ({len(entries)} entries)")

    return result


# ── 3. Drift Detection ─────────────────────────────────────────────────────

def detect_drift(dry_run: bool) -> dict:
    """Scan for broken internal markdown links and stale paths."""
    _section("Drift Detection")
    result = {"changed": False, "details": [], "broken_refs": [], "drift_notes": []}

    # Scan markdown files for relative links
    md_files = list(REPO_ROOT.rglob("*.md"))
    md_files = [f for f in md_files if ".git" not in f.parts]
    link_re = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')

    broken = []
    for md_file in md_files:
        try:
            content = md_file.read_text(errors="replace")
        except OSError:
            continue
        for match in link_re.finditer(content):
            label, target = match.group(1), match.group(2)
            # Skip external links, anchors, mailto
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            # Resolve relative to file's directory
            ref_path = (md_file.parent / target.split("#")[0]).resolve()
            if not ref_path.exists():
                rel_md = md_file.relative_to(REPO_ROOT).as_posix()
                broken.append(f"{rel_md} → {target}")

    result["broken_refs"] = broken

    if broken:
        _warn(f"Found {len(broken)} broken internal link(s)")
        for b in broken[:10]:
            _warn(f"  {b}")
        if len(broken) > 10:
            _warn(f"  ... and {len(broken) - 10} more")
        result["details"].append(f"{len(broken)} broken links detected")
    else:
        _ok("No broken internal links detected")
        result["details"].append("no drift detected")

    return result


# ── 4. Auto-update Root README ──────────────────────────────────────────────

def _build_tree(base: Path, prefix: str = "", max_depth: int = 3, depth: int = 0) -> list:
    """Build filesystem tree lines for a directory."""
    if depth >= max_depth:
        return []
    lines = []
    try:
        items = sorted(base.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
    except PermissionError:
        return []

    # Filter
    items = [i for i in items if i.name not in TREE_EXCLUDE and not i.name.startswith(".")]

    for idx, item in enumerate(items):
        is_last = idx == len(items) - 1
        connector = "└── " if is_last else "├── "
        rel = item.relative_to(REPO_ROOT).as_posix()

        if item.is_dir():
            lines.append(f"{prefix}{connector}{item.name}/")
            extension = "    " if is_last else "│   "
            lines.extend(_build_tree(item, prefix + extension, max_depth, depth + 1))
        else:
            size = item.stat().st_size
            if size > 1048576:
                sz = f"{size / 1048576:.1f}MB"
            elif size > 1024:
                sz = f"{size / 1024:.0f}KB"
            else:
                sz = f"{size}B"
            lines.append(f"{prefix}{connector}{item.name} ({sz})")

    return lines


def generate_readme(dry_run: bool, drift_notes: list = None, csv_count: int = 0) -> dict:
    """Generate the root README focused on filesystem structure."""
    _section("Root README")
    result = {"changed": False, "details": []}

    tree_lines = _build_tree(REPO_ROOT, max_depth=2)

    # Build department CSV summary
    csv_section = ""
    if CSV_MANIFEST.exists():
        try:
            entries = json.loads(CSV_MANIFEST.read_text())
            csv_lines = []
            for e in entries:
                csv_lines.append(f"| `{e['path']}` | {e['department']} | {e['size']:,}B |")
            csv_section = (
                "| Path | Department | Size |\n"
                "|------|-----------|------|\n"
                + "\n".join(csv_lines)
            )
        except Exception:
            csv_section = "_CSV manifest not available._"

    # Drift section
    drift_section = ""
    if drift_notes:
        drift_section = "\n".join(f"- {d}" for d in drift_notes[:20])
    else:
        drift_section = "_No drift detected._"

    # Count files
    total_md = len(list(REPO_ROOT.rglob("*.md")))
    total_csv = len(list(REPO_ROOT.rglob("*.csv")))
    total_json = len(list(p for p in REPO_ROOT.rglob("*.json") if ".git" not in p.parts))
    total_py = len(list(REPO_ROOT.rglob("*.py")))

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    readme_content = f"""# ARTIFACT VIRTUAL ENTERPRISE REPOSITORY

**Artifact Virtual (SMC-Private) Limited** — SECP Registration: 0325693

> This is the authoritative enterprise repository. For a comprehensive business overview, see [`ARTIFACT-VIRTUAL.md`](ARTIFACT-VIRTUAL.md).

**Classification:** Confidential — Private Repository
**Last Auto-Update:** {now}

---

## Repository Structure

```
enterprise/
{chr(10).join(tree_lines)}
```

---

## Quick Navigation

| Area | Entry Point | Description |
|------|------------|-------------|
| **Business Overview** | [`ARTIFACT-VIRTUAL.md`](ARTIFACT-VIRTUAL.md) | Full company brief, org structure, strategy |
| **CEO Dashboard** | [`docs/enterprise-dashboard.html`](docs/enterprise-dashboard.html) | Eagle-eye enterprise dashboard |
| **Board Roadmap** | [`admin/BOD_ROADMAP.md`](admin/BOD_ROADMAP.md) | 8-phase strategic roadmap (BOD) |
| **CEO Execution** | [`admin/CEO_EXECUTION_PLAN.md`](admin/CEO_EXECUTION_PLAN.md) | Tactical execution plan |
| **Enterprise Map** | [`enterprise/00_ERP_MAP.md`](enterprise/00_ERP_MAP.md) | Enterprise overview dashboard |
| **Stakeholders** | [`enterprise/stakeholders/README.md`](enterprise/stakeholders/README.md) | Investor & partner portal |
| **Projects** | [`enterprise/projects/PROJECT-INDEX.md`](enterprise/projects/PROJECT-INDEX.md) | 18-project portfolio |
| **Databases** | [`database/README.md`](database/README.md) | 4 JSON databases + RAG index |
| **CEO Workspace** | [`obsidian/README.md`](obsidian/README.md) | CEO operating system |
| **CSV Visualizer** | [`docs/csv-visualizer.html`](docs/csv-visualizer.html) | Interactive CSV dashboard viewer |
| **Update Script** | [`update-enterprise.sh`](update-enterprise.sh) | Single-command enterprise refresh |
| **Changelog** | [`changelog/CHANGELOG.md`](changelog/CHANGELOG.md) | Monolithic enterprise changelog |

---

## Enterprise Update

Run the update script to refresh all enterprise data:

```bash
# Preview changes (dry-run, default)
./update-enterprise.sh

# Apply changes
./update-enterprise.sh --apply

# Skip database sync (faster)
./update-enterprise.sh --apply --skip-db
```

The update script:
- Syncs all 4 JSON databases from repo files
- Regenerates CSV manifest across all departments
- Detects drift (broken links, stale references)
- Auto-updates this README
- Refreshes CEO workspace summary
- Appends changes to changelog (semver, append-only)

---

## CSV Dashboards

{csv_section}

---

## Drift Report

{drift_section}

---

## Repository Statistics

| Metric | Count |
|--------|-------|
| Markdown files | {total_md} |
| CSV dashboards | {total_csv} |
| JSON databases | {total_json} |
| Python scripts | {total_py} |

---

## Security

- **Shield256** encryption for confidential data (`.enc` files)
- Pre-commit hooks auto-encrypt CONFIDENTIAL/TOP_SECRET/RESTRICTED markers
- Toggle: `python toggle_encrypt.py`
- Documentation: [`scripts/shield/`](scripts/shield/)

---

## Key Contacts

| Role | Email |
|------|-------|
| CEO | ceo@artifactvirtual.com |
| Stakeholders | stakeholders@artifactvirtual.com |
| Legal | legal@artifactvirtual.com |
| Security | security@artifactvirtual.com |

---

**Confidentiality:** This repository is private and proprietary. Do not share contents with unauthorized parties.

**License:** [`LICENSE.md`](LICENSE.md) — Proprietary

*Auto-generated by `update-enterprise.sh` — do not edit manually.*
"""

    if dry_run:
        _info("Would regenerate root README.md with current filesystem tree")
        result["details"].append("README.md regeneration (dry-run)")
        return result

    old = README_FILE.read_text() if README_FILE.exists() else ""
    if readme_content.strip() != old.strip():
        README_FILE.write_text(readme_content)
        result["changed"] = True
        _ok("Root README.md updated with current filesystem structure")
        result["details"].append("README.md updated")
    else:
        _ok("Root README.md already current")
        result["details"].append("README.md unchanged")

    return result


# ── 5. CEO Workspace Refresh ───────────────────────────────────────────────

def refresh_ceo_workspace(dry_run: bool) -> dict:
    """Refresh CEO obsidian workspace with latest enterprise data."""
    _section("CEO Workspace Refresh")
    result = {"changed": False, "details": []}

    # Ensure obsidian CEO_CALENDAR matches the one in executive/ceo/
    src = ENTERPRISE_DIR / "divisions/departments/executive/ceo/CEO_CALENDAR.csv"
    dst = OBSIDIAN_DIR / "CEO_CALENDAR.csv"

    if src.exists() and dst.exists():
        if _file_hash(src) != _file_hash(dst):
            if dry_run:
                _info("Would sync CEO_CALENDAR.csv to obsidian/")
                result["details"].append("CEO_CALENDAR sync (dry-run)")
            else:
                import shutil
                shutil.copy2(str(src), str(dst))
                result["changed"] = True
                _ok("Synced CEO_CALENDAR.csv → obsidian/")
                result["details"].append("CEO_CALENDAR.csv synced")
        else:
            _ok("CEO_CALENDAR.csv already in sync")
            result["details"].append("CEO_CALENDAR.csv in sync")
    elif src.exists() and not dst.exists():
        if not dry_run:
            import shutil
            shutil.copy2(str(src), str(dst))
            result["changed"] = True
            _ok("Copied CEO_CALENDAR.csv → obsidian/")
            result["details"].append("CEO_CALENDAR.csv copied")
    else:
        _info("CEO_CALENDAR.csv source not found, skipping sync")
        result["details"].append("CEO_CALENDAR source missing")

    return result


# ── 6. Changelog ───────────────────────────────────────────────────────────

def _get_current_version() -> str:
    """Read current enterprise semver."""
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip()
    return "1.0.0"


def _bump_patch(ver: str) -> str:
    parts = ver.split(".")
    parts[2] = str(int(parts[2]) + 1)
    return ".".join(parts)


def append_changelog(changes: list, dry_run: bool) -> dict:
    """Append entry to monolithic changelog. Never overwrites."""
    _section("Changelog")
    result = {"changed": False, "details": [], "new_version": ""}

    if not changes:
        _ok("No changes to log")
        result["details"].append("no changelog entry needed")
        return result

    current = _get_current_version()
    new_ver = _bump_patch(current)
    result["new_version"] = new_ver
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    entry_lines = [
        f"## [{new_ver}] — {now}",
        "",
    ]
    for c in changes:
        entry_lines.append(f"- {c}")
    entry_lines.append("")
    entry_lines.append("---")
    entry_lines.append("")
    entry = "\n".join(entry_lines)

    if dry_run:
        _info(f"Would append changelog entry v{new_ver} with {len(changes)} change(s)")
        result["details"].append(f"changelog v{new_ver} (dry-run)")
        return result

    # Create changelog directory and file if needed
    CHANGELOG_DIR.mkdir(exist_ok=True)

    if not CHANGELOG_FILE.exists():
        header = (
            "# Enterprise Changelog\n\n"
            "Monolithic semver changelog tracking all enterprise-level changes.\n"
            "**Append-only** — entries are never modified or removed.\n\n"
            "---\n\n"
        )
        CHANGELOG_FILE.write_text(header + entry)
        _ok(f"Created changelog with initial entry v{new_ver}")
    else:
        existing = CHANGELOG_FILE.read_text()
        # Append after the header (after first ---)
        CHANGELOG_FILE.write_text(existing + entry)
        _ok(f"Appended changelog entry v{new_ver}")

    # Update version file
    VERSION_FILE.write_text(new_ver + "\n")
    result["changed"] = True
    result["details"].append(f"changelog v{new_ver} appended ({len(changes)} changes)")

    return result


# ── 7. Terminal Report ─────────────────────────────────────────────────────

def print_report(results: dict, dry_run: bool):
    """Print structured terminal report."""
    _header("ENTERPRISE UPDATE REPORT")

    mode = "DRY-RUN (no changes applied)" if dry_run else "APPLIED"
    print(f"\n  Mode: {_BOLD}{mode}{_RESET}")
    print(f"  Time: {_ts()}")
    print(f"  Repo: {REPO_ROOT}")

    total_changes = sum(1 for r in results.values() if r.get("changed"))

    _section("Summary")
    for name, r in results.items():
        status = f"{_GREEN}changed{_RESET}" if r.get("changed") else f"{_DIM}unchanged{_RESET}"
        print(f"  [{status}] {name}")
        for d in r.get("details", []):
            print(f"         {_DIM}{d}{_RESET}")

    if results.get("drift", {}).get("broken_refs"):
        _section("Broken References (Action Required)")
        for b in results["drift"]["broken_refs"][:15]:
            _warn(b)

    _section("Result")
    if dry_run:
        _info(f"{total_changes} section(s) would change. Run with --apply to commit changes.")
    else:
        if total_changes:
            _ok(f"{total_changes} section(s) updated successfully")
        else:
            _ok("Enterprise is fully up to date — no changes needed")

    print(f"\n{'═' * 72}\n")


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Enterprise Update Engine — single-command enterprise refresh",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python scripts/update_engine.py              # dry-run (default)
              python scripts/update_engine.py --apply      # apply all changes
              python scripts/update_engine.py --apply --skip-db  # skip database sync
        """),
    )
    parser.add_argument("--apply", action="store_true", help="Apply changes (default is dry-run)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying (default)")
    parser.add_argument("--skip-db", action="store_true", help="Skip database sync step")
    parser.add_argument("--skip-csv", action="store_true", help="Skip CSV manifest regeneration")
    args = parser.parse_args()

    dry_run = not args.apply

    _header("ARTIFACT VIRTUAL — ENTERPRISE UPDATE ENGINE")
    print(f"\n  {_DIM}Mode: {'DRY-RUN' if dry_run else 'APPLY'}{_RESET}")
    print(f"  {_DIM}Time: {_ts()}{_RESET}")
    print(f"  {_DIM}Root: {REPO_ROOT}{_RESET}")

    if dry_run:
        print(f"\n  {_YELLOW}This is a dry-run. Use --apply to commit changes.{_RESET}")

    results = OrderedDict()

    # 1. Database sync
    if args.skip_db:
        _section("Database Sync")
        _info("Skipped (--skip-db)")
        results["databases"] = {"changed": False, "details": ["skipped"]}
    else:
        results["databases"] = run_database_sync(dry_run)

    # 2. CSV manifest
    if args.skip_csv:
        _section("CSV Manifest")
        _info("Skipped (--skip-csv)")
        results["csv_manifest"] = {"changed": False, "details": ["skipped"], "csvs": []}
    else:
        results["csv_manifest"] = regenerate_csv_manifest(dry_run)

    # 3. Drift detection (always runs)
    results["drift"] = detect_drift(dry_run)

    # 4. Root README
    drift_notes = results["drift"].get("broken_refs", [])
    csv_count = len(results.get("csv_manifest", {}).get("csvs", []))
    results["readme"] = generate_readme(dry_run, drift_notes, csv_count)

    # 5. CEO workspace
    results["ceo_workspace"] = refresh_ceo_workspace(dry_run)

    # 6. Changelog
    all_changes = []
    for name, r in results.items():
        if r.get("changed"):
            for d in r.get("details", []):
                all_changes.append(d)

    results["changelog"] = append_changelog(all_changes, dry_run)

    # 7. Report
    print_report(results, dry_run)

    # Exit code
    has_errors = any("FAILED" in str(r.get("details", [])) for r in results.values())

    # 8. Auto-launch CEO dashboard in browser (only on --apply, not dry-run)
    if not dry_run and not has_errors:
        _section("Dashboard Launch")
        if DASHBOARD_HTML.exists():
            import webbrowser
            dashboard_url = f"file://{DASHBOARD_HTML.resolve()}"
            try:
                webbrowser.open(dashboard_url)
                _ok(f"Opened CEO dashboard in browser")
            except Exception:
                _info(f"Open manually: {DASHBOARD_HTML}")
        else:
            _warn("CEO dashboard not found at docs/enterprise-dashboard.html")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
