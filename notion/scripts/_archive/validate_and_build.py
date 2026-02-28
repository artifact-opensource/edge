#!/usr/bin/env python3
"""Validate schema mappings and run live build if checks pass."""
import os
from dotenv import load_dotenv
load_dotenv('../.env')

from av_notion_client import NotionIntegration
from build_notion_portal import NotionPortalBuilder

print('Starting schema validation...')
notion = NotionIntegration(os.environ.get('NOTION_API_KEY'))
print('Notion test connection:', notion.test_connection())

builder = NotionPortalBuilder(dry_run=True)

# Collect schema provider methods
schema_methods = [m for m in dir(builder) if m.startswith('_get_') and m.endswith('_schema')]
issues = []
for name in sorted(schema_methods):
    schema = getattr(builder, name)()
    props = notion.format_properties_from_schema(schema)
    # Basic validations
    # 1) Must include at least one property where type is title
    has_title = any(v.get('title') is not None for v in props.values())
    if not has_title:
        issues.append((name, 'Missing title property mapping'))
    # 2) For select/multi_select ensure non-empty options when provided in source
    for src_name, src_def in schema.items():
        if isinstance(src_def, dict) and src_def.get('type') in ('select','multi_select'):
            opts = src_def.get('options', [])
            if not opts:
                issues.append((name, f'Select property "{src_name}" has no options'))

    print(f'Validated {name}: {len(props)} properties')

if issues:
    print('\nIssues found:')
    for i in issues:
        print(' -', i[0], ':', i[1])
    raise SystemExit('Schema validation failed - fix issues and re-run')

print('\nAll schemas passed basic validation')

# Confirm with user before running live build
print('\nProceeding to run live build (creating pages & databases in Notion)...')
confirm = os.environ.get('FORCE_NOTION_BUILD','false').lower() == 'true'
if not confirm:
    print('To run the live build, set environment variable FORCE_NOTION_BUILD=true and re-run this script.')
    raise SystemExit('Aborting live build')

# Run live build
builder = NotionPortalBuilder(dry_run=False)
builder.build_portal()
print('\nLive build completed')
