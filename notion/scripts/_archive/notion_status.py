#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv('../.env')
from av_notion_client import NotionIntegration

n = NotionIntegration()
print('Connected as:', n.test_connection().get('user'))

pages_to_check = [
    'Artifact Virtual Notion Portal',
    'Stakeholder Hub',
    'Community Hub',
    'AV Live Dashboard'
]

print('\nPages:')
for title in pages_to_check:
    results = n.search(title, filter_type='page')
    matched = [r for r in results if r.get('title') == title]
    if matched:
        for r in matched:
            print(f" - {title}: id={r.get('id')} url={r.get('url')}")
    elif results:
        print(f" - {title}: {len(results)} matches (no exact title match); first: {results[0].get('title')} id={results[0].get('id')}")
    else:
        print(f" - {title}: not found")

# Check databases
print('\nDatabases:')
dbs = n.list_databases()
expected_db_names = [
    'Master Stakeholder Database','Investor Database','Partner Database','Advisor Database','Board Members Database',
    'Key Customers Database','Analytics & Reports Database','Communications Log Database','Documents & Agreements Database',
    'Master Projects Database','Open Source Portfolio Database','Community Engagement Database','Project Management Database',
    'Roadmap Database','Sprints Database','Events & Calendar Database','Feedback & Feature Requests Database',
    'Live Updates Database','Alerts & Notifications Database','Manual Updates Database','System Status Database'
]
found = {d['title']: d for d in dbs}
for t in expected_db_names:
    if t in found:
        d = found[t]
        print(f" - {t}: id={d.get('id')} url={d.get('url')}")
    else:
        # try contains
        matches = [d for d in dbs if t.lower() in d['title'].lower()]
        if matches:
            d = matches[0]
            print(f" - {t}: partial match -> {d.get('title')} id={d.get('id')}")
        else:
            print(f" - {t}: not found")

print('\nSummary:')
print(f" - Pages found (of {len(pages_to_check)}): {sum(1 for t in pages_to_check if any(r.get('title')==t for r in n.search(t, filter_type='page')))}")
print(f" - Databases accessible: {len(dbs)}")
