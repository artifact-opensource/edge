# Enterprise Backend Database System

**Version:** 1.0.0  
**Date:** 2026-02-09  
**Status:** Production Ready

---

## Overview

The Enterprise Backend Database System is a centralized, lightweight database infrastructure designed to:

- **Consolidate all enterprise data** into 3 core databases (public, internal, projects)
- **Enable RAG capabilities** through an indexed database
- **Sync with Notion workspace** to keep external portals up to date
- **Provide a simple update mechanism** accessible from the repository root
- **Match Notion schemas** for seamless integration

---

## Database Structure

### Core Databases

#### 1. **Public Database** (`public_db.json`)
Contains all public data and documentation visible to stakeholders and community.

**Tables:**
- `stakeholders` - Master stakeholder registry
- `community` - Community members and engagement
- `public_documents` - Public documentation and announcements

#### 2. **Internal Database** (`internal_db.json`)
Contains all internal data and documentation for management use only.

**Tables:**
- `management` - Management decisions and directives
- `operations` - Operational workflows and procedures
- `internal_documents` - Internal documentation and policies

#### 3. **Projects Database** (`projects_db.json`)
Contains project information with links to repositories and documentation.

**Tables:**
- `projects` - Master projects registry
- `project_tasks` - Tasks and milestones
- `project_documentation` - Documentation pulled from repos

#### 4. **Indexed Database** (`indexed_db.json`)
Lightweight indexed database for RAG (Retrieval-Augmented Generation) capabilities.

**Features:**
- Full-text indexing of all documents
- Keyword extraction and indexing
- Tag and category indexing
- Fast search and retrieval

---

## Quick Start

### Simple Update (Recommended)

From the repository root, run:

```bash
# Update all databases
./update-enterprise.sh

# Or using Python directly
python3 update-enterprise.py
```

This will:
1. Scan the repository for new/updated files
2. Sync data to databases
3. Update the indexed database for RAG
4. Validate all data
5. Show statistics

### View Statistics Only

```bash
python3 update-dbs.py --stats
```

### Validate Only

```bash
python3 update-dbs.py --validate
```

---

## Directory Structure

```
enterprise/
├── database/
│   ├── data/                          # Database files (JSON)
│   │   ├── public_db.json            # Public database
│   │   ├── internal_db.json          # Internal database
│   │   ├── projects_db.json          # Projects database
│   │   └── indexed_db.json           # Indexed database for RAG
│   │
│   ├── schemas/                       # Schema definitions
│   │   ├── public_schema.json        # Public DB schema
│   │   ├── internal_schema.json      # Internal DB schema
│   │   └── projects_schema.json      # Projects DB schema
│   │
│   ├── utils/                         # Utility modules
│   │   ├── db_manager.py             # Core database management
│   │   └── sync_from_repo.py         # Repository sync utilities
│   │
│   ├── update_databases.py           # Main update script
│   └── README.md                     # This file
│
├── update-dbs.py                     # Root update script (Python)
└── update-dbs.sh                     # Root update script (Bash)
```

---

## How It Works

### Data Flow

```
Repository Files
    ↓
[Sync Process]
    ↓
Core Databases (JSON)
    ↓
[Indexing Process]
    ↓
Indexed Database (RAG)
    ↓
[Export Process]
    ↓
Notion Workspace
```

### Sync Sources

The system automatically scans and syncs from the **entire repository** - it's **location-agnostic**:

**Projects Database:**
- **Comprehensive Scan**: Walks entire repository looking for project directories
- **Project Indicators**: README.md, package.json, Cargo.toml, go.mod, pom.xml, etc.
- **Location Agnostic**: Finds projects anywhere in the repository
- **Excludes**: .git, node_modules, build artifacts, cache directories
- Extracts: README files, project metadata, GitHub links

**Public Database:**
- **Comprehensive Scan**: Searches entire repository for public documentation
- **Public Indicators**: docs/, documentation/, guide/, tutorial/, readme, changelog
- **Content-Aware**: Automatically excludes internal/confidential documents
- **Location Agnostic**: Finds documentation wherever it exists
- Extracts: Documentation, announcements, policies

**Internal Database:**
- **Comprehensive Scan**: Finds stakeholder and internal documents anywhere
- **Stakeholder Indicators**: stakeholder/, business/, executive/, partner/, investor/
- **Classification-Aware**: Respects document classification
- **Location Agnostic**: Adapts to repository reorganization
- Extracts: Internal policies, decisions, reports

**Key Features:**
- **No hardcoded paths** - scans entire repository
- **Keyword-based detection** - finds content by meaning, not location
- **Comprehensive** - won't miss files even after refactoring
- **Authoritative** - definitive source of truth for all data
- **Smart exclusions** - skips build artifacts, node_modules, etc.

