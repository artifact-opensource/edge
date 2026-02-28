# Copyright Tool Wrapper Script (PowerShell)
# Easy-to-use wrapper for the copyright tool

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Tool = Join-Path $ScriptDir "copyright-tool.js"

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║       Artifact Virtual - Copyright Tool Wrapper               ║" -ForegroundColor Blue
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Blue
Write-Host ""

# Check if Node.js is installed
$nodeVersion = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeVersion) {
    Write-Host "⚠️  Node.js is not installed. Please install Node.js to use this tool." -ForegroundColor Yellow
    exit 1
}

# Display quick menu if no arguments
if ($args.Count -eq 0) {
    Write-Host "Quick Actions:"
    Write-Host ""
    Write-Host "  1) Preview changes (dry-run) on current directory"
    Write-Host "  2) Apply to current directory"
    Write-Host "  3) Apply to entire repository"
    Write-Host "  4) Show help"
    Write-Host "  5) Run tests"
    Write-Host ""
    
    $option = Read-Host "Select an option (1-5)"
    
    switch ($option) {
        "1" {
            Write-Host ""
            Write-Host "Running dry-run on current directory..." -ForegroundColor Green
            node $Tool --dry-run
        }
        "2" {
            Write-Host ""
            Write-Host "⚠️  This will modify files in the current directory." -ForegroundColor Yellow
            $confirm = Read-Host "Continue? (y/N)"
            if ($confirm -eq "y" -or $confirm -eq "Y") {
                node $Tool
            } else {
                Write-Host "Cancelled."
            }
        }
        "3" {
            Write-Host ""
            try {
                $repoRoot = git rev-parse --show-toplevel 2>$null
                if (-not $repoRoot) {
                    $repoRoot = Get-Location
                }
            } catch {
                $repoRoot = Get-Location
            }
            Write-Host "⚠️  This will modify ALL markdown files in: $repoRoot" -ForegroundColor Yellow
            $confirm = Read-Host "Continue? (y/N)"
            if ($confirm -eq "y" -or $confirm -eq "Y") {
                node $Tool --path $repoRoot
            } else {
                Write-Host "Cancelled."
            }
        }
        "4" {
            node $Tool --help
        }
        "5" {
            Write-Host ""
            Write-Host "Running test suite..." -ForegroundColor Green
            $testScript = Join-Path $ScriptDir "test-copyright-tool.js"
            node $testScript
        }
        default {
            Write-Host "Invalid option. Use --help for usage information." -ForegroundColor Red
            exit 1
        }
    }
} else {
    # Pass through all arguments to the tool
    node $Tool $args
}

Write-Host ""
