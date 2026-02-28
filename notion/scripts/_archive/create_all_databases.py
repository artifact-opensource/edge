#!/usr/bin/env python3
"""Create all portal databases in Notion (idempotent).
This will ensure all DBs exist under the Hub pages.
"""
from dotenv import load_dotenv
load_dotenv('../.env')

from build_notion_portal import NotionPortalBuilder

# Make sure NOTION_API_KEY and NOTION_PARENT_PAGE_ID are set in .env
builder = NotionPortalBuilder(dry_run=False)

print('Creating root and hub databases (idempotent)')
# Ensure root and hub pages exist
builder._build_root_structure()

# Create stakeholder/ community/ avlive databases
builder._build_stakeholder_hub()
builder._build_community_hub()
builder._build_avlive_dashboard()

print('\nAll database creation steps completed. Review created databases in Notion UI.')
