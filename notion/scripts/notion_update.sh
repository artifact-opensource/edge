#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# Artifact Virtual — Notion Update (one-click)
#
# Updates local databases from repository, then syncs everything
# to the Notion workspace (Community Portal + Stakeholder Portal).
#
# Prerequisites:
#   export NOTION_API_KEY="secret_…"
#   export NOTION_PARENT_PAGE_ID="…"
#
# Usage:
#   ./notion/scripts/notion_update.sh              # full sync
#   ./notion/scripts/notion_update.sh --dry-run    # test run
#   ./notion/scripts/notion_update.sh --skip-db-update  # only push to Notion
#   ./notion/scripts/notion_update.sh --populate-only   # only refill DBs
# ─────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load .env if present (repo root or notion/)
for env_file in "$SCRIPT_DIR/../../.env" "$SCRIPT_DIR/../.env"; do
    if [[ -f "$env_file" ]]; then
        set -a; source "$env_file"; set +a
    fi
done

# Validate
if [[ -z "${NOTION_API_KEY:-}" ]]; then
    echo "ERROR: NOTION_API_KEY not set. Export it or add to .env"
    exit 1
fi
if [[ -z "${NOTION_PARENT_PAGE_ID:-}" ]]; then
    echo "ERROR: NOTION_PARENT_PAGE_ID not set. Export it or add to .env"
    exit 1
fi

exec python3 "$SCRIPT_DIR/notion_sync.py" "$@"
