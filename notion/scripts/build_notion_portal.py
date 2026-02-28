#!/usr/bin/env python3
"""
Artifact Virtual — Notion Portal Builder
=========================================

Creates and populates TWO Notion portal pages from local JSON databases:

  1. Community Portal  — Projects, tasks, community members, feedback
  2. Stakeholder Portal — Stakeholder directory, management, operations, docs, roadmap

Idempotent: searches for existing pages/databases by title and reuses them.
Populates databases from database/data/*.json on every run.

Usage:
    python build_notion_portal.py                  # full build + populate
    python build_notion_portal.py --dry-run        # log actions without API calls
    python build_notion_portal.py --portal community   # build only community
    python build_notion_portal.py --portal stakeholder # build only stakeholder
    python build_notion_portal.py --populate-only  # skip page/db creation, just populate

Environment Variables (required):
    NOTION_API_KEY          — Notion integration token (secret_… or ntn_…)
    NOTION_PARENT_PAGE_ID   — Parent page ID where portals will be created
"""

import os
import sys
import json
import argparse
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger("build_notion_portal")

# ---------------------------------------------------------------------------
# Import Notion wrapper (same directory)
# ---------------------------------------------------------------------------
try:
    from av_notion_client import NotionIntegration
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from av_notion_client import NotionIntegration

# ---------------------------------------------------------------------------
# Paths to local JSON databases
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DB_DATA   = REPO_ROOT / "database" / "data"

PROJECTS_DB  = DB_DATA / "projects_db.json"
PUBLIC_DB    = DB_DATA / "public_db.json"
INTERNAL_DB  = DB_DATA / "internal_db.json"


# ═══════════════════════════════════════════════════════════════════════════
# Schema Definitions (field → Notion property type)
# ═══════════════════════════════════════════════════════════════════════════

COMMUNITY_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "Projects": {
        "Name":         {"type": "title"},
        "Status":       {"type": "select",  "options": ["Active", "Planning", "Complete", "Blocked", "Concept", "On Hold"]},
        "Category":     {"type": "select",  "options": ["Product", "Platform", "Research", "Operations", "Infrastructure", "AI/ML", "Other"]},
        "Priority":     {"type": "select",  "options": ["Critical", "High", "Medium", "Low"]},
        "Stage":        {"type": "select",  "options": ["Concept", "Planning", "MVP", "Beta", "General Availability", "Maintenance"]},
        "Health Score": {"type": "number",  "format": "number"},
        "Progress":     {"type": "number",  "format": "percent"},
        "Open Source":  {"type": "checkbox"},
        "Tech Stack":   {"type": "multi_select", "options": []},
        "Tags":         {"type": "multi_select", "options": []},
        "Description":  {"type": "rich_text"},
        "GitHub URL":   {"type": "url"},
    },

    "Project Tasks": {
        "Name":     {"type": "title"},
        "Status":   {"type": "select",  "options": ["Todo", "In Progress", "Review", "Done", "Blocked"]},
        "Priority": {"type": "select",  "options": ["Critical", "High", "Medium", "Low"]},
        "Project":  {"type": "rich_text"},
    },

    "Community Members": {
        "Name":        {"type": "title"},
        "Type":        {"type": "select",  "options": ["Platform", "Discord", "Forum", "GitHub", "Social", "Newsletter", "Other"]},
        "Status":      {"type": "select",  "options": ["Active", "Inactive", "Planned", "Archived"]},
        "Description": {"type": "rich_text"},
    },

    "Feedback & Requests": {
        "Name":    {"type": "title"},
        "Type":    {"type": "select",  "options": ["Bug", "Feature", "Improvement", "Question"]},
        "Status":  {"type": "select",  "options": ["Open", "In Progress", "Planned", "Closed"]},
        "Votes":   {"type": "number",  "format": "number"},
        "Source":  {"type": "rich_text"},
    },
}

