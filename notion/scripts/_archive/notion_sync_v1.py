#!/usr/bin/env python3
"""
Notion Sync - Complete sync from repository → databases → Notion

This script performs the complete sync workflow:
1. Update local databases from repository files
2. Export databases to Notion workspace
3. Update sync logs

This is the main script to keep Notion workspace up to date.

Usage:
    python notion_sync.py [--dry-run] [--skip-db-update]
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add database directory to path
db_path = Path(__file__).parent.parent.parent / 'database'
sys.path.insert(0, str(db_path))
sys.path.insert(0, str(db_path / 'utils'))

from update_databases import main as update_databases

# export_to_notion lives in database/utils/
try:
    from export_to_notion import NotionExporter
except ImportError:
    NotionExporter = None


def notion_sync(dry_run: bool = False, skip_db_update: bool = False):
    """Perform complete notion sync
    
    Args:
        dry_run: If True, don't make actual changes
        skip_db_update: If True, skip database update and only export
    """
    print()
    print("=" * 70)
    print("NOTION SYNC - Complete Workflow")
    print("=" * 70)
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"Timestamp: {datetime.utcnow().isoformat()}Z")
    print("=" * 70)
    print()
    
    # Step 1: Update local databases (unless skipped)
    if skip_db_update:
        print("⏭️  Skipping database update (--skip-db-update)")
        print()
    else:
        print("STEP 1: UPDATE LOCAL DATABASES")
        print("=" * 70)
        print()
        
        # Import and run update_databases
        # We'll use subprocess to call it cleanly
        import subprocess
        result = subprocess.run(
            [sys.executable, str(db_path / 'update_databases.py')],
            capture_output=False,
            text=True
        )
        
        if result.returncode != 0:
            print()
            print("❌ Database update failed!")
            return False
        
        print()
        print("✅ Database update complete!")
        print()
    
    # Step 2: Export to Notion
    print("STEP 2: EXPORT TO NOTION")
    print("=" * 70)
    print()
    
    # Check environment variables
    api_key = os.getenv('NOTION_API_KEY')
    parent_page_id = os.getenv('NOTION_PARENT_PAGE_ID')
    
    if not api_key:
        print("❌ Error: NOTION_API_KEY environment variable not set")
        print("Set it with: export NOTION_API_KEY='secret_...'")
        return False
    
    if not parent_page_id:
        print("❌ Error: NOTION_PARENT_PAGE_ID environment variable not set")
        print("Set it with: export NOTION_PARENT_PAGE_ID='...'")
        return False
    
    if NotionExporter is None:
        print("⚠️  NotionExporter not available. Falling back to build_notion_portal...")
        try:
            from build_notion_portal import NotionPortalBuilder
            builder = NotionPortalBuilder(dry_run=dry_run)
            builder.build_portal()
        except Exception as e:
            print(f"❌ Portal build failed: {e}")
            return False
    else:
        # Create exporter and run
        exporter = NotionExporter(api_key, parent_page_id, dry_run=dry_run)
        exporter.export_all()
    
    print()
    print("=" * 70)
    print("✅ NOTION SYNC COMPLETE")
    print("=" * 70)
    print()
    
    if dry_run:
        print("This was a dry run. Run without --dry-run to actually sync.")
        print()
    
    return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Complete notion sync workflow')
    parser.add_argument('--dry-run', action='store_true',
                       help='Test run without making changes')
    parser.add_argument('--skip-db-update', action='store_true',
                       help='Skip database update, only export to Notion')
    
    args = parser.parse_args()
    
    success = notion_sync(dry_run=args.dry_run, skip_db_update=args.skip_db_update)
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
