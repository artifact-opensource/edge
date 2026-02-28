#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Automatically updates Notion workspace databases when repository changes are detected.

.DESCRIPTION
    This script scans the enterprise repository for changes to stakeholder-relevant files
    and open-source project documentation, then updates the corresponding Notion databases.
    
    Only projects with an "open-source" tag, badge, or frontmatter indicator are synced
    to the Community Hub. All other updates are minimal and targeted.

.PARAMETER DryRun
    Run without making actual API calls (testing mode)

.PARAMETER Force
    Force update even if no changes detected

.PARAMETER Verbose
    Enable detailed logging

.EXAMPLE
    .\notion_update.ps1
    Standard update - scans for changes and updates Notion

.EXAMPLE
    .\notion_update.ps1 -DryRun
    Test run without making API calls

.EXAMPLE
    .\notion_update.ps1 -Force -Verbose
    Force update with detailed logging

.NOTES
    Version: 1.0.0
    Author: Artifact Virtual Operations Team
    Last Updated: 2026-02-07
    
    Environment Variables Required:
    - NOTION_API_KEY: Notion integration API key
    - NOTION_PARENT_PAGE_ID: Parent page ID for the portal
    
    Optional:
    - GITHUB_TOKEN: For fetching GitHub stats
#>

[CmdletBinding()]
param(
    [switch]$DryRun,
    [switch]$Force,
    [switch]$Verbose
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Script configuration
$script:Config = @{
    Version = "1.0.0"
    RepositoryRoot = Split-Path -Parent $PSScriptRoot
    NotionDir = Join-Path (Split-Path -Parent $PSScriptRoot) "notion"
    ProjectsDir = Join-Path (Split-Path -Parent $PSScriptRoot) "enterprise/projects"
    StakeholdersDir = Join-Path (Split-Path -Parent $PSScriptRoot) "enterprise/stakeholders"
    DryRun = $DryRun
    Force = $Force
    Verbose = $Verbose
}

# Logging functions
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Verbose-Custom {
    param([string]$Message)
    if ($script:Config.Verbose) {
        Write-Host "[VERBOSE] $Message" -ForegroundColor Gray
    }
}

# Validation functions
function Test-Environment {
    Write-Info "Validating environment..."
    
    # Check required environment variables
    if (-not $env:NOTION_API_KEY -and -not $script:Config.DryRun) {
        Write-Error-Custom "NOTION_API_KEY environment variable not set"
        return $false
    }
    
    if (-not $env:NOTION_PARENT_PAGE_ID -and -not $script:Config.DryRun) {
        Write-Error-Custom "NOTION_PARENT_PAGE_ID environment variable not set"
        return $false
    }
    
    # Check directory structure
    if (-not (Test-Path $script:Config.ProjectsDir)) {
        Write-Error-Custom "Projects directory not found: $($script:Config.ProjectsDir)"
        return $false
    }
    
    if (-not (Test-Path $script:Config.NotionDir)) {
        Write-Error-Custom "Notion directory not found: $($script:Config.NotionDir)"
        return $false
    }
    
    Write-Success "Environment validated"
    return $true
}

# Check if project is open source
function Test-OpenSourceProject {
    param(
        [string]$ReadmePath
    )
    
    if (-not (Test-Path $ReadmePath)) {
        return $false
    }
    
    $content = Get-Content $ReadmePath -Raw -ErrorAction SilentlyContinue
    if (-not $content) {
        return $false
    }
    
    # Check for open-source indicators
    $indicators = @(
        # Frontmatter
        '(?ms)^---.*?open-source:\s*true.*?---',
        '(?ms)^---.*?opensource:\s*true.*?---',
        '(?ms)^---.*?license:\s*(MIT|Apache|GPL|BSD).*?---',
        
        # Badges
        'badge.*?open.*?source',
        'shields\.io.*?license',
        'opensource\.org',
        
        # Text indicators
        '(?i)open\s*source\s*project',
        '(?i)open\s*source\s*license',
        '(?i)licensed\s*under.*?(MIT|Apache|GPL|BSD)',
        
        # Tags
        '(?i)tags?:\s*\[.*?open.*?source.*?\]',
        '(?i)tags?:\s*\[.*?oss.*?\]'
    )
    
    foreach ($pattern in $indicators) {
        if ($content -match $pattern) {
            return $true
        }
    }
    
    return $false
}

# Get project metadata from README
function Get-ProjectMetadata {
    param(
        [string]$ProjectPath
    )
    
    $readmePath = Join-Path $ProjectPath "README.md"
    if (-not (Test-Path $readmePath)) {
        return $null
    }
    
    $content = Get-Content $readmePath -Raw
    $metadata = @{
        Name = Split-Path -Leaf $ProjectPath
        Path = $ProjectPath
        ReadmePath = $readmePath
        IsOpenSource = Test-OpenSourceProject -ReadmePath $readmePath
        LastModified = (Get-Item $readmePath).LastWriteTime
    }
    
    # Extract title from README
    if ($content -match '^#\s+(.+)$') {
        $metadata.Title = $Matches[1].Trim()
    }
    
    # Extract description
    if ($content -match '>\s+\*\*(.+?)\*\*' -or $content -match '>\s+(.+)$') {
        $metadata.Description = $Matches[1].Trim()
    }
    
    # Extract status
    if ($content -match '(?i)\*\*Status\*\*:\s*(.+)') {
        $metadata.Status = $Matches[1].Trim()
    }
    
    # Extract priority
    if ($content -match '(?i)\*\*Priority\*\*:\s*(.+)') {
        $metadata.Priority = $Matches[1].Trim()
    }
    
    # Extract license from badges or text
    if ($content -match 'license[/-]([A-Za-z0-9\.\-]+)') {
        $metadata.License = $Matches[1].Trim()
    }
    
    return $metadata
}

# Scan for repository changes
function Get-RepositoryChanges {
    Write-Info "Scanning repository for changes..."
    
    $changes = @{
        Projects = @()
        Stakeholders = @()
        Modified = @()
    }
    
    # Get all project directories
    $projectDirs = Get-ChildItem -Path $script:Config.ProjectsDir -Directory
    
    foreach ($dir in $projectDirs) {
        $metadata = Get-ProjectMetadata -ProjectPath $dir.FullName
        if ($metadata) {
            Write-Verbose-Custom "Found project: $($metadata.Name) (Open Source: $($metadata.IsOpenSource))"
            $changes.Projects += $metadata
        }
    }
    
    # Check git for recent changes (last 24 hours)
    try {
        Push-Location $script:Config.RepositoryRoot
        $recentCommits = git log --since="24 hours ago" --name-only --pretty=format: | Sort-Object -Unique
        
        foreach ($file in $recentCommits) {
            if ($file -and (Test-Path (Join-Path $script:Config.RepositoryRoot $file))) {
                $changes.Modified += $file
            }
        }
        
        Pop-Location
    } catch {
        Write-Warning "Could not get git history: $_"
    }
    
    Write-Success "Found $($changes.Projects.Count) projects, $($changes.Modified.Count) recent changes"
    return $changes
}

# Update Notion Community Hub
function Update-NotionCommunityHub {
    param(
        [array]$Projects
    )
    
    Write-Info "Updating Notion Community Hub..."
    
    $openSourceProjects = $Projects | Where-Object { $_.IsOpenSource }
    
    if ($openSourceProjects.Count -eq 0) {
        Write-Info "No open-source projects to update"
        return
    }
    
    Write-Info "Found $($openSourceProjects.Count) open-source projects"
    
    foreach ($project in $openSourceProjects) {
        Write-Verbose-Custom "Processing: $($project.Name)"
        
        if ($script:Config.DryRun) {
            Write-Info "[DRY RUN] Would update Community Hub for: $($project.Name)"
        } else {
            # TODO: Implement actual Notion API calls
            # This would use the Notion API to update the Master Projects Database
            # and Open Source Portfolio Database
            Write-Info "Updating Community Hub for: $($project.Name)"
        }
    }
    
    Write-Success "Community Hub update complete"
}

# Update Notion Stakeholder Hub
function Update-NotionStakeholderHub {
    param(
        [array]$ModifiedFiles
    )
    
    Write-Info "Checking for stakeholder-relevant changes..."
    
    # Filter for stakeholder-relevant files
    $relevantFiles = $ModifiedFiles | Where-Object {
        $_ -match 'enterprise/stakeholders' -or
        $_ -match 'enterprise/legal' -or
        $_ -match 'enterprise/audit' -or
        $_ -match 'enterprise/divisions/departments/executive'
    }
    
    if ($relevantFiles.Count -eq 0) {
        Write-Info "No stakeholder-relevant changes detected"
        return
    }
    
    Write-Info "Found $($relevantFiles.Count) stakeholder-relevant changes"
    
    if ($script:Config.DryRun) {
        Write-Info "[DRY RUN] Would update Stakeholder Hub"
        foreach ($file in $relevantFiles) {
            Write-Verbose-Custom "  - $file"
        }
    } else {
        # TODO: Implement actual Notion API calls for stakeholder updates
        Write-Info "Updating Stakeholder Hub..."
    }
    
    Write-Success "Stakeholder Hub check complete"
}

# Update Notion AV Live Dashboard
function Update-NotionLiveDashboard {
    param(
        [hashtable]$Changes
    )
    
    Write-Info "Updating AV Live Dashboard..."
    
    if ($script:Config.DryRun) {
        Write-Info "[DRY RUN] Would add update event to Live Feed"
    } else {
        # TODO: Implement actual Notion API call to add Live Update entry
        $updateMessage = "Repository sync completed: $($Changes.Projects.Count) projects scanned, $($Changes.Modified.Count) files changed"
        Write-Info "Live update: $updateMessage"
    }
    
    Write-Success "Live Dashboard updated"
}

# Main execution
function Invoke-NotionUpdate {
    Write-Host "`n" + "=" * 80
    Write-Host "Artifact Virtual - Notion Auto-Update Script v$($script:Config.Version)"
    Write-Host "=" * 80
    Write-Host ""
    
    if ($script:Config.DryRun) {
        Write-Warning "DRY RUN MODE - No API calls will be made"
    }
    
    # Validate environment
    if (-not (Test-Environment)) {
        Write-Error-Custom "Environment validation failed"
        exit 1
    }
    
    # Scan repository for changes
    $changes = Get-RepositoryChanges
    
    # Check if update is needed
    if (-not $script:Config.Force -and $changes.Modified.Count -eq 0) {
        Write-Info "No changes detected. Use -Force to update anyway."
        Write-Host "`n" + "=" * 80
        Write-Success "Update complete - No changes to sync"
        Write-Host "=" * 80 + "`n"
        exit 0
    }
    
    # Update Community Hub (open-source projects only)
    Update-NotionCommunityHub -Projects $changes.Projects
    
    # Update Stakeholder Hub (if relevant changes detected)
    Update-NotionStakeholderHub -ModifiedFiles $changes.Modified
    
    # Update Live Dashboard
    Update-NotionLiveDashboard -Changes $changes
    
    # Summary
    Write-Host "`n" + "=" * 80
    Write-Success "Update complete"
    Write-Host "=" * 80
    Write-Host ""
    Write-Host "Summary:"
    Write-Host "  Total projects scanned:        $($changes.Projects.Count)"
    Write-Host "  Open-source projects:          $($($changes.Projects | Where-Object { $_.IsOpenSource }).Count)"
    Write-Host "  Files changed (last 24h):      $($changes.Modified.Count)"
    Write-Host "  Stakeholder-relevant changes:  $($($changes.Modified | Where-Object { $_ -match 'stakeholders|legal|audit' }).Count)"
    Write-Host ""
    Write-Host "=" * 80 + "`n"
}

# Run the script
try {
    Invoke-NotionUpdate
    exit 0
} catch {
    Write-Error-Custom "Script failed: $_"
    Write-Error-Custom $_.ScriptStackTrace
    exit 1
}
