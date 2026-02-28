Param(
  [string]$Path = '.',
  [switch]$Recursive,
  [switch]$Delete,
  [switch]$DryRun
)

if (-not $env:SHIELD_PASSPHRASE) {
  Write-Error 'SHIELD_PASSPHRASE environment variable is not set. Set it and re-run.'
  exit 2
}

$argList = @($Path)
if ($Recursive.IsPresent) { $argList += '--recursive' }
if ($Delete.IsPresent) { $argList += '--delete' }
if ($DryRun.IsPresent) { $argList += '--dry-run' }

# Use current Python in PATH
& python .\toggle_encrypt.py @argList
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
