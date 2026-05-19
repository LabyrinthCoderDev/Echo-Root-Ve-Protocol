# Environment Setup — Vulpine Echo (VE)

Reproducible environment specification.

---

## Python

| Requirement | Value |
|------------|-------|
| Minimum version | Python **3.8** |
| Tested on | 3.8, 3.9, 3.10, 3.11, 3.12 |
| External dependencies | **None** — stdlib only |
| Verify | `python -c "import hashlib, json, argparse; print('OK')"` |

```bash
# Pin to a specific version with pyenv
pyenv install 3.11.9
pyenv local 3.11.9
python --version  # Python 3.11.9
```

`requirements.txt` lists no packages intentionally.
VE's design principle: no external dependencies. Every import is stdlib.

---

## PowerShell

| Requirement | Value |
|------------|-------|
| Minimum version | PowerShell **5.1** (Windows built-in) |
| Recommended | PowerShell **7.4+** (cross-platform) |
| CI version | `windows-latest` (PS 7) + `ubuntu-latest` (PS 7) |
| Compatibility | PS 5.1-safe — no PS7-only syntax used in core |

**Windows (built-in PS 5.1):**
```powershell
$PSVersionTable.PSVersion  # should show 5.1.x or higher
```

**Install PS 7 (recommended):**
```bash
# macOS
brew install powershell

# Ubuntu
sudo apt-get install -y powershell

# Windows
winget install Microsoft.PowerShell
```

**Known PS 5.1 vs 7 differences:**
- `Get-CimInstance` — available in both, preferred over `Get-WmiObject`
- `ConvertTo-Json -Depth` — default depth differs; VE always passes `-Depth 4`
- String interpolation — identical for all patterns VE uses

---

## Docker (recommended for CI and reproducibility)

```bash
# Build
docker build -t vulpine-echo .

# Run all Python tests
docker run --rm vulpine-echo -m pytest Tests/ -v

# Run quickcheck only
docker run --rm vulpine-echo core/ve_kernel.py quickcheck

# Interactive shell
docker run --rm -it --entrypoint bash vulpine-echo
```

---

## Git

```bash
git clone https://github.com/BioAnkh84/echo-root-ve.git
cd echo-root-ve

# Verify integrity of a known release
git verify-tag v0.1b   # if GPG signing is set up
```

---

## Compatibility Matrix

| Platform | Python | PowerShell | Status |
|---------|--------|-----------|--------|
| Windows 10/11 | 3.8+ | 5.1 built-in | ✓ Supported |
| Windows 10/11 | 3.8+ | 7.4+ | ✓ Recommended |
| Ubuntu 20.04+ | 3.8+ | 7.4+ | ✓ CI-tested |
| macOS 12+ | 3.8+ | 7.4+ | ✓ Supported |
| Docker (python:3.11-slim) | 3.11 | — | ✓ Python tests only |

---

## Quick Environment Check

```bash
# Linux/Mac
python3 -c "import sys; assert sys.version_info >= (3,8), 'Python 3.8+ required'"
python3 core/ve_kernel.py quickcheck

# Windows
python core\ve_kernel.py quickcheck
powershell -ExecutionPolicy Bypass -File runners\run_all.ps1 -Quick
```

Both should exit 0 with no errors.