STAKEHOLDER_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "Stakeholder Directory": {
        "Name":             {"type": "title"},
        "Role":             {"type": "select",  "options": ["Founder", "Investor", "Advisor", "Partner", "Board Member", "Government", "Community", "Customer", "Vendor", "Other"]},
        "Tier":             {"type": "select",  "options": ["Executive", "Strategic", "Standard", "Limited"]},
        "Status":           {"type": "select",  "options": ["Active", "Inactive", "Prospect", "Former"]},
        "Engagement Score": {"type": "number",  "format": "number"},
        "Influence":        {"type": "select",  "options": ["Critical", "High", "Medium", "Low"]},
        "Description":      {"type": "rich_text"},
    },

    "Management": {
        "Name":            {"type": "title"},
        "Type":            {"type": "select",  "options": ["Recurring", "One-time", "Strategic", "Compliance", "Review"]},
        "Urgency":         {"type": "select",  "options": ["Critical", "High", "Medium", "Low"]},
        "Status":          {"type": "select",  "options": ["Active", "Inactive", "Pending", "Complete"]},
        "Business Impact": {"type": "select",  "options": ["Critical", "High", "Medium", "Low"]},
        "Approval":        {"type": "checkbox"},
        "Description":     {"type": "rich_text"},
    },

    "Operations": {
        "Name":          {"type": "title"},
        "Type":          {"type": "select",  "options": ["DevOps", "Security", "Monitoring", "Database", "Network", "Compliance", "Other"]},
        "Criticality":   {"type": "select",  "options": ["Critical", "High", "Medium", "Low"]},
        "Status":        {"type": "select",  "options": ["Active", "Inactive", "Maintenance", "Planned"]},
        "SLA":           {"type": "rich_text"},
        "Automation":    {"type": "select",  "options": ["Fully Automated", "Partially Automated", "Manual", "Planned"]},
        "Description":   {"type": "rich_text"},
    },

    "Documents": {
        "Name":          {"type": "title"},
        "Document Type": {"type": "select",  "options": ["Contract", "Agreement", "Policy", "Business Plan", "Research", "Memo", "Presentation", "Report", "Other"]},
        "Status":        {"type": "select",  "options": ["Draft", "Review", "Approved", "Executed", "Expired", "Published"]},
        "Classification":{"type": "select",  "options": ["Public", "Internal", "Confidential", "Restricted"]},
        "File Path":     {"type": "rich_text"},
    },

    "Roadmap": {
        "Name":     {"type": "title"},
        "Quarter":  {"type": "select",  "options": ["Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026", "Q1 2027"]},
        "Status":   {"type": "select",  "options": ["Planned", "In Progress", "Complete", "Deferred"]},
        "Priority": {"type": "select",  "options": ["Critical", "High", "Medium", "Low"]},
        "Category": {"type": "select",  "options": ["Product", "Platform", "Operations", "Business", "Research"]},
        "Notes":    {"type": "rich_text"},
    },
}


# ═══════════════════════════════════════════════════════════════════════════
# Data Loaders — read local JSON → list of dicts ready for Notion insert
# ═══════════════════════════════════════════════════════════════════════════

def _load_json(path: Path) -> dict:
    if not path.exists():
        log.warning(f"Database file not found: {path}")
        return {}
    with open(path) as f:
        return json.load(f)


def load_projects() -> List[Dict]:
    """Load projects from projects_db.json → rows for Projects DB."""
    data = _load_json(PROJECTS_DB)
    rows = []
    for p in data.get("projects", []):
        rows.append({
            "Name":         p.get("project_name", "Untitled"),
            "Status":       p.get("status", ""),
            "Category":     p.get("category", ""),
            "Priority":     p.get("priority", ""),
            "Stage":        p.get("lifecycle_stage", ""),
            "Health Score": p.get("health_score", 0),
            "Progress":     p.get("progress", 0),
            "Open Source":  bool(p.get("open_source", False)),
            "Tech Stack":   p.get("tech_stack", []) if isinstance(p.get("tech_stack"), list) else [],
            "Tags":         p.get("tags", []) if isinstance(p.get("tags"), list) else [],
            "Description":  p.get("description", ""),
            "GitHub URL":   p.get("github_repository", ""),
        })
    return rows


