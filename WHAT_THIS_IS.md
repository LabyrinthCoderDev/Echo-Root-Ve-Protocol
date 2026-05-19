# WHAT THIS IS
## Vulpine Echo (VE) — Echo Root OS Execution Harness

**One sentence:** VE is the trust gate and audit ledger that sits beneath Echo Root's governance layer.

---

## The System

```
Input
  → Echo Gate (ρ/γ/Δ scoring)     — should I proceed?
  → Redivous (decision)           — PROCEED / PAUSE / ABORT
  → Bridge (route_hint contract)  — where does this go?
  → VE Execution                  — do the work
  → Ledger (JSONL, hash-chained)  — prove it happened
```

**Gate thresholds:**
- ρ ≥ 0.70 — confidence
- γ ≥ 0.70 — intent alignment
- Δ ≤ 0.30 — drift tolerance

**Key property:** The ledger is tamper-evident. Every run is traceable.
You cannot quietly undo what happened. The chain makes modification visible.

**PAUSE is not failure.** It is the system saying: something is ambiguous.
I am not blocking — I am holding for a human decision. That honesty is structural.

---

## Key Files

| File | Role |
|------|------|
| `core/ve_kernel.ps1` | Primary entrypoint |
| `core/ve_kernel.py` | Python bridge |
| `core/ve_gatecheck.py` | Gate logic (ρ/γ/Δ) — 20 lines |
| `core/ve_guard.ps1` | Write guard (ve_data/ only) |
| `core/policy.ve.psl` | Policy spec (operator-readable) |
| `ledger/ve_schema_check.py` | Ledger chain validator |
| `ledger/ve_quickcheck.py` | Integrity checker |
| `verify/ve_manifest_verify.py` | File manifest verification |
| `runners/run_all.ps1` | Entry point → calls ve_fullstack |
| `runners/ve_fullstack.ps1` | Complete pipeline runner |
| `.ve_snapshots/` | Snapshot sequence (seq-0004 → seq-0021) |

---

## Install in 2 Minutes

```powershell
# Windows
git clone https://github.com/BioAnkh84/echo-root-ve.git
cd echo-root-ve
powershell -ExecutionPolicy Bypass -File .\runners\run_all.ps1
```

```bash
# Linux / Mac
git clone https://github.com/BioAnkh84/echo-root-ve.git
cd echo-root-ve && chmod +x ./ve_kernel.sh ./ve_parse.sh
./ve_parse.sh audit
```

---

## Contact
**@BioAnkh84** — GitHub
