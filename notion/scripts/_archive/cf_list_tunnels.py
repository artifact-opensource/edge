#!/usr/bin/env python3
"""List Cloudflare tunnels for the account. Reads CLOUDFLARE_API_TOKEN from .env or environment."""
import os, sys, json, requests

# try to read token from env or .env file
CF_TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN') or os.environ.get('CF_API_TOKEN')
if not CF_TOKEN:
    envp = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
    if os.path.exists(envp):
        with open(envp, 'r') as f:
            for l in f:
                if l.strip().startswith('CLOUDFLARE_API_TOKEN'):
                    CF_TOKEN = l.split('=',1)[1].strip()
                    break
if not CF_TOKEN:
    print('ERROR: CLOUDFLARE_API_TOKEN not set (env or .env)')
    sys.exit(1)

API = 'https://api.cloudflare.com/client/v4'
HEAD = {'Authorization': f'Bearer {CF_TOKEN}', 'Content-Type': 'application/json'}
ZONE_NAME = 'artifactvirtual.com'

try:
    zr = requests.get(f'{API}/zones', params={'name': ZONE_NAME}, headers=HEAD)
    zr.raise_for_status()
    zones = zr.json().get('result', [])
    if not zones:
        print('Zone not found')
        sys.exit(1)
    zone_id = zones[0]['id']
    zr2 = requests.get(f'{API}/zones/{zone_id}', headers=HEAD)
    zr2.raise_for_status()
    account_id = zr2.json().get('result', {}).get('account', {}).get('id')
    if not account_id:
        print('Account id not found')
        sys.exit(1)
    tr = requests.get(f'{API}/accounts/{account_id}/tunnels', headers=HEAD)
    tr.raise_for_status()
    data = tr.json()
    if not data.get('success'):
        print('API returned error:', data)
        sys.exit(1)
    tunnels = data.get('result', [])
    if not tunnels:
        print('No tunnels found for account', account_id)
    else:
        print(json.dumps(tunnels, indent=2))
except Exception as e:
    print('Error:', e)
    sys.exit(1)