def load_project_tasks() -> List[Dict]:
    """Load project tasks → rows for Project Tasks DB."""
    data = _load_json(PROJECTS_DB)
    rows = []
    for t in data.get("project_tasks", []):
        rows.append({
            "Name":     t.get("title", "Untitled"),
            "Status":   t.get("status", ""),
            "Priority": t.get("priority", ""),
            "Project":  t.get("project", ""),
        })
    return rows


def load_community() -> List[Dict]:
    """Load community channels → rows for Community Members DB."""
    data = _load_json(PUBLIC_DB)
    rows = []
    for c in data.get("community", []):
        rows.append({
            "Name":        c.get("name", "Untitled"),
            "Type":        c.get("type", ""),
            "Status":      c.get("status", ""),
            "Description": c.get("description", ""),
        })
    return rows


def load_stakeholders() -> List[Dict]:
    """Load stakeholders → rows for Stakeholder Directory DB."""
    data = _load_json(PUBLIC_DB)
    rows = []
    for s in data.get("stakeholders", []):
        rows.append({
            "Name":             s.get("name", "Untitled"),
            "Role":             s.get("role", ""),
            "Tier":             s.get("tier", ""),
            "Status":           s.get("status", ""),
            "Engagement Score": s.get("engagement_score", 0),
            "Influence":        s.get("influence", ""),
            "Description":      s.get("description", ""),
        })
    return rows


def load_management() -> List[Dict]:
    """Load management items → rows for Management DB."""
    data = _load_json(INTERNAL_DB)
    rows = []
    for m in data.get("management", []):
        rows.append({
            "Name":            m.get("title", "Untitled"),
            "Type":            m.get("type", ""),
            "Urgency":         m.get("urgency", ""),
            "Status":          m.get("status", ""),
            "Business Impact": m.get("business_impact", ""),
            "Approval":        bool(m.get("approval_required", False)),
            "Description":     m.get("description", ""),
        })
    return rows


def load_operations() -> List[Dict]:
    """Load operations → rows for Operations DB."""
    data = _load_json(INTERNAL_DB)
    rows = []
    for o in data.get("operations", []):
        rows.append({
            "Name":        o.get("title", "Untitled"),
            "Type":        o.get("type", ""),
            "Criticality": o.get("business_criticality", ""),
            "Status":      o.get("status", ""),
            "SLA":         o.get("sla", ""),
            "Automation":  o.get("automation_status", ""),
            "Description": o.get("description", ""),
        })
    return rows


def load_documents() -> List[Dict]:
    """Combined key documents from internal + public databases."""
    rows = []
    # Internal documents (top 30)
    data = _load_json(INTERNAL_DB)
    for d in data.get("internal_documents", [])[:30]:
        rows.append({
            "Name":           d.get("title", "Untitled"),
            "Document Type":  d.get("type", "Other"),
            "Status":         d.get("status", ""),
            "Classification": d.get("classification", "Internal"),
            "File Path":      d.get("file_path", ""),
        })
    # Public documents (top 30)
    data2 = _load_json(PUBLIC_DB)
    for d in data2.get("public_documents", [])[:30]:
        rows.append({
            "Name":           d.get("title", "Untitled"),
            "Document Type":  d.get("type", "Other"),
            "Status":         d.get("status", ""),
            "Classification": "Public",
            "File Path":      d.get("file_path", ""),
        })
    return rows


def load_roadmap() -> List[Dict]:
    """Generate roadmap items from project data."""
    data = _load_json(PROJECTS_DB)
    rows = []
    status_map = {"Active": "In Progress", "Planning": "Planned", "Complete": "Complete", "Concept": "Planned"}
    for p in data.get("projects", []):
        rows.append({
            "Name":     p.get("project_name", "Untitled"),
            "Quarter":  "Q1 2026",
            "Status":   status_map.get(p.get("status", ""), "Planned"),
            "Priority": p.get("priority", "Medium"),
            "Category": p.get("category", "Product"),
            "Notes":    p.get("description", ""),
        })
    return rows


