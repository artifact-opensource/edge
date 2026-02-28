#!/usr/bin/env python3
"""
Update Databases - Main script to update all enterprise databases

This is the core update script that:
1. Syncs data from repository files
2. Validates all data
3. Syncs to SQLite + FTS5 (the real RAG engine)
4. Regenerates knowledge graph
5. Generates statistics

Usage:
    python update_databases.py [--sync-only] [--validate-only] [--stats]
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent / 'utils'))

from db_manager import get_db_manager
from sync_from_repo import RepositorySync


def validate_databases():
    """Validate all databases against schemas"""
    print("=" * 70)
    print("VALIDATING DATABASES")
    print("=" * 70)
    print()
    
    db_manager = get_db_manager()
    validation_errors = []
    
    # Validate public_db
    print("✓ Validating public_db...")
    try:
        db = db_manager.load_db('public_db')
        schema = db_manager.load_schema('public_schema')
        
        for db_type in ['stakeholders', 'community', 'public_documents']:
            if db_type in db:
                for record in db[db_type]:
                    is_valid, errors = db_manager.validate_record(record, schema, db_type)
                    if not is_valid:
                        validation_errors.extend([f"public_db.{db_type}: {e}" for e in errors])
        
        print(f"  ✓ public_db validated")
    except Exception as e:
        print(f"  ✗ Error validating public_db: {e}")
        validation_errors.append(f"public_db: {e}")
    
    # Validate internal_db
    print("✓ Validating internal_db...")
    try:
        db = db_manager.load_db('internal_db')
        schema = db_manager.load_schema('internal_schema')
        
        for db_type in ['management', 'operations', 'internal_documents']:
            if db_type in db:
                for record in db[db_type]:
                    is_valid, errors = db_manager.validate_record(record, schema, db_type)
                    if not is_valid:
                        validation_errors.extend([f"internal_db.{db_type}: {e}" for e in errors])
        
        print(f"  ✓ internal_db validated")
    except Exception as e:
        print(f"  ✗ Error validating internal_db: {e}")
        validation_errors.append(f"internal_db: {e}")
    
    # Validate projects_db
    print("✓ Validating projects_db...")
    try:
        db = db_manager.load_db('projects_db')
        schema = db_manager.load_schema('projects_schema')
        
        for db_type in ['projects', 'project_tasks', 'project_documentation']:
            if db_type in db:
                for record in db[db_type]:
                    is_valid, errors = db_manager.validate_record(record, schema, db_type)
                    if not is_valid:
                        validation_errors.extend([f"projects_db.{db_type}: {e}" for e in errors])
        
        print(f"  ✓ projects_db validated")
    except Exception as e:
        print(f"  ✗ Error validating projects_db: {e}")
        validation_errors.append(f"projects_db: {e}")
    
    print()
    if validation_errors:
        print(f"⚠️  Found {len(validation_errors)} validation errors:")
        for error in validation_errors[:10]:  # Show first 10
            print(f"  - {error}")
        if len(validation_errors) > 10:
            print(f"  ... and {len(validation_errors) - 10} more")
    else:
        print("✅ All databases validated successfully!")
    
    print("=" * 70)
    print()
    
    return len(validation_errors) == 0


def show_statistics():
    """Show database statistics"""
    print("=" * 70)
    print("DATABASE STATISTICS")
    print("=" * 70)
    print()
    
    db_manager = get_db_manager()
    
    # Public DB stats
    public_stats = db_manager.get_stats('public_db')
    print("📊 Public Database (public_db)")
    print(f"  Version: {public_stats['version']}")
    print(f"  Last Updated: {public_stats['last_updated']}")
    for table, info in public_stats['tables'].items():
        print(f"  - {table}: {info['count']} records")
    print()
    
    # Internal DB stats
    internal_stats = db_manager.get_stats('internal_db')
    print("🔒 Internal Database (internal_db)")
    print(f"  Version: {internal_stats['version']}")
    print(f"  Last Updated: {internal_stats['last_updated']}")
    for table, info in internal_stats['tables'].items():
        print(f"  - {table}: {info['count']} records")
    print()
    
    # Projects DB stats
    projects_stats = db_manager.get_stats('projects_db')
    print("🚀 Projects Database (projects_db)")
    print(f"  Version: {projects_stats['version']}")
    print(f"  Last Updated: {projects_stats['last_updated']}")
    for table, info in projects_stats['tables'].items():
        print(f"  - {table}: {info['count']} records")
    print()
    
    # SQLite DB stats
    try:
        from enterprise_db import get_db
        db = get_db()
        doc_stats = db.get_document_stats()
        grc = db.get_grc_summary()
        print("🔍 SQLite + FTS5 Database (enterprise.db)")
        print(f"  Documents: {doc_stats['total']}")
        print(f"  GRC Controls: {grc['total']} ({grc['readiness_percent']}% compliant)")
        print(f"  Projects: {db.count('projects')}")
        print(f"  Stakeholders: {db.count('stakeholders')}")
    except Exception as e:
        print(f"  ⚠️  Could not read SQLite stats: {e}")
    print()
    
    print("=" * 70)


def sync_to_sqlite(repo_root: Path):
    """Re-run SQLite migration from JSON databases to keep enterprise.db current."""
    try:
        migrate_script = Path(__file__).parent / 'migrate_to_sqlite.py'
        if not migrate_script.exists():
            print("  ⚠️  migrate_to_sqlite.py not found, skipping SQLite sync")
            return

        import subprocess
        proc = subprocess.run(
            [sys.executable, str(migrate_script)],
            capture_output=True, text=True, timeout=60,
            cwd=str(repo_root),
        )
        if proc.returncode == 0:
            print("  ✓ SQLite + FTS5 database synced")
            # Print key lines from output
            for line in proc.stdout.strip().splitlines():
                if '✓' in line or 'records' in line.lower() or 'total' in line.lower():
                    print(f"    {line.strip()}")
        else:
            print(f"  ⚠️  SQLite sync returned code {proc.returncode}")
            for line in proc.stderr.strip().splitlines()[-3:]:
                print(f"    {line}")
    except Exception as e:
        print(f"  ⚠️  SQLite sync error: {e}")
    print()


def regenerate_knowledge_graph():
    """Regenerate the knowledge graph from SQLite database."""
    try:
        kg_script = Path(__file__).parent / 'generate_knowledge_graph.py'
        if not kg_script.exists():
            print("  ⚠️  generate_knowledge_graph.py not found, skipping")
            return

        import subprocess
        proc = subprocess.run(
            [sys.executable, str(kg_script)],
            capture_output=True, text=True, timeout=60,
            cwd=str(Path(__file__).parent),
        )
        if proc.returncode == 0:
            print("  ✓ Knowledge graph regenerated")
            for line in proc.stdout.strip().splitlines():
                if 'nodes' in line.lower() or 'links' in line.lower() or 'saved' in line.lower():
                    print(f"    {line.strip()}")
        else:
            print(f"  ⚠️  Knowledge graph generation returned code {proc.returncode}")
            for line in proc.stderr.strip().splitlines()[-3:]:
                print(f"    {line}")
    except Exception as e:
        print(f"  ⚠️  Knowledge graph error: {e}")
    print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Update enterprise databases')
    parser.add_argument('--sync-only', action='store_true', 
                       help='Only sync JSON databases from repository files (skip SQLite migration, knowledge graph, and statistics)')
    parser.add_argument('--validate-only', action='store_true',
                       help='Only validate databases')
    parser.add_argument('--stats', action='store_true',
                       help='Show database statistics')
    
    args = parser.parse_args()
    
    print()
    print("🔄 ENTERPRISE DATABASE UPDATE")
    print()
    
    if args.stats:
        show_statistics()
        return
    
    if args.validate_only:
        validate_databases()
        return
    
    # Get repository root
    script_path = Path(__file__).resolve()
    # database/update_databases.py -> database -> repo_root
    repo_root = script_path.parent.parent
    
    # Sync from repository
    print("Step 1: Syncing from repository...")
    print()
    sync = RepositorySync(repo_root)
    sync.sync_all()
    print()
    
    if args.sync_only:
        print("\n\u2705 Sync-only complete (skipped SQLite migration, knowledge graph, and statistics)")
        print()
        return

    # Validate
    print("Step 2: Validating databases...")
        print()
        validate_databases()
    
    # Sync to SQLite + FTS5 (the real search engine)
    print("Step 3: Syncing to SQLite + FTS5...")
    print()
    sync_to_sqlite(repo_root)
    
    # Regenerate knowledge graph
    print("Step 4: Regenerating knowledge graph...")
    print()
    regenerate_knowledge_graph()
    
    # Show final statistics
    print("Step 5: Database Statistics")
    print()
    show_statistics()
    
    print()
    print("✅ Database update complete!")
    print()


if __name__ == '__main__':
    main()
