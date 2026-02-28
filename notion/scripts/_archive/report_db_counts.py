#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv('../.env')
import sys, os, time
from av_notion_client import NotionIntegration

n = NotionIntegration()
print('Connected as:', n.test_connection().get('user'))

expected_db_names = [
    'Master Stakeholder Database','Investor Database','Partner Database','Advisor Database','Board Members Database',
    'Key Customers Database','Analytics & Reports Database','Communications Log Database','Documents & Agreements Database',
    'Master Projects Database','Open Source Portfolio Database','Community Engagement Database','Project Management Database',
    'Roadmap Database','Sprints Database','Events & Calendar Database','Feedback & Feature Requests Database',
    'Live Updates Database','Alerts & Notifications Database','Manual Updates Database','System Status Database'
]

print('\nDatabase status:')
for name in expected_db_names:
    # find DB
    db = None
    try:
        results = n.list_databases()
        for d in results:
            if d['title'].strip().lower() == name.strip().lower() or name.strip().lower() in d['title'].strip().lower():
                db = d
                break
    except Exception as e:
        print(f' - {name}: list_databases failed: {e}')
        db = None
    if not db:
        print(f' - {name}: NOT FOUND')
        continue
    db_id = db['id']
    # try to query for one row
    has_rows = False
    err = None
    for attempt in range(3):
        try:
            res = n.query_database(db_id, page_size=1)
            if res and len(res) > 0:
                has_rows = True
            break
        except Exception as e:
            err = e
            time.sleep(0.6 * (attempt+1))
    if err and not has_rows:
        print(f' - {name}: QUERY ERROR: {err}')
    else:
        print(f' - {name}: {"has entries" if has_rows else "empty"}')

print('\nDone')
