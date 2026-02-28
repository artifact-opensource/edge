#!/usr/bin/env python3
"""
Artifact Virtual Enterprise Database — SQLite Engine
=====================================================

Replaces the JSON flat-file database with SQLite + FTS5 for:
  - ACID transactions (no data loss from concurrent access)
  - Full-text search via FTS5 (real search, not keyword grep)
  - Proper schema enforcement via SQL constraints
  - O(log n) queries instead of O(n) scans
  - File locking built in
  - Zero external dependencies (sqlite3 is in Python stdlib)

Tables:
  - stakeholders      (from public_db.json)
  - community         (from public_db.json)
  - documents         (merged public_documents + internal_documents)
  - projects          (from projects_db.json)
  - project_tasks     (from projects_db.json)
  - management        (from internal_db.json)
  - operations        (from internal_db.json)
  - documents_fts     (FTS5 virtual table for RAG search)

Copyright (c) 2025-2026 Artifact Virtual (SMC-Private) Limited
"""

import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# ── Paths ────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_DIR = REPO_ROOT / "database"
DATA_DIR = DB_DIR / "data"
SQLITE_DB = DATA_DIR / "enterprise.db"

# ── Schema ───────────────────────────────────────────────────────────────────

SCHEMA_SQL = """
-- Enable WAL mode for better concurrent read performance
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- ┌──────────────────────────────────────────────────────────┐
-- │  STAKEHOLDERS                                            │
-- └──────────────────────────────────────────────────────────┘
CREATE TABLE IF NOT EXISTS stakeholders (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    role            TEXT,
    tier            TEXT CHECK(tier IN ('Platinum','Gold','Silver','Bronze','Executive','Strategic','Standard','Limited')),
    description     TEXT,
    engagement_score REAL DEFAULT 0,
    influence       TEXT,
    status          TEXT DEFAULT 'Active' CHECK(status IN ('Active','Inactive','Pending','Archived')),
    email           TEXT,
    phone           TEXT,
    linkedin        TEXT,
    classification  TEXT DEFAULT 'Internal' CHECK(classification IN ('Public','Internal','Confidential','Restricted','Top Secret')),
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

-- ┌──────────────────────────────────────────────────────────┐
-- │  COMMUNITY                                               │
-- └──────────────────────────────────────────────────────────┘
CREATE TABLE IF NOT EXISTS community (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    type            TEXT,
    status          TEXT DEFAULT 'Active',
    description     TEXT,
    platform        TEXT,
    url             TEXT,
    member_count    INTEGER DEFAULT 0,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

-- ┌──────────────────────────────────────────────────────────┐
-- │  DOCUMENTS (merged public + internal)                    │
-- └──────────────────────────────────────────────────────────┘
CREATE TABLE IF NOT EXISTS documents (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    type            TEXT,
    category        TEXT,
    content         TEXT,
    file_path       TEXT,
    status          TEXT DEFAULT 'Active',
    classification  TEXT DEFAULT 'Public' CHECK(classification IN ('Public','Internal','Confidential','Restricted','Top Secret')),
    source_db       TEXT CHECK(source_db IN ('public','internal','projects')),
    published_date  TEXT,
    tags            TEXT,  -- JSON array stored as text
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

-- ┌──────────────────────────────────────────────────────────┐
-- │  PROJECTS                                                │
-- └──────────────────────────────────────────────────────────┘
CREATE TABLE IF NOT EXISTS projects (
    id              TEXT PRIMARY KEY,
    project_name    TEXT NOT NULL,
    status          TEXT NOT NULL,
    category        TEXT,
    priority        TEXT CHECK(priority IN ('Critical','High','Medium','Low')),
    lifecycle_stage TEXT,
    health_score    REAL DEFAULT 0,
    progress        REAL DEFAULT 0,
    open_source     INTEGER DEFAULT 0,  -- boolean
    tech_stack      TEXT,  -- JSON array
    tags            TEXT,  -- JSON array
    readme_path     TEXT,
    description     TEXT,
    github_repository TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

-- ┌──────────────────────────────────────────────────────────┐
-- │  PROJECT TASKS                                           │
-- └──────────────────────────────────────────────────────────┘
CREATE TABLE IF NOT EXISTS project_tasks (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    status          TEXT DEFAULT 'Open' CHECK(status IN ('Open','In Progress','Done','Blocked','Cancelled')),
    priority        TEXT CHECK(priority IN ('Critical','High','Medium','Low')),
    project_id      TEXT,  -- loose reference to projects (data may not always match)
    assignee        TEXT,
    due_date        TEXT,
    description     TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

-- ┌──────────────────────────────────────────────────────────┐
-- │  MANAGEMENT DECISIONS & DIRECTIVES                       │
-- └──────────────────────────────────────────────────────────┘
CREATE TABLE IF NOT EXISTS management (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    type            TEXT,
    urgency         TEXT,
    description     TEXT,
    business_impact TEXT,
    approval_required INTEGER DEFAULT 0,
    status          TEXT DEFAULT 'Active',
    classification  TEXT DEFAULT 'Internal',
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

-- ┌──────────────────────────────────────────────────────────┐
-- │  OPERATIONS                                              │
-- └──────────────────────────────────────────────────────────┘
CREATE TABLE IF NOT EXISTS operations (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    type            TEXT,
    business_criticality TEXT,
    description     TEXT,
    sla             TEXT,
    automation_status TEXT,
    status          TEXT DEFAULT 'Active',
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

-- ┌──────────────────────────────────────────────────────────┐
-- │  GRC CONTROLS                                            │
-- └──────────────────────────────────────────────────────────┘
CREATE TABLE IF NOT EXISTS grc_controls (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    category        TEXT NOT NULL,
    description     TEXT,
    status          TEXT DEFAULT 'Not Started' CHECK(status IN ('Compliant','Partial','Not Started','Non-Compliant','In Progress')),
    priority        TEXT DEFAULT 'Medium' CHECK(priority IN ('Critical','High','Medium','Low')),
    owner           TEXT,
    evidence_path   TEXT,
    implementation_notes TEXT,
    frameworks      TEXT,  -- JSON array: ["SOC2", "ISO27001", "GDPR"]
    last_audit_date TEXT,
    next_audit_date TEXT,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

-- ┌──────────────────────────────────────────────────────────┐
-- │  FTS5 FULL-TEXT SEARCH (the RAG engine)                  │
-- └──────────────────────────────────────────────────────────┘
CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
    title,
    content,
    tags,
    category,
    file_path,
    content_rowid='rowid',
    tokenize='porter unicode61'
);

-- Trigger: auto-index documents into FTS on insert
CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
    INSERT INTO documents_fts(rowid, title, content, tags, category, file_path)
    VALUES (
        new.rowid,
        new.title,
        COALESCE(new.content, ''),
        COALESCE(new.tags, ''),
        COALESCE(new.category, ''),
        COALESCE(new.file_path, '')
    );
END;

-- Trigger: auto-update FTS on document update
CREATE TRIGGER IF NOT EXISTS documents_au AFTER UPDATE ON documents BEGIN
    DELETE FROM documents_fts WHERE rowid = old.rowid;
    INSERT INTO documents_fts(rowid, title, content, tags, category, file_path)
    VALUES (
        new.rowid,
        new.title,
        COALESCE(new.content, ''),
        COALESCE(new.tags, ''),
        COALESCE(new.category, ''),
        COALESCE(new.file_path, '')
    );
END;

-- Trigger: auto-delete from FTS
CREATE TRIGGER IF NOT EXISTS documents_ad AFTER DELETE ON documents BEGIN
    DELETE FROM documents_fts WHERE rowid = old.rowid;
END;

-- Index for common queries
CREATE INDEX IF NOT EXISTS idx_documents_classification ON documents(classification);
CREATE INDEX IF NOT EXISTS idx_documents_source ON documents(source_db);
CREATE INDEX IF NOT EXISTS idx_documents_category ON documents(category);
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
CREATE INDEX IF NOT EXISTS idx_stakeholders_tier ON stakeholders(tier);
CREATE INDEX IF NOT EXISTS idx_grc_status ON grc_controls(status);
CREATE INDEX IF NOT EXISTS idx_grc_category ON grc_controls(category);
"""


