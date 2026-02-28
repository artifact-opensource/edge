#!/usr/bin/env python3
"""
Migrate JSON flat-file databases to SQLite + FTS5
=================================================

Reads all 4 JSON databases and inserts data into enterprise.db.
Safe to run multiple times (uses INSERT OR REPLACE).

Usage:
    python database/migrate_to_sqlite.py
    python database/migrate_to_sqlite.py --verify
"""

import json
import sys
from pathlib import Path

# Ensure imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from database.enterprise_db import EnterpriseDB, SQLITE_DB, DATA_DIR


def load_json(name: str) -> dict:
    path = DATA_DIR / name
    if not path.exists():
        print(f"  SKIP: {name} not found")
        return {}
    data = json.loads(path.read_text())
    print(f"  Loaded {name} ({path.stat().st_size:,} bytes)")
    return data


def clean_record(rec: dict, allowed_keys: set) -> dict:
    """Filter record to only allowed keys and normalize."""
    cleaned = {}
    for k, v in rec.items():
        if k not in allowed_keys:
            continue
        # Convert lists/dicts to JSON strings for storage
        if isinstance(v, (list, dict)):
            cleaned[k] = json.dumps(v)
        elif isinstance(v, bool):
            cleaned[k] = int(v)
        else:
            cleaned[k] = v
    return cleaned


