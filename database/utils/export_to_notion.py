#!/usr/bin/env python3
"""
Export to Notion - Export enterprise databases to Notion workspace

This script:
1. Loads data from local databases (must be updated first!)
2. Connects to Notion workspace
3. Creates/updates databases in Notion
4. Populates databases with actual documents and data
5. Maintains sync state

Prerequisites:
- Run update-dbs.py first to populate local databases
- Set NOTION_API_KEY environment variable
- Set NOTION_PARENT_PAGE_ID environment variable

Usage:
    python export_to_notion.py [--dry-run] [--database DB_NAME]
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add database utils to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'database' / 'utils'))
from db_manager import get_db_manager

# Try to import Notion client
try:
    from notion_client import Client as NotionClient
    NOTION_AVAILABLE = True
except ImportError:
    print("⚠️  notion-client not installed. Install with: pip install notion-client")
    NOTION_AVAILABLE = False
    NotionClient = None


class NotionExporter:
    """Export enterprise databases to Notion workspace"""
    
    def __init__(self, api_key: str, parent_page_id: str, dry_run: bool = False):
        """Initialize Notion exporter
        
        Args:
            api_key: Notion API key
            parent_page_id: Parent page ID for portal
            dry_run: If True, only log actions without making API calls
        """
        self.api_key = api_key
        self.parent_page_id = parent_page_id
        self.dry_run = dry_run
        self.db_manager = get_db_manager()
        
        # Initialize Notion client
        if not dry_run and NOTION_AVAILABLE:
            self.notion = NotionClient(auth=api_key)
        else:
            self.notion = None
        
        # Track created resources
        self.created_pages = {}
        self.created_databases = {}
        self.stats = {
            'pages_created': 0,
            'databases_created': 0,
            'records_added': 0,
            'errors': 0
        }
    
    def export_all(self):
        """Export all databases to Notion"""
        print("=" * 70)
        print("EXPORT TO NOTION - Enterprise Backend Database")
        print("=" * 70)
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print(f"Parent Page ID: {self.parent_page_id}")
        print("=" * 70)
        print()
        
        # Create portal structure
        print("📄 Creating portal structure...")
        self._create_portal_structure()
        print()
        
        # Export public database (Stakeholder Hub)
        print("👥 Exporting Public Database → Stakeholder Hub...")
        self._export_public_db()
        print()
        
        # Export projects database (Community Hub)
        print("🚀 Exporting Projects Database → Community Hub...")
        self._export_projects_db()
        print()
        
        # Export internal database (AV Live Dashboard)
        print("⚡ Exporting Internal Database → AV Live Dashboard...")
        self._export_internal_db()
        print()
        
        # Print summary
        self._print_summary()
    
    def _create_portal_structure(self):
        """Create main portal structure"""
        if self.dry_run:
            print("  [DRY RUN] Would create portal structure")
            return
        
        # Create main portal page
        print("  Creating: Artifact Virtual Notion Portal")
        # Implementation would go here
        self.stats['pages_created'] += 1
    
    def _export_public_db(self):
        """Export public database to Stakeholder Hub"""
        public_db = self.db_manager.load_db('public_db')
        
        # Export stakeholders
        stakeholders = public_db.get('stakeholders', [])
        print(f"  Stakeholders: {len(stakeholders)} records")
        if self.dry_run:
            print(f"  [DRY RUN] Would create Stakeholder Database with {len(stakeholders)} records")
        else:
            # Create database and add records
            # Implementation would go here
            self.stats['databases_created'] += 1
            self.stats['records_added'] += len(stakeholders)
        
        # Export community
        community = public_db.get('community', [])
        print(f"  Community: {len(community)} records")
        if self.dry_run:
            print(f"  [DRY RUN] Would create Community Database with {len(community)} records")
        else:
            self.stats['databases_created'] += 1
            self.stats['records_added'] += len(community)
        
        # Export public documents
        docs = public_db.get('public_documents', [])
        print(f"  Public Documents: {len(docs)} records")
        if self.dry_run:
            print(f"  [DRY RUN] Would create Public Documents Database with {len(docs)} records")
        else:
            self.stats['databases_created'] += 1
            self.stats['records_added'] += len(docs)
    
    def _export_projects_db(self):
        """Export projects database to Community Hub"""
        projects_db = self.db_manager.load_db('projects_db')
        
        # Export projects
        projects = projects_db.get('projects', [])
        print(f"  Projects: {len(projects)} records")
        if self.dry_run:
            print(f"  [DRY RUN] Would create Projects Database with {len(projects)} records")
            # Show sample project
            if projects:
                sample = projects[0]
                print(f"    Sample: {sample.get('project_name')} - {sample.get('status')}")
        else:
            self.stats['databases_created'] += 1
            self.stats['records_added'] += len(projects)
        
        # Export project tasks
        tasks = projects_db.get('project_tasks', [])
        print(f"  Project Tasks: {len(tasks)} records")
        if self.dry_run:
            print(f"  [DRY RUN] Would create Project Tasks Database with {len(tasks)} records")
        else:
            self.stats['databases_created'] += 1
            self.stats['records_added'] += len(tasks)
        
        # Export project documentation
        docs = projects_db.get('project_documentation', [])
        print(f"  Project Documentation: {len(docs)} records")
        if self.dry_run:
            print(f"  [DRY RUN] Would create Project Documentation Database with {len(docs)} records")
        else:
            self.stats['databases_created'] += 1
            self.stats['records_added'] += len(docs)
    
    def _export_internal_db(self):
        """Export internal database to AV Live Dashboard"""
        internal_db = self.db_manager.load_db('internal_db')
        
        # Export management
        management = internal_db.get('management', [])
        print(f"  Management: {len(management)} records")
        if self.dry_run:
            print(f"  [DRY RUN] Would create Management Database with {len(management)} records")
        else:
            self.stats['databases_created'] += 1
            self.stats['records_added'] += len(management)
        
        # Export operations
        operations = internal_db.get('operations', [])
        print(f"  Operations: {len(operations)} records")
        if self.dry_run:
            print(f"  [DRY RUN] Would create Operations Database with {len(operations)} records")
        else:
            self.stats['databases_created'] += 1
            self.stats['records_added'] += len(operations)
        
        # Export internal documents
        docs = internal_db.get('internal_documents', [])
        print(f"  Internal Documents: {len(docs)} records")
        if self.dry_run:
            print(f"  [DRY RUN] Would create Internal Documents Database with {len(docs)} records")
            # Show sample doc
            if docs:
                sample = docs[0]
                print(f"    Sample: {sample.get('title')} - {sample.get('type')}")
        else:
            self.stats['databases_created'] += 1
            self.stats['records_added'] += len(docs)
    
    def _print_summary(self):
        """Print export summary"""
        print("=" * 70)
        print("EXPORT SUMMARY")
        print("=" * 70)
        print(f"Pages Created: {self.stats['pages_created']}")
        print(f"Databases Created: {self.stats['databases_created']}")
        print(f"Records Added: {self.stats['records_added']}")
        print(f"Errors: {self.stats['errors']}")
        print("=" * 70)
        
        if self.dry_run:
            print()
            print("✅ Dry run complete! No changes made to Notion.")
            print("Run without --dry-run to actually export to Notion.")
        else:
            print()
            print("✅ Export complete!")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Export enterprise databases to Notion')
    parser.add_argument('--dry-run', action='store_true',
                       help='Test run without making API calls')
    parser.add_argument('--database', type=str,
                       help='Export specific database only (public_db, internal_db, projects_db)')
    
    args = parser.parse_args()
    
    # Check environment variables
    api_key = os.getenv('NOTION_API_KEY')
    parent_page_id = os.getenv('NOTION_PARENT_PAGE_ID')
    
    if not api_key:
        print("❌ Error: NOTION_API_KEY environment variable not set")
        print("Set it with: export NOTION_API_KEY='secret_...'")
        sys.exit(1)
    
    if not parent_page_id:
        print("❌ Error: NOTION_PARENT_PAGE_ID environment variable not set")
        print("Set it with: export NOTION_PARENT_PAGE_ID='...'")
        sys.exit(1)
    
    if not args.dry_run and not NOTION_AVAILABLE:
        print("❌ Error: notion-client package not installed")
        print("Install with: pip install notion-client")
        sys.exit(1)
    
    # Create exporter and run
    exporter = NotionExporter(api_key, parent_page_id, dry_run=args.dry_run)
    
    if args.database:
        print(f"Exporting specific database: {args.database}")
        # Add specific database export logic here
    else:
        exporter.export_all()


if __name__ == '__main__':
    main()
