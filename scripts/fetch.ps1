# Fetch UPPERCASE markdown files into ./data (scans entire repo root and subdirectories)
# Only copies files where filename starts with an uppercase letter (A-Z)
# Usage: From repo root:  PowerShell -File .\scripts\fetch.ps1
#        From scripts dir: .\fetch.ps1
# Requires PowerShell 7+

# Resolve script and repo root robustly
$scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Definition }
$repoRoot = Split-Path -Parent $scriptDir
$repoRoot = $repoRoot.TrimEnd('\','/')
$dataDir = Join-Path $repoRoot 'data'

# Ensure data dir exists (create or prompt)
if (-not (Test-Path $dataDir)) {
    New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
    Write-Host "Created directory: $dataDir"
} else {
    $resp = Read-Host "Directory '$dataDir' already exists. Use it? [Y/N] (Default: Y)"
    if ($resp -match '^[Nn]') {
        $newName = Read-Host "Enter new data directory name (will be created in repo root):"
        if (-not $newName) { Write-Host "Aborting." -ForegroundColor Red; exit 1 }
        $dataDir = Join-Path $repoRoot $newName
        if (-not (Test-Path $dataDir)) { New-Item -ItemType Directory -Path $dataDir -Force | Out-Null; Write-Host "Created directory: $dataDir" } else { Write-Host "Using existing: $dataDir" }
    } else { Write-Host "Using existing: $dataDir" }
}

# Overwrite behavior selection
$option = Read-Host "If destination files exist, choose: [O]verwrite / [S]kip existing / [A]ll overwrite / [K]eep existing (default: O)"
$overwriteAll = $false
$skipExisting = $false
switch (($option ?? '').ToUpper()) {
    'A' { $overwriteAll = $true }
    'S' { $skipExisting = $true }
    'K' { $skipExisting = $true }
    'O' { $overwriteAll = $true }
    default { $overwriteAll = $true }
}

$counters = @{Copied=0;Skipped=0;Errors=0;LowercaseSkipped=0}

# Scan the entire repo root for markdown files (exclude the destination data dir, .git, and node_modules)
$files = Get-ChildItem -Path $repoRoot -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object {
        ($_.Extension -in '.md', '.markdown') -and
        -not ($_.FullName.StartsWith($dataDir, [System.StringComparison]::InvariantCultureIgnoreCase)) -and
        -not ($_.FullName -match '[\\/]\.git[\\/]') -and
        -not ($_.FullName -match '[\\/]node_modules[\\/]')
    }

if (-not $files) {
    Write-Host "No markdown files found under repo root: $repoRoot" -ForegroundColor Yellow
    exit 0
}

Write-Host "Found $($files.Count) markdown files. Filtering for UPPERCASE filenames only..." -ForegroundColor Cyan

foreach ($f in $files) {
    # Skip files that start with lowercase letter (only copy UPPERCASE files)
    $firstChar = $f.Name.Substring(0, 1)
    if ($firstChar -cmatch '^[a-z]') {
        $counters.LowercaseSkipped++
        Write-Host "  Skipping lowercase: $($f.Name)" -ForegroundColor DarkGray
        continue
    }

    try {
        $relative = [System.IO.Path]::GetRelativePath($repoRoot, $f.FullName)
    } catch {
        $relative = $f.FullName.Substring($repoRoot.Length).TrimStart('\','/')
    }

    $destPath = Join-Path $dataDir $relative
    $destDir = Split-Path $destPath -Parent
    if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }

    try {
        if (Test-Path $destPath) {
            if ($overwriteAll) {
                Copy-Item -Path $f.FullName -Destination $destPath -Force -ErrorAction Stop
                Write-Host "  Copied (overwrite): $relative" -ForegroundColor Green
                $counters.Copied++
            } elseif ($skipExisting) {
                $counters.Skipped++
            } else {
                $r = Read-Host "File exists: $destPath. Overwrite? [Y/N]"
                if ($r -match '^[Yy]') { Copy-Item -Path $f.FullName -Destination $destPath -Force -ErrorAction Stop; $counters.Copied++ } else { $counters.Skipped++ }
            }
        } else {
            Copy-Item -Path $f.FullName -Destination $destPath -ErrorAction Stop
            Write-Host "  Copied: $relative" -ForegroundColor Green
            $counters.Copied++
        }
    } catch {
        Write-Host "Error copying $($f.FullName) -> $destPath : $($_.Exception.Message)" -ForegroundColor Red
        $counters.Errors++
    }
}

Write-Host ""
Write-Host "========== SUMMARY ==========" -ForegroundColor Cyan
Write-Host "Copied:            $($counters.Copied)" -ForegroundColor Green
Write-Host "Skipped (exists):  $($counters.Skipped)" -ForegroundColor Yellow
Write-Host "Skipped (lowercase): $($counters.LowercaseSkipped)" -ForegroundColor DarkGray
Write-Host "Errors:            $($counters.Errors)" -ForegroundColor Red
Write-Host "=============================" -ForegroundColor Cyan
