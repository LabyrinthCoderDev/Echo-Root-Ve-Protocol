# Architecture — Vulpine Echo (VE)

## State Machine

```
                         ┌─────────────────────────────────────────┐
                         │              INPUT                      │
                         │  (payload string, route_hint request)   │
                         └──────────────────┬──────────────────────┘
                                            │
                                            ▼
                         ┌─────────────────────────────────────────┐
                         │            POLICY CHECK                 │
                         │  policy.ve.psl — allowed ext/targets    │
                         └──────────────────┬──────────────────────┘
                                            │
                                            ▼
                         ┌─────────────────────────────────────────┐
                         │             ECHO GATE                   │
                         │  ρ (confidence)   ≥ 0.70               │
                         │  γ (alignment)    ≥ 0.70               │
                         │  Δ (drift)        ≤ 0.30               │
                         └──────┬─────────────┬──────────┬─────────┘
                                │             │          │
                          PROCEED           PAUSE      ABORT
                                │             │          │
                                ▼             ▼          ▼
                    ┌──────────────┐  ┌──────────┐  ┌────────────┐
                    │   EXECUTE    │  │   HOLD   │  │   BLOCK    │
                    │  (allowlist  │  │ (notify  │  │ (no exec)  │
                    │   dispatch)  │  │ operator)│  │            │
                    └──────┬───────┘  └──────────┘  └─────┬──────┘
                           │                               │
                           ▼                               ▼
                    ┌──────────────┐               ┌──────────────┐
                    │  EPISTEMIC   │               │    LEDGER    │
                    │   LABEL      │               │  (ABORT log) │
                    │ CLEAR/CAUTION│               └──────────────┘
                    │ HIGH_DRIFT/  │
                    │ UNRELIABLE   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────────────────────────────────────┐
                    │                  LEDGER                      │
                    │  JSONL append — hash_prev / hash_self chain  │
                    │  Every decision recorded. Chain tamper-evident│
                    └──────────────────────┬───────────────────────┘
                                           │
                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │               VERIFY (post-run)              │
                    │  ve_quickcheck.py    — chain integrity       │
                    │  ve_manifest_verify  — snapshot integrity    │
                    │  ve_schema_check.py  — schema + ψ_eff floor  │
                    └──────────────────────┬───────────────────────┘
                                           │
                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │               SNAPSHOT                       │
                    │  .ve_snapshots/seq-NNNN/                     │
                    │  manifest.json — per-file SHA-256 hashes     │
                    │  Verifiable restore points                   │
                    └──────────────────────────────────────────────┘
```

---

## Component Map

```
CORE
  ve_kernel.ps1         Entrypoint — HMAC envelope, ledger, policy, gate dispatch
  ve_kernel.py          Python bridge — echo:, py: (allowlisted), quickcheck
  ve_gatecheck.py       Gate logic — ρ/γ/Δ → PROCEED/PAUSE/ABORT (20 lines)
  ve_labeler.py         Epistemic labels — CLEAR/CAUTION/HIGH_DRIFT/UNRELIABLE
  ve_guard.ps1          Write guard — blocks writes outside ve_data/
  policy.ve.psl         Operator policy — thresholds, allowed extensions, targets
  ve_key_rotate.ps1     Key rotation — archive + generate 128-bit key

LEDGER
  ve_ledger_append.ps1       Append entry (standard)
  ve_ledger_append_atomic.ps1 Append entry (race-safe)
  ve_ledger_pin.ps1          Write genesis (-Force required to overwrite)
  ve_schema_check.py         Full chain + ψ_eff validator
  ve_quickcheck.py           Fast chain integrity checker

VERIFY
  ve_manifest_verify.py  File hash verification against snapshot
  ve_handshake.ps1       PS↔Python handshake protocol
  ve_selftest.ps1        Self-test suite
  ve_prepush_check.ps1   Pre-push gate

RUNNERS
  run_all.ps1      Entry point → ve_fullstack.ps1 (or -Quick → verify/ve_prepush_check.ps1)
  ve_fullstack.ps1 Complete pipeline: unblock→handshake→gate→label→ledger→sysinfo→quickcheck

DIAG
  ve_audit.ps1    Audit ledger
  ve_status.ps1   Repo health check (portable $PSScriptRoot)
  ve_syscheck.ps1 System check

CI
  .github/workflows/ve-ci.yml          Windows quickcheck on push/PR
  .github/workflows/ve-linux.yml       Linux audit on push/PR
  .github/workflows/ve-pr-check.yml    Schema + quickcheck + ve_checks.py
  .github/ve_checks.py                 Required-files + runtime-not-tracked check
```

---

## Trust Boundary

```
TRUSTED ZONE                        UNTRUSTED ZONE
─────────────────────────────────   ──────────────────────────────
operator               │            payload (ρ/γ/Δ-scored input)
policy.ve.psl          │            py: expressions (allowlisted)
secrets/ve_shared.key  │            echo: strings (passthrough)
ledger (append-only)   │
snapshots              │
                       │── GATE ───▶ execution surface (allowlisted)
```

---

## Ledger Chain

```
GENESIS
  hash_prev = "0000...0000" (64 zeros)
  hash_self = SHA-256(entry without hash_self)

ENTRY N
  hash_prev = hash_self of entry N-1
  hash_self = SHA-256(entry N without hash_self)

TAMPER DETECTION
  Modify any field → hash_self no longer matches
  Move entry → hash_prev no longer matches
  Delete entry → next entry's hash_prev breaks
  ve_quickcheck.py detects all three cases
```

---

## ψ_eff (Aggregate Signal)

```
ψ_eff = ρ + γ

Gate floor:    ρ ≥ 0.70, γ ≥ 0.70  →  ψ_eff ≥ 1.40 to PROCEED
Ledger floor:  ψ_eff ≥ 1.38        (checked by ve_schema_check.py)

The ledger floor is slightly below the gate floor to allow entries
near the PROCEED threshold to pass validation while rejecting
clearly failed entries.
```

---

*@BioAnkh84 — sole authority*
*Architecture documentation: @LabyrinthCoder, May 2026*