# ═══════════════════════════════════════════════════════════════════════════
# Notion Helpers
# ═══════════════════════════════════════════════════════════════════════════

def _find_or_create_page(notion: Optional[NotionIntegration], title: str,
                         parent_id: str, icon: str, description: str,
                         dry_run: bool) -> str:
    """Find existing page by title, or create a new one. Returns page_id."""
    if dry_run:
        log.info(f"  [DRY] Would create page: {title}")
        return f"dry-page-{title}"

    results = notion.search(title, filter_type="page")
    for r in results:
        if r.get("title", "").strip() == title:
            log.info(f"  ↺ Reusing page: {title} ({r['id'][:8]}…)")
            return r["id"]

    result = notion.create_page_in_parent(
        parent_id=parent_id, title=title, icon=icon, description=description
    )
    if result.get("status") == "success":
        log.info(f"  ✓ Created page: {title} ({result['page_id'][:8]}…)")
        return result["page_id"]
    raise RuntimeError(f"Failed to create page '{title}': {result.get('error')}")


def _find_or_create_db(notion: Optional[NotionIntegration], title: str,
                       parent_id: str, schema: Dict, dry_run: bool) -> str:
    """Find existing database by title, or create a new one. Returns database_id."""
    if dry_run:
        log.info(f"    [DRY] Would create DB: {title}")
        return f"dry-db-{title}"

    results = notion.search(title, filter_type="database")
    for r in results:
        if r.get("title", "").strip() == title:
            log.info(f"    ↺ Reusing DB: {title} ({r['id'][:8]}…)")
            return r["id"]

    result = notion.create_database_from_schema(
        parent_page_id=parent_id, title=title, schema=schema
    )
    if result.get("status") == "success":
        log.info(f"    ✓ Created DB: {title} ({result['database_id'][:8]}…)")
        return result["database_id"]
    raise RuntimeError(f"Failed to create DB '{title}': {result.get('error')}")


def _clear_database(notion: NotionIntegration, db_id: str) -> int:
    """Archive all existing rows from a database for fresh population."""
    count = 0
    try:
        rows = notion.query_database(db_id, page_size=100)
        for row in rows:
            row_id = row.get("id")
            if row_id:
                if notion.client:
                    notion.client.pages.update(page_id=row_id, archived=True)
                else:
                    notion._http.patch(f"/pages/{row_id}", json_body={"archived": True})
                count += 1
                time.sleep(0.15)
    except Exception as e:
        log.warning(f"    Could not fully clear DB {db_id[:8]}…: {e}")
    return count


def _build_notion_properties(row: Dict, schema: Dict) -> Dict[str, Any]:
    """Convert a flat row dict to Notion API property format."""
    props = {}
    for key, value in row.items():
        if key not in schema:
            continue
        meta = schema[key]
        ptype = meta.get("type") if isinstance(meta, dict) else meta

        if ptype == "title":
            props[key] = {"title": [{"text": {"content": str(value)[:2000]}}]}
        elif ptype == "rich_text":
            props[key] = {"rich_text": [{"text": {"content": str(value)[:2000]}}]}
        elif ptype == "select":
            if value:
                props[key] = {"select": {"name": str(value)}}
        elif ptype == "multi_select":
            if isinstance(value, list) and value:
                props[key] = {"multi_select": [{"name": str(v)} for v in value[:25]]}
        elif ptype == "number":
            try:
                props[key] = {"number": float(value) if value else 0}
            except (ValueError, TypeError):
                props[key] = {"number": 0}
        elif ptype == "checkbox":
            props[key] = {"checkbox": bool(value)}
        elif ptype == "url":
            if value:
                props[key] = {"url": str(value)}
        elif ptype == "date":
            if value:
                props[key] = {"date": {"start": str(value)}}
        elif ptype == "email":
            if value:
                props[key] = {"email": str(value)}

    return props