---

## Usage Examples

### Update All Databases

```bash
cd /path/to/enterprise
./update-dbs.sh
```

### Programmatic Access

```python
from database.utils.db_manager import get_db_manager

# Get database manager
db = get_db_manager()

# Query projects
projects = db.query('projects_db', 'projects', {'status': 'Active'})

# Add a new project
project_data = {
    'project_name': 'New Project',
    'status': 'Planning',
    'category': 'Flagship Products',
    'description': 'A new flagship product'
}
project_id = db.add_record('projects_db', 'projects', project_data)

# Update a project
db.update_record('projects_db', 'projects', project_id, {
    'status': 'Active',
    'progress': 25
})

# Get statistics
stats = db.get_stats('projects_db')
print(f"Total projects: {stats['tables']['projects']['count']}")
```

### Search in Indexed Database

```python
from database.utils.db_manager import get_db_manager

db = get_db_manager()
indexed = db.load_db('indexed_db')

# Search by keyword
keyword = 'stakeholder'
if keyword in indexed['indexes']['by_keywords']:
    doc_ids = indexed['indexes']['by_keywords'][keyword]
    print(f"Found {len(doc_ids)} documents matching '{keyword}'")
```

---

## Notion Integration

### Automatic Sync

The Notion integration has been redesigned to:

1. **Update local databases first** - Always sync repository → databases
2. **Then push to Notion** - Export databases → Notion workspace
3. **Populate documents properly** - No more empty databases!

### Updated Notion Scripts

Located in `notion/scripts/`:

- `export_to_notion.py` - Export databases to Notion (NEW)
- `notion_sync.py` - Full sync: repo → DBs → Notion (CONSOLIDATED)

### Usage

```bash
# Update local databases AND push to Notion
cd notion/scripts
python3 notion_sync.py

# Only export to Notion (assumes DBs are updated)
python3 export_to_notion.py
```

---

## Database Schemas

All schemas match Notion database schemas for seamless integration.

### Public Database Schema

**Stakeholders Table:**
- Required: `id`, `name`
- Properties: category, tier, status, region, engagement_score, total_value, contacts, etc.
- Indexes: name, category, status, tier

**Community Table:**
- Required: `id`, `member_name`, `username`
- Properties: member_type, status, contributions, github_username, skills, etc.
- Indexes: member_name, username, status

**Public Documents Table:**
- Required: `id`, `title`
- Properties: type, category, content, file_path, published_date, tags, etc.
- Indexes: title, type, status, published_date

### Projects Database Schema

**Projects Table:**
- Required: `id`, `project_name`
- Properties: category, status, priority, health_score, progress, dates, team, budget, github_repository, tech_stack, etc.
- Indexes: project_name, category, status, priority, open_source

**Project Tasks Table:**
- Required: `id`, `task_name`, `project_id`
- Properties: status, priority, assignee, dates, description, tags
- Indexes: task_name, project_id, status, assignee

**Project Documentation Table:**
- Required: `id`, `project_id`, `doc_title`
- Properties: doc_type, file_path, content, last_synced, repo_url, commit_sha
- Indexes: project_id, doc_title, doc_type

### Internal Database Schema

**Management Table:**
- Required: `id`, `title`
- Properties: type, department, status, priority, owner, stakeholders, content, dates, etc.
- Indexes: title, type, status, department

**Operations Table:**
- Required: `id`, `operation_name`
- Properties: type, department, status, frequency, owner, description, steps, etc.
- Indexes: operation_name, type, department, status

**Internal Documents Table:**
- Required: `id`, `title`
- Properties: type, category, classification, content, file_path, author, department, version, etc.
- Indexes: title, type, classification, status, department

---

## RAG Capabilities

The indexed database provides lightweight RAG (Retrieval-Augmented Generation) capabilities:

### Features

1. **Full-Text Indexing** - All documents indexed by content
2. **Keyword Extraction** - Automatic keyword extraction and indexing
3. **Tag-Based Search** - Search by tags and categories
4. **Fast Retrieval** - Optimized for quick lookups

### Index Structure

```json
{
  "indexes": {
    "by_content": {},      // Full-text index
    "by_keywords": {},     // Keyword → document IDs
    "by_tags": {},         // Tag → document IDs
    "by_category": {}      // Category → document IDs
  },
  "documents": [],         // All indexed documents
  "metadata": {
    "total_documents": 0,
    "total_keywords": 0,
    "last_indexed": "ISO timestamp"
  }
}
```

### Example RAG Query