# ── Database Engine ──────────────────────────────────────────────────────────

class EnterpriseDB:
    """SQLite-backed enterprise database with FTS5 search."""

    VALID_TABLES = frozenset({
        "stakeholders", "community", "documents", "projects",
        "project_tasks", "management", "operations", "grc_controls",
    })

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or SQLITE_DB
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(
                str(self.db_path),
                detect_types=sqlite3.PARSE_DECLTYPES,
            )
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
        return self._conn

    def initialize(self):
        """Create all tables and indexes."""
        self.conn.executescript(SCHEMA_SQL)
        self.conn.commit()

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self):
        self.initialize()
        return self

    def __exit__(self, *args):
        self.close()

    # ── Generic CRUD ─────────────────────────────────────────────────────

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _validate_table(self, table: str) -> None:
        """Reject table names not in the whitelist (prevents SQL injection)."""
        if table not in self.VALID_TABLES:
            raise ValueError(
                f"Invalid table '{table}'. "
                f"Allowed: {', '.join(sorted(self.VALID_TABLES))}"
            )

    def upsert(self, table: str, record: dict):
        """Insert or replace a record."""
        self._validate_table(table)
        record["updated_at"] = self._now()
        if "created_at" not in record:
            record["created_at"] = self._now()

        cols = list(record.keys())
        placeholders = ", ".join(["?"] * len(cols))
        col_names = ", ".join(cols)
        sql = f"INSERT OR REPLACE INTO {table} ({col_names}) VALUES ({placeholders})"
        self.conn.execute(sql, [record[c] for c in cols])

    def upsert_many(self, table: str, records: list[dict]):
        """Bulk upsert within a single transaction."""
        with self.conn:
            for rec in records:
                self.upsert(table, rec)

    def query(self, sql: str, params: tuple = ()) -> list[dict]:
        """Execute SQL and return list of dicts."""
        cursor = self.conn.execute(sql, params)
        rows = cursor.fetchall()
        return [dict(r) for r in rows]

    def count(self, table: str) -> int:
        self._validate_table(table)
        return self.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    def get_by_id(self, table: str, record_id: str) -> Optional[dict]:
        self._validate_table(table)
        rows = self.query(f"SELECT * FROM {table} WHERE id = ?", (record_id,))
        return rows[0] if rows else None

    def delete(self, table: str, record_id: str):
        self._validate_table(table)
        self.conn.execute(f"DELETE FROM {table} WHERE id = ?", (record_id,))
        self.conn.commit()

    # ── RAG Search (FTS5) ────────────────────────────────────────────────

    def search(self, query: str, limit: int = 20, classification_filter: str = None) -> list[dict]:
        """Full-text search across all documents using FTS5.

        Uses BM25 ranking (built into FTS5) for relevance scoring.
        Supports:
          - Simple queries: "machine learning"
          - Boolean: "machine AND learning"
          - Phrase: '"machine learning"'
          - Prefix: "mach*"
          - Column filter: "title:HEKTOR"
          - NEAR: "NEAR(machine learning, 5)"
        """
        if not query.strip():
            return []

        sql = """
            SELECT d.*, 
                   rank as relevance_score
            FROM documents d
            JOIN documents_fts ON d.rowid = documents_fts.rowid
            WHERE documents_fts MATCH ?
        """
        params: list = [query]

        if classification_filter:
            sql += " AND d.classification = ?"
            params.append(classification_filter)

        sql += " ORDER BY rank LIMIT ?"
        params.append(limit)

        return self.query(sql, tuple(params))

    def search_similar(self, document_id: str, limit: int = 10) -> list[dict]:
        """Find documents similar to a given document using shared terms.
        
        Extracts key terms from the source document and searches for them.
        """
        doc = self.get_by_id("documents", document_id)
        if not doc:
            return []

        # Build search query from document content
        terms = []
        if doc.get("title"):
            terms.append(doc["title"])
        if doc.get("tags"):
            try:
                tag_list = json.loads(doc["tags"])
                terms.extend(tag_list[:5])
            except (json.JSONDecodeError, TypeError):
                pass
        if doc.get("category"):
            terms.append(doc["category"])

        if not terms:
            return []

        # OR-combine terms for broad matching; escape double quotes to prevent FTS5 injection
        safe_terms = [t.replace('"', '""') for t in terms if t.strip()]
        fts_query = " OR ".join(f'"{t}"' for t in safe_terms)
        results = self.search(fts_query, limit=limit + 1)
        # Exclude the source document
        return [r for r in results if r["id"] != document_id][:limit]

    def search_by_category(self, category: str, limit: int = 50) -> list[dict]:
        """Get all documents in a category."""
        return self.query(
            "SELECT * FROM documents WHERE category = ? ORDER BY updated_at DESC LIMIT ?",
            (category, limit),
        )

    def search_by_tags(self, tag: str, limit: int = 50) -> list[dict]:
        """Search documents that contain a specific tag."""
        return self.query(
            "SELECT * FROM documents WHERE tags LIKE ? ORDER BY updated_at DESC LIMIT ?",
            (f"%{tag}%", limit),
        )

    # ── Analytics Queries ────────────────────────────────────────────────

    def get_project_summary(self) -> list[dict]:
        """Aggregate project stats by status."""
        return self.query("""
            SELECT status, COUNT(*) as count, 
                   ROUND(AVG(health_score), 1) as avg_health,
                   ROUND(AVG(progress), 1) as avg_progress
            FROM projects GROUP BY status ORDER BY count DESC
        """)

    def get_stakeholder_summary(self) -> list[dict]:
        """Aggregate stakeholder stats by tier."""
        return self.query("""
            SELECT tier, COUNT(*) as count,
                   ROUND(AVG(engagement_score), 1) as avg_engagement
            FROM stakeholders GROUP BY tier ORDER BY count DESC
        """)

    def get_grc_summary(self) -> dict:
        """GRC compliance dashboard data."""
        rows = self.query("""
            SELECT status, COUNT(*) as count
            FROM grc_controls GROUP BY status
        """)
        total = sum(r["count"] for r in rows)
        compliant = next((r["count"] for r in rows if r["status"] == "Compliant"), 0)
        return {
            "total": total,
            "compliant": compliant,
            "readiness_percent": round(compliant / total * 100, 1) if total else 0,
            "by_status": {r["status"]: r["count"] for r in rows},
        }

    def get_document_stats(self) -> dict:
        """Document statistics across the repository."""
        total = self.count("documents")
        by_classification = self.query("""
            SELECT classification, COUNT(*) as count
            FROM documents GROUP BY classification ORDER BY count DESC
        """)
        by_category = self.query("""
            SELECT category, COUNT(*) as count
            FROM documents GROUP BY category ORDER BY count DESC LIMIT 20
        """)
        return {
            "total": total,
            "by_classification": {r["classification"]: r["count"] for r in by_classification},
            "by_category": {r["category"]: r["count"] for r in by_category},
        }

    # ── Export (for backward compat with JSON consumers) ─────────────────

    def export_table_json(self, table: str) -> list[dict]:
        """Export all rows from a table as a list of dicts."""
        self._validate_table(table)
        return self.query(f"SELECT * FROM {table}")

    def export_all_json(self) -> dict:
        """Export entire database as a JSON-compatible dict structure."""
        return {
            "version": "2.0.0",
            "engine": "sqlite",
            "exported_at": self._now(),
            "stakeholders": self.export_table_json("stakeholders"),
            "community": self.export_table_json("community"),
            "documents": self.export_table_json("documents"),
            "projects": self.export_table_json("projects"),
            "project_tasks": self.export_table_json("project_tasks"),
            "management": self.export_table_json("management"),
            "operations": self.export_table_json("operations"),
            "grc_controls": self.export_table_json("grc_controls"),
        }


# ── Convenience singleton ────────────────────────────────────────────────────

_db: Optional[EnterpriseDB] = None


def get_db(db_path: Optional[Path] = None) -> EnterpriseDB:
    """Get or create a singleton database instance."""
    global _db
    if _db is None:
        _db = EnterpriseDB(db_path)
        _db.initialize()
    return _db


def reset_db():
    """Close and reset the singleton (useful for testing)."""
    global _db
    if _db:
        _db.close()
        _db = None
