# ve_key_rotate.ps1 — Key rotation for ve_shared.key
# Generates a new shared key, archives the old one with a timestamp,
# and updates the secrets/ folder.
#
# Usage:
#   .\core\ve_key_rotate.ps1
#   .\core\ve_key_rotate.ps1 -SecretsDir .\secrets
#
# When to rotate:
#   - Regularly (monthly or quarterly for production deployments)
#   - After any suspected key compromise
#   - When adding or removing operators
#
# After rotation: any systems using the old key will fail HMAC verification
# until they receive the new key. Coordinate rotation across all operators.

param(
    [string]$SecretsDir = ".\secrets"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$SecretsPath = Resolve-Path -LiteralPath $SecretsDir -ErrorAction SilentlyContinue
if (-not $SecretsPath) {
    New-Item -ItemType Directory -Path $SecretsDir | Out-Null
    $SecretsPath = Resolve-Path -LiteralPath $SecretsDir
}

$KeyFile = Join-Path $SecretsPath "ve_shared.key"

# Archive old key if it exists
if (Test-Path $KeyFile) {
    $ts = (Get-Date).ToUniversalTime().ToString("yyyyMMdd_HHmmss")
    $Archive = Join-Path $SecretsPath "ve_shared.key.bak_$ts"
    Copy-Item $KeyFile $Archive
    Write-Host "Archived old key → $Archive"
}

# Generate new key: 32 random bytes as hex string
$bytes = New-Object byte[] 32
[System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
$newKey = -join ($bytes | ForEach-Object { $_.ToString("x2") })

# Write new key (no newline — consistent with how ve_kernel.ps1 reads it)
[System.IO.File]::WriteAllText($KeyFile, $newKey, [System.Text.Encoding]::ASCII)

Write-Host "✅ New key written to $KeyFile"
Write-Host "   Key length: $($newKey.Length) hex chars (128-bit entropy)"
Write-Host ""
Write-Host "NEXT STEPS:"
Write-Host "  1. Distribute the new key to all authorized operators"
Write-Host "  2. Verify HMAC-signed envelopes still pass: .\runners\run_all.ps1 -Quick"
Write-Host "  3. Delete archived key files once rotation is confirmed: $SecretsPath\*.bak_*"