def _populate_database(notion: Optional[NotionIntegration], db_id: str,
                       db_title: str, schema: Dict, rows: List[Dict],
                       dry_run: bool, clear_first: bool = True) -> int:
    """Populate a Notion database from row dicts. Returns rows created."""
    if dry_run:
        log.info(f"    [DRY] Would populate {db_title} with {len(rows)} rows")
        return len(rows)

    if clear_first:
        cleared = _clear_database(notion, db_id)
        if cleared:
            log.info(f"    Cleared {cleared} existing rows from {db_title}")

    created = 0
    for i, row in enumerate(rows):
        props = _build_notion_properties(row, schema)
        if not props:
            continue
        result = notion.create_page_in_database(db_id, props)
        if result.get("status") == "success":
            created += 1
        else:
            log.warning(f"    Row {i} failed: {result.get('error', 'unknown')}")
        # Rate limiting: ~3 requests per second
        if (i + 1) % 3 == 0:
            time.sleep(1.1)

    log.info(f"    ✓ Populated {db_title}: {created}/{len(rows)} rows")
    return created


# ═══════════════════════════════════════════════════════════════════════════
# Content Builders — rich page content for each portal
# ═══════════════════════════════════════════════════════════════════════════

def _community_content_blocks() -> List[Dict]:
    """Rich content blocks for the Community Portal landing page."""
    return [
        {"object": "block", "type": "heading_1", "heading_1": {
            "rich_text": [{"type": "text", "text": {"content": "🚀 Community Portal"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {
            "rich_text": [{"type": "text", "text": {"content":
                "Welcome to the Artifact Virtual Community Portal. This is the public-facing hub for "
                "all projects, community engagement, and collaboration. Use this portal to track project "
                "progress, submit feature requests, and stay connected with the AV community."}}]}},
        {"object": "block", "type": "divider", "divider": {}},
        {"object": "block", "type": "heading_2", "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "📊 Quick Stats"}}]}},
        {"object": "block", "type": "callout", "callout": {
            "icon": {"type": "emoji", "emoji": "🏗️"},
            "rich_text": [{"type": "text", "text": {"content":
                "21 Active Projects  •  17 Open Tasks  •  8 Community Channels\n"
                "Open Source First  •  AI/ML + Infrastructure + Platform"}}]}},
        {"object": "block", "type": "divider", "divider": {}},
        {"object": "block", "type": "heading_2", "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "🗂️ Databases"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {
            "rich_text": [{"type": "text", "text": {"content":
                "Scroll down to browse the Projects, Tasks, Community Members, and Feedback databases. "
                "All data is synced from the Artifact Virtual repository."}}]}},
        {"object": "block", "type": "divider", "divider": {}},
        {"object": "block", "type": "heading_2", "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "💡 How to Contribute"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "Browse projects and find one that interests you"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "Submit feedback or feature requests via the Feedback database"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "Join community channels (Discord, GitHub, Forum)"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "Participate in consensus discussions and roadmap votes"}}]}},
    ]


def _stakeholder_content_blocks() -> List[Dict]:
    """Rich content blocks for the Stakeholder Portal landing page."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return [
        {"object": "block", "type": "heading_1", "heading_1": {
            "rich_text": [{"type": "text", "text": {"content": "👥 Stakeholder Portal"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {
            "rich_text": [{"type": "text", "text": {"content":
                "Artifact Virtual (SMC-Private) Limited — SECP Registration #0325693\n"
                "Comprehensive stakeholder management portal with directory, management view, "
                "operations dashboard, document library, and strategic roadmap."}}]}},
        {"object": "block", "type": "divider", "divider": {}},
        {"object": "block", "type": "heading_2", "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "📈 Executive Dashboard"}}]}},
        {"object": "block", "type": "callout", "callout": {
            "icon": {"type": "emoji", "emoji": "🏢"},
            "rich_text": [{"type": "text", "text": {"content":
                f"Last Synced: {now}\n"
                "25 Stakeholders  •  8 Management Items  •  8 Operations Systems\n"
                "21 Projects on Roadmap  •  60+ Key Documents"}}]}},
        {"object": "block", "type": "divider", "divider": {}},
        {"object": "block", "type": "heading_2", "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "🏛️ Company Overview"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {
            "rich_text": [{"type": "text", "text": {"content":
                "Artifact Virtual is a technology company focused on AI/ML research, open-source "
                "development, and enterprise solutions. Incorporated February 6, 2026 under SECP Pakistan. "
                "The company operates across multiple divisions: Technology, Research, Operations, and Community."}}]}},
        {"object": "block", "type": "divider", "divider": {}},
        {"object": "block", "type": "heading_2", "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "🗂️ Portal Contents"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "Stakeholder Directory — All stakeholders with engagement scores and tiers"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "Management — Executive review items, compliance, and strategic decisions"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "Operations — DevOps, security, monitoring, and infrastructure systems"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "Documents — Key contracts, policies, business plans, and research papers"}}]}},
        {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": "Roadmap — Strategic project roadmap with quarterly milestones"}}]}},
    ]


# ═══════════════════════════════════════════════════════════════════════════
# Main Builder Class
# ═══════════════════════════════════════════════════════════════════════════

class PortalBuilder:
    """Builds and populates the two Notion portals."""

    COMMUNITY_DBS: List[Tuple[str, Any]] = [
        ("Projects",           load_projects),
        ("Project Tasks",      load_project_tasks),
        ("Community Members",  load_community),
        ("Feedback & Requests", lambda: []),
    ]

    STAKEHOLDER_DBS: List[Tuple[str, Any]] = [
        ("Stakeholder Directory", load_stakeholders),
        ("Management",            load_management),
        ("Operations",            load_operations),
        ("Documents",             load_documents),
        ("Roadmap",               load_roadmap),
    ]

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.api_key = os.getenv("NOTION_API_KEY")
        self.parent_id = os.getenv("NOTION_PARENT_PAGE_ID")
        self.notion: Optional[NotionIntegration] = None

        if not dry_run:
            if not self.api_key:
                raise ValueError("NOTION_API_KEY not set")
            if not self.parent_id:
                raise ValueError("NOTION_PARENT_PAGE_ID not set")
            self.notion = NotionIntegration(self.api_key)
            conn = self.notion.test_connection()
            if conn.get("status") != "connected":
                raise RuntimeError(f"Notion connection failed: {conn.get('error')}")
            log.info(f"Connected to Notion as: {conn.get('user')}")

        self.pages: Dict[str, str] = {}
        self.databases: Dict[str, str] = {}
        self.stats: Dict[str, int] = {}

    def build_community(self) -> str:
        """Build the Community Portal page and its databases."""
        log.info("=" * 60)
        log.info("BUILDING COMMUNITY PORTAL")
        log.info("=" * 60)

        page_id = _find_or_create_page(
            self.notion, "Community Portal", self.parent_id,
            "🚀", "Artifact Virtual — Projects, community engagement, and collaboration",
            self.dry_run
        )
        self.pages["community"] = page_id

        if not self.dry_run and self.notion:
            self.notion.append_children(page_id, _community_content_blocks())

        for db_title, loader in self.COMMUNITY_DBS:
            schema = COMMUNITY_SCHEMAS[db_title]
            db_id = _find_or_create_db(self.notion, db_title, page_id, schema, self.dry_run)
            self.databases[f"community/{db_title}"] = db_id
            rows = loader()
            n = _populate_database(self.notion, db_id, db_title, schema, rows, self.dry_run)
            self.stats[db_title] = n

        log.info("✓ Community Portal complete\n")
        return page_id

    def build_stakeholder(self) -> str:
        """Build the Stakeholder Portal page and its databases."""
        log.info("=" * 60)
        log.info("BUILDING STAKEHOLDER PORTAL")
        log.info("=" * 60)

        page_id = _find_or_create_page(
            self.notion, "Stakeholder Portal", self.parent_id,
            "👥", "Artifact Virtual — Stakeholder directory, management, operations, and roadmap",
            self.dry_run
        )
        self.pages["stakeholder"] = page_id

        if not self.dry_run and self.notion:
            self.notion.append_children(page_id, _stakeholder_content_blocks())

        for db_title, loader in self.STAKEHOLDER_DBS:
            schema = STAKEHOLDER_SCHEMAS[db_title]
            db_id = _find_or_create_db(self.notion, db_title, page_id, schema, self.dry_run)
            self.databases[f"stakeholder/{db_title}"] = db_id
            rows = loader()
            n = _populate_database(self.notion, db_id, db_title, schema, rows, self.dry_run)
            self.stats[db_title] = n

        log.info("✓ Stakeholder Portal complete\n")
        return page_id

    def build_all(self, portal: Optional[str] = None, populate_only: bool = False):
        """Build everything (or specific portal)."""
        log.info("=" * 60)
        log.info("ARTIFACT VIRTUAL — NOTION PORTAL BUILDER")
        log.info(f"  Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        log.info(f"  Time: {datetime.now(timezone.utc).isoformat()}")
        log.info("=" * 60 + "\n")

        if populate_only:
            self._populate_existing()
            return

        if portal in (None, "community"):
            self.build_community()
        if portal in (None, "stakeholder"):
            self.build_stakeholder()

        self._print_summary()

    def _populate_existing(self):
        """Populate-only mode: find existing DBs and repopulate."""
        log.info("POPULATE-ONLY MODE — finding existing databases…\n")

        all_dbs = {}
        for title, loader in self.COMMUNITY_DBS:
            all_dbs[title] = (loader, COMMUNITY_SCHEMAS[title])
        for title, loader in self.STAKEHOLDER_DBS:
            all_dbs[title] = (loader, STAKEHOLDER_SCHEMAS[title])

        for db_title, (loader, schema) in all_dbs.items():
            db_id = None
            if not self.dry_run and self.notion:
                results = self.notion.search(db_title, filter_type="database")
                for r in results:
                    if r.get("title", "").strip() == db_title:
                        db_id = r["id"]
                        break
            if not db_id:
                log.warning(f"  DB not found: {db_title} — skipping")
                continue
            rows = loader()
            n = _populate_database(self.notion, db_id, db_title, schema, rows, self.dry_run)
            self.stats[db_title] = n

        self._print_summary()

    def _print_summary(self):
        """Print final build summary."""
        log.info("=" * 60)
        log.info("BUILD SUMMARY")
        log.info("=" * 60)
        log.info(f"Pages:     {len(self.pages)}")
        log.info(f"Databases: {len(self.databases)}")
        total_rows = sum(self.stats.values())
        log.info(f"Rows:      {total_rows}")
        for name, count in self.stats.items():
            log.info(f"  {name}: {count}")
        log.info("=" * 60)

    def save_manifest(self, path: Optional[Path] = None):
        """Save JSON manifest of created resources for sync tracking."""
        if path is None:
            path = REPO_ROOT / "notion" / "portal-manifest.json"
        manifest = {
            "built_at": datetime.now(timezone.utc).isoformat(),
            "mode": "dry-run" if self.dry_run else "live",
            "pages": self.pages,
            "databases": self.databases,
            "stats": self.stats,
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(manifest, f, indent=2)
        log.info(f"Manifest saved to {path}")


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Build and populate Artifact Virtual Notion portals"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Log actions without making API calls")
    parser.add_argument("--portal", choices=["community", "stakeholder"],
                        help="Build only a specific portal (default: both)")
    parser.add_argument("--populate-only", action="store_true",
                        help="Skip page/DB creation; just repopulate existing databases")
    parser.add_argument("--no-manifest", action="store_true",
                        help="Skip saving portal-manifest.json")

    args = parser.parse_args()

    try:
        builder = PortalBuilder(dry_run=args.dry_run)
        builder.build_all(portal=args.portal, populate_only=args.populate_only)
        if not args.no_manifest:
            builder.save_manifest()
        return 0
    except Exception as e:
        log.error(f"Build failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