def migrate():
    print("=" * 60)
    print("  ENTERPRISE DATABASE MIGRATION: JSON → SQLite")
    print("=" * 60)

    # Load JSON sources
    print("\n[1/6] Loading JSON databases...")
    public = load_json("public_db.json")
    internal = load_json("internal_db.json")
    projects = load_json("projects_db.json")

    # Initialize SQLite
    print("\n[2/6] Initializing SQLite database...")
    db = EnterpriseDB(SQLITE_DB)
    db.initialize()
    print(f"  Database: {SQLITE_DB}")

    # ── Stakeholders ─────────────────────────────────────────────────
    print("\n[3/6] Migrating stakeholders & community...")
    stakeholder_keys = {
        "id", "name", "role", "tier", "description", "engagement_score",
        "influence", "status", "email", "phone", "linkedin",
        "classification", "created_at", "updated_at",
    }
    stakeholders = public.get("stakeholders", [])
    for s in stakeholders:
        rec = clean_record(s, stakeholder_keys)
        if "id" in rec:
            db.upsert("stakeholders", rec)
    print(f"  Stakeholders: {len(stakeholders)}")

    community_keys = {
        "id", "name", "type", "status", "description", "platform",
        "url", "member_count", "created_at", "updated_at",
    }
    community = public.get("community", [])
    for c in community:
        rec = clean_record(c, community_keys)
        if "id" in rec:
            db.upsert("community", rec)
    print(f"  Community: {len(community)}")

    # ── Documents (merge public + internal) ──────────────────────────
    print("\n[4/6] Migrating documents (public + internal)...")
    doc_keys = {
        "id", "title", "type", "category", "content", "file_path",
        "status", "classification", "source_db", "published_date",
        "tags", "created_at", "updated_at",
    }

    doc_count = 0
    for doc in public.get("public_documents", []):
        rec = clean_record(doc, doc_keys)
        if "id" in rec:
            rec["source_db"] = "public"
            rec.setdefault("classification", "Public")
            db.upsert("documents", rec)
            doc_count += 1

    for doc in internal.get("internal_documents", []):
        rec = clean_record(doc, doc_keys)
        if "id" in rec:
            rec["source_db"] = "internal"
            rec.setdefault("classification", "Internal")
            db.upsert("documents", rec)
            doc_count += 1

    # Also pull project documentation
    for doc in projects.get("project_documentation", []):
        rec = clean_record(doc, doc_keys)
        if "id" in rec:
            rec["source_db"] = "projects"
            rec.setdefault("classification", "Internal")
            db.upsert("documents", rec)
            doc_count += 1

    print(f"  Documents: {doc_count}")

    # ── Projects ─────────────────────────────────────────────────────
    print("\n[5/6] Migrating projects & tasks...")
    project_keys = {
        "id", "project_name", "status", "category", "priority",
        "lifecycle_stage", "health_score", "progress", "open_source",
        "tech_stack", "tags", "readme_path", "description",
        "github_repository", "created_at", "updated_at",
    }
    proj_list = projects.get("projects", [])
    for p in proj_list:
        rec = clean_record(p, project_keys)
        if "id" in rec:
            # Normalize priority to allowed values
            prio = rec.get("priority", "Medium")
            if prio not in ("Critical", "High", "Medium", "Low"):
                rec["priority"] = "Medium"
            db.upsert("projects", rec)
    print(f"  Projects: {len(proj_list)}")

    task_keys = {
        "id", "title", "status", "priority", "project_id",
        "assignee", "due_date", "description", "created_at", "updated_at",
    }
    tasks = projects.get("project_tasks", [])
    for t in tasks:
        rec = clean_record(t, task_keys)
        if "id" in rec:
            # Map 'project' field to 'project_id' if needed
            if "project" in t and "project_id" not in rec:
                rec["project_id"] = t["project"]
            # Normalize status
            status = rec.get("status", "Open")
            if status not in ("Open", "In Progress", "Done", "Blocked", "Cancelled"):
                rec["status"] = "Open"
            prio = rec.get("priority", "Medium")
            if prio not in ("Critical", "High", "Medium", "Low"):
                rec["priority"] = "Medium"
            db.upsert("project_tasks", rec)
    print(f"  Tasks: {len(tasks)}")

    # ── Management & Operations ──────────────────────────────────────
    mgmt_keys = {
        "id", "title", "type", "urgency", "description",
        "business_impact", "approval_required", "status",
        "classification", "created_at", "updated_at",
    }
    mgmt = internal.get("management", [])
    for m in mgmt:
        rec = clean_record(m, mgmt_keys)
        if "id" in rec:
            db.upsert("management", rec)
    print(f"  Management: {len(mgmt)}")

    ops_keys = {
        "id", "title", "type", "business_criticality", "description",
        "sla", "automation_status", "status", "created_at", "updated_at",
    }
    ops = internal.get("operations", [])
    for o in ops:
        rec = clean_record(o, ops_keys)
        if "id" in rec:
            db.upsert("operations", rec)
    print(f"  Operations: {len(ops)}")

    # ── Commit ───────────────────────────────────────────────────────
    print("\n[6/6] Committing transaction...")
    db.conn.commit()

    # ── Verify ───────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  MIGRATION COMPLETE — VERIFICATION")
    print("=" * 60)
    tables = ["stakeholders", "community", "documents", "projects",
              "project_tasks", "management", "operations", "grc_controls"]
    for t in tables:
        n = db.count(t)
        print(f"  {t:25s} {n:>6,} records")

    # Test FTS5
    print("\n  FTS5 Search Test:")
    results = db.search("enterprise")
    print(f"    'enterprise' → {len(results)} results")
    results = db.search("security")
    print(f"    'security'   → {len(results)} results")
    results = db.search("machine learning")
    print(f"    'machine learning' → {len(results)} results")

    db_size = SQLITE_DB.stat().st_size
    print(f"\n  Database size: {db_size:,} bytes ({db_size/1024:.1f} KB)")
    print(f"  Location: {SQLITE_DB}")

    db.close()
    print("\nDone.")


def verify():
    """Verify the SQLite database integrity."""
    print("Verifying enterprise.db...")
    db = EnterpriseDB(SQLITE_DB)
    db.initialize()

    # Integrity check
    result = db.query("PRAGMA integrity_check")
    print(f"  Integrity: {result[0]['integrity_check']}")

    # Table counts
    tables = ["stakeholders", "community", "documents", "projects",
              "project_tasks", "management", "operations", "grc_controls"]
    for t in tables:
        n = db.count(t)
        print(f"  {t:25s} {n:>6,} records")

    # GRC summary
    grc = db.get_grc_summary()
    print(f"\n  GRC: {grc['total']} controls, {grc['readiness_percent']}% compliant")
    print(f"  Breakdown: {grc['by_status']}")

    # FTS5 test
    print(f"\n  FTS5 search 'infrastructure': {len(db.search('infrastructure'))} results")

    db.close()


if __name__ == "__main__":
    if "--verify" in sys.argv:
        verify()
    else:
        migrate()
