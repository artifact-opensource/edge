"""
Enterprise Tools
================

Concrete tool implementations wrapping the enterprise database, document
search, GRC controls, report generation, and file operations.

Each function decorated with ``@tool`` automatically becomes available
to agents that have it in their ``tools`` list.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from agents.tools import tool

logger = logging.getLogger(__name__)

# ── Lazy-loaded shared resources ─────────────────────────────────────────────
# These get injected by the runtime at startup via set_shared_resources()

_db = None
_rag = None
_repo_root: Path = Path(__file__).resolve().parent.parent.parent


def set_shared_resources(db: Any, rag: Any, repo_root: Path | None = None) -> None:
    """Inject shared database and RAG instances for tools to use."""
    global _db, _rag, _repo_root
    _db = db
    _rag = rag
    if repo_root:
        _repo_root = repo_root


def _get_db():
    if _db is None:
        from database.enterprise_db import get_db

        return get_db()
    return _db


# ── Document Search Tools ────────────────────────────────────────────────────


@tool("search_documents", "Search enterprise documents using hybrid RAG (keyword + semantic)")
async def search_documents(query: str, limit: int = 5) -> list[dict]:
    """Search documents across the enterprise knowledge base.

    Args:
        query: Natural language search query.
        limit: Maximum number of results to return.
    """
    if _rag is not None:
        results = await _rag.search(query, limit=limit)
        return [
            {
                "id": r.document_id,
                "title": r.title,
                "content": r.content[:300],
                "file_path": r.file_path,
                "category": r.category,
                "score": round(r.score, 4),
            }
            for r in results
        ]
    # Fallback to keyword-only search
    db = _get_db()
    rows = db.search(query, limit=limit)
    return [
        {
            "id": row.get("id", ""),
            "title": row.get("title", ""),
            "content": (row.get("content", "") or "")[:300],
            "file_path": row.get("file_path", ""),
            "category": row.get("category", ""),
        }
        for row in rows
    ]


@tool("search_by_category", "Search documents filtered by category")
def search_by_category(category: str, limit: int = 20) -> list[dict]:
    """Search documents within a specific category.

    Args:
        category: Document category to filter by.
        limit: Maximum number of results.
    """
    db = _get_db()
    rows = db.search_by_category(category, limit=limit)
    return [
        {
            "id": row.get("id", ""),
            "title": row.get("title", ""),
            "file_path": row.get("file_path", ""),
        }
        for row in rows
    ]


# ── Database Query Tools ─────────────────────────────────────────────────────


@tool("query_database", "Execute a read-only SQL query against the enterprise database")
def query_database(sql: str) -> list[dict]:
    """Execute a SELECT query on the enterprise database.

    Args:
        sql: SQL SELECT statement to execute. Only SELECT is allowed.
    """
    if not sql.strip().upper().startswith("SELECT"):
        return [{"error": "Only SELECT queries are allowed"}]
    db = _get_db()
    try:
        return db.query(sql)
    except Exception as exc:
        return [{"error": str(exc)}]


@tool("get_project_summary", "Get aggregate project statistics by status")
def get_project_summary() -> list[dict]:
    """Get project summary statistics grouped by status."""
    db = _get_db()
    return db.get_project_summary()


@tool("get_stakeholder_summary", "Get aggregate stakeholder statistics by tier")
def get_stakeholder_summary() -> list[dict]:
    """Get stakeholder summary statistics grouped by tier."""
    db = _get_db()
    return db.get_stakeholder_summary()


# ── GRC Tools ────────────────────────────────────────────────────────────────


@tool("get_grc_summary", "Get GRC compliance dashboard data")
def get_grc_summary() -> dict:
    """Get GRC compliance summary with status breakdowns."""
    db = _get_db()
    return db.get_grc_summary()


@tool("get_grc_controls", "List GRC controls, optionally filtered by status or category")
def get_grc_controls(
    status: str = "", category: str = "", limit: int = 52
) -> list[dict]:
    """List GRC controls with optional filtering.

    Args:
        status: Filter by status (Compliant, Partial, Not Started, etc.).
        category: Filter by category.
        limit: Maximum controls to return.
    """
    db = _get_db()
    sql = "SELECT id, title, category, status, priority, owner FROM grc_controls WHERE 1=1"
    params: list[Any] = []
    if status:
        sql += " AND status = ?"
        params.append(status)
    if category:
        sql += " AND category = ?"
        params.append(category)
    sql += " ORDER BY category, priority LIMIT ?"
    params.append(limit)
    return db.query(sql, tuple(params))


@tool("update_grc_control", "Update a GRC control's status or notes")
def update_grc_control(
    control_id: str, status: str = "", notes: str = ""
) -> dict:
    """Update a GRC control.

    Args:
        control_id: The GRC control ID to update.
        status: New status (Compliant, Partial, Not Started, In Progress, Non-Compliant).
        notes: Implementation notes to set.
    """
    db = _get_db()
    control = db.get_by_id("grc_controls", control_id)
    if not control:
        return {"error": f"GRC control '{control_id}' not found"}

    if status:
        valid = {"Compliant", "Partial", "Not Started", "In Progress", "Non-Compliant"}
        if status not in valid:
            return {"error": f"Invalid status. Must be one of: {valid}"}
        control["status"] = status
    if notes:
        control["implementation_notes"] = notes

    db.upsert("grc_controls", control)
    db.conn.commit()
    return {"success": True, "control_id": control_id, "status": control.get("status")}


# ── Report Tools ─────────────────────────────────────────────────────────────


@tool("get_document_stats", "Get document statistics across the repository")
def get_document_stats() -> dict:
    """Get comprehensive document statistics."""
    db = _get_db()
    return db.get_document_stats()


@tool("generate_report", "Generate a markdown report from database data")
def generate_report(report_type: str) -> str:
    """Generate a formatted report.

    Args:
        report_type: Type of report: 'grc', 'projects', 'stakeholders', 'documents'.
    """
    db = _get_db()

    if report_type == "grc":
        summary = db.get_grc_summary()
        controls = db.query(
            "SELECT category, status, COUNT(*) as cnt FROM grc_controls GROUP BY category, status ORDER BY category"
        )
        lines = [
            f"# GRC Compliance Report",
            f"",
            f"**Total Controls:** {summary['total']}",
            f"**Compliant:** {summary['compliant']}",
            f"**Readiness:** {summary['readiness_percent']}%",
            f"",
            f"## Status Breakdown",
        ]
        for status, count in summary["by_status"].items():
            lines.append(f"- {status}: {count}")
        lines.append(f"\n## By Category")
        for row in controls:
            lines.append(f"- {row['category']} / {row['status']}: {row['cnt']}")
        return "\n".join(lines)

    elif report_type == "projects":
        summaries = db.get_project_summary()
        lines = ["# Project Status Report", ""]
        for s in summaries:
            lines.append(
                f"- **{s['status']}**: {s['count']} projects "
                f"(avg health: {s['avg_health']}, avg progress: {s['avg_progress']}%)"
            )
        return "\n".join(lines)

    elif report_type == "stakeholders":
        summaries = db.get_stakeholder_summary()
        lines = ["# Stakeholder Summary Report", ""]
        for s in summaries:
            lines.append(
                f"- **{s['tier']}**: {s['count']} stakeholders "
                f"(avg engagement: {s['avg_engagement']})"
            )
        return "\n".join(lines)

    elif report_type == "documents":
        stats = db.get_document_stats()
        lines = [
            f"# Document Statistics Report",
            f"",
            f"**Total Documents:** {stats['total']}",
            f"",
            f"## By Classification",
        ]
        for cls, cnt in stats["by_classification"].items():
            lines.append(f"- {cls}: {cnt}")
        lines.append(f"\n## Top Categories")
        for cat, cnt in list(stats["by_category"].items())[:10]:
            lines.append(f"- {cat}: {cnt}")
        return "\n".join(lines)

    return f"Unknown report type: {report_type}. Available: grc, projects, stakeholders, documents"


# ── File System Tools ────────────────────────────────────────────────────────


@tool("read_file", "Read the contents of a file in the repository")
def read_file(file_path: str, max_lines: int = 100) -> str:
    """Read a file from the enterprise repository.

    Args:
        file_path: Relative path from repo root.
        max_lines: Maximum number of lines to return.
    """
    target = _repo_root / file_path
    if not target.exists():
        return f"File not found: {file_path}"
    if not target.is_file():
        return f"Not a file: {file_path}"
    # Security: ensure path is within repo
    try:
        target.resolve().relative_to(_repo_root.resolve())
    except ValueError:
        return "Access denied: path is outside the repository"

    try:
        lines = target.read_text(encoding="utf-8", errors="replace").splitlines()
        if len(lines) > max_lines:
            return "\n".join(lines[:max_lines]) + f"\n\n... ({len(lines) - max_lines} more lines)"
        return "\n".join(lines)
    except Exception as exc:
        return f"Error reading file: {exc}"


@tool("list_directory", "List contents of a directory in the repository")
def list_directory(path: str = ".") -> list[str]:
    """List files and directories at the given path.

    Args:
        path: Relative path from repo root.
    """
    target = _repo_root / path
    if not target.exists():
        return [f"Directory not found: {path}"]
    if not target.is_dir():
        return [f"Not a directory: {path}"]

    entries = []
    for item in sorted(target.iterdir()):
        name = item.name
        if item.is_dir():
            name += "/"
        entries.append(name)
    return entries


# ── Workflow Tools ───────────────────────────────────────────────────────────


@tool("list_workflows", "List all available workflow definitions")
def list_workflows() -> list[dict]:
    """List all workflow definitions with their enabled/disabled status."""
    workflows_dir = _repo_root / "enterprise" / "workflows"
    results = []
    for json_file in sorted(workflows_dir.rglob("*.json")):
        try:
            data = json.loads(json_file.read_text())
            results.append(
                {
                    "name": data.get("name", json_file.stem),
                    "enabled": data.get("enabled", False),
                    "department": data.get("department", ""),
                    "type": data.get("type", ""),
                    "path": str(json_file.relative_to(_repo_root)),
                }
            )
        except (json.JSONDecodeError, Exception):
            continue
    return results
