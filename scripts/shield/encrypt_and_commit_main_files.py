#!/usr/bin/env python3
"""Encrypt all sensitive files listed in csv-manifest.json, commit .enc files and remove plaintext from repo, push to origin.
Usage: python scripts/shield/encrypt_and_commit_main_files.py <passphrase>
Environment: set GIT_AUTHOR_NAME/EMAIL if running in CI.
"""
import sys
import json
import shutil
import subprocess
from pathlib import Path
from zipfile import ZipFile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'docs' / 'csv-manifest.json'
BACKUPS_DIR = ROOT / 'backups'

try:
    from shield256 import Shield256
except Exception as e:
    print('Shield import failed:', e)
    raise

if len(sys.argv) > 1:
    passphrase = sys.argv[1]
else:
    passphrase = None
    # fall back to env
    import os
    passphrase = os.environ.get('SHIELD_PASSPHRASE')

if not passphrase:
    print('Passphrase required (CLI arg or SHIELD_PASSPHRASE env)')
    raise SystemExit(1)

# create a fresh backup
print('Creating fresh backup...')
subprocess.run(['python','scripts/create_repo_backup.py'], check=True)
# find latest backup
backups = sorted(BACKUPS_DIR.glob('artifactvirtual-backup-*.zip'), key=lambda p: p.stat().st_mtime, reverse=True)
if not backups:
    print('No backup found after creation, aborting')
    raise SystemExit(1)
backup_zip = backups[0]
print('Backup created:', backup_zip)

# load manifest
m = json.load(open(MANIFEST))
sensitive = [Path(it['path']) for it in m if it.get('sensitive')]
print(f'Files to encrypt: {len(sensitive)}')
if not sensitive:
    print('No sensitive files found, nothing to do')
    raise SystemExit(0)

shield = Shield256()
shield.config['delete_original_after_encrypt'] = False
shield.config['dry_run'] = False

# keep copies of originals in temp dir for safety
tmpdir = Path(tempfile.mkdtemp(prefix='shield-'))
orig_copies = []
failed = False
try:
    for p in sensitive:
        full = ROOT / p
        if not full.exists():
            print('Missing file, skipping:', full)
            continue
        # copy original to temp
        tmp = tmpdir / p.name
        tmp.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(full, tmp)
        orig_copies.append((full, tmp))

        print('Encrypting', full)
        ok = shield.encrypt_file(full, passphrase)
        if not ok:
            print('Encryption failed for', full)
            failed = True
            break
        enc_path = full.with_suffix(full.suffix + '.enc')
        if not enc_path.exists():
            print('Encrypted file missing for', full)
            failed = True
            break
        # stage encrypted and remove plaintext from git
        subprocess.run(['git','add', str(enc_path)], check=True)
        subprocess.run(['git','rm','-f', str(full)], check=True)

    if failed:
        print('Failure during encryption; aborting and reverting staged changes')
        subprocess.run(['git','reset'], check=False)
        # restore originals from tmp copies
        for full, tmp in orig_copies:
            if not full.exists() and tmp.exists():
                shutil.copy2(tmp, full)
        raise SystemExit(1)

    # commit & push
    subprocess.run(['git','commit','-m','chore(shield): encrypt sensitive files and remove plaintext'], check=True)
    subprocess.run(['git','push','origin','main'], check=True)
    print('Encrypted files committed and pushed')

    # verification: extract backup and compare
    verify_tmp = Path(tempfile.mkdtemp(prefix='shield-verify-'))
    with ZipFile(backup_zip, 'r') as zf:
        zf.extractall(path=verify_tmp)
    for full, tmp in orig_copies:
        rel = full.relative_to(ROOT)
        orig_in_backup = verify_tmp / rel
        if not orig_in_backup.exists():
            print('Warning: original not found in backup for', full)
            continue
        # decrypt the encrypted file from repo to verify roundtrip
        enc_path = full.with_suffix(full.suffix + '.enc')
        # Copy .enc to tmpdir (preserving .enc extension so decrypt_file accepts it)
        verify_enc = tmpdir / enc_path.name
        shutil.copy2(enc_path, verify_enc)
        # decrypt_file writes plaintext to tmpdir/<stem> and deletes the .enc copy
        ok = shield.decrypt_file(verify_enc, passphrase)
        if not ok:
            print('Decryption failed for', enc_path)
            failed = True
            break
        # Compare restored plaintext with the backup original
        restored = tmpdir / Path(enc_path.name).stem
        if restored.exists():
            if restored.read_bytes() == orig_in_backup.read_bytes():
                print('Verified:', full)
            else:
                print('Verification mismatch for', full)
                failed = True
                break
        else:
            print('Expected restored file not found for', full)
            failed = True
            break

    if failed:
        print('Verification failed after push; abort and manual review required')
        raise SystemExit(1)
    else:
        print('Encryption and verification complete and pushed to origin/main')

finally:
    # cleanup temp dirs
    shutil.rmtree(tmpdir, ignore_errors=True)
    # remove verify tmp
    try:
        shutil.rmtree(verify_tmp, ignore_errors=True)
    except Exception:
        pass

print('Done')
