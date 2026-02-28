#!/usr/bin/env python3
"""
Notion Integration Test Script (using our wrapper)
Tests connectivity and workspace access using `av_notion_client.NotionIntegration`.
"""

import os
import sys

try:
    from av_notion_client import NotionIntegration
except ImportError as e:
    print("ERROR: notion-client not installed or wrapper failed. Run: pip install notion-client")
    print(e)
    sys.exit(1)

# Load .env for credentials when running tests locally
try:
    from dotenv import load_dotenv
    load_dotenv('../.env')
except Exception:
    pass


def main():
    api_key = os.environ.get("NOTION_API_KEY")
    if not api_key:
        print("ERROR: NOTION_API_KEY not set")
        return False

    print("=" * 60)
    print("ARTIFACT VIRTUAL - NOTION INTEGRATION TEST (wrapper)")
    print("=" * 60)
    print()

    print("1. Initializing NotionIntegration wrapper...")
    try:
        notion = NotionIntegration(api_key)
        print("   ✓ Wrapper initialized")
    except Exception as e:
        print(f"   ❌ Failed to initialize wrapper: {e}")
        return False

    print("\n2. Testing API connection...")
    res = notion.test_connection()
    if res.get('status') == 'connected':
        print("   ✓ Connected successfully!")
        print(f"   User: {res.get('user')}")
        print(f"   ID: {res.get('id')}")
    else:
        print(f"   ❌ Connection failed: {res}")
        return False

    print("\n3. Listing databases...")
    dbs = notion.list_databases()
    if dbs:
        print(f"   ✓ Found {len(dbs)} database(s):")
        for db in dbs[:10]:
            print(f"     - {db.get('title')} (ID: {db.get('id')})")
    else:
        print("   No accessible databases found")

    print("\n4. Example: format a sample schema to Notion properties")
    sample_schema = {'Name': {'type': 'title'}, 'Status': {'type': 'select', 'options': ['Active','Inactive']}, 'Start': {'type': 'date'}}
    props = notion.format_properties_from_schema(sample_schema)
    print(f"   ✓ Example properties: {list(props.keys())}")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
