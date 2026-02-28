#!/usr/bin/env python3
"""
Artifact Virtual Shield256 — AES-256-GCM Authenticated Encryption
=================================================================

Replaces the legacy XOR-based "Quantum Shield" with real cryptography.

Cipher:    AES-256-GCM (authenticated encryption with associated data)
KDF:       scrypt (memory-hard, CPU-hard — resistant to brute-force)
Nonce:     96-bit random per encryption (as recommended by NIST SP 800-38D)
Salt:      32-byte random per encryption (unique key derivation per file)
Integrity: GCM tag provides authentication — tampered ciphertext is rejected
Format:    SHIELD256::v1::<salt_hex>::<nonce_hex>::<ciphertext+tag>

This module is a drop-in replacement for quantum_shield.py.
All existing QuantumShield call sites work unchanged.

Copyright (c) 2025-2026 Artifact Virtual (SMC-Private) Limited
"""

import json
import os
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidTag

# ── Configuration ────────────────────────────────────────────────────────────

SHIELD_DIR = Path.home() / ".artifact_shield"
CONFIG_FILE = SHIELD_DIR / "config.json"
AUDIT_LOG = SHIELD_DIR / "audit.log"

ENCRYPTION_MARKER = b"SHIELD256"
FORMAT_VERSION = b"v1"

# scrypt parameters — OWASP recommended for 2024+
# N=2^17 (~128 MiB memory), r=8, p=1
SCRYPT_N = 2**17
SCRYPT_R = 8
SCRYPT_P = 1
SCRYPT_KEY_LENGTH = 32  # AES-256

SALT_LENGTH = 32  # bytes
NONCE_LENGTH = 12  # 96-bit GCM nonce (NIST recommended)


# ── Shield256 Class ──────────────────────────────────────────────────────────

