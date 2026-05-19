# KNOWN GAPS — Vulpine Echo (VE)
## v0.1b | May 2026

This file documents what is open, what is closed, and what is deferred.
Honest list. Nothing hidden. Nothing inflated.

The statement "0 open gaps" means: no currently known unresolved critical gaps
under present operational assumptions. New classes of gaps will emerge as the
system scales, faces adversarial input, or is distributed. This is a
stabilization milestone, not a finality claim.

---

## CLOSED — Fixed in this build

| Gap | What | Resolution |
|-----|------|-----------|
| GAP-01 | run_all.ps1 only called ve_syscheck.ps1 | Wired to ve_fullstack.ps1 + -Quick flag |
| GAP-02 | ve-pr-check.yml was a TODO stub | Wired with schema check + quickcheck + ve_checks.py |
| GAP-03 | .ve_snapshots seq-0001→0003 absent | Documented in .ve_snapshots/README.md |
| GAP-04 | ve_kernel.py eval() weak sandbox | Replaced with _PY_SAFE_BUILTINS allowlist |
| GAP-05 | No key rotation mechanism | core/ve_key_rotate.ps1 added |
| GAP-06 | ρ/γ/Δ thresholds undocumented | THRESHOLDS.md with reasoning + ψ_eff formula |
| GAP-07 | PS 5.1 vs 7.x compatibility undocumented | Documented — both supported, CI runs PS7 |
| GAP-08 | ve_status.ps1 hardcoded path | Replaced with $PSScriptRoot |
| GAP-09 | ve_ledger_pin.ps1 overwrote live ledger | -Force guard added |
| GAP-10 | .gitignore missing *.lock | Added *.lock + runtime output patterns |
| GAP-11 | Tests/ had only one file | 42 tests across 6 files, all passing |
| GAP-12 | CI broken after restructure | Root shims + ve_quickcheck_stub.py |
| GAP-13 | ve_kernel.ps1 used Invoke-Expression | Replaced with allowlisted & dispatch |
| GAP-14 | ve_fullstack.ps1 wrote scripts at runtime | Replaced with tracked file paths |
| GAP-15 | run_all.ps1 -Quick had wrong path | Fixed to verify/ve_prepush_check.ps1 |

---

## DEFERRED — v0.2 Work

| Item | Why deferred |
|------|-------------|
| Z3 formal proof of ρ/γ/Δ thresholds | Requires defining formal model of "good execution" — non-trivial |
| PS 5.1 vs 7.x full parity | Minor behavioral differences; low practical impact for v0.1 |
| Multi-operator key distribution protocol | Out of scope for single-operator v0.1 deployment |
| Adversarial input hardening | Requires threat model expansion beyond current use cases |
| Distributed execution and async recovery | Architectural expansion — not in scope for v0.1 |

---

## KNOWN ASSUMPTIONS (current operational context)

- Single operator deployment
- Trusted execution environment (not hostile)
- Python 3.8+ available
- PowerShell 5.1+ (Windows) or 7+ (cross-platform)
- No concurrent multi-process ledger writes without atomic append

These assumptions are documented. If any change, re-evaluate the deferred items.

---

*@BioAnkh84 — sole authority on all releases and decisions.*
*External review: @LabyrinthCoder, May 2026*
