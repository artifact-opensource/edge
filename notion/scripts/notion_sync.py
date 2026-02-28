#!/usr/bin/env python3
"""
Artifact Virtual — Notion Sync Pipeline
=========================================

One-click pipeline that:
  1. Updates local JSON databases from repository files
  2. Builds / refreshes Notion portal pages
  3. Populates all Notion databases from local data

This is the SINGLE entry point for keeping Notion in sync.

Usage:
    python notion_sync.py                     # full sync (update DBs + build portals)
    python notion_sync.py --skip-db-update    # skip local DB rebuild, just push to Notion
    python notion_sync.py --populate-only     # only repopulate existing Notion DBs
    python notion_sync.py --dry-run           # test run without API calls

Environment Variables (required):
    NOTION_API_KEY          — Notion integration token
    NOTION_PARENT_PAGE_ID   — Parent page ID for portals
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, timezone
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger("notion_sync")

REPO_ROOT   = Path(__file__).resolve().parent.parent.parent
DB_UPDATER  = REPO_ROOT / "database" / "update_databases.py"
SCRIPT_DIR  = Path(__file__).resolve().parent


def step_update_local_databases() -> bool:
    """Step 1: Run update_databases.py to refresh local JSON databases."""
    log.info("=" * 60)
    log.info("STEP 1: UPDATE LOCAL DATABASES")
    log.info("=" * 60)

    if not DB_UPDATER.exists():
        log.error(f"Database updater not found: {DB_UPDATER}")
        return False

    result = subprocess.run(
        [sys.executable, str(DB_UPDATER)],
        cwd=str(REPO_ROOT),
        capture_output=False,
        text=True,
    )

    if result.returncode != 0:
        log.error("Local database update failed!")
        return False

    log.info("✅ Local databases updated\n")
    return True


def step_build_notion_portals(dry_run: bool = False, populate_only: bool = False) -> bool:
    """Step 2: Run build_notion_portal.py to create/populate Notion portals."""
    log.info("=" * 60)
    log.info("STEP 2: BUILD / POPULATE NOTION PORTALS")
    log.info("=" * 60)

    # Check required env vars
    if not os.getenv("NOTION_API_KEY"):
        log.error("NOTION_API_KEY not set. Export it before running.")
        return False
    if not os.getenv("NOTION_PARENT_PAGE_ID"):
        log.error("NOTION_PARENT_PAGE_ID not set. Export it before running.")
        return False

    cmd = [sys.executable, str(SCRIPT_DIR / "build_notion_portal.py")]
    if dry_run:
        cmd.append("--dry-run")
    if populate_only:
        cmd.append("--populate-only")

    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=False, text=True)

    if result.returncode != 0:
        log.error("Notion portal build failed!")
        return False

    log.info("✅ Notion portals synced\n")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Artifact Virtual — Notion Sync Pipeline"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Test run without making API calls to Notion")
    parser.add_argument("--skip-db-update", action="store_true",
                        help="Skip local database rebuild (use current JSON data)")
    parser.add_argument("--populate-only", action="store_true",
                        help="Only repopulate existing Notion databases (no page creation)")

    args = parser.parse_args()

    log.info("=" * 60)
    log.info("ARTIFACT VIRTUAL — NOTION SYNC PIPELINE")
    log.info(f"  Time: {datetime.now(timezone.utc).isoformat()}")
    log.info(f"  Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    log.info("=" * 60 + "\n")

    # Step 1: Update local databases
    if args.skip_db_update:
        log.info("⏭️  Skipping local database update (--skip-db-update)\n")
    else:
        if not step_update_local_databases():
            log.error("Pipeline aborted at Step 1")
            return 1

    # Step 2: Build/populate Notion portals
    if not step_build_notion_portals(
        dry_run=args.dry_run,
        populate_only=args.populate_only
    ):
        log.error("Pipeline aborted at Step 2")
        return 1

    log.info("=" * 60)
    log.info("✅ NOTION SYNC PIPELINE COMPLETE")
    log.info("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