```python
from database.utils.db_manager import get_db_manager

db = get_db_manager()
indexed = db.load_db('indexed_db')

def search_documents(query: str):
    """Search documents by keyword"""
    results = []
    keywords = query.lower().split()
    
    for keyword in keywords:
        if keyword in indexed['indexes']['by_keywords']:
            doc_ids = indexed['indexes']['by_keywords'][keyword]
            for doc in indexed['documents']:
                if doc['id'] in doc_ids:
                    results.append(doc)
    
    return results

# Search for "stakeholder management"
results = search_documents("stakeholder management")
for doc in results:
    print(f"- {doc['title']} ({doc['source_db']})")
```

---

## Security

### Data Classification

- **Public Database** - Safe to share externally
- **Internal Database** - Internal use only, contains sensitive information
- **Projects Database** - Mix of public (open source) and internal projects
- **Indexed Database** - Includes all data, handle with care

### Git Configuration

The `.gitignore` file is configured to:
- **Include** database schemas (version controlled)
- **Include** database structure files
- **Exclude** database data files (optional - configure as needed)

To version control database data:
```bash
# Add to git
git add database/data/*.json
```

To exclude database data:
```bash
# Add to .gitignore
database/data/*.json
!database/data/.gitkeep
```

---

## Testing

### Manual Testing

```bash
# 1. Update databases
./update-dbs.sh

# 2. Check statistics
python3 update-dbs.py --stats

# 3. Validate data
python3 update-dbs.py --validate
```

### Automated Testing

```bash
# Run tests (if test suite exists)
cd database
python3 -m pytest tests/
```

---

## Maintenance

### Regular Updates

**Daily:**
- Run `./update-dbs.sh` to sync latest changes

**Weekly:**
- Review database statistics
- Validate data integrity
- Check for schema updates

**Monthly:**
- Backup database files
- Review and archive old data
- Update documentation

### Backup Strategy

```bash
# Backup all databases
timestamp=$(date +%Y%m%d_%H%M%S)
tar -czf database_backup_${timestamp}.tar.gz database/data/

# Restore from backup
tar -xzf database_backup_YYYYMMDD_HHMMSS.tar.gz
```

---

## Troubleshooting

### Database Not Updating

**Problem:** `update-dbs.sh` runs but no data is synced

**Solution:**
```bash
# Check if files exist in expected locations
ls -la enterprise/projects/
ls -la enterprise/stakeholders/
ls -la docs/

# Run with verbose output
python3 database/update_databases.py
```

### Schema Validation Errors

**Problem:** Validation fails with type errors

**Solution:**
```bash
# Check schema files
cat database/schemas/public_schema.json
cat database/schemas/projects_schema.json

# Validate manually
python3 update-dbs.py --validate
```

### Notion Sync Issues

**Problem:** Notion databases are empty

**Solution:**
1. First update local databases: `./update-dbs.sh`
2. Then sync to Notion: `cd notion/scripts && python3 notion_sync.py`
3. Check Notion API key: `echo $NOTION_API_KEY`

---

## Advanced Configuration

### Custom Sync Sources

Edit `database/utils/sync_from_repo.py` to add custom sync sources:

```python
def sync_custom_data(self):
    """Sync custom data source"""
    custom_dir = self.repo_root / "custom" / "data"
    # Add your sync logic here
```

### Custom Indexes

Edit `database/update_databases.py` to add custom indexes:

```python
# Add to update_indexed_db() function
indexed_db['indexes']['by_custom'] = {}
# Build your custom index
```

---

## API Reference

### DatabaseManager

**Methods:**
- `load_db(db_name)` - Load a database
- `save_db(db_name, data)` - Save a database
- `load_schema(schema_name)` - Load a schema
- `validate_record(record, schema, db_type)` - Validate a record
- `add_record(db_name, db_type, record)` - Add a record
- `update_record(db_name, db_type, record_id, updates)` - Update a record
- `query(db_name, db_type, filters)` - Query records
- `get_stats(db_name)` - Get statistics

### RepositorySync

**Methods:**
- `sync_all()` - Sync all data from repository
- `sync_projects()` - Sync projects only
- `sync_stakeholder_docs()` - Sync stakeholder documents only
- `sync_public_docs()` - Sync public documents only

---

## Contributing

This is an internal system. For improvements:

1. Test changes thoroughly
2. Update documentation
3. Run validation: `python3 update-dbs.py --validate`
4. Update schemas if needed
5. Document any breaking changes

---

## License

Internal use only. Proprietary to Artifact Virtual (SMC-Private) Limited.

---

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the API reference
- Contact the DevOps team

---

**Last Updated:** 2026-02-09  
**Version:** 1.0.0  
**Next Review:** 2026-03-09
