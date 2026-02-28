# Notion Portal Build Script

## Overview

The Artifact Virtual Notion Portal system creates and maintains **two** Notion portal pages, each with inline databases populated from the local JSON data store.

| Portal | Icon | Databases | Data Source |
|--------|------|-----------|-------------|
| **Community Portal** | 🚀 | Projects, Project Tasks, Community Members, Feedback & Requests | `projects_db.json`, `public_db.json` |
| **Stakeholder Portal** | 👥 | Stakeholder Directory, Management, Operations, Documents, Roadmap | `public_db.json`, `internal_db.json`, `projects_db.json` |

## Architecture

```
notion/scripts/
├── av_notion_client.py      # Core Notion API wrapper (348 lines)
├── build_notion_portal.py   # Portal builder + database populator
├── notion_sync.py           # One-click pipeline (DB update → Notion sync)
├── notion_update.sh         # Shell entry point (bash)
├── notion_update.ps1        # Shell entry point (PowerShell)
└── _archive/                # Archived legacy scripts
```

### Data Flow

```
Repository Files  ──►  update_databases.py  ──►  JSON Databases  ──►  build_notion_portal.py  ──►  Notion API
  (markdown, etc)        (database/utils/)      (database/data/)       (notion/scripts/)         (2 pages + 9 DBs)
```

## Prerequisites

1. **Python 3.8+** with `notion-client`, `python-dotenv`, `requests`
2. **Notion Integration** — Create at https://www.notion.so/my-integrations
3. **Parent Page** — A Notion page where portals will be created (grant integration access)

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NOTION_API_KEY` | ✅ | Integration token (`secret_…` or `ntn_…`) |
| `NOTION_PARENT_PAGE_ID` | ✅ | UUID of the parent page |

Set them via export or a `.env` file at the repo root:

```bash
# .env
NOTION_API_KEY=secret_abc123...
NOTION_PARENT_PAGE_ID=12345678-abcd-1234-abcd-123456789abc
```

## Usage

### One-Click Sync (recommended)

```bash
# Full pipeline: update local DBs → build pages → populate Notion
./notion/scripts/notion_update.sh

# Or on Windows:
.\notion\scripts\notion_update.ps1
```

### Build Script (direct)

```bash
# Build both portals (creates pages + databases + populates)
python notion/scripts/build_notion_portal.py

# Dry run (no API calls)
python notion/scripts/build_notion_portal.py --dry-run

# Build only community portal
python notion/scripts/build_notion_portal.py --portal community

# Build only stakeholder portal
python notion/scripts/build_notion_portal.py --portal stakeholder

# Repopulate existing databases only (no page creation)
python notion/scripts/build_notion_portal.py --populate-only
```

### Sync Pipeline (direct)

```bash
# Full sync: update local DBs + build/populate Notion
python notion/scripts/notion_sync.py

# Skip local DB update (push current data to Notion)
python notion/scripts/notion_sync.py --skip-db-update

# Only repopulate existing Notion DBs
python notion/scripts/notion_sync.py --populate-only
```

## Build Behavior

The build script is **idempotent**:

1. **Searches** for existing pages/databases by exact title match
2. **Reuses** found resources (no duplicates)
3. **Creates** only what's missing
4. **Clears & repopulates** all database rows on every run
5. **Saves** `notion/portal-manifest.json` with page/DB IDs

## Database Schemas

### Community Portal

| Database | Key Properties | Row Count |
|----------|---------------|-----------|
| Projects | Name, Status, Category, Priority, Stage, Health Score, Progress, Open Source, Tech Stack, Tags, Description, GitHub URL | 21 |
| Project Tasks | Name, Status, Priority, Project | 17 |
| Community Members | Name, Type, Status, Description | 8 |
| Feedback & Requests | Name, Type, Status, Votes, Source | 0 (manual) |

### Stakeholder Portal

| Database | Key Properties | Row Count |
|----------|---------------|-----------|
| Stakeholder Directory | Name, Role, Tier, Status, Engagement Score, Influence, Description | 25 |
| Management | Name, Type, Urgency, Status, Business Impact, Approval, Description | 8 |
| Operations | Name, Type, Criticality, Status, SLA, Automation, Description | 8 |
| Documents | Name, Document Type, Status, Classification, File Path | 60 |
| Roadmap | Name, Quarter, Status, Priority, Category, Notes | 21 |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `NOTION_API_KEY not set` | Export the variable or add to `.env` |
| `Notion connection failed` | Verify API key, check integration is active |
| `Failed to create page` | Ensure integration has access to parent page |
| Rate limiting errors | Script has built-in throttling (3 req/sec) |
| Duplicate databases | Script searches before creating; delete stale ones manually |
