#!/usr/bin/env python3
"""Check portal databases and seed one sample row if empty."""
from dotenv import load_dotenv
load_dotenv('../.env')
import sys
import time
from datetime import datetime

from av_notion_client import NotionIntegration

n = NotionIntegration()
print('Connected as:', n.test_connection().get('user'))

# Expected portal database name fragments and a sample row generator
DBS = {
    'Master Stakeholder Database': lambda: {'Name': 'ACME Holdings', 'Category': 'Investor', 'Tier': 'Strategic', 'Status': 'Active'},
    'Investor Database': lambda: {'Investor Name': 'ACME Capital', 'Investment Stage': 'Series A', 'Investment Amount': 500000},
    'Partner Database': lambda: {'Partner Name': 'Infra Co', 'Partnership Type': 'Integration', 'Start Date': datetime.utcnow().date().isoformat()},
    'Advisor Database': lambda: {'Advisor Name': 'Dr. Smith', 'Advisor Type': 'Technical Advisor', 'Status': 'Active'},
    'Board Members Database': lambda: {'Member Name': 'Jane Doe', 'Position': 'Independent Director', 'Status': 'Active'},
    'Key Customers Database': lambda: {'Customer Name': 'BigCorp', 'Company': 'BigCorp Ltd', 'Status': 'Active'},
    'Analytics & Reports Database': lambda: {'Report Name': 'Q1 Ops', 'Report Type': 'Operational', 'Period': 'Q1'},
    'Communications Log Database': lambda: {'Communication Title': 'Intro Call', 'Date': datetime.utcnow().date().isoformat(), 'Type': 'Call', 'Status': 'Completed'},
    'Documents & Agreements Database': lambda: {'Document Name': 'Master Service Agreement', 'Document Type': 'Contract', 'Status': 'Draft'},
    'Master Projects Database': lambda: {'Project Name': 'Project X', 'Category': 'Product', 'Status': '🟢 Active'},
    'Open Source Portfolio Database': lambda: {'Repository Name': 'artifactvirtual/foo', 'GitHub URL': 'https://github.com/artifactvirtual/foo', 'License': 'MIT'},
    'Community Engagement Database': lambda: {'Member Name': 'alice', 'Username': 'alice', 'Member Type': 'Member', 'Status': 'Active'},
    'Project Management Database': lambda: {'Task Name': 'Initial plan', 'Status': '📋 Todo', 'Priority': '🔴 Critical'},
    'Roadmap Database': lambda: {'Initiative Name': 'Platform Upgrade', 'Quarter': 'Q2', 'Status': 'Planned'},
    'Sprints Database': lambda: {'Sprint Name': 'Sprint 1', 'Sprint Number': 1, 'Status': 'Planning'},
    'Events & Calendar Database': lambda: {'Event Name': 'All Hands', 'Event Type': 'Meeting', 'Date': datetime.utcnow().date().isoformat()},
    'Feedback & Feature Requests Database': lambda: {'Request Title': 'Improve onboarding', 'Type': 'Feature', 'Status': 'Open'},
    'Live Updates Database': lambda: {'Event Title': 'Repo sync', 'Event Type': 'Deploy', 'Impact Level': 'Low'},
    'Alerts & Notifications Database': lambda: {'Alert Title': 'High CPU', 'Alert Type': 'Incident', 'Priority': 'High', 'Status': 'Open'},
    'Manual Updates Database': lambda: {'Update Title': 'Manual note', 'Date & Time': datetime.utcnow().isoformat(), 'Update Type': 'Note', 'Space': 'AV Live'},
    'System Status Database': lambda: {'Component Name': 'API', 'Status': '✅ Operational', 'Uptime': 99.99}
}

# helper: find database by name (exact or substring)

def find_db_by_name(name):
    results = n.list_databases()
    for d in results:
        if d['title'].strip().lower() == name.strip().lower():
            return d
    for d in results:
        if name.strip().lower() in d['title'].strip().lower():
            return d
    return None


def find_title_prop(db_props):
    # return a property name which is a title field
    for k, v in db_props.items():
        if v.get('type') == 'title':
            return k
    # fallback heuristics
    for k in ['Name', 'Title', 'Project Name','Request Title']:
        if k in db_props:
            return k
    return None


