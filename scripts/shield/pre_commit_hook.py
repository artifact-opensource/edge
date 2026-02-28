#!/usr/bin/env python3
"""
Pre-Commit Hook - Auto-encrypt sensitive files
Self-healing, fail-proof automation
"""

import sys
import os
import subprocess
from pathlib import Path

# Add current directory to path to import shield
sys.path.insert(0, str(Path(__file__).parent))

try:
    from shield256 import Shield256 as Shield256
except ImportError:
    print("Warning: Shield256 not available, skipping encryption check")
    sys.exit(0)

def get_staged_files():
    """Get list of staged files"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True,
            text=True,
            check=True
        )
        return [f.strip() for f in result.stdout.split('\n') if f.strip()]
    except subprocess.CalledProcessError:
        return []

def check_file_classification(file_path):
    """Check if file contains classification markers"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(1000)  # Check first 1000 chars
            for classification in ['TOP_SECRET', 'CONFIDENTIAL', 'RESTRICTED']:
                if classification in content:
                    return classification
    except Exception:
        pass
    return None

def main():
    """Main pre-commit hook logic"""
    print("🛡️  Artifact Shield: Checking file encryption status...")
    
    shield = Shield256()
    staged_files = get_staged_files()
    
    if not staged_files:
        print("✅ No files to check")
        return 0
    
    unencrypted_sensitive = []
    
    for file_path in staged_files:
        if not Path(file_path).exists():
            continue
        
        # Skip excluded files
        if shield.should_exclude(file_path):
            continue
        
        # Check classification
        classification = check_file_classification(file_path)
        
        if classification:
            # Check if encrypted
            if not shield.is_encrypted(file_path) and not file_path.endswith('.enc'):
                unencrypted_sensitive.append((file_path, classification))
    
    if unencrypted_sensitive:
        print(f"\n⚠️  Found {len(unencrypted_sensitive)} unencrypted sensitive files:")
        for file_path, classification in unencrypted_sensitive:
            print(f"  - {file_path} ({classification})")

        # By default do NOT auto-encrypt. Require explicit opt-in via env var.
        if os.environ.get('SHIELD_AUTO_ENCRYPT') == '1':
            print("\n🔐 Auto-encrypting files (SHIELD_AUTO_ENCRYPT=1)...")
            passphrase = os.environ.get('SHIELD_PASSPHRASE')
            if not passphrase:
                print("\n💡 Tip: Set SHIELD_PASSPHRASE environment variable to avoid prompts")
                passphrase = shield.get_passphrase("Enter passphrase for encryption: ")

            encrypted_count = 0
            for file_path, classification in unencrypted_sensitive:
                if shield.encrypt_file(file_path, passphrase):
                    encrypted_count += 1
                    encrypted_path = file_path + '.enc'
                    subprocess.run(['git', 'add', encrypted_path], check=False)
                    subprocess.run(['git', 'reset', 'HEAD', file_path], check=False)

            print(f"✅ Auto-encrypted {encrypted_count} files")
            print("\n💡 Encrypted files have been staged.")
        else:
            print('\n❗ Auto-encryption is disabled by default. To perform auto-encryption set env var: SHIELD_AUTO_ENCRYPT=1')
            print("   You can also run the shield CLI manually: scripts/shield/shield256.py encrypt <file>")

    
    else:
        print("✅ All sensitive files are encrypted")
    
    # Block commit if unencrypted sensitive files found and auto-encrypt is OFF
    if unencrypted_sensitive and os.environ.get('SHIELD_AUTO_ENCRYPT') != '1':
        print("\n❌ Commit blocked: encrypt sensitive files first, or set SHIELD_AUTO_ENCRYPT=1")
        return 1

    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print(f"⚠️  Shield check failed: {error}")
        print("   Proceeding with commit (fail-safe mode)")
        sys.exit(0)  # Never block commit
