param(
    [string]$LedgerPath = ".\ve_ledger.jsonl",
    [switch]$Force
)

# Guard: refuse to overwrite a non-empty ledger unless -Force is passed
if (-not $Force -and (Test-Path $LedgerPath)) {
    $size = (Get-Item $LedgerPath).Length
    if ($size -gt 0) {
        Write-Error "ABORT: '$LedgerPath' already exists and is non-empty ($size bytes). Use -Force to overwrite."
        exit 1
    }
}

$pinned = '{"ts":"2025-10-31T02:50:00.0000000-04:00","actor":"VE_Helper","action":"init-ledger","hash_prev":"","hash_self":"94e596ff62a914031377843be88b3eae01e69cf8bba1dfcc43e7fceba4709546"}'
$pinned | Set-Content -Encoding UTF8 -NoNewline $LedgerPath
Write-Host "✅ pinned genesis written to $LedgerPath"
