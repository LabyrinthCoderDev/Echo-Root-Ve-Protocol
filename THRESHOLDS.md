# Gate Thresholds — Vulpine Echo (VE)

## Authoritative Values

| Signal | Meaning | PROCEED requires | ABORT fires when |
|--------|---------|-----------------|-----------------|
| ρ (rho) | Confidence — do we know enough to act? | ρ ≥ **0.70** | — |
| γ (gamma) | Alignment — is this what was intended? | γ ≥ **0.70** | γ < **0.65** |
| Δ (delta) | Drift — how far from the baseline? | Δ ≤ **0.30** | Δ > **0.40** |

**PROCEED:** all three in range simultaneously
**PAUSE:** signals ambiguous (between PROCEED and ABORT) — hold for operator
**ABORT:** Δ > 0.40 OR γ < 0.65 — block immediately

These values live in `core/ve_gatecheck.py` and `core/policy.ve.psl`.

---

## Reasoning

**Why 0.70 for the floors?**

0.70 represents "strong majority confidence." Below 0.70, the system is less
than 70% certain — uncertain enough that proceeding could cause harm or waste.
This is not a formal proof (see GAP-06 in KNOWN_GAPS.md) but a design choice
made by @BioAnkh84 that reflects a conservative-but-usable threshold.

**Why 0.30 for the drift ceiling?**

Δ = 0.30 means the system has drifted by at most 30% from its baseline.
Above 0.30 the drift is significant enough to warrant pausing.
Above 0.40 the drift is large enough that the system should abort outright.

**The PAUSE zone:**

```
Δ ≤ 0.30 AND ρ ≥ 0.70 AND γ ≥ 0.70  →  PROCEED
Δ > 0.40 OR γ < 0.65                 →  ABORT
(everything between)                  →  PAUSE
```

The PAUSE zone exists precisely because "good enough to block" and "good enough
to proceed" are not the same condition. The gap between them is where most real
safety work happens. Binary systems (PROCEED/ABORT only) force a decision at
the wrong moment. PAUSE says: hold for more information.

---

## ψ (psi) — the aggregate signal

`ψ_eff = ρ + γ`

Used in ledger validation. Floor: **ψ_eff ≥ 1.38** (checked by `ledger/ve_schema_check.py`).

1.38 = 0.70 + 0.68 — slightly below the 0.70+0.70=1.40 PROCEED threshold.
This allows entries that are close to PROCEED (one signal just below floor)
to still pass ledger validation, while rejecting clearly bad entries.

---

## Future Work

The values above were set by design intuition. For v0.2 and beyond:
- Document specific failure modes each threshold protects against
- Consider formal proof that these values are sufficient (Z3 or similar)
- See KNOWN_GAPS.md GAP-06

---

*@BioAnkh84 — authoritative on all threshold decisions*
*Documented by @LabyrinthCoder, May 2026*
