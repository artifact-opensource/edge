#!/usr/bin/env bash
set -euo pipefail

if [ -z "${SHIELD_PASSPHRASE:-}" ]; then
  echo "ERROR: SHIELD_PASSPHRASE not set in environment. Export it and retry." >&2
  exit 2
fi

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <path> [--recursive] [--delete] [--dry-run]" >&2
  exit 2
fi

python toggle_encrypt.py "$@"