class Shield256:
    """AES-256-GCM authenticated encryption with scrypt key derivation."""

    def __init__(self):
        self.ensure_shield_directory()
        self.config = self.load_or_create_config()

    # ── Setup ────────────────────────────────────────────────────────────

    def ensure_shield_directory(self):
        """Create shield config directory if missing."""
        SHIELD_DIR.mkdir(parents=True, exist_ok=True)
        gitignore = SHIELD_DIR / ".gitignore"
        if not gitignore.exists():
            gitignore.write_text("*\n!.gitignore\n")

    def load_or_create_config(self) -> dict:
        """Load or create default configuration."""
        try:
            if CONFIG_FILE.exists():
                return json.loads(CONFIG_FILE.read_text())
        except Exception as e:
            self.log_event(f"Config load failed: {e}")

        default = {
            "version": "2.0.0",
            "cipher": "AES-256-GCM",
            "kdf": "scrypt",
            "min_key_length": 16,
            "max_key_length": 1000,
            "auto_encrypt": False,
            "delete_original_after_encrypt": False,
            "classifications": ["TOP_SECRET", "CONFIDENTIAL", "RESTRICTED"],
            "exclude_patterns": [
                ".shield", "backups", "scripts/shield",
                "node_modules", ".git", "__pycache__",
            ],
            "encryption_marker": "SHIELD256",
            "dry_run": False,
        }

        try:
            CONFIG_FILE.write_text(json.dumps(default, indent=2))
        except Exception as e:
            self.log_event(f"Config save failed: {e}")

        return default

    # ── Logging ──────────────────────────────────────────────────────────

    def log_event(self, message: str):
        """Append to audit log. Never raises."""
        try:
            ts = datetime.now(timezone.utc).isoformat()
            with open(AUDIT_LOG, "a") as f:
                f.write(f"{ts} | {message}\n")
        except Exception:
            pass

    # ── Core Crypto ──────────────────────────────────────────────────────

    @staticmethod
    def _derive_key(passphrase: str, salt: bytes) -> bytes:
        """Derive a 256-bit key from passphrase using scrypt.

        scrypt is memory-hard: an attacker cannot speed up brute-force
        by using GPUs/ASICs without proportionally more RAM.
        """
        kdf = Scrypt(
            salt=salt,
            length=SCRYPT_KEY_LENGTH,
            n=SCRYPT_N,
            r=SCRYPT_R,
            p=SCRYPT_P,
        )
        return kdf.derive(passphrase.encode("utf-8"))

    def encrypt_data(self, plaintext: bytes, passphrase: str) -> bytes:
        """Encrypt plaintext using AES-256-GCM with a fresh salt and nonce.

        Returns: SHIELD256::v1::<salt_hex>::<nonce_hex>::<ciphertext+tag>
        """
        salt = secrets.token_bytes(SALT_LENGTH)
        nonce = secrets.token_bytes(NONCE_LENGTH)
        key = self._derive_key(passphrase, salt)

        aesgcm = AESGCM(key)
        # GCM appends a 16-byte authentication tag to the ciphertext
        ciphertext_with_tag = aesgcm.encrypt(nonce, plaintext, associated_data=None)

        # Build package
        package = (
            ENCRYPTION_MARKER + b"::"
            + FORMAT_VERSION + b"::"
            + salt.hex().encode() + b"::"
            + nonce.hex().encode() + b"::"
            + ciphertext_with_tag
        )
        return package

    def decrypt_data(self, package: bytes, passphrase: str) -> bytes:
        """Decrypt a Shield256 package.

        Returns plaintext bytes.
        Raises ValueError if the package is malformed.
        Raises cryptography.exceptions.InvalidTag if the passphrase is wrong
        or the ciphertext has been tampered with. NEVER silently returns None.
        """
        parts = package.split(b"::", 4)
        if len(parts) != 5:
            self.log_event("Decrypt failed: invalid package format")
            raise ValueError("Invalid Shield256 package format")

        marker, version, salt_hex, nonce_hex, ciphertext_with_tag = parts

        if marker != ENCRYPTION_MARKER:
            self.log_event("Decrypt failed: wrong marker")
            raise ValueError(f"Wrong encryption marker: {marker}")

        salt = bytes.fromhex(salt_hex.decode())
        nonce = bytes.fromhex(nonce_hex.decode())
        key = self._derive_key(passphrase, salt)

        aesgcm = AESGCM(key)
        # InvalidTag will propagate — this is intentional.
        # Callers MUST handle authentication failures explicitly.
        plaintext = aesgcm.decrypt(nonce, ciphertext_with_tag, associated_data=None)
        return plaintext

    # ── Legacy Compatibility ─────────────────────────────────────────────

    def _is_legacy_encrypted(self, data: bytes) -> bool:
        """Check if data uses the old XOR-based format."""
        return data.startswith(b"ARTIFACT_SHIELD_ENCRYPTED::")

    def decrypt_legacy(self, package: bytes, passphrase: str) -> bytes | None:
        """Decrypt legacy Quantum Shield XOR format for migration.

        This exists solely to allow migrating old .enc files to Shield256.
        """
        try:
            import hashlib
            parts = package.split(b"::", 3)
            if len(parts) != 4:
                return None

            _marker, _version, salt_bytes, encrypted = parts
            file_salt = salt_bytes.decode("utf-8")

            # Legacy key derivation
            combined = f"{passphrase}::{file_salt}".encode("utf-8")
            r1 = hashlib.sha3_512(combined).digest()
            r2 = hashlib.blake2b(r1, digest_size=64).digest()
            key = hashlib.sha512(r2).digest()

            # Reverse legacy encryption layers
            data = bytearray(encrypted)
            klen = len(key)
            for i in range(len(data)):
                data[i] ^= (i + 1) % 256
            for i in range(len(data) - 1, -1, -1):
                data[i] ^= key[(len(data) - i - 1) % klen]
            for i in range(len(data)):
                data[i] ^= key[i % klen]

            return bytes(data)
        except Exception:
            return None

    # ── File Operations ──────────────────────────────────────────────────

    def is_encrypted(self, file_path) -> bool:
        """Check if a file is encrypted (Shield256 or legacy)."""
        try:
            with open(file_path, "rb") as f:
                header = f.read(120)
            return (
                header.startswith(ENCRYPTION_MARKER + b"::")
                or header.startswith(b"ARTIFACT_SHIELD_ENCRYPTED::")
            )
        except Exception:
            return False

    def should_exclude(self, file_path) -> bool:
        """Check if file should be excluded from encryption operations."""
        s = str(file_path)
        for pattern in self.config.get("exclude_patterns", []):
            if pattern in s:
                return True
        if s.endswith("shield256.py") or s.endswith("quantum_shield.py"):
            return True
        return False

    def encrypt_file(self, file_path, passphrase: str) -> bool:
        """Encrypt a single file → file.enc"""
        try:
            file_path = Path(file_path)

            if self.should_exclude(file_path):
                self.log_event(f"Skipped (excluded): {file_path}")
                return False

            if self.is_encrypted(file_path):
                self.log_event(f"Already encrypted: {file_path}")
                return True

            plaintext = file_path.read_bytes()
            encrypted = self.encrypt_data(plaintext, passphrase)

            enc_path = file_path.parent / (file_path.name + ".enc")
            enc_path.write_bytes(encrypted)

            if self.config.get("delete_original_after_encrypt") and not self.config.get("dry_run"):
                try:
                    file_path.unlink()
                except Exception as e:
                    self.log_event(f"Failed to remove original {file_path}: {e}")

            self.log_event(f"Encrypted: {file_path} -> {enc_path}")
            return True

        except Exception as e:
            self.log_event(f"Encryption error for {file_path}: {e}")
            return False

    def decrypt_file(self, file_path, passphrase: str) -> bool:
        """Decrypt a .enc file → original filename."""
        try:
            file_path = Path(file_path)
            if not str(file_path).endswith(".enc"):
                print(f"Not an encrypted file: {file_path}")
                return False

            data = file_path.read_bytes()

            plaintext = None

            # Try Shield256 format first
            try:
                plaintext = self.decrypt_data(data, passphrase)
            except (InvalidTag, ValueError):
                pass  # Fall through to legacy attempt

            # Fall back to legacy format for migration
            if plaintext is None and self._is_legacy_encrypted(data):
                self.log_event(f"Attempting legacy decryption: {file_path}")
                plaintext = self.decrypt_legacy(data, passphrase)
                if plaintext is not None:
                    self.log_event(f"Legacy decryption succeeded: {file_path}")

            if plaintext is None:
                print(f"Decryption failed: {file_path} (wrong passphrase or corrupted)")
                return False

            original_path = file_path.parent / file_path.stem  # strip .enc
            original_path.write_bytes(plaintext)
            file_path.unlink()

            self.log_event(f"Decrypted: {file_path} -> {original_path}")
            return True

        except Exception as e:
            self.log_event(f"Decryption error for {file_path}: {e}")
            return False

    def migrate_file(self, file_path, passphrase: str) -> bool:
        """Migrate a legacy .enc file to Shield256 format in-place."""
        try:
            file_path = Path(file_path)
            data = file_path.read_bytes()

            if not self._is_legacy_encrypted(data):
                if data.startswith(ENCRYPTION_MARKER + b"::"):
                    self.log_event(f"Already Shield256: {file_path}")
                    return True
                self.log_event(f"Not encrypted: {file_path}")
                return False

            plaintext = self.decrypt_legacy(data, passphrase)
            if plaintext is None:
                self.log_event(f"Legacy decrypt failed during migration: {file_path}")
                return False

            new_encrypted = self.encrypt_data(plaintext, passphrase)
            file_path.write_bytes(new_encrypted)
            self.log_event(f"Migrated to Shield256: {file_path}")
            return True

        except Exception as e:
            self.log_event(f"Migration error for {file_path}: {e}")
            return False

    def scan_and_encrypt_directory(self, directory, passphrase: str, classification=None):
        """Scan a directory and encrypt files matching criteria."""
        directory = Path(directory)
        encrypted_count = 0
        skipped_count = 0

        for file_path in sorted(directory.rglob("*")):
            if not file_path.is_file():
                continue

            if classification:
                try:
                    content = file_path.read_text(errors="ignore")[:500]
                    if classification not in content:
                        continue
                except Exception:
                    continue

            if self.encrypt_file(file_path, passphrase):
                encrypted_count += 1
            else:
                skipped_count += 1

        return encrypted_count, skipped_count

    # ── Passphrase Input ─────────────────────────────────────────────────

    def get_passphrase(self, prompt: str = "Enter passphrase: ") -> str:
        """Get passphrase from user with validation."""
        import getpass

        min_len = self.config.get("min_key_length", 12)
        max_len = self.config.get("max_key_length", 1000)

        while True:
            p = getpass.getpass(prompt)
            if len(p) < min_len:
                print(f"Passphrase too short (minimum {min_len} characters)")
                continue
            if len(p) > max_len:
                print(f"Passphrase too long (maximum {max_len} characters)")
                continue
            return p

    # ── CLI ──────────────────────────────────────────────────────────────

    def display_banner(self):
        print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     ARTIFACT VIRTUAL SHIELD256                                ║
