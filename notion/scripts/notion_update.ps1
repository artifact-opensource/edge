# ─────────────────────────────────────────────────────────────
# Artifact Virtual — Notion Update (one-click)  [PowerShell]
#
# Updates local databases from repository, then syncs everything
# to the Notion workspace (Community Portal + Stakeholder Portal).
#
# Prerequisites:
#   $env:NOTION_API_KEY = "secret_…"
#   $env:NOTION_PARENT_PAGE_ID = "…"
#
# Usage:
#   .\notion\scripts\notion_update.ps1              # full sync
#   .\notion\scripts\notion_update.ps1 --dry-run    # test run
#   .\notion\scripts\notion_update.ps1 --skip-db-update
#   .\notion\scripts\notion_update.ps1 --populate-only
# ─────────────────────────────────────────────────────────────
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Load .env if present
foreach ($envFile in @(
    (Join-Path $ScriptDir "../../.env"),
    (Join-Path $ScriptDir "../.env")
)) {
    if (Test-Path $envFile) {
        Get-Content $envFile | ForEach-Object {
            if ($_ -match '^\s*([A-Z_]+)\s*=\s*(.+)$') {
                [System.Environment]::SetEnvironmentVariable($Matches[1], $Matches[2].Trim('"').Trim("'"), "Process")
            }
        }
    }
}

# Validate
if (-not $env:NOTION_API_KEY) {
    Write-Error "NOTION_API_KEY not set. Export it or add to .env"
    exit 1
}
if (-not $env:NOTION_PARENT_PAGE_ID) {
    Write-Error "NOTION_PARENT_PAGE_ID not set. Export it or add to .env"
    exit 1
}

& python3 (Join-Path $ScriptDir "notion_sync.py") @args
