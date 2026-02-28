#!/bin/bash

#
# Copyright Tool Wrapper Script
# Easy-to-use wrapper for the copyright tool
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TOOL="$SCRIPT_DIR/copyright-tool.js"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       Artifact Virtual - Copyright Tool Wrapper               ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠️  Node.js is not installed. Please install Node.js to use this tool.${NC}"
    exit 1
fi

# Display quick menu if no arguments
if [ $# -eq 0 ]; then
    echo "Quick Actions:"
    echo ""
    echo "  1) Preview changes (dry-run) on current directory"
    echo "  2) Apply to current directory"
    echo "  3) Apply to entire repository"
    echo "  4) Show help"
    echo "  5) Run tests"
    echo ""
    read -p "Select an option (1-5): " option
    
    case $option in
        1)
            echo ""
            echo -e "${GREEN}Running dry-run on current directory...${NC}"
            node "$TOOL" --dry-run
            ;;
        2)
            echo ""
            echo -e "${YELLOW}⚠️  This will modify files in the current directory.${NC}"
            read -p "Continue? (y/N): " confirm
            if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
                node "$TOOL"
            else
                echo "Cancelled."
            fi
            ;;
        3)
            echo ""
            REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
            echo -e "${YELLOW}⚠️  This will modify ALL markdown files in: $REPO_ROOT${NC}"
            read -p "Continue? (y/N): " confirm
            if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
                node "$TOOL" --path "$REPO_ROOT"
            else
                echo "Cancelled."
            fi
            ;;
        4)
            node "$TOOL" --help
            ;;
        5)
            echo ""
            echo -e "${GREEN}Running test suite...${NC}"
            node "$SCRIPT_DIR/test-copyright-tool.js"
            ;;
        *)
            echo "Invalid option. Use --help for usage information."
            exit 1
            ;;
    esac
else
    # Pass through all arguments to the tool
    node "$TOOL" "$@"
fi

echo ""
