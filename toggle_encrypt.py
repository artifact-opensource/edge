#!/usr/bin/env python3
"""toggle_encrypt.py

Usage: toggle_encrypt.py <path> [--recursive] [--delete] [--dry-run]

This script uses the local Shield256 implementation to:
- Encrypt files that are not encrypted
- Decrypt files that are encrypted (detected by extension or marker)

Passphrase is taken from the environment variable `SHIELD_PASSPHRASE`.
"""

import argparse
import os
import sys
from pathlib import Path

from scripts.shield.shield256 import Shield256 as Shield256
from cryptography.exceptions import InvalidTag


def error(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


def main():
    parser = argparse.ArgumentParser(description='Toggle encryption on path(s) using Shield256')
    parser.add_argument('path', nargs='?', default='.', help='File or directory to toggle')
    parser.add_argument('--recursive', '-r', action='store_true', help='Recurse into directories')
    parser.add_argument('--delete', action='store_true', help='Delete original file after encryption')
    parser.add_argument('--dry-run', action='store_true', help="Don't write changes; show what would happen")

    args = parser.parse_args()

    passphrase = os.environ.get('SHIELD_PASSPHRASE')
    if not passphrase:
        error('Environment variable SHIELD_PASSPHRASE is not set. Export it and retry.')

    shield = Shield256()
    shield.config['dry_run'] = args.dry_run
    shield.config['delete_original_after_encrypt'] = args.delete

    target = Path(args.path)

    if not target.exists():
        error(f'Path not found: {target}')

    def process_file(file_path: Path):
        # Skip excluded files
        if shield.should_exclude(file_path):
            print(f'  Skipping (excluded): {file_path}')
            return

        # If it's an .enc file -> decrypt
        if str(file_path).endswith('.enc') or shield.is_encrypted(file_path):
            # If it's already an .enc file, use decrypt_file
            if str(file_path).endswith('.enc'):
                print(f'  Decrypting: {file_path}')
                if not args.dry_run:
                    ok = shield.decrypt_file(file_path, passphrase)
                    print('    OK' if ok else '    FAIL')
            else:
                # File contains encrypted marker but not .enc -- try to decrypt in place
                print(f'  Decrypting (in-place): {file_path}')
                if not args.dry_run:
                    data = file_path.read_bytes()
                    try:
                        plaintext = shield.decrypt_data(data, passphrase)
                    except InvalidTag:
                        print('    FAIL: wrong passphrase or tampered ciphertext')
                        return
                    except ValueError as e:
                        print(f'    FAIL: {e}')
                        return
                    bak = file_path.with_suffix(file_path.suffix + '.enc.bak')
                    file_path.replace(bak)
                    file_path.write_bytes(plaintext)
                    print('    OK (backup written to %s)' % bak)
        else:
            # Encrypt plaintext file
            print(f'  Encrypting: {file_path}')
            if not args.dry_run:
                ok = shield.encrypt_file(file_path, passphrase)
                print('    OK' if ok else '    FAIL')

    # If target is directory
    if target.is_dir():
        if not args.recursive:
            # Only operate on top-level files
            for f in sorted(target.iterdir()):
                if f.is_file():
                    process_file(f)
        else:
            for f in sorted(target.rglob('*')):
                if f.is_file():
                    process_file(f)
    else:
        process_file(target)

    return 0


if __name__ == '__main__':
    sys.exit(main())
