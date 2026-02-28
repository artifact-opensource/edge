# RAG Usage Guide — Enterprise Database

> **Engine:** SQLite + FTS5 (replaced the JSON flat-file system)
> **Module:** `database/enterprise_db.py`
> **Database:** `database/data/enterprise.db`

---

## Quick Start

```python
from database.enterprise_db import get_db

db = get_db()

# Full-text search across all documents
results = db.search("machine learning")

for doc in results:
    print(f"{doc['title']} (score: {doc['relevance_score']:.2f})")
    print(f"  Path: {doc['file_path']}")
    print(f"  Category: {doc['category']}")
```

---

## Architecture

The enterprise database uses **SQLite with FTS5** (Full-Text Search 5):

- **ACID transactions** — no data loss from concurrent access
- **FTS5 full-text search** — BM25 ranking, boolean queries, phrase matching
- **SQL schema enforcement** — constraints, foreign keys, type checking
- **O(log n) queries** — indexed lookups instead of linear scans
- **WAL mode** — concurrent readers don't block each other
- **Zero external deps** — `sqlite3` is in Python's standard library

### Tables

| Table | Contents | Records |
|-------|----------|---------|
| `documents` | All indexed markdown/text files | ~490 |
| `documents_fts` | FTS5 virtual table (auto-synced) | ~490 |
| `projects` | Project metadata and status | ~46 |
| `project_tasks` | Task breakdown per project | varies |
| `stakeholders` | Stakeholder profiles | ~25 |
| `community` | Community members | varies |
| `management` | Management records | varies |
| `operations` | Operational data | varies |
| `grc_controls` | GRC compliance controls | 52 |

---

## API Reference

### Initialization

```python
from database.enterprise_db import get_db, reset_db

# Get singleton instance (creates DB if needed)
db = get_db()

# Or with custom path
from pathlib import Path
db = get_db(db_path=Path("/custom/path/enterprise.db"))

# Reset singleton (useful in tests)
reset_db()
```

### Context Manager

```python
from database.enterprise_db import EnterpriseDB

with EnterpriseDB() as db:
    results = db.search("encryption")
    # auto-closes on exit
```

---

### Full-Text Search

#### Basic Search

```python
results = db.search("infrastructure")
# Returns list of dicts with all document columns + relevance_score
```

#### Boolean Queries

```python
# AND — both terms required
results = db.search("machine AND learning")

# OR — either term
results = db.search("security OR compliance")

# NOT — exclude term
results = db.search("encryption NOT legacy")
```

#### Phrase Search

```python
# Exact phrase matching
results = db.search('"data center"')
```

#### Prefix Search

```python
# Matches: machine, machinery, machining, etc.
results = db.search("mach*")
```

#### Column-Specific Search

```python
# Search only in the title field
results = db.search("title:HEKTOR")
```

#### Proximity Search

```python
# Terms within 5 tokens of each other
results = db.search("NEAR(machine learning, 5)")
```

#### Filtered Search

```python
# Filter by document classification
results = db.search("security", classification_filter="internal")
results = db.search("roadmap", classification_filter="public")
```

#### Limit Results

```python
# Default limit is 20; override as needed
results = db.search("enterprise", limit=50)
```

### Similarity Search

```python
# Find documents similar to a given document
similar = db.search_similar("doc-001", limit=10)
```

### Category and Tag Search

```python
# All documents in a category
docs = db.search_by_category("security", limit=50)

# Documents with a specific tag
docs = db.search_by_tags("encryption", limit=50)
```

---

### CRUD Operations

#### Read

```python
# Get a single record by ID
doc = db.get_by_id("documents", "doc-001")

# Count records in a table
total = db.count("documents")

# Raw SQL query
rows = db.query("SELECT title, category FROM documents WHERE category = ?", ("security",))
```

#### Write

```python
# Upsert (insert or replace)
db.upsert("documents", {
    "id": "doc-new",
    "title": "New Document",
    "content": "Full text content here...",
    "category": "operations",
    "classification": "internal",
    "path": "docs/new-doc.md",
})
db.conn.commit()

# Bulk upsert (single transaction)
db.upsert_many("documents", [
    {"id": "doc-1", "title": "First", "content": "..."},
    {"id": "doc-2", "title": "Second", "content": "..."},
])
```

