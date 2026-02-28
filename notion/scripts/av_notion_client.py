#!/usr/bin/env python3
"""
Artifact Virtual wrapper for Notion API client to avoid local name collisions.
Provides `NotionIntegration` class (thin wrapper around the official client) and
helpers to convert simplified schemas to Notion property definitions.
"""
import os
import json
import sys
from datetime import datetime
from typing import Optional, Dict, List, Any
import importlib.util

# Try to locate the installed notion client in site-packages to avoid importing
# the local `notion_client.py` file by accident. Use multiple fallback paths.
Client = None
APIResponseError = Exception

try:
    # Prefer package 'notion' (some installs expose `notion.notion_client`)
    spec = importlib.util.find_spec('notion')
    if spec and spec.origin and 'site-packages' in spec.origin:
        from notion.notion_client import Client
        from notion_client.errors import APIResponseError
    else:
        # Try the standard published package name `notion_client`
        spec2 = importlib.util.find_spec('notion_client')
        if spec2 and spec2.origin and 'site-packages' in spec2.origin:
            from notion_client import Client
            from notion_client.errors import APIResponseError
        else:
            # Last resort: try direct import and hope sys.path is set to site-packages
            try:
                from notion_client import Client
                from notion_client.errors import APIResponseError
            except Exception as e:
                raise ImportError(e)
except Exception as e:
    # Fall back to simple requests-based Notion API helper if the official
    # client package is not importable (this avoids local filename collisions).
    import requests
    
    class _SimpleNotionHTTP:
        BASE = 'https://api.notion.com/v1'
        def __init__(self, token: str):
            self.token = token
            self.headers = {
                'Authorization': f'Bearer {token}',
                'Notion-Version': '2022-06-28',
                'Content-Type': 'application/json'
            }
        def get(self, path: str, timeout: int = 15, **kwargs):
            try:
                return requests.get(f"{self.BASE}{path}", headers=self.headers, timeout=timeout, **kwargs)
            except requests.exceptions.RequestException as e:
                raise RuntimeError(f"HTTP GET failed: {e}")
        def post(self, path: str, json_body: dict, timeout: int = 20, **kwargs):
            try:
                return requests.post(f"{self.BASE}{path}", headers=self.headers, json=json_body, timeout=timeout, **kwargs)
            except requests.exceptions.RequestException as e:
                raise RuntimeError(f"HTTP POST failed: {e}")
        def patch(self, path: str, json_body: dict, timeout: int = 15, **kwargs):
            try:
                return requests.patch(f"{self.BASE}{path}", headers=self.headers, json=json_body, timeout=timeout, **kwargs)
            except requests.exceptions.RequestException as e:
                raise RuntimeError(f"HTTP PATCH failed: {e}")

    # We'll continue with a flag to indicate we are using HTTP fallback
    _HTTP_FALLBACK = True
    APIResponseError = Exception
    Client = None
    print('Note: using HTTP fallback for Notion API (official client not importable).')


