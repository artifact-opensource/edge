#!/usr/bin/env python3
from pathlib import Path
from shield256 import Shield256
from cryptography.exceptions import InvalidTag

s = Shield256()
import os, sys
passphrase = os.environ.get('SHIELD_PASSPHRASE') or (sys.argv[1] if len(sys.argv) > 1 else None)
if not passphrase:
    print("Usage: verify_sample_decrypt.py <passphrase> or set SHIELD_PASSPHRASE in env")
    sys.exit(1)
paths = list(Path('enterprise/divisions/departments/executive').rglob('*.enc')) + list(Path('enterprise/divisions/departments/legal-compliance').rglob('*.enc'))
print('Found .enc files:', len(paths))
ok = 0
fail = 0
for i,p in enumerate(sorted(paths)[:100]):
    b = p.read_bytes()
    try:
        dec = s.decrypt_data(b, passphrase)
        status = 'OK'
        ok += 1
    except InvalidTag:
        status = 'FAIL (wrong passphrase or tampered)'
        fail += 1
    except ValueError as e:
        status = f'FAIL ({e})'
        fail += 1
    print(f'{i+1}. {p} -> {status}')
print(f'OK: {ok} / {len(paths)} (checked up to 100)')
if fail:
    print(f'FAILED: {fail}')
    sys.exit(1)
