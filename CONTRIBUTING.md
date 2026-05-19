# Contributing to Vulpine Echo (VE)

Thanks for helping. This repo aims to stay tiny, auditable, and PS 5.1-safe.

---

## Dev Environment

- Windows 10/11, PowerShell 5.1+ (stock)
- Python 3.8+ (for gate logic and ledger checks)
- No external modules required beyond stdlib

---

## Quick Start

```powershell
# Windows — full pipeline
powershell -ExecutionPolicy Bypass -File .\runners\run_all.ps1

# Quick dev loop
powershell -ExecutionPolicy Bypass -File .\runners\run_all.ps1 -Quick

# Linux / Mac
chmod +x ./ve_kernel.sh ./ve_parse.sh
./ve_parse.sh audit
```

**Expect:** `[AUDIT] OK`

---

## Repository Layout

```
core/      kernel, gate, guard, policy
ledger/    append, validator, quickcheck
verify/    handshake, manifest, selftest, prepush
runners/   run_all (entry), fullstack, stable, demo
diag/      audit, status, syscheck, tools
release/   release tooling
```

Root shims (`ve_kernel.ps1`, `ve_kernel.sh`, `ve_parse.sh`) exist at root for CI
compatibility — they delegate to the real files in `core/`.

See [STRUCTURE.md](STRUCTURE.md) for the complete map.

---

## Workflow

1. Fork → branch: `feat/<topic>` or `fix/<topic>`
2. Keep PRs small — exact repro steps and before/after output
3. Add tests where relevant (`Tests/` or smoke checks in `verify/`)
4. CI must pass: `runners/run_all.ps1` and `verify/ve_prepush_check.ps1`

---

## Commit Style

- Conventional: `feat: ...`, `fix: ...`, `docs: ...`, `chore: ...`
- Present tense, imperative ("add", "fix", "update")

---

## Versioning

- Tags: `v0.1a`, `v0.1b`, `v0.2.0`, ...
- CHANGELOG.md updated before every release

---

## Security

Don't file public issues with exploit details. See [SECURITY.md](SECURITY.md).
