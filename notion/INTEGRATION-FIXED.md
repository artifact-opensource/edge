# Notion Integration - Consolidated & Fixed

## Overview

The Notion integration has been **completely redesigned** to fix the issue where Notion databases were empty. The new system follows a proper workflow:

```
Repository Files
    ↓
[Local Databases] ← Update first!
    ↓
[Notion Workspace] ← Then sync
```

## Key Changes

### ✅ What's Fixed

1. **Databases Update First** - Local databases are always updated from repository before syncing to Notion
2. **Documents Are Populated** - Notion databases now receive actual document content, not just empty structures
3. **Consolidated Scripts** - Reduced from 14+ scripts to 2 main scripts
4. **Clear Workflow** - Simple, sequential process that's easy to understand
5. **RAG Integration** - Indexed database provides context for AI assistants

### 🗑️ Scripts Consolidated/Replaced

The following scripts are **redundant** and replaced by the new system:

**Replaced by `/database/` system:**
- `create_all_databases.py` - Replaced by `database/update_databases.py`
- `fix_titles_and_create_dbs.py` - No longer needed
- `check_and_seed_dbs.py` - Replaced by database sync
- `seed_stakeholder_and_community.py` - Replaced by sync_from_repo.py
- `report_db_counts.py` - Replaced by `update-dbs.py --stats`

**Cloudflare scripts (unrelated to Notion):**
- `cf_configure_github_pages.py` - Move to separate cloudflare/ dir
- `cf_list_tunnels.py` - Move to separate cloudflare/ dir
- `cf_set_ssl.py` - Move to separate cloudflare/ dir

**Keep these:**
- ✅ `notion_sync.py` - **NEW** - Main sync script (repo → DBs → Notion)
- ✅ `av_notion_client.py` - Notion API client wrapper
- ✅ `build_notion_portal.py` - Portal structure builder (for initial setup)
- ✅ `notion_status.py` - Check Notion connection status
- ✅ `validate_and_build.py` - Validation utilities

## Usage

### Simple Sync (Recommended)

From repository root:

```bash
# Update databases only (no Notion)
./update-dbs.sh

# Full sync: Update DBs + Push to Notion
cd notion/scripts
python3 notion_sync.py --dry-run  # Test first
python3 notion_sync.py             # Live sync
```

### Advanced Usage

```bash
# Export databases to Notion only (skip DB update)
python3 notion_sync.py --skip-db-update

# Export specific database
cd ../../database/utils
python3 export_to_notion.py --database public_db --dry-run
```

## Architecture

### Local Database Layer

Located in `/database/`:

- **public_db.json** - Stakeholders, community, public docs
- **internal_db.json** - Management, operations, internal docs
- **projects_db.json** - Projects, tasks, documentation
- **indexed_db.json** - RAG-enabled index for all documents

### Notion Layer

Located in `/notion/scripts/`:

- **notion_sync.py** - Complete sync workflow
- **export_to_notion.py** - Export databases to Notion
- **av_notion_client.py** - Notion API wrapper

### Sync Flow

```
1. Repository Changes
   ↓
2. Run: ./update-dbs.sh
   → Scans enterprise/projects/
   → Scans enterprise/stakeholders/
   → Scans docs/
   → Updates local JSON databases
   → Builds indexed database for RAG
   ↓
3. Run: notion_sync.py
   → Reads local databases
   → Creates/updates Notion databases
   → Populates with actual documents
   → Updates sync logs
```

## Why This Fixes Empty Databases

### The Problem

Old scripts created database **structures** in Notion but didn't populate them with content because:

1. They read directly from repository files (inconsistent)
2. No intermediate data layer
3. No validation or indexing
4. Sync was fragile and error-prone

### The Solution

New system:

1. **Centralizes data** in local JSON databases
2. **Validates** all data against schemas
3. **Indexes** for fast retrieval
4. **Populates Notion** from validated, structured data
5. **Maintains sync state** to avoid duplicates

## Environment Variables

Required for Notion sync:

```bash
# Notion API key (get from https://www.notion.so/my-integrations)
export NOTION_API_KEY="secret_xxxxxxxxxxxx"

# Parent page ID (where portal will be created)
export NOTION_PARENT_PAGE_ID="xxxxxxxxxxxx"
```

## Migration Guide

### From Old Scripts to New System

**Step 1: Update local databases**
```bash
cd /path/to/enterprise
./update-dbs.sh
```

**Step 2: Verify data**
```bash
python3 update-dbs.py --stats
```

You should see:
- 19 projects
- 17 internal documents
- 9 public documents
- 2066+ keywords in indexed DB

**Step 3: Export to Notion**
```bash
cd notion/scripts
python3 notion_sync.py --dry-run  # Test first
python3 notion_sync.py             # Live sync
```

**Step 4: Verify Notion**
- Open Notion workspace
- Check databases have actual records
- Verify documents have content

## Cleanup Recommendations

### Immediate Actions

1. **Move Cloudflare scripts** to separate directory
2. **Archive old scripts** that are replaced
3. **Update documentation** references

### Optional Cleanup

```bash
# Create archive directory
mkdir -p notion/scripts/archived

# Move old scripts
mv notion/scripts/create_all_databases.py notion/scripts/archived/
mv notion/scripts/fix_titles_and_create_dbs.py notion/scripts/archived/
mv notion/scripts/check_and_seed_dbs.py notion/scripts/archived/
mv notion/scripts/seed_stakeholder_and_community.py notion/scripts/archived/
mv notion/scripts/report_db_counts.py notion/scripts/archived/

# Move Cloudflare scripts
mkdir -p cloudflare/scripts
mv notion/scripts/cf_*.py cloudflare/scripts/
```

## Testing

### Test Database System

```bash
# Test database creation
cd /path/to/enterprise
python3 update-dbs.py

# Verify statistics
python3 update-dbs.py --stats

# Validate schemas
python3 update-dbs.py --validate
```

### Test Notion Export

```bash
# Dry run (no actual changes)
cd notion/scripts
python3 notion_sync.py --dry-run

# Check what would be exported
cd ../../database/utils
python3 export_to_notion.py --dry-run
```

## Troubleshooting

### Database Not Updating

**Problem:** No data in databases after running update-dbs.sh

**Solution:**
```bash
# Check paths
ls -la enterprise/projects/
ls -la enterprise/stakeholders/
ls -la docs/

# Run with verbose output
python3 database/update_databases.py
```

### Notion API Errors

**Problem:** Notion API key errors

**Solution:**
```bash
# Check API key
echo $NOTION_API_KEY

# Test connection
cd notion/scripts
python3 notion_status.py
```

### Empty Databases in Notion

**Problem:** Notion databases created but empty

**Solution:**
1. First update local databases: `./update-dbs.sh`
2. Verify local data: `python3 update-dbs.py --stats`
3. Then sync to Notion: `cd notion/scripts && python3 notion_sync.py`

## Support

For issues:
1. Check this README
2. Check `/database/README.md`
3. Run with `--dry-run` to test
4. Contact DevOps team

---

**Last Updated:** 2026-02-09  
**Version:** 2.0.0 (Complete Redesign)
