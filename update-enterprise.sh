#!/bin/bash
#
# Enterprise Update Script
# Single entry point for refreshing all enterprise data.
#
# Usage:
#   ./update-enterprise.sh              # dry-run (preview changes)
#   ./update-enterprise.sh --apply      # apply all changes
#   ./update-enterprise.sh --apply --skip-db   # skip database sync
#   ./update-enterprise.sh --apply --skip-csv  # skip CSV manifest regen
#

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found"
    exit 1
fi

cd "$SCRIPT_DIR"
python3 scripts/update_engine.py "$@"
ENGINE_EXIT=$?

# Fallback dashboard launch: if --apply was passed and engine succeeded,
# try opening the dashboard if the engine's webbrowser call didn't work.
if [[ " $* " == *" --apply "* ]] && [ $ENGINE_EXIT -eq 0 ]; then
    DASHBOARD="$SCRIPT_DIR/docs/enterprise-dashboard.html"
    if [ -f "$DASHBOARD" ]; then
        # Try platform-specific openers (silent fail is fine — engine already tried)
        if command -v xdg-open &> /dev/null; then
            xdg-open "$DASHBOARD" 2>/dev/null &
        elif command -v open &> /dev/null; then
            open "$DASHBOARD" 2>/dev/null &
        fi
    fi
fi

exit $ENGINE_EXIT
