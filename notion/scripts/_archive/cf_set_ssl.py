#!/usr/bin/env python3
import os
import requests
CF_TOKEN = os.environ.get('CF_API_TOKEN')
if not CF_TOKEN:
    raise SystemExit('CF_API_TOKEN not set')
API = 'https://api.cloudflare.com/client/v4'
HEADERS = {'Authorization':f'Bearer {CF_TOKEN}','Content-Type':'application/json'}
ZONE = 'artifactvirtual.com'

r = requests.get(f'{API}/zones', params={'name': ZONE}, headers=HEADERS)
r.raise_for_status()
zone_id = r.json()['result'][0]['id']
print('zone id:', zone_id)

def set_setting(name, value):
    resp = requests.patch(f'{API}/zones/{zone_id}/settings/{name}', json={'value': value}, headers=HEADERS)
    if resp.status_code >= 400:
        print(f'FAILED: set {name} -> {value}: {resp.status_code} {resp.text}')
        return False
    print(f'OK: set {name} -> {value}')
    return True

# Apply settings
set_setting('ssl', 'full_strict')
set_setting('always_use_https', 'on')
set_setting('automatic_https_rewrites', 'on')
set_setting('minimum_tls_version', '1.2')

# Verify
resp = requests.get(f'{API}/zones/{zone_id}/settings', headers=HEADERS)
resp.raise_for_status()
print('\nCurrent relevant settings:')
for s in resp.json().get('result', []):
    if s['id'] in ('ssl', 'always_use_https', 'automatic_https_rewrites', 'minimum_tls_version'):
        print(s['id'], '->', s.get('value'))

# Test site
try:
    h = requests.get('https://www.artifactvirtual.com', timeout=10)
    print('\nwww.artifactvirtual.com status:', h.status_code)
except Exception as e:
    print('\nCould not fetch site:', e)
