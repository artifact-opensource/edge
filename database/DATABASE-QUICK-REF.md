# Enterprise Backend Database - Quick Reference

## Quick Start

### Update All Databases

```bash
# From repository root
./update-dbs.sh

# Or using Python
python3 update-dbs.py
```

### View Statistics

```bash
python3 update-dbs.py --stats
```

### Sync to Notion

```bash
# Test first (dry run)
cd notion/scripts
python3 notion_sync.py --dry-run

# Live sync
python3 notion_sync.py
```

---

## Database Summary

| Database | Location | Purpose | Current Records |
|----------|----------|---------|-----------------|
| **Public DB** | `database/data/public_db.json` | Stakeholders, community, public docs | 9 docs |
| **Internal DB** | `database/data/internal_db.json` | Management, operations, internal docs | 17 docs |
| **Projects DB** | `database/data/projects_db.json` | Projects, tasks, documentation | 19 projects |
| **Indexed DB** | `database/data/indexed_db.json` | RAG-enabled document index | 26 docs, 2066 keywords |

---

## Common Workflows

### Daily Sync

```bash
# 1. Update databases from repository
./update-dbs.sh

# 2. Push to Notion (optional)
cd notion/scripts && python3 notion_sync.py
```

### Adding New Projects

Projects are automatically detected from `enterprise/projects/` directory.

1. Add project directory with README.md
2. Run: `./update-dbs.sh`
3. Project appears in `projects_db.json`

### Adding Documentation

Public docs from `docs/` and internal docs from `enterprise/stakeholders/` are automatically synced.

1. Add/update markdown files
2. Run: `./update-dbs.sh`
3. Documents appear in respective databases

### Querying Data

```python
from database.utils.db_manager import get_db_manager

db = get_db_manager()

# Get all active projects
projects = db.query('projects_db', 'projects', {'status': 'Active'})
print(f"Active projects: {len(projects)}")

# Search indexed database
indexed = db.load_db('indexed_db')
keyword = 'stakeholder'
if keyword in indexed['indexes']['by_keywords']:
    docs = indexed['indexes']['by_keywords'][keyword]
    print(f"Found {len(docs)} documents with '{keyword}'")
```

---

## Troubleshooting

### Database Not Updating

```bash
# Check if directories exist
ls enterprise/projects/
ls enterprise/stakeholders/
ls docs/

# Run update manually
python3 database/update_databases.py
```

### Notion Sync Issues

```bash
# Check environment variables
echo $NOTION_API_KEY
echo $NOTION_PARENT_PAGE_ID

# Test connection
cd notion/scripts && python3 notion_status.py

# Try dry run first
python3 notion_sync.py --dry-run
```

### Validation Errors

```bash
# Run validation
python3 update-dbs.py --validate

# Check schemas
cat database/schemas/public_schema.json
cat database/schemas/internal_schema.json
cat database/schemas/projects_schema.json
```

---

## Documentation

- **Full Guide:** `/database/README.md`
- **Notion Integration:** `/notion/INTEGRATION-FIXED.md`
- **Schemas:** `/database/schemas/`

---

## Key Features

### Centralized Data
All enterprise data in 3 core databases (public, internal, projects)

### RAG-Enabled
Indexed database with 2066+ keywords for fast search and AI context

### Auto-Sync
Automatically scans repository and updates databases

### Notion Integration
Proper workflow: repo → DBs → Notion (DBs always updated first!)

### Schema Validation
All data validated against schemas before adding

### Simple Interface
One command to update everything: `./update-dbs.sh`

---

## Support

**Database Issues:** Check `/database/README.md`  
**Notion Issues:** Check `/notion/INTEGRATION-FIXED.md`  
**General Help:** Contact DevOps team

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-09
