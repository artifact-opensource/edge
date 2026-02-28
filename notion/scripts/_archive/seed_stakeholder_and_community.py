#!/usr/bin/env python3
"""Seed Stakeholder & Community Notion DBs from repo content.
- Scans `enterprise/stakeholders/` for markdown docs and creates entries in "Documents & Agreements Database".
- Extracts allowed emails from website backend README / .env and creates minimal Stakeholder entries in "Master Stakeholder Database".

This script is idempotent: it searches for existing document records by path/title and skips duplicates.
"""
from dotenv import load_dotenv
load_dotenv('../.env')
import os, re, json
from pathlib import Path
from notion.scripts.av_notion_client import NotionIntegration

ROOT = Path(__file__).resolve().parents[1] / 'enterprise' / 'stakeholders'
if not ROOT.exists():
    print('Stakeholder docs directory not found:', ROOT)
    raise SystemExit(1)

n = NotionIntegration()

DOC_DB_NAME = 'Documents & Agreements Database'
STAKE_DB_NAME = 'Master Stakeholder Database'

def excerpt_from_file(p: Path, max_chars=300):
    txt = p.read_text(encoding='utf-8')
    # remove markdown frontmatter if any
    txt = re.sub(r'^---[\s\S]*?---\n', '', txt)
    # find first paragraph
    parts = [s.strip() for s in txt.split('\n\n') if s.strip()]
    if parts:
        return parts[0][:max_chars]
    return ''


def ensure_document_entry(file_path: Path):
    title = file_path.name
    rel = str(file_path.relative_to(Path.cwd()))
    excerpt = excerpt_from_file(file_path)

    # Check for existing doc by path (custom property 'Repo Path')
    # We'll search Documents DB for the repo path text
    existing = None
    try:
        dbs = n.list_databases()
        doc_db = None
        for d in dbs:
            if d['title'].strip().lower() == DOC_DB_NAME.strip().lower():
                doc_db = d
                break
        if not doc_db:
            print('Documents DB not found in Notion; skipping', title)
            return False
        # Search for any page that has the repo path in its properties (we will do a search)
        found = n.search(rel)
        for f in found:
            # heuristics: match title or repo path inside page content
            if f.get('title','').strip().lower() == title.strip().lower():
                existing = f
                break
    except Exception as e:
        print('Error searching for document', e)

    if existing:
        print('Skipping existing document:', title)
        return False

    props = {
        'Document Name': title,
        'Document Type': 'Guide',
        'Repo Path': rel,
        'Summary': excerpt,
    }
    try:
        res = n.create_page_in_database(doc_db['id'], props)
        print('Created document row:', title, '->', res.get('page_id'))
        return True
    except Exception as e:
        print('Failed to create document entry for', title, ':', e)
        return False


def seed_documents():
    md_files = list(ROOT.rglob('*.md'))
    print('Found', len(md_files), 'markdown files under enterprise/stakeholders')
    created = 0
    for p in md_files:
        ok = ensure_document_entry(p)
        if ok:
            created += 1
    print(f'Created {created} new document entries')


def seed_allowed_emails():
    # Look for ALLOWED_EMAILS in website backend readme or .env
    candidates = []
    webr = Path('website/src/backend/.env.production.example')
    if webr.exists():
        txt = webr.read_text()
        m = re.search(r'ALLOWED_EMAILS=(.+)', txt)
        if m:
            candidates = [e.strip() for e in m.group(1).split(',') if e.strip()]
    # fallback to top-level README
    if not candidates:
        top = Path('website/README.md')
        if top.exists():
            txt = top.read_text()
            m = re.search(r'ALLOWED_EMAILS=(.+)', txt)
            if m:
                candidates = [e.strip() for e in m.group(1).split(',') if e.strip()]

    if not candidates:
        print('No allowed emails discovered; skipping stakeholder contact seeding')
        return

    # Find stakeholder DB
    dbs = n.list_databases()
    stake_db = None
    for d in dbs:
        if d['title'].strip().lower() == STAKE_DB_NAME.strip().lower():
            stake_db = d
            break
    if not stake_db:
        print('Master Stakeholder DB not found; skipping contact seeding')
        return

    created = 0
    for email in candidates:
        # simple upsert heuristic: search by email
        res = n.search(email)
        exists = False
        for r in res:
            if email in json.dumps(r).lower():
                exists = True
                break
        if exists:
            print('Stakeholder exists, skipping:', email)
            continue
        props = {
            'Name': email.split('@')[0].replace('.', ' ').title(),
            'Email': email,
            'Type': 'Investor'
        }
        try:
            r = n.create_page_in_database(stake_db['id'], props)
            print('Created stakeholder:', email, '->', r.get('page_id'))
            created += 1
        except Exception as e:
            print('Failed to create stakeholder', email, e)
    print('Created', created, 'stakeholder entries')


if __name__ == '__main__':
    seed_documents()
    seed_allowed_emails()
    print('Seeding complete.')
