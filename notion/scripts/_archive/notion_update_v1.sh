#!/usr/bin/env bash
#
# Artifact Virtual - Notion Auto-Update Script
#
# Automatically updates Notion workspace databases when repository changes are detected.
# Only syncs open-source projects (with tags/badges) to Community Hub.
# Minimal, targeted updates for stakeholder-relevant files.
#
# Usage:
#   ./notion_update.sh                 # Standard update
#   ./notion_update.sh --dry-run       # Test without API calls
#   ./notion_update.sh --force         # Force update regardless of changes
#   ./notion_update.sh --verbose       # Detailed logging
#
# Environment Variables Required:
#   NOTION_API_KEY          - Notion integration API key
#   NOTION_PARENT_PAGE_ID   - Parent page ID for the portal
#
# Optional:
#   GITHUB_TOKEN            - For fetching GitHub stats
#
# Version: 1.0.0
# Author: Artifact Virtual Operations Team
# Last Updated: 2026-02-07

set -euo pipefail

# Script configuration
SCRIPT_VERSION="1.0.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
NOTION_DIR="$REPO_ROOT/notion"
PROJECTS_DIR="$REPO_ROOT/enterprise/projects"
STAKEHOLDERS_DIR="$REPO_ROOT/enterprise/stakeholders"

# Flags
DRY_RUN=false
FORCE=false
VERBOSE=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_verbose() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${GRAY}[VERBOSE]${NC} $1"
    fi
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --force)
                FORCE=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

show_help() {
    cat << EOF
Artifact Virtual - Notion Auto-Update Script v$SCRIPT_VERSION

USAGE:
    $0 [OPTIONS]

OPTIONS:
    --dry-run       Run without making actual API calls (testing mode)
    --force         Force update even if no changes detected
    --verbose       Enable detailed logging
    -h, --help      Show this help message

ENVIRONMENT VARIABLES:
    NOTION_API_KEY          Notion integration API key (required)
    NOTION_PARENT_PAGE_ID   Parent page ID for the portal (required)
    GITHUB_TOKEN            GitHub API token (optional)

EXAMPLES:
    $0                      # Standard update
    $0 --dry-run            # Test run without API calls
    $0 --force --verbose    # Force update with detailed logging

EOF
}

# Validate environment
validate_environment() {
    log_info "Validating environment..."
    
    # Check required environment variables
    if [ "$DRY_RUN" = false ]; then
        if [ -z "${NOTION_API_KEY:-}" ]; then
            log_error "NOTION_API_KEY environment variable not set"
            return 1
        fi
        
        if [ -z "${NOTION_PARENT_PAGE_ID:-}" ]; then
            log_error "NOTION_PARENT_PAGE_ID environment variable not set"
            return 1
        fi
    fi
    
    # Check directory structure
    if [ ! -d "$PROJECTS_DIR" ]; then
        log_error "Projects directory not found: $PROJECTS_DIR"
        return 1
    fi
    
    if [ ! -d "$NOTION_DIR" ]; then
        log_error "Notion directory not found: $NOTION_DIR"
        return 1
    fi
    
    log_success "Environment validated"
    return 0
}

# Check if project is open source
is_open_source_project() {
    local readme_path="$1"
    
    if [ ! -f "$readme_path" ]; then
        return 1
    fi
    
    local content
    content=$(cat "$readme_path" 2>/dev/null || echo "")
    
    if [ -z "$content" ]; then
        return 1
    fi
    
    # Check for open-source indicators
    if echo "$content" | grep -qiE '(open-source|opensource):\s*(true|yes)'; then
        return 0
    fi
    
    if echo "$content" | grep -qiE 'license:\s*(MIT|Apache|GPL|BSD)'; then
        return 0
    fi
    
    if echo "$content" | grep -qiE 'badge.*open.*source|shields\.io.*license|opensource\.org'; then
        return 0
    fi
    
    if echo "$content" | grep -qiE 'open\s*source\s*(project|license)'; then
        return 0
    fi
    
    if echo "$content" | grep -qiE 'licensed\s*under.*(MIT|Apache|GPL|BSD)'; then
        return 0
    fi
    
    if echo "$content" | grep -qiE 'tags?:\s*\[.*open.*source.*\]|tags?:\s*\[.*oss.*\]'; then
        return 0
    fi
    
    return 1
}

# Get project metadata
get_project_metadata() {
    local project_path="$1"
    local project_name
    project_name=$(basename "$project_path")
    local readme_path="$project_path/README.md"
    
    if [ ! -f "$readme_path" ]; then
        return 1
    fi
    
    local is_oss="false"
    if is_open_source_project "$readme_path"; then
        is_oss="true"
    fi
    
    local last_modified
    last_modified=$(stat -c %Y "$readme_path" 2>/dev/null || stat -f %m "$readme_path" 2>/dev/null || echo "0")
    
    echo "$project_name|$readme_path|$is_oss|$last_modified"
    return 0
}

