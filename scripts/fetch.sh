#!/bin/bash
# Fetch UPPERCASE markdown files into ./data (scans entire repo root and subdirectories)
# Only copies files where filename starts with an uppercase letter (A-Z)
# Usage: From repo root:  ./scripts/fetch.sh
#        From scripts dir: ./fetch.sh
# Requires: bash 4+

# Don't exit on error (arithmetic operations can return 1)
# set -e

# Resolve script and repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$REPO_ROOT/data"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

# Counters
COPIED=0
SKIPPED=0
LOWERCASE_SKIPPED=0
ERRORS=0

# Ensure data dir exists (create or prompt)
if [ ! -d "$DATA_DIR" ]; then
    mkdir -p "$DATA_DIR"
    echo -e "${GREEN}Created directory: $DATA_DIR${NC}"
else
    read -p "Directory '$DATA_DIR' already exists. Use it? [Y/N] (Default: Y): " resp
    if [[ "$resp" =~ ^[Nn]$ ]]; then
        read -p "Enter new data directory name (will be created in repo root): " newName
        if [ -z "$newName" ]; then
            echo -e "${RED}Aborting.${NC}"
            exit 1
        fi
        DATA_DIR="$REPO_ROOT/$newName"
        if [ ! -d "$DATA_DIR" ]; then
            mkdir -p "$DATA_DIR"
            echo -e "${GREEN}Created directory: $DATA_DIR${NC}"
        else
            echo "Using existing: $DATA_DIR"
        fi
    else
        echo "Using existing: $DATA_DIR"
    fi
fi

# Overwrite behavior selection
read -p "If destination files exist, choose: [O]verwrite / [S]kip existing / [A]ll overwrite / [K]eep existing (default: O): " option
option="${option^^}"  # uppercase
OVERWRITE_ALL=false
SKIP_EXISTING=false

case "$option" in
    A|O|"")
        OVERWRITE_ALL=true
        ;;
    S|K)
        SKIP_EXISTING=true
        ;;
    *)
        OVERWRITE_ALL=true
        ;;
esac

# Find all markdown files in repo (exclude data dir, .git, node_modules)
echo -e "${CYAN}Scanning for markdown files...${NC}"

# Use find to get all .md and .markdown files
while IFS= read -r -d '' file; do
    # Get just the filename
    filename=$(basename "$file")
    
    # Get first character
    first_char="${filename:0:1}"
    
    # Skip files starting with lowercase letter (only copy UPPERCASE)
    if [[ "$first_char" =~ ^[a-z]$ ]]; then
        LOWERCASE_SKIPPED=$((LOWERCASE_SKIPPED + 1))
        echo -e "  ${GRAY}Skipping lowercase: $filename${NC}"
        continue
    fi
    
    # Get relative path from repo root
    relative="${file#$REPO_ROOT/}"
    
    # Destination path
    dest_path="$DATA_DIR/$relative"
    dest_dir=$(dirname "$dest_path")
    
    # Create destination directory if needed
    mkdir -p "$dest_dir"
    
    # Copy logic
    if [ -f "$dest_path" ]; then
        if [ "$OVERWRITE_ALL" = true ]; then
            if cp "$file" "$dest_path" 2>/dev/null; then
                echo -e "  ${GREEN}Copied (overwrite): $relative${NC}"
                COPIED=$((COPIED + 1))
            else
                echo -e "  ${RED}Error copying: $relative${NC}"
                ERRORS=$((ERRORS + 1))
            fi
        elif [ "$SKIP_EXISTING" = true ]; then
            SKIPPED=$((SKIPPED + 1))
        else
            read -p "File exists: $dest_path. Overwrite? [Y/N]: " r
            if [[ "$r" =~ ^[Yy]$ ]]; then
                if cp "$file" "$dest_path" 2>/dev/null; then
                    COPIED=$((COPIED + 1))
                else
                    ERRORS=$((ERRORS + 1))
                fi
            else
                SKIPPED=$((SKIPPED + 1))
            fi
        fi
    else
        if cp "$file" "$dest_path" 2>/dev/null; then
            echo -e "  ${GREEN}Copied: $relative${NC}"
            COPIED=$((COPIED + 1))
        else
            echo -e "  ${RED}Error copying: $relative${NC}"
            ERRORS=$((ERRORS + 1))
        fi
    fi
done < <(find "$REPO_ROOT" -type f \( -name "*.md" -o -name "*.markdown" \) \
    ! -path "$DATA_DIR/*" \
    ! -path "*/.git/*" \
    ! -path "*/node_modules/*" \
    -print0 2>/dev/null)

echo ""
echo -e "${CYAN}========== SUMMARY ==========${NC}"
echo -e "${GREEN}Copied:              $COPIED${NC}"
echo -e "${YELLOW}Skipped (exists):    $SKIPPED${NC}"
echo -e "${GRAY}Skipped (lowercase): $LOWERCASE_SKIPPED${NC}"
echo -e "${RED}Errors:              $ERRORS${NC}"
echo -e "${CYAN}=============================${NC}"
