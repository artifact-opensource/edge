<#
.SYNOPSIS
Enterprise Update Script (PowerShell)

Single entry point for refreshing all enterprise data.

USAGE:
  .\update-enterprise.ps1              # dry-run (preview changes)
  .\update-enterprise.ps1 --apply      # apply all changes
  .\update-enterprise.ps1 --apply --skip-db   # skip database sync
#>

[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

if ($PSScriptRoot) {
    $scriptDir = $PSScriptRoot
} else {
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
}

# Find python3 or python
$pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
}

if (-not $pythonCmd) {
    Write-Error "Error: Python 3 is required but not found on PATH"
    exit 1
}

$pythonPath = $pythonCmd.Path

# Verify Python 3.x
try {
    $versionOutput = & $pythonPath --version 2>&1
} catch {
    Write-Error "Failed to run Python to determine version: $_"
    exit 1
}

if ($versionOutput -notmatch 'Python\s+3\.') {
    Write-Error "Python 3 is required. Detected: $versionOutput"
    exit 1
}

Push-Location $scriptDir
try {
    & $pythonPath scripts/update_engine.py @args
    $exitCode = $LASTEXITCODE
} finally {
    Pop-Location
}

# Fallback dashboard launch after --apply
if (($args -contains '--apply') -and ($exitCode -eq 0)) {
    $dashboard = Join-Path $scriptDir 'docs' 'enterprise-dashboard.html'
    if (Test-Path $dashboard) {
        try { Start-Process $dashboard } catch { }
    }
}

exit $exitCode