class NotionIntegration:
    """Notion API integration for Artifact Virtual (wrapper)

    Uses the official `notion-client` package internally. Provides convenience
    methods and a schema conversion helper for the simplified schema used by
    `build_notion_portal.py`.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('NOTION_API_KEY')
        if not self.api_key:
            raise ValueError('NOTION_API_KEY not set in environment or provided')
        if not (self.api_key.startswith('secret_') or self.api_key.startswith('ntn_')):
            raise ValueError("Invalid Notion API key format. Must start with 'secret_' or 'ntn_'")
        self.workspace_id = os.environ.get('NOTION_WORKSPACE_ID')
        if Client:
            # official client
            self.client = Client(auth=self.api_key)
            self._http = None
        else:
            # fallback requests-based simple client
            self.client = None
            self._http = _SimpleNotionHTTP(self.api_key)

    def test_connection(self) -> Dict[str, Any]:
        try:
            if self.client:
                response = self.client.users.me()
                return {'status': 'connected', 'user': response.get('name', 'Unknown'), 'type': response.get('type', 'Unknown'), 'id': response.get('id', 'Unknown'), 'timestamp': datetime.now().isoformat()}
            else:
                r = self._http.get('/users/me')
                r.raise_for_status()
                data = r.json()
                return {'status': 'connected', 'user': data.get('name', 'Unknown'), 'type': data.get('type', 'Unknown'), 'id': data.get('id', 'Unknown'), 'timestamp': datetime.now().isoformat()}
        except Exception as e:
            return {'status': 'error', 'error': str(e), 'timestamp': datetime.now().isoformat()}

    def list_databases(self) -> List[Dict]:
        """List all accessible databases (with retries)."""
        for attempt in range(3):
            try:
                if self.client:
                    response = self.client.search(filter={'property': 'object', 'value': 'database'})
                    results = response.get('results', [])
                else:
                    body = {'filter': {'property': 'object', 'value': 'database'}}
                    r = self._http.post('/search', json_body=body)
                    r.raise_for_status()
                    results = r.json().get('results', [])

                databases = []
                for db in results:
                    title = ''
                    if db.get('title'):
                        title = ''.join([t.get('plain_text', '') for t in db['title']])
                    databases.append({'id': db['id'], 'title': title or 'Untitled', 'url': db.get('url', ''), 'created_time': db.get('created_time', ''), 'last_edited_time': db.get('last_edited_time', '')})
                return databases
            except Exception as e:
                print(f'list_databases attempt {attempt+1} failed: {e}')
                import time
                time.sleep(0.6 * (attempt + 1))
        print('Error listing databases after retries')
        return []

    def get_database(self, database_id: str) -> Dict[str, Any]:
        try:
            if self.client:
                db = self.client.databases.retrieve(database_id=database_id)
            else:
                r = self._http.post('/databases/query', json_body={'database_id': database_id})
                r.raise_for_status()
                db = r.json()
            return {'id': db['id'], 'title': ''.join([t.get('plain_text', '') for t in db.get('title', [])]), 'properties': db.get('properties', {}), 'url': db.get('url', '')}
        except Exception as e:
            return {'error': str(e)}

    def query_database(self, database_id: str, filter_obj: Optional[Dict] = None, sorts: Optional[List] = None, page_size: int = 100) -> List[Dict]:
        try:
            if self.client:
                params = {'database_id': database_id, 'page_size': page_size}
                if filter_obj:
                    params['filter'] = filter_obj
                if sorts:
                    params['sorts'] = sorts
                response = self.client.databases.query(**params)
                return response.get('results', [])
            else:
                # Use the database-specific query endpoint for HTTP fallback
                body = {'page_size': page_size}
                if filter_obj:
                    body['filter'] = filter_obj
                if sorts:
                    body['sorts'] = sorts
                r = self._http.post(f'/databases/{database_id}/query', json_body=body)
                r.raise_for_status()
                return r.json().get('results', [])
        except Exception as e:
            print(f'Error querying database: {e}')
            return []

    def create_page_in_parent(self, parent_id: str, title: str, icon: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Build children with a heading block for the page title (safer for parent page creation)
            children = []
            children.append({'object': 'block', 'type': 'heading_1', 'heading_1': {'rich_text': [{'type': 'text', 'text': {'content': title}}]}})
            if description:
                children.append({'object': 'block', 'type': 'paragraph', 'paragraph': {'rich_text': [{'type': 'text', 'text': {'content': description}}]}})
            params = {'parent': {'page_id': parent_id}, 'children': children}
            if icon:
                params['icon'] = {'type': 'emoji', 'emoji': icon}
            if self.client:
                response = self.client.pages.create(**params)
                return {'status': 'success', 'page_id': response.get('id'), 'url': response.get('url', '')}
            else:
                r = self._http.post('/pages', json_body=params)
                try:
                    r.raise_for_status()
                except Exception as ex:
                    return {'status': 'error', 'error': f'{ex}: {r.status_code} {r.text}'}
                response = r.json()
                return {'status': 'success', 'page_id': response.get('id'), 'url': response.get('url', '')}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def create_database(self, parent_page_id: str, title: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if self.client:
                response = self.client.databases.create(parent={'type': 'page_id', 'page_id': parent_page_id}, title=[{'type': 'text', 'text': {'content': title}}], properties=properties)
                return {'status': 'success', 'database_id': response.get('id'), 'url': response.get('url', '')}
            else:
                body = {'parent': {'type': 'page_id', 'page_id': parent_page_id}, 'title': [{'type': 'text', 'text': {'content': title}}], 'properties': properties}
                r = self._http.post('/databases', json_body=body)
                r.raise_for_status()
                response = r.json()
                return {'status': 'success', 'database_id': response.get('id'), 'url': response.get('url', '')}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def create_page_in_database(self, database_id: str, properties: Dict[str, Any], content: Optional[list] = None) -> Dict[str, Any]:
        """Create a new page (row) in a database."""
        try:
            params = {'parent': {'database_id': database_id}, 'properties': properties}
            if content:
                params['children'] = content
            if self.client:
                response = self.client.pages.create(**params)
                return {'status': 'success', 'page_id': response.get('id'), 'url': response.get('url', '')}
            else:
                r = self._http.post('/pages', json_body=params)
                try:
                    r.raise_for_status()
                except Exception as ex:
                    return {'status': 'error', 'error': f'{ex}: {r.status_code} {r.text}'}
                response = r.json()
                return {'status': 'success', 'page_id': response.get('id'), 'url': response.get('url', '')}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def append_children(self, block_id: str, children: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Append blocks to a page or block."""
        try:
            if self.client:
                res = self.client.blocks.children.append(block_id=block_id, children=children)
                return {'status': 'success', 'result': res}
            else:
                r = self._http.post(f'/blocks/{block_id}/children', json_body={'children': children})
                r.raise_for_status()
                return {'status': 'success', 'result': r.json()}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def update_page(self, page_id: str, icon: Optional[Dict[str, Any]] = None, properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update page metadata (icon, properties)."""
        try:
            if self.client:
                body = {}
                if icon is not None:
                    body['icon'] = icon
                if properties is not None:
                    body['properties'] = properties
                res = self.client.pages.update(page_id=page_id, **body)
                return {'status': 'success', 'result': res}
            else:
                body = {}
                if icon is not None:
                    body['icon'] = icon
                if properties is not None:
                    body['properties'] = properties
                r = self._http.patch(f'/pages/{page_id}', json_body=body)
                try:
                    r.raise_for_status()
                except Exception as ex:
                    return {'status': 'error', 'error': f'{ex}: {r.status_code} {r.text}'}
                return {'status': 'success', 'result': r.json()}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    def create_database_from_schema(self, parent_page_id: str, title: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        properties = self.format_properties_from_schema(schema)
        return self.create_database(parent_page_id=parent_page_id, title=title, properties=properties)

    def format_properties_from_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        prop_map: Dict[str, Any] = {}
        for name, meta in schema.items():
            typ = meta.get('type') if isinstance(meta, dict) else meta
            if typ == 'title':
                prop_map[name] = {'title': {}}
            elif typ == 'rich_text':
                prop_map[name] = {'rich_text': {}}
            elif typ == 'select':
                options = meta.get('options', []) if isinstance(meta, dict) else []
                prop_map[name] = {'select': {'options': [{'name': o} for o in options]}}
            elif typ == 'multi_select':
                options = meta.get('options', []) if isinstance(meta, dict) else []
                prop_map[name] = {'multi_select': {'options': [{'name': o} for o in options]}}
            elif typ == 'number':
                fmt = meta.get('format') if isinstance(meta, dict) else None
                prop_map[name] = {'number': {'format': fmt if fmt in ['number', 'dollar', 'percent'] else 'number'}}
            elif typ == 'date':
                prop_map[name] = {'date': {}}
            elif typ == 'email':
                prop_map[name] = {'email': {}}
            elif typ == 'phone_number':
                prop_map[name] = {'phone_number': {}}
            elif typ == 'url':
                prop_map[name] = {'url': {}}
            elif typ == 'checkbox':
                prop_map[name] = {'checkbox': {}}
            elif typ == 'created_time':
                prop_map[name] = {'created_time': {}}
            else:
                prop_map[name] = {'rich_text': {}}
        return prop_map

    def search(self, query: str, filter_type: Optional[str] = None) -> List[Dict]:
        """Search workspace for pages or databases."""
        try:
            if self.client:
                params = {"query": query}
                if filter_type in ["page", "database"]:
                    params["filter"] = {"property": "object", "value": filter_type}
                response = self.client.search(**params)
                results = []
                for item in response.get('results', []):
                    title = ''
                    if item.get('title'):
                        title = ''.join([t.get('plain_text', '') for t in item['title']])
                    elif item.get('properties', {}).get('title', {}).get('title'):
                        title = ''.join([t.get('plain_text', '') for t in item['properties']['title']['title']])
                    results.append({'id': item['id'], 'object': item['object'], 'title': title or 'Untitled', 'url': item.get('url', '')})
                return results
            else:
                body = {'query': query}
                if filter_type in ['page', 'database']:
                    body['filter'] = {'property': 'object', 'value': filter_type}
                r = self._http.post('/search', json_body=body)
                r.raise_for_status()
                response = r.json()
                results = []
                for item in response.get('results', []):
                    title = ''
                    if item.get('title'):
                        title = ''.join([t.get('plain_text', '') for t in item.get('title', [])])
                    elif item.get('properties', {}).get('title', {}).get('title'):
                        title = ''.join([t.get('plain_text', '') for t in item['properties']['title']['title']])
                    results.append({'id': item['id'], 'object': item['object'], 'title': title or 'Untitled', 'url': item.get('url', '')})
                return results
        except Exception as e:
            print(f'Search error: {e}')
            return []

# Keep a small test harness like original file
if __name__ == '__main__':
    print('This is the Artifact Virtual Notion wrapper (av_notion_client).')
    print('Use the NotionIntegration class to interact with Notion safely.')
