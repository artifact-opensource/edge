#!/usr/bin/env python3
"""Configure Cloudflare DNS and settings for GitHub Pages site.
Reads Cloudflare API token from env var CF_API_TOKEN.
"""
import os
import sys
import requests

CF_TOKEN = os.environ.get('CF_API_TOKEN')
ZONE_NAME = 'artifactvirtual.com'
GH_TARGET = 'artifactvirtual.github.io'

if not CF_TOKEN:
    print('ERROR: CF_API_TOKEN not set in environment')
    sys.exit(1)

HEADERS = {
    'Authorization': f'Bearer {CF_TOKEN}',
    'Content-Type': 'application/json'
}
API = 'https://api.cloudflare.com/client/v4'

def get_zone_id(zone_name):
    r = requests.get(f'{API}/zones', params={'name': zone_name}, headers=HEADERS)
    r.raise_for_status()
    data = r.json()
    if not data.get('success'):
        raise RuntimeError(data)
    results = data.get('result', [])
    if not results:
        raise RuntimeError('Zone not found')
    return results[0]['id']


def find_dns_record(zone_id, name):
    r = requests.get(f'{API}/zones/{zone_id}/dns_records', params={'name': name}, headers=HEADERS)
    r.raise_for_status()
    data = r.json()
    if not data.get('success'):
        raise RuntimeError(data)
    results = data.get('result', [])
    return results


def create_or_update_cname(zone_id, name, target):
    # Look for existing
    recs = find_dns_record(zone_id, name)
    for r in recs:
        if r['type'] in ('CNAME','A'):
            # Update to CNAME -> target
            print(f'Updating DNS record {name} (id={r["id"]}) -> CNAME {target} (proxied=true)')
            payload = {'type': 'CNAME', 'name': name, 'content': target, 'ttl': 1, 'proxied': True}
            resp = requests.put(f'{API}/zones/{zone_id}/dns_records/{r["id"]}', json=payload, headers=HEADERS)
            resp.raise_for_status()
            print('Updated')
            return resp.json()
    # Create new
    print(f'Creating CNAME {name} -> {target} (proxied=true)')
    payload = {'type': 'CNAME', 'name': name, 'content': target, 'ttl': 1, 'proxied': True}
    resp = requests.post(f'{API}/zones/{zone_id}/dns_records', json=payload, headers=HEADERS)
    resp.raise_for_status()
    print('Created')
    return resp.json()


def set_zone_setting(zone_id, setting, value):
    resp = requests.patch(f'{API}/zones/{zone_id}/settings/{setting}', json={'value': value}, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    if not data.get('success'):
        print('Warning: setting change did not succeed', data)
    else:
        print(f'Set {setting} -> {value}')
    return data


def purge_cache(zone_id):
    resp = requests.post(f'{API}/zones/{zone_id}/purge_cache', json={'purge_everything': True}, headers=HEADERS)
    resp.raise_for_status()
    print('Purged cache')
    return resp.json()


if __name__ == '__main__':
    zone_id = get_zone_id(ZONE_NAME)
    print('Zone id:', zone_id)

    # Handle www
    create_or_update_cname(zone_id, 'www.' + ZONE_NAME, GH_TARGET)

    # Handle apex with CNAME flattening by creating a CNAME record for root
    try:
        create_or_update_cname(zone_id, ZONE_NAME, GH_TARGET)
    except Exception as e:
        print('Could not create root CNAME (Cloudflare may disallow direct CNAME for apex); creating A records to GitHub Pages IPs')
        GH_IPS = ['185.199.108.153','185.199.109.153','185.199.110.153','185.199.111.153']
        for ip in GH_IPS:
            # see if A record exists for this ip
            recs = find_dns_record(zone_id, ZONE_NAME)
            updated = False
            for r in recs:
                if r['type']=='A' and r['content']==ip:
                    print('A record exists for', ip)
                    updated = True
            if not updated:
                payload = {'type':'A','name':ZONE_NAME,'content':ip,'ttl':1,'proxied':True}
                resp = requests.post(f'{API}/zones/{zone_id}/dns_records', json=payload, headers=HEADERS)
                resp.raise_for_status()
                print('Created A record for', ip)

    # Set SSL settings
    set_zone_setting(zone_id, 'ssl', 'full')
    set_zone_setting(zone_id, 'always_use_https', 'on')
    set_zone_setting(zone_id, 'automatic_https_rewrites', 'on')

    purge_cache(zone_id)

    print('\nVerification:')
    print('www.', ZONE_NAME, 'CNAME records:')
    print(find_dns_record(zone_id, 'www.'+ZONE_NAME))
    print('\nroot records:')
    print(find_dns_record(zone_id, ZONE_NAME))
    print('\nDone. Please allow DNS propagation (may be immediate via Cloudflare).')