#### Delete

```python
db.delete("documents", "doc-001")
```

---

### Analytics Queries

```python
# Project status summary
summary = db.get_project_summary()
# [{"status": "Active", "count": 18, "avg_health": 72.5, "avg_progress": 35.0}, ...]

# Stakeholder breakdown by tier
tiers = db.get_stakeholder_summary()
# [{"tier": "Platinum", "count": 3, "avg_engagement": 85.0}, ...]

# GRC compliance dashboard
grc = db.get_grc_summary()
# {"total": 52, "compliant": 19, "readiness_percent": 36.5, "by_status": {...}}

# Document statistics
stats = db.get_document_stats()
# {"total": 490, "by_classification": {...}, "by_category": {...}}
```

---

### Export

```python
# Export a single table as list of dicts
docs = db.export_table_json("projects")

# Export entire database as JSON-compatible dict
full_export = db.export_all_json()
# {"version": "2.0.0", "engine": "sqlite", "exported_at": "...", "stakeholders": [...], ...}
```

---

## Return Format

All query methods return `list[dict]`. Each dict contains the row's column values:

```python
result = db.search("shield256")[0]
# {
#     "id": "doc-123",
#     "title": "Shield256 Encryption System",
#     "content": "AES-256-GCM authenticated encryption...",
#     "file_path": "scripts/shield/shield256.py",
#     "category": "security",
#     "classification": "internal",
#     "tags": "[\"encryption\", \"aes\", \"security\"]",
#     "created_at": "2026-02-06T...",
#     "updated_at": "2026-02-06T...",
#     "relevance_score": -12.45  # BM25 score (lower = more relevant)
# }
```

> **Note on BM25 scores:** FTS5 returns negative BM25 scores where *lower* (more negative) means *more relevant*. Results are sorted by `rank` ascending, so the most relevant appear first.

---

## Common Patterns

### RAG Pipeline Integration

```python
def retrieve_context(query: str, top_k: int = 5) -> str:
    """Retrieve relevant context for an LLM prompt."""
    db = get_db()
    results = db.search(query, limit=top_k)
    
    context_parts = []
    for doc in results:
        context_parts.append(
            f"--- {doc['title']} ({doc['file_path']}) ---\n"
            f"{doc['content'][:2000]}\n"
        )
    
    return "\n".join(context_parts)
```

### Building a Search API

```python
def search_api(query: str, category: str = None, limit: int = 20) -> dict:
    """Search endpoint for API integration."""
    db = get_db()
    
    if category:
        results = db.search_by_category(category, limit=limit)
    else:
        results = db.search(query, limit=limit)
    
    return {
        "query": query,
        "count": len(results),
        "results": [
            {
                "id": r["id"],
                "title": r["title"],
                "file_path": r["file_path"],
                "category": r["category"],
                "score": r.get("relevance_score"),
            }
            for r in results
        ],
    }
```

### GRC Compliance Check

```python
def check_compliance() -> str:
    """Generate a GRC compliance summary."""
    db = get_db()
    grc = db.get_grc_summary()
    
    return (
        f"GRC Readiness: {grc['readiness_percent']}%\n"
        f"Controls: {grc['compliant']}/{grc['total']} compliant\n"
        f"Breakdown: {grc['by_status']}"
    )
```

---

## Database Location

```
database/
├── data/
│   └── enterprise.db          # SQLite database (WAL mode)
├── enterprise_db.py            # EnterpriseDB class + get_db()
├── update_databases.py         # Sync markdown → SQLite
├── generate_knowledge_graph.py # Generate graph from DB
└── RAG-USAGE-GUIDE.md         # This file
```

## Updating the Database

```bash
# Re-scan all markdown files and sync to SQLite
python database/update_databases.py
```

This scans the repository, extracts document metadata, syncs everything to SQLite, and regenerates the knowledge graph.
