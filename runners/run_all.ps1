# run_all.ps1
# Full pipeline: unblock → handshake → gatecheck → ledger → sysinfo → quickcheck
# Delegates to ve_fullstack.ps1 which owns the complete chain.
#
# Usage:
#   .\run_all.ps1           — full pipeline
#   .\run_all.ps1 -Quick    — pre-push check only (faster dev loop)

param([switch]$Quick)

Get-ChildItem $PSScriptRoot -Filter *.ps1 | Unblock-File

if ($Quick) {
    Write-Host "[run_all] Quick mode — running pre-push check only"
    . "$PSScriptRoot\..\verify\ve_prepush_check.ps1"
    exit $LASTEXITCODE
}

Write-Host "[run_all] Full pipeline via ve_fullstack.ps1"
. "$PSScriptRoot\ve_fullstack.ps1"
exit $LASTEXITCODE
