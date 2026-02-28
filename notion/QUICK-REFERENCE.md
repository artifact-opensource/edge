# Notion Portal — Quick Reference

## Portal Structure

```
Parent Page (NOTION_PARENT_PAGE_ID)
├── 🚀 Community Portal
│   ├── Projects (21 rows)
│   ├── Project Tasks (17 rows)
│   ├── Community Members (8 rows)
│   └── Feedback & Requests (manual)
│
└── 👥 Stakeholder Portal
    ├── Stakeholder Directory (25 rows)
    ├── Management (8 rows)
    ├── Operations (8 rows)
    ├── Documents (60 rows)
    └── Roadmap (21 rows)
```

**Total: 2 pages, 9 databases, ~168 rows**

## One-Click Update

```bash
./notion/scripts/notion_update.sh
```

This runs: `update_databases.py` → `build_notion_portal.py`

## Quick Commands

| Command | What it does |
|---------|-------------|
| `./notion/scripts/notion_update.sh` | Full pipeline (recommended) |
| `python notion/scripts/build_notion_portal.py --dry-run` | Preview without API calls |
| `python notion/scripts/build_notion_portal.py --populate-only` | Refresh data only |
| `python notion/scripts/notion_sync.py --skip-db-update` | Push current JSON → Notion |

## Required Environment

```bash
export NOTION_API_KEY="secret_…"
export NOTION_PARENT_PAGE_ID="…"
```

## Files

| File | Purpose | Lines |
|------|---------|-------|
| `av_notion_client.py` | Core Notion API wrapper | ~350 |
| `build_notion_portal.py` | Portal builder + populator | ~480 |
| `notion_sync.py` | Pipeline orchestrator | ~110 |
| `notion_update.sh` | Bash entry point | ~40 |
| `notion_update.ps1` | PowerShell entry point | ~40 |

## Status Codes

| Color | Status |
|-------|--------|
| 🟢 | Active / Operational |
| 🟡 | Planning / Pending |
| 🔵 | Complete |
| 🔴 | Blocked / Critical |
| ⚪ | Concept / Inactive |

## Manifest

After each build, `notion/portal-manifest.json` is saved with:
- Page IDs and URLs
- Database IDs and URLs
- Row counts per database
- Build timestamp

Use this to track what exists in Notion without re-searching.