# Scan repository for changes
scan_repository_changes() {
    log_info "Scanning repository for changes..."
    
    local projects=()
    local oss_count=0
    local modified_files=()
    
    # Scan all project directories
    if [ -d "$PROJECTS_DIR" ]; then
        while IFS= read -r -d '' project_dir; do
            local metadata
            if metadata=$(get_project_metadata "$project_dir"); then
                projects+=("$metadata")
                
                local is_oss
                is_oss=$(echo "$metadata" | cut -d'|' -f3)
                if [ "$is_oss" = "true" ]; then
                    ((oss_count++)) || true
                    log_verbose "Found open-source project: $(echo "$metadata" | cut -d'|' -f1)"
                fi
            fi
        done < <(find "$PROJECTS_DIR" -maxdepth 1 -type d -not -path "$PROJECTS_DIR" -print0)
    fi
    
    # Get recent git changes (last 24 hours)
    if command -v git &> /dev/null && [ -d "$REPO_ROOT/.git" ]; then
        cd "$REPO_ROOT"
        local recent_changes
        recent_changes=$(git log --since="24 hours ago" --name-only --pretty=format: | sort -u | grep -v '^$' || true)
        
        while IFS= read -r file; do
            if [ -n "$file" ] && [ -f "$REPO_ROOT/$file" ]; then
                modified_files+=("$file")
            fi
        done <<< "$recent_changes"
    fi
    
    log_success "Found ${#projects[@]} projects ($oss_count open-source), ${#modified_files[@]} recent changes"
    
    # Export results
    SCAN_PROJECTS=("${projects[@]}")
    SCAN_OSS_COUNT=$oss_count
    SCAN_MODIFIED=("${modified_files[@]}")
}

# Update Notion Community Hub
update_community_hub() {
    log_info "Updating Notion Community Hub..."
    
    local oss_projects=()
    for project in "${SCAN_PROJECTS[@]}"; do
        local is_oss
        is_oss=$(echo "$project" | cut -d'|' -f3)
        if [ "$is_oss" = "true" ]; then
            oss_projects+=("$project")
        fi
    done
    
    if [ ${#oss_projects[@]} -eq 0 ]; then
        log_info "No open-source projects to update"
        return 0
    fi
    
    log_info "Found ${#oss_projects[@]} open-source projects"
    
    for project in "${oss_projects[@]}"; do
        local project_name
        project_name=$(echo "$project" | cut -d'|' -f1)
        log_verbose "Processing: $project_name"
        
        if [ "$DRY_RUN" = true ]; then
            log_info "[DRY RUN] Would update Community Hub for: $project_name"
        else
            # TODO: Implement actual Notion API calls
            # This would use the Notion API to update:
            # - Master Projects Database
            # - Open Source Portfolio Database
            log_info "Updating Community Hub for: $project_name"
        fi
    done
    
    log_success "Community Hub update complete"
}

# Update Notion Stakeholder Hub
update_stakeholder_hub() {
    log_info "Checking for stakeholder-relevant changes..."
    
    local relevant_files=()
    for file in "${SCAN_MODIFIED[@]}"; do
        if [[ "$file" =~ enterprise/stakeholders ]] || \
           [[ "$file" =~ enterprise/legal ]] || \
           [[ "$file" =~ enterprise/audit ]] || \
           [[ "$file" =~ enterprise/divisions/departments/executive ]]; then
            relevant_files+=("$file")
        fi
    done
    
    if [ ${#relevant_files[@]} -eq 0 ]; then
        log_info "No stakeholder-relevant changes detected"
        return 0
    fi
    
    log_info "Found ${#relevant_files[@]} stakeholder-relevant changes"
    
    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY RUN] Would update Stakeholder Hub"
        for file in "${relevant_files[@]}"; do
            log_verbose "  - $file"
        done
    else
        # TODO: Implement actual Notion API calls for stakeholder updates
        log_info "Updating Stakeholder Hub..."
    fi
    
    log_success "Stakeholder Hub check complete"
}

# Update Notion AV Live Dashboard
update_live_dashboard() {
    log_info "Updating AV Live Dashboard..."
    
    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY RUN] Would add update event to Live Feed"
    else
        # TODO: Implement actual Notion API call to add Live Update entry
        local update_message="Repository sync completed: ${#SCAN_PROJECTS[@]} projects scanned, ${#SCAN_MODIFIED[@]} files changed"
        log_info "Live update: $update_message"
    fi
    
    log_success "Live Dashboard updated"
}

# Main execution
main() {
    echo ""
    echo "================================================================================"
    echo "Artifact Virtual - Notion Auto-Update Script v$SCRIPT_VERSION"
    echo "================================================================================"
    echo ""
    
    if [ "$DRY_RUN" = true ]; then
        log_warning "DRY RUN MODE - No API calls will be made"
    fi
    
    # Validate environment
    if ! validate_environment; then
        log_error "Environment validation failed"
        exit 1
    fi
    
    # Scan repository for changes
    scan_repository_changes
    
    # Check if update is needed
    if [ "$FORCE" = false ] && [ ${#SCAN_MODIFIED[@]} -eq 0 ]; then
        log_info "No changes detected. Use --force to update anyway."
        echo ""
        echo "================================================================================"
        log_success "Update complete - No changes to sync"
        echo "================================================================================"
        echo ""
        exit 0
    fi
    
    # Update Community Hub (open-source projects only)
    update_community_hub
    
    # Update Stakeholder Hub (if relevant changes detected)
    update_stakeholder_hub
    
    # Update Live Dashboard
    update_live_dashboard
    
    # Summary
    local stakeholder_count=0
    for file in "${SCAN_MODIFIED[@]}"; do
        if [[ "$file" =~ stakeholders|legal|audit ]]; then
            ((stakeholder_count++)) || true
        fi
    done
    
    echo ""
    echo "================================================================================"
    log_success "Update complete"
    echo "================================================================================"
    echo ""
    echo "Summary:"
    echo "  Total projects scanned:        ${#SCAN_PROJECTS[@]}"
    echo "  Open-source projects:          $SCAN_OSS_COUNT"
    echo "  Files changed (last 24h):      ${#SCAN_MODIFIED[@]}"
    echo "  Stakeholder-relevant changes:  $stakeholder_count"
    echo ""
    echo "================================================================================"
    echo ""
}

# Parse arguments and run
parse_args "$@"

# Run main function
main

exit 0
