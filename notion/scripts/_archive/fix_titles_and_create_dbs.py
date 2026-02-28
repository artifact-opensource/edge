#!/usr/bin/env python3
"""Fix portal page titles/icons and ensure hub databases exist."""
from dotenv import load_dotenv
load_dotenv('../.env')
import time
from av_notion_client import NotionIntegration
from build_notion_portal import NotionPortalBuilder

notion = NotionIntegration()
print('Connected as:', notion.test_connection().get('user'))

# Hubs mapping: title -> icon
hubs = [
    ('Artifact Virtual Notion Portal', '🏢'),
    ('Stakeholder Hub', '👥'),
    ('Community Hub', '🚀'),
    ('AV Live Dashboard', '⚡')
]

# For each hub: find best page, append heading, set icon
page_ids = {}
for title, icon in hubs:
    results = notion.search(title, filter_type='page')
    # prefer exact title matches
    match = None
    for r in results:
        if r.get('title') == title:
            match = r
            break
    if not match and results:
        match = results[0]
        print(f"Using best match for '{title}': {match.get('title')} (id={match.get('id')})")
    if not match:
        # create it
        print(f"No page found for '{title}', creating new page")
        create_res = notion.create_page_in_parent(parent_id=notion.workspace_id or None, title=title, icon=icon, description=f"{title} created by builder")
        if create_res.get('status') != 'success':
            raise SystemExit(f"Failed to create page {title}: {create_res}")
        pid = create_res.get('page_id')
        page_ids[title] = pid
        # add heading block
        notion.append_children(pid, [{'object':'block','type':'heading_1','heading_1':{'rich_text':[{'type':'text','text':{'content':title}}]}}])
        continue

    pid = match.get('id')
    page_ids[title] = pid
    # append a heading block with the desired title (idempotent if we look for existing)
    children = [{'object':'block','type':'heading_1','heading_1':{'rich_text':[{'type':'text','text':{'content':title}}]}}]
    res = notion.append_children(pid, children)
    if res.get('status') != 'success':
        print(f"Warning: could not append heading to {title} (id={pid}): {res}")
    # set icon
    icon_payload = {'type':'emoji','emoji':icon} if icon else None
    res2 = notion.update_page(pid, icon=icon_payload)
    if res2.get('status') != 'success':
        print(f"Warning: could not update icon for {title} (id={pid}): {res2}")
    print(f"Fixed title/icon for '{title}' -> id={pid}")
    time.sleep(0.7)

# Now ensure databases exist under each hub
builder = NotionPortalBuilder(dry_run=False)
# Reuse existing page ids as parents when building spaces
if 'Stakeholder Hub' in page_ids:
    print('\nEnsuring Stakeholder Hub databases...')
    builder._build_stakeholder_hub()
if 'Community Hub' in page_ids:
    print('\nEnsuring Community Hub databases...')
    builder._build_community_hub()
if 'AV Live Dashboard' in page_ids:
    print('\nEnsuring AV Live Dashboard databases...')
    builder._build_avlive_dashboard()

print('\nDone: updated pages and ensured databases. Recommend verifying in Notion web UI.')