║     AES-256-GCM Authenticated Encryption                      ║
║     scrypt Key Derivation                                     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
""")

    def display_menu(self):
        print("""
  [1] Encrypt File
  [2] Decrypt File
  [3] Encrypt Directory
  [4] Encrypt by Classification
  [5] Migrate Legacy .enc Files
  [6] Check Status
  [7] View Audit Log
  [8] Configuration
  [0] Exit
""")

    def run_interactive(self):
        self.display_banner()
        while True:
            self.display_menu()
            choice = input("Select option: ").strip()

            if choice == "0":
                print("Shield deactivated.")
                break
            elif choice == "1":
                fp = input("File path: ").strip()
                if not Path(fp).exists():
                    print("File not found"); continue
                pw = self.get_passphrase("Passphrase for encryption: ")
                ok = self.encrypt_file(fp, pw)
                print("Encrypted." if ok else "Failed.")
            elif choice == "2":
                fp = input("Encrypted file path (.enc): ").strip()
                if not Path(fp).exists():
                    print("File not found"); continue
                pw = self.get_passphrase("Passphrase for decryption: ")
                ok = self.decrypt_file(fp, pw)
                print("Decrypted." if ok else "Failed.")
            elif choice == "3":
                d = input("Directory: ").strip()
                if not Path(d).exists():
                    print("Not found"); continue
                pw = self.get_passphrase()
                enc, skip = self.scan_and_encrypt_directory(d, pw)
                print(f"Encrypted: {enc}, Skipped: {skip}")
            elif choice == "4":
                for i, c in enumerate(self.config["classifications"], 1):
                    print(f"  [{i}] {c}")
                ci = input("Classification #: ").strip()
                try:
                    cls = self.config["classifications"][int(ci) - 1]
                except (ValueError, IndexError):
                    print("Invalid"); continue
                d = input("Directory (default .): ").strip() or "."
                pw = self.get_passphrase()
                enc, _ = self.scan_and_encrypt_directory(d, pw, cls)
                print(f"Encrypted {enc} {cls} files.")
            elif choice == "5":
                d = input("Directory with legacy .enc files: ").strip() or "."
                pw = self.get_passphrase("Legacy passphrase: ")
                migrated = 0
                for f in sorted(Path(d).rglob("*.enc")):
                    if self.migrate_file(f, pw):
                        migrated += 1
                print(f"Migrated {migrated} files to Shield256.")
            elif choice == "6":
                d = Path(input("Directory (default .): ").strip() or ".")
                enc_files = sum(1 for f in d.rglob("*.enc") if f.is_file())
                print(f"Encrypted files: {enc_files}")
            elif choice == "7":
                if AUDIT_LOG.exists():
                    lines = AUDIT_LOG.read_text().splitlines()
                    for line in lines[-20:]:
                        print(f"  {line}")
                else:
                    print("No audit log.")
            elif choice == "8":
                print(json.dumps(self.config, indent=2))

            input("\nPress Enter...")
            print()


# ── Backward-compatible alias ────────────────────────────────────────────────
# All existing code that does `from quantum_shield import QuantumShield` or
# `from shield256 import Shield256` will work.
QuantumShield = Shield256


def main():
    shield = Shield256()

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "encrypt" and len(sys.argv) > 2:
            pw = os.environ.get("SHIELD_PASSPHRASE") or shield.get_passphrase()
            shield.encrypt_file(sys.argv[2], pw)
        elif cmd == "decrypt" and len(sys.argv) > 2:
            pw = os.environ.get("SHIELD_PASSPHRASE") or shield.get_passphrase()
            shield.decrypt_file(sys.argv[2], pw)
        elif cmd == "migrate":
            d = sys.argv[2] if len(sys.argv) > 2 else "."
            pw = os.environ.get("SHIELD_PASSPHRASE") or shield.get_passphrase()
            migrated = 0
            for f in sorted(Path(d).rglob("*.enc")):
                if shield.migrate_file(f, pw):
                    migrated += 1
            print(f"Migrated {migrated} files.")
        elif cmd == "status":
            d = sys.argv[2] if len(sys.argv) > 2 else "."
            enc = sum(1 for f in Path(d).rglob("*.enc") if f.is_file())
            print(f"Encrypted files in {d}: {enc}")
        else:
            print("Usage: shield256.py [encrypt|decrypt|migrate|status] <path>")
    else:
        shield.run_interactive()


if __name__ == "__main__":
    main()
