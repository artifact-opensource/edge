#!/usr/bin/env python3
"""
Artifact Virtual Notion Portal Builder

This script builds the complete Notion portal structure including:
- Stakeholder Hub with all nested databases
- Community Hub with project management
- AV Live Dashboard with real-time monitoring

Configuration is managed via environment variables for security and flexibility.

Usage:
    python build_notion_portal.py [--dry-run] [--space SPACE]

Environment Variables:
    NOTION_API_KEY          - Notion integration API key (required)
    NOTION_PARENT_PAGE_ID   - Parent page ID where portal will be created (required)
    GITHUB_TOKEN            - GitHub API token for integration (optional)
    SLACK_WEBHOOK_URL       - Slack webhook for notifications (optional)
    DISCORD_WEBHOOK_URL     - Discord webhook for notifications (optional)
    EMAIL_SMTP_HOST         - SMTP host for email integration (optional)
    EMAIL_SMTP_PORT         - SMTP port (optional)
    EMAIL_USERNAME          - Email username (optional)
    EMAIL_PASSWORD          - Email password (optional)
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Notion integration helper (use wrapper to avoid name collisions)
try:
    from av_notion_client import NotionIntegration
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from av_notion_client import NotionIntegration

class NotionPortalBuilder:
    """Main builder class for Notion portal construction."""
    
    def __init__(self, dry_run: bool = False):
        """
        Initialize the portal builder.
        
        Args:
            dry_run: If True, only log actions without making API calls
        """
        self.dry_run = dry_run
        self.notion_api_key = os.getenv('NOTION_API_KEY')
        self.parent_page_id = os.getenv('NOTION_PARENT_PAGE_ID')
        self.github_token = os.getenv('GITHUB_TOKEN')
        
        # Notion client (initialized for live runs)
        self.notion = None
        if not self.dry_run:
            self._validate_config()
            # initialize Notion client
            try:
                self.notion = NotionIntegration(self.notion_api_key)
                logger.info("✓ Notion client initialized")
            except Exception as e:
                logger.error(f"✗ Failed to initialize Notion client: {e}")
                raise
        
        # Track created resources
        self.created_pages = {}
        self.created_databases = {}
    
    def _validate_config(self):
        """Validate required configuration."""
        if not self.notion_api_key:
            raise ValueError("NOTION_API_KEY environment variable is required")
        if not self.parent_page_id:
            raise ValueError("NOTION_PARENT_PAGE_ID environment variable is required")
        
        logger.info("✓ Configuration validated")
    
    def build_portal(self, space: Optional[str] = None):
        """
        Build the complete Notion portal or specific space.
        
        Args:
            space: Specific space to build ('stakeholder', 'community', 'avlive', or None for all)
        """
        logger.info("=" * 70)
        logger.info("Artifact Virtual Notion Portal Builder")
        logger.info("=" * 70)
        logger.info(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        logger.info(f"Building: {space if space else 'All Spaces'}")
        logger.info("=" * 70)
        
        try:
            # Build main portal structure
            if not space or space == 'root':
                self._build_root_structure()
            
            # Build Stakeholder Hub
            if not space or space == 'stakeholder':
                self._build_stakeholder_hub()
            
            # Build Community Hub
            if not space or space == 'community':
                self._build_community_hub()
            
            # Build AV Live Dashboard
            if not space or space == 'avlive':
                self._build_avlive_dashboard()
            
            # Summary
            self._print_summary()
            
            logger.info("=" * 70)
            logger.info("✓ Portal build complete!")
            logger.info("=" * 70)
            
        except Exception as e:
            logger.error(f"✗ Build failed: {str(e)}")
            raise
    
    def _build_root_structure(self):
        """Build the root portal structure."""
        logger.info("\n" + "=" * 70)
        logger.info("Building Root Portal Structure")
        logger.info("=" * 70)
        
        # Create main portal page
        portal_page = self._create_page(
            title="Artifact Virtual Notion Portal",
            parent_id=self.parent_page_id,
            icon="🏢",
            description="Complete stakeholder and community portal system"
        )
        self.created_pages['portal_root'] = portal_page
        
        # Create overview sections
        self._add_overview_content(portal_page)
        
        logger.info("✓ Root structure created")
    
    def _build_stakeholder_hub(self):
        """Build the Stakeholder Hub with all databases."""
        logger.info("\n" + "=" * 70)
        logger.info("Building Stakeholder Hub")
        logger.info("=" * 70)
        
        # Create Stakeholder Hub page
        hub_page = self._create_page(
            title="Stakeholder Hub",
            parent_id=self.created_pages.get('portal_root', self.parent_page_id),
            icon="👥",
            description="Complete stakeholder management and analytics"
        )
        self.created_pages['stakeholder_hub'] = hub_page
        
        # Create dashboard
        self._create_stakeholder_dashboard(hub_page)
        
        # Create databases
        databases = [
            ('master_stakeholder', 'Master Stakeholder Database', self._get_stakeholder_schema()),
            ('investors', 'Investor Database', self._get_investor_schema()),
            ('partners', 'Partner Database', self._get_partner_schema()),
            ('advisors', 'Advisor Database', self._get_advisor_schema()),
            ('board_members', 'Board Members Database', self._get_board_schema()),
            ('key_customers', 'Key Customers Database', self._get_customer_schema()),
            ('analytics_reports', 'Analytics & Reports Database', self._get_analytics_schema()),
            ('communications', 'Communications Log Database', self._get_communications_schema()),
            ('documents', 'Documents & Agreements Database', self._get_documents_schema()),
        ]
        
        for db_key, db_title, db_schema in databases:
            db = self._create_database(
                title=db_title,
                parent_id=hub_page,
                schema=db_schema
            )
            self.created_databases[f'stakeholder_{db_key}'] = db
            logger.info(f"  ✓ Created: {db_title}")
        
        logger.info("✓ Stakeholder Hub complete")
    
    def _build_community_hub(self):
        """Build the Community Hub with all databases."""
        logger.info("\n" + "=" * 70)
        logger.info("Building Community Hub")
        logger.info("=" * 70)
        
        # Create Community Hub page
        hub_page = self._create_page(
            title="Community Hub",
            parent_id=self.created_pages.get('portal_root', self.parent_page_id),
            icon="🚀",
            description="Project portfolio and community engagement"
        )
        self.created_pages['community_hub'] = hub_page
        
        # Create dashboard
        self._create_community_dashboard(hub_page)
        
        # Create databases
        databases = [
            ('master_projects', 'Master Projects Database', self._get_projects_schema()),
            ('open_source', 'Open Source Portfolio Database', self._get_opensource_schema()),
            ('community_engagement', 'Community Engagement Database', self._get_community_schema()),
            ('project_management', 'Project Management Database', self._get_tasks_schema()),
            ('roadmap', 'Roadmap Database', self._get_roadmap_schema()),
            ('sprints', 'Sprints Database', self._get_sprints_schema()),
            ('events', 'Events & Calendar Database', self._get_events_schema()),
            ('feedback', 'Feedback & Feature Requests Database', self._get_feedback_schema()),
        ]
        
        for db_key, db_title, db_schema in databases:
            db = self._create_database(
                title=db_title,
                parent_id=hub_page,
                schema=db_schema
            )
            self.created_databases[f'community_{db_key}'] = db
            logger.info(f"  ✓ Created: {db_title}")
        
        logger.info("✓ Community Hub complete")
    
    def _build_avlive_dashboard(self):
        """Build the AV Live Dashboard."""
        logger.info("\n" + "=" * 70)
        logger.info("Building AV Live Dashboard")
        logger.info("=" * 70)
        
        # Create AV Live page
        live_page = self._create_page(
            title="AV Live Dashboard",
            parent_id=self.created_pages.get('portal_root', self.parent_page_id),
            icon="⚡",
            description="Real-time updates and system monitoring"
        )
        self.created_pages['avlive'] = live_page
        
        # Create live dashboard content
        self._create_live_dashboard(live_page)
        
        # Create databases
        databases = [
            ('live_updates', 'Live Updates Database', self._get_live_updates_schema()),
            ('alerts', 'Alerts & Notifications Database', self._get_alerts_schema()),
            ('manual_updates', 'Manual Updates Database', self._get_manual_updates_schema()),
            ('system_status', 'System Status Database', self._get_system_status_schema()),
        ]
        
        for db_key, db_title, db_schema in databases:
            db = self._create_database(
                title=db_title,
                parent_id=live_page,
                schema=db_schema
            )
            self.created_databases[f'avlive_{db_key}'] = db
            logger.info(f"  ✓ Created: {db_title}")
        
        logger.info("✓ AV Live Dashboard complete")
    
    def _create_page(self, title: str, parent_id: str, icon: str, description: str) -> Dict:
        """Create a Notion page."""
        if self.dry_run:
            logger.info(f"[DRY RUN] Would create page: {title}")
            return {'id': f'dry-run-page-{len(self.created_pages)}'}
        
        # Use Notion integration to create or reuse a page
        logger.info(f"Creating page: {title}")
        if not self.notion:
            raise RuntimeError("Notion client is not initialized")

        # Check for existing page with same title
        existing = self.notion.search(title, filter_type='page')
        for item in existing:
            if item.get('title') == title:
                logger.info(f"  ↺ Reusing existing page: {title} (id={item.get('id')})")
                return {'id': item.get('id'), 'url': item.get('url')}

        parent = parent_id if isinstance(parent_id, str) else (parent_id.get('page_id') or parent_id.get('id') if isinstance(parent_id, dict) else parent_id)
        result = self.notion.create_page_in_parent(parent_id=parent, title=title, icon=icon, description=description)
        if result.get('status') == 'success':
            return {'id': result.get('page_id'), 'url': result.get('url')}
        else:
            raise RuntimeError(f"Failed to create page {title}: {result.get('error')}")
    
    def _create_database(self, title: str, parent_id: str, schema: Dict) -> Dict:
        """Create a Notion database."""
        if self.dry_run:
            logger.info(f"[DRY RUN] Would create database: {title}")
            return {'id': f'dry-run-db-{len(self.created_databases)}'}
        
        # Use Notion integration to create or reuse a database
        logger.info(f"Creating database: {title}")
        if not self.notion:
            raise RuntimeError("Notion client is not initialized")

        # Check for existing database with same title
        existing = self.notion.search(title, filter_type='database')
        for item in existing:
            if item.get('title') == title:
                logger.info(f"  ↺ Reusing existing database: {title} (id={item.get('id')})")
                return {'id': item.get('id'), 'url': item.get('url')}

        parent = parent_id if isinstance(parent_id, str) else (parent_id.get('page_id') or parent_id.get('id') if isinstance(parent_id, dict) else parent_id)
        result = self.notion.create_database_from_schema(parent_page_id=parent, title=title, schema=schema)
        if result.get('status') == 'success':
            return {'id': result.get('database_id'), 'url': result.get('url')}
        else:
            raise RuntimeError(f"Failed to create database {title}: {result.get('error')}")
    
    def _add_overview_content(self, page_id: str):
        """Add overview content to portal root."""
        logger.info("  Adding overview content...")
        # Implementation would add rich content blocks
    
    def _create_stakeholder_dashboard(self, page_id: str):
        """Create stakeholder dashboard visualizations."""
        logger.info("  Creating stakeholder dashboard...")
        # Implementation would add dashboard widgets
    
    def _create_community_dashboard(self, page_id: str):
        """Create community dashboard visualizations."""
        logger.info("  Creating community dashboard...")
        # Implementation would add dashboard widgets
    
    def _create_live_dashboard(self, page_id: str):
        """Create live dashboard visualizations."""
        logger.info("  Creating live dashboard...")
        # Implementation would add dashboard widgets and live feeds
    
    # Database schema methods
    def _get_stakeholder_schema(self) -> Dict:
        """Get Master Stakeholder Database schema."""
        return {
            'Name': {'type': 'title'},
            'Category': {'type': 'select', 'options': ['Investor', 'Partner', 'Advisor', 'Board Member', 'Customer', 'Other']},
            'Tier': {'type': 'select', 'options': ['Executive', 'Strategic', 'Standard', 'Limited']},
            'Status': {'type': 'select', 'options': ['Active', 'Inactive', 'Prospect', 'Former']},
            'Region': {'type': 'select', 'options': ['Pakistan', 'US', 'EU', 'MENA', 'Asia Pacific', 'Other']},
            'Engagement Score': {'type': 'number', 'format': 'number'},
            'Total Value': {'type': 'number', 'format': 'dollar'},
            'First Contact': {'type': 'date'},
            'Last Contact': {'type': 'date'},
            'Next Action': {'type': 'date'},
            'Email': {'type': 'email'},
            'Phone': {'type': 'phone_number'},
            'Company': {'type': 'rich_text'},
            'LinkedIn': {'type': 'url'},
            'Tags': {'type': 'multi_select', 'options': ['Strategic', 'VIP', 'Potential']},
            'Notes': {'type': 'rich_text'},
            'Risk Level': {'type': 'select', 'options': ['Low', 'Medium', 'High', 'Critical']},
        }
    
    def _get_investor_schema(self) -> Dict:
        """Get Investor Database schema."""
        return {
            'Investor Name': {'type': 'title'},
            'Investment Stage': {'type': 'select', 'options': ['Seed', 'Series A', 'Series B', 'Growth', 'Strategic']},
            'Investment Amount': {'type': 'number', 'format': 'dollar'},
            'Investment Date': {'type': 'date'},
            'Ownership Percentage': {'type': 'number', 'format': 'percent'},
            'Board Seat': {'type': 'checkbox'},
            'Investor Type': {'type': 'select', 'options': ['Angel', 'VC', 'Corporate', 'Strategic', 'Family Office', 'Other']},
            'Lead Investor': {'type': 'checkbox'},
            'Expected Returns': {'type': 'number', 'format': 'percent'},
            'Due Diligence Status': {'type': 'select', 'options': ['Not Started', 'In Progress', 'Complete']},
            'Satisfaction Score': {'type': 'number'},
        }
    
    def _get_partner_schema(self) -> Dict:
        """Get Partner Database schema."""
        return {
            'Partner Name': {'type': 'title'},
            'Partnership Type': {'type': 'select', 'options': ['Technology', 'Channel', 'Strategic', 'Referral', 'Integration']},
            'Partnership Status': {'type': 'select', 'options': ['Prospect', 'Negotiation', 'Active', 'On Hold', 'Terminated']},
            'Start Date': {'type': 'date'},
            'End Date': {'type': 'date'},
            'Partnership Value': {'type': 'number', 'format': 'dollar'},
            'Revenue Generated': {'type': 'number', 'format': 'dollar'},
            'Performance Score': {'type': 'number'},
        }
    
    def _get_advisor_schema(self) -> Dict:
        """Get Advisor Database schema."""
        return {
            'Advisor Name': {'type': 'title'},
            'Expertise Area': {'type': 'multi_select', 'options': ['General']},
            'Advisor Type': {'type': 'select', 'options': ['Board Advisor', 'Strategic Advisor', 'Technical Advisor', 'Domain Expert', 'Mentor']},
            'Status': {'type': 'select', 'options': ['Active', 'Inactive', 'Prospective']},
            'Start Date': {'type': 'date'},
            'Satisfaction Score': {'type': 'number'},
        }
    
    def _get_board_schema(self) -> Dict:
        """Get Board Members Database schema."""
        return {
            'Member Name': {'type': 'title'},
            'Position': {'type': 'select', 'options': ['Chairman', 'CEO', 'Executive Director', 'Independent Director', 'Observer']},
            'Status': {'type': 'select', 'options': ['Active', 'Resigned', 'Retired']},
            'Appointment Date': {'type': 'date'},
            'Term End Date': {'type': 'date'},
            'Attendance Rate': {'type': 'number', 'format': 'percent'},
        }
    
    def _get_customer_schema(self) -> Dict:
        """Get Key Customers Database schema."""
        return {
            'Customer Name': {'type': 'title'},
            'Company': {'type': 'rich_text'},
            'Industry': {'type': 'select', 'options': ['SaaS', 'Healthcare', 'Finance', 'Education', 'Other']},
            'Status': {'type': 'select', 'options': ['Prospect', 'Trial', 'Active', 'At Risk', 'Churned']},
            'Contract Value': {'type': 'number', 'format': 'dollar'},
            'MRR': {'type': 'number', 'format': 'dollar'},
            'Health Score': {'type': 'number'},
            'NPS Score': {'type': 'number'},
        }
    
    def _get_analytics_schema(self) -> Dict:
        """Get Analytics & Reports Database schema."""
        return {
            'Report Name': {'type': 'title'},
            'Report Type': {'type': 'select', 'options': ['Operational', 'Financial', 'KPI', 'Ad-hoc']},
            'Period': {'type': 'select', 'options': ['Q1', 'Q2', 'Q3', 'Q4', 'FY']},
            'Created Date': {'type': 'date'},
            'Status': {'type': 'select', 'options': ['Draft', 'Review', 'Approved', 'Distributed']},
        }
    
    def _get_communications_schema(self) -> Dict:
        """Get Communications Log Database schema."""
        return {
            'Communication Title': {'type': 'title'},
            'Date': {'type': 'date'},
            'Type': {'type': 'select', 'options': ['Email', 'Call', 'Meeting', 'Presentation', 'Report', 'Newsletter', 'Ad-hoc']},
            'Status': {'type': 'select', 'options': ['Scheduled', 'Completed', 'Cancelled', 'Rescheduled']},
        }
    
    def _get_documents_schema(self) -> Dict:
        """Get Documents & Agreements Database schema."""
        return {
            'Document Name': {'type': 'title'},
            'Document Type': {'type': 'select', 'options': ['Contract', 'Agreement', 'Policy', 'Memo', 'Other']},
            'Status': {'type': 'select', 'options': ['Draft', 'Under Review', 'Approved', 'Executed', 'Expired']},
            'Created Date': {'type': 'date'},
        }
    
    def _get_projects_schema(self) -> Dict:
        """Get Master Projects Database schema."""
        return {
            'Project Name': {'type': 'title'},
            'Category': {'type': 'select', 'options': ['Product', 'Platform', 'Research', 'Operations', 'Other']},
            'Status': {'type': 'select', 'options': ['🟢 Active', '🟡 Planning', '🔵 Complete', '🔴 Blocked', '⚪ Concept']},
            'Priority': {'type': 'select', 'options': ['P0 Critical', 'High', 'Medium', 'Low']},
            'Health Score': {'type': 'number'},
            'Progress': {'type': 'number', 'format': 'percent'},
        }
    
    def _get_opensource_schema(self) -> Dict:
        """Get Open Source Portfolio Database schema."""
        return {
            'Repository Name': {'type': 'title'},
            'GitHub URL': {'type': 'url'},
            'License': {'type': 'select', 'options': ['MIT', 'Apache-2.0', 'GPL-3.0', 'BSD-3-Clause', 'Other']},
            'Stars': {'type': 'number'},
            'Contributors': {'type': 'number'},
        }
    
    def _get_community_schema(self) -> Dict:
        """Get Community Engagement Database schema."""
        return {
            'Member Name': {'type': 'title'},
            'Username': {'type': 'rich_text'},
            'Member Type': {'type': 'select', 'options': ['Member', 'Contributor', 'Maintainer', 'Moderator']},
            'Status': {'type': 'select', 'options': ['Active', 'Inactive', 'Alumni', 'Banned']},
            'Community Score': {'type': 'number'},
        }
    
    def _get_tasks_schema(self) -> Dict:
        """Get Project Management Database schema."""
        return {
            'Task Name': {'type': 'title'},
            'Status': {'type': 'select', 'options': ['📋 Todo', '🔄 In Progress', '👀 Review', '✅ Done', '🚫 Blocked']},
            'Priority': {'type': 'select', 'options': ['🔴 Critical', '🟠 High', '🟡 Medium', '🟢 Low']},
            'Due Date': {'type': 'date'},
        }
    
    def _get_roadmap_schema(self) -> Dict:
        """Get Roadmap Database schema."""
        return {
            'Initiative Name': {'type': 'title'},
            'Quarter': {'type': 'select', 'options': ['Q1', 'Q2', 'Q3', 'Q4']},
            'Status': {'type': 'select', 'options': ['Planned', 'In Progress', 'Complete', 'Blocked']},
            'Priority': {'type': 'select', 'options': ['High', 'Medium', 'Low']},
        }
    
    def _get_sprints_schema(self) -> Dict:
        """Get Sprints Database schema."""
        return {
            'Sprint Name': {'type': 'title'},
            'Sprint Number': {'type': 'number'},
            'Status': {'type': 'select', 'options': ['Planning', 'Active', 'Review', 'Complete', 'Cancelled']},
            'Start Date': {'type': 'date'},
            'End Date': {'type': 'date'},
        }
    
    def _get_events_schema(self) -> Dict:
        """Get Events & Calendar Database schema."""
        return {
            'Event Name': {'type': 'title'},
            'Event Type': {'type': 'select', 'options': ['Meeting', 'Conference', 'Webinar', 'Workshop', 'Other']},
            'Date': {'type': 'date'},
            'Status': {'type': 'select', 'options': ['Scheduled', 'Completed', 'Cancelled']},
        }
    
    def _get_feedback_schema(self) -> Dict:
        """Get Feedback & Feature Requests Database schema."""
        return {
            'Request Title': {'type': 'title'},
            'Type': {'type': 'select', 'options': ['Bug', 'Feature', 'Improvement']},
            'Status': {'type': 'select', 'options': ['Open', 'In Progress', 'Planned', 'Closed']},
            'Upvotes': {'type': 'number'},
        }
    
    def _get_live_updates_schema(self) -> Dict:
        """Get Live Updates Database schema."""
        return {
            'Event Title': {'type': 'title'},
            'Timestamp': {'type': 'created_time'},
            'Event Type': {'type': 'select', 'options': ['Deploy', 'Incident', 'Note', 'Maintenance']},
            'Impact Level': {'type': 'select', 'options': ['Low', 'Medium', 'High', 'Critical']},
        }
    
    def _get_alerts_schema(self) -> Dict:
        """Get Alerts & Notifications Database schema."""
        return {
            'Alert Title': {'type': 'title'},
            'Alert Type': {'type': 'select', 'options': ['Incident', 'Maintenance', 'Info']},
            'Priority': {'type': 'select', 'options': ['Low', 'Medium', 'High', 'Critical']},
            'Status': {'type': 'select', 'options': ['Open', 'Acknowledged', 'Resolved']},
            'Due Date': {'type': 'date'},
        }
    
    def _get_manual_updates_schema(self) -> Dict:
        """Get Manual Updates Database schema."""
        return {
            'Update Title': {'type': 'title'},
            'Date & Time': {'type': 'date'},
            'Update Type': {'type': 'select', 'options': ['Note', 'Manual Entry', 'Correction']},
            'Space': {'type': 'select', 'options': ['Stakeholder', 'Community', 'AV Live']},
        }
    
    def _get_system_status_schema(self) -> Dict:
        """Get System Status Database schema."""
        return {
            'Component Name': {'type': 'title'},
            'Status': {'type': 'select', 'options': ['✅ Operational', '⚠ Degraded', '🔴 Down', '🔄 Maintenance']},
            'Uptime': {'type': 'number', 'format': 'percent'},
        }
    
    def _print_summary(self):
        """Print build summary."""
        logger.info("\n" + "=" * 70)
        logger.info("Build Summary")
        logger.info("=" * 70)
        logger.info(f"Pages created: {len(self.created_pages)}")
        logger.info(f"Databases created: {len(self.created_databases)}")
        logger.info("")
        logger.info("Created Pages:")
        for key, page in self.created_pages.items():
            logger.info(f"  - {key}: {page.get('id', 'N/A')}")
        logger.info("")
        logger.info("Created Databases:")
        for key, db in self.created_databases.items():
            logger.info(f"  - {key}: {db.get('id', 'N/A')}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Build Artifact Virtual Notion Portal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without making actual API calls (for testing)'
    )
    parser.add_argument(
        '--space',
        choices=['root', 'stakeholder', 'community', 'avlive'],
        help='Build only specific space (default: all)'
    )
    
    args = parser.parse_args()
    
    try:
        builder = NotionPortalBuilder(dry_run=args.dry_run)
        builder.build_portal(space=args.space)
        return 0
    except Exception as e:
        logger.error(f"Build failed: {str(e)}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
