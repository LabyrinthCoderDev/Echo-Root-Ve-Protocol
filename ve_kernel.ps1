# ve_kernel.ps1 — root shim (calls core/ve_kernel.ps1)
# CI compatibility shim. The real kernel lives in core/ve_kernel.ps1
param(
  [Parameter(Position=0)][string]$Mode = "",
  [Parameter(ValueFromRemainingArguments=$true)][string[]]$Rest
)
$coreKernel = Join-Path $PSScriptRoot "core\ve_kernel.ps1"
if (-not (Test-Path $coreKernel)) { throw "core/ve_kernel.ps1 not found" }
& $coreKernel $Mode @Rest
exit $LASTEXITCODE