def build_properties_for_create(db_props, sample):
    props = {}
    for k, info in db_props.items():
        t = info.get('type')
        # match from sample (key names may differ)
        # use simple heuristics
        if t == 'title' or t == 'rich_text':
            # pick sample value by looking for matching key
            val = None
            for s_k in sample:
                if s_k.lower() in k.lower() or k.lower() in s_k.lower():
                    val = str(sample[s_k])
                    break
            if val is None:
                val = next(iter(sample.values()))
            props[k] = {'title' if t == 'title' else 'rich_text': [{'type': 'text', 'text': {'content': str(val)}}]}
        elif t == 'select':
            # pick matching option if present
            val = None
            for s_k in sample:
                if s_k.lower() in k.lower() or k.lower() in s_k.lower():
                    val = sample[s_k]
                    break
            if val is None:
                # default to first option if exists
                opts = info.get('select', {}).get('options', [])
                val = opts[0]['name'] if opts else 'Default'
            props[k] = {'select': {'name': str(val)}}
        elif t == 'multi_select':
            val = None
            for s_k in sample:
                if s_k.lower() in k.lower() or k.lower() in s_k.lower():
                    val = sample[s_k]
                    break
            if val is None:
                props[k] = {'multi_select': []}
            else:
                props[k] = {'multi_select': [{'name': str(val)}]}
        elif t == 'number':
            # find a numeric sample
            val = None
            for s_k in sample:
                try:
                    val = float(sample[s_k])
                    break
                except Exception:
                    continue
            if val is None:
                val = 0
            props[k] = {'number': val}
        elif t == 'date':
            # find a date-like sample
            val = None
            for s_k in sample:
                if 'date' in s_k.lower() or 'time' in s_k.lower() or 'start' in s_k.lower():
                    val = sample[s_k]
                    break
            if val is None:
                val = datetime.utcnow().date().isoformat()
            props[k] = {'date': {'start': str(val)}}
        elif t == 'checkbox':
            props[k] = {'checkbox': False}
        elif t == 'url':
            props[k] = {'url': str(next(iter(sample.values())))}
        elif t == 'email':
            props[k] = {'email': 'support@artifactvirtual.com'}
        else:
            # default
            props[k] = {'rich_text': [{'type': 'text', 'text': {'content': str(next(iter(sample.values())))}}]}
    return props


summary = []
for db_name, sample_fn in DBS.items():
    print('\nChecking DB:', db_name)
    db = find_db_by_name(db_name)
    if not db:
        print(' - Database not found; skipping')
        summary.append((db_name, 'not found'))
        continue
    db_id = db['id']
    print(' - Found:', db['title'], db_id)

    # query for entries (we use query but the wrapper may use query_database)
    # perform query with retries
    rows = []
    for attempt in range(3):
        try:
            rows = n.query_database(db_id, page_size=1)
            break
        except Exception as e:
            print(f' - Query attempt {attempt+1} failed: {e}')
            rows = []
            time.sleep(0.7 * (attempt + 1))
    if rows:
        print(' - Has entries:', len(rows))
        summary.append((db_name, 'has entries'))
        continue

    print(' - DB is empty, seeding one sample row...')
    # get properties from database (with retry)
    db_info = None
    for attempt in range(3):
        try:
            db_info = n.get_database(db_id)
            break
        except Exception as e:
            print(f' - get_database attempt {attempt+1} failed: {e}')
            time.sleep(0.7 * (attempt + 1))
    if not db_info:
        print(' - Could not retrieve database properties; skipping')
        summary.append((db_name, 'skip-get-db'))
        continue

    props_def = db_info.get('properties', {})
    sample = sample_fn()
    page_props = build_properties_for_create(props_def, sample)
    # content optional
    content = [{'object':'block','type':'paragraph','paragraph':{'rich_text':[{'type':'text','text':{'content':'Created by seed script'}}]}}]

    seeded = False
    for attempt in range(4):
        res = n.create_page_in_database(database_id=db_id, properties=page_props, content=content)
        if res.get('status') == 'success':
            print(' - Seeded row: page_id=', res.get('page_id'))
            summary.append((db_name, 'seeded'))
            seeded = True
            break
        else:
            print(f' - Seed attempt {attempt+1} failed: {res}')
            time.sleep(0.9 * (attempt + 1))
    if not seeded:
        summary.append((db_name, 'seed-failed'))
    time.sleep(0.75)

print('\nSummary Report:')
for s in summary:
    print(' -', s[0], ':', s[1])

print('\nDone. Verify the databases in Notion UI.')
