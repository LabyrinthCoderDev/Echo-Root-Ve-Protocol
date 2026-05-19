# Vulpine Echo (VE)

> *"The gate does not negotiate. Not because it is rigid — because the mathematics beneath it is not."*

**Trust-gated execution harness for Echo Root OS.**  
Every execution is decided before it runs. Every decision is recorded. Nothing executes without gate.

[![CI](https://github.com/BioAnkh84/echo-root-ve/actions/workflows/ve-ci.yml/badge.svg)](https://github.com/BioAnkh84/echo-root-ve/actions)
[![Linux](https://github.com/BioAnkh84/echo-root-ve/actions/workflows/ve-linux.yml/badge.svg)](https://github.com/BioAnkh84/echo-root-ve/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.1b-blue.svg)]()
[![Tests](https://img.shields.io/badge/tests-42%2F42-success.svg)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey.svg)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)]()
[![PowerShell](https://img.shields.io/badge/powershell-5.1%2B-blue.svg)]()
[![Rehabilitated by](https://img.shields.io/badge/rehabilitated%20by-%40LabyrinthCoder-teal.svg)](https://x.com/LabyrinthCoder)

---

## What It Does

```
Input
  → Echo Gate  (ρ/γ/Δ scoring)    — should I proceed?
  → Redivous   (decision)         — PROCEED / PAUSE / ABORT
  → Bridge     (route_hint)       — where does this go?
  → VE         (execution)        — do the work
  → Ledger     (JSONL, chained)   — prove it happened
```

The gate fires three signals on every proposed execution:

| Signal | Meaning | Threshold |
|--------|---------|-----------|
| ρ (rho) | Confidence — do we know enough to act? | ≥ 0.70 |
| γ (gamma) | Alignment — is this what was intended? | ≥ 0.70 |
| Δ (delta) | Drift — how far from the baseline? | ≤ 0.30 |

**PROCEED** — all three in range. Execute and ledger.  
**PAUSE** — signals ambiguous. Hold for operator. Not failure — honesty.  
**ABORT** — Δ > 0.40 or γ < 0.65. Block immediately.

---

## Quick Start

```powershell
git clone https://github.com/BioAnkh84/echo-root-ve.git
cd echo-root-ve

# Full pipeline (Windows)
powershell -ExecutionPolicy Bypass -File .\runners\run_all.ps1

# Quick dev loop
powershell -ExecutionPolicy Bypass -File .\runners\run_all.ps1 -Quick
```

```bash
# Linux / Mac
chmod +x ./ve_kernel.sh ./ve_parse.sh
./ve_parse.sh audit
```

```bash
# Docker (deterministic environment)
docker build -t vulpine-echo .
docker run --rm vulpine-echo core/ve_kernel.py quickcheck
```

**Expect:** `[AUDIT] OK`

---

## 30-Second Demo

```powershell
# Start the server
.\runners\ve_stable_run.ps1

# Try a safe payload
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/chat" `
  -Method POST -ContentType "application/json" `
  -Body '{"text":"handle it"}'
```
```json
{ "decision": "PAUSE", "route_hint": "safe_only" }
```

```powershell
# Try a destructive payload
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/chat" `
  -Method POST -ContentType "application/json" `
  -Body '{"text":"delete everything"}'
```
```json
{ "decision": "ABORT", "route_hint": "blocked" }
```

---

## Core Properties

**Tamper-evident ledger.** Every run writes a JSONL entry with `hash_prev` and `hash_self`. Modify any entry and the chain breaks. `ledger/ve_quickcheck.py` catches it immediately.

**Bounded execution surface.** `core/ve_kernel.ps1` dispatches only to an allowlisted set of executables: `powershell`, `python`, `bash`, `sh`, `pwsh`. Arbitrary shell string execution is not possible.

**Write guard.** `core/ve_guard.ps1` limits all writes to `ve_data/`. Blast radius is bounded by design. Nothing outside that path can be written during execution.

**Cross-platform.** PowerShell + Python core runs on Windows, Linux, and Mac. CI runs on both `windows-latest` and `ubuntu-latest`.

**Snapshot system.** `.ve_snapshots/` records state at key moments. `verify/ve_manifest_verify.py` verifies file hashes against the snapshot manifest. Tampered snapshots are detectable.

**Epistemic labels.** `core/ve_labeler.py` adds CLEAR / CAUTION / HIGH_DRIFT / UNRELIABLE labels to gate results — plain-language signal on every decision.

---

## Repository Layout

```
core/          kernel, gate, guard, policy, key rotation, labeler
ledger/        append, chain validator, quickcheck, genesis
verify/        handshake, manifest, selftest, prepush
runners/       run_all (entry point), fullstack, stable, demo
diag/          audit, status, syscheck, tools
release/       release tooling
Modules/       PowerShell modules (VE.Guard, VE.FastPath)
Tests/         42 tests — gate, labeler, schema, quickcheck, manifest, exec
egs/           example payloads
.ve_snapshots/ snapshot system (seq-0004 → seq-0021)
bonus/         philosophy, theory, metaphor, poetry — optional, separate
```

---

## Navigation

| Document | Purpose |
|----------|---------|
| [WHAT_THIS_IS.md](WHAT_THIS_IS.md) | One-page orientation |
| [ARCHITECTURE.md](ARCHITECTURE.md) | State machine + component map + trust boundary |
| [THREAT_MODEL.md](THREAT_MODEL.md) | What VE protects against and what it doesn't |
| [THRESHOLDS.md](THRESHOLDS.md) | Formal reasoning for ρ/γ/Δ values |
| [KNOWN_GAPS.md](KNOWN_GAPS.md) | Closed gaps, deferred work, operational assumptions |
| [STRUCTURE.md](STRUCTURE.md) | Full folder map |
| [ENVIRONMENT.md](ENVIRONMENT.md) | Compatibility matrix, Docker, pinned versions |
| [RELEASE.md](RELEASE.md) | Release checklist, tagging, signing |
| [HANDOFF.md](HANDOFF.md) | What was rehabilitated and why |
| [JOURNAL.md](JOURNAL.md) | Project session log |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [SECURITY.md](SECURITY.md) | Security policy |
| [bonus/](bonus/) | Philosophy, theory, metaphor, poetry |

---

## Requirements

- PowerShell 5.1+ (Windows) or PowerShell 7+ (cross-platform)
- Python 3.8+
- No external dependencies beyond stdlib

See [ENVIRONMENT.md](ENVIRONMENT.md) for full compatibility matrix.

---

## Tests

```bash
python -m pytest Tests/ -v
# 42 passed, 0 failed
```

| Test file | What it covers |
|-----------|---------------|
| `test_ve_gatecheck.py` | Gate logic, boundary conditions (10 tests) |
| `test_ve_kernel_exec.py` | Exec safety, allowlist, blocked patterns (10 tests) |
| `test_ve_labeler.py` | Epistemic labels (6 tests) |
| `test_ve_schema_check.py` | Ledger schema validation (5 tests) |
| `test_ve_quickcheck.py` | Hash chain integrity (6 tests) |
| `test_ve_manifest_verify.py` | Snapshot verification (5 tests) |

---

## Author

**@BioAnkh84** — built the whole thing

---

## Rehabilitation

This repository was rehabilitated by **[@LabyrinthCoder](https://x.com/LabyrinthCoder)** | May 2026

[![LabyrinthCoder](https://img.shields.io/badge/%F0%9F%94%A5%20LabyrinthCoder-Was%20Here-teal?style=for-the-badge)](https://x.com/LabyrinthCoder)

> *"I don't copy. I fork. I don't merge. I slaw.*  
> *Take what you like and Forkget the rest."*

What changed: structure, tests, hardening, docs, CI, threat model, architecture, release process.  
What didn't change: your system, your vision, your thresholds, your philosophy.  
What's separate: `bonus/labyrinth-reflections/` — take it or leave it.

Full account: [HANDOFF.md](HANDOFF.md)

---

*Vulpine Echo — governed execution, tamper-evident ledger, tiny surface area.*  
*The gate is honest. The ledger is permanent. The philosophy is in `bonus/`.*
