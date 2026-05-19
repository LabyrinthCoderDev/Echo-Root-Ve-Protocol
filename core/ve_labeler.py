#!/usr/bin/env python3
"""
ve_labeler.py — Epistemic label layer for Vulpine Echo gate results
====================================================================
Adds CLEAR / CAUTION / HIGH_DRIFT / UNRELIABLE labels to gate output.

Labels tell the operator what the gate result means in plain terms.
Not a replacement for the gate decision — additional signal for the human layer.

Signal mapping:
  rho   → confidence channel
  gamma → alignment channel
  delta → drift channel

Labels:
  CLEAR       — all signals healthy, result is reliable
  CAUTION     — one signal near threshold, proceed with awareness
  HIGH_DRIFT  — delta approaching or above warning zone
  UNRELIABLE  — multiple signals weak, result confidence is low

Ported from Labyrinth OS output_labeler.py (MIT compatible)
@LabyrinthCoder, May 2026
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


# Thresholds (match core/ve_gatecheck.py and THRESHOLDS.md)
RHO_FLOOR    = 0.70
GAMMA_FLOOR  = 0.70
DELTA_CEIL   = 0.30
CAUTION_BAND = 0.08   # within this of a threshold = CAUTION


@dataclass
class VELabel:
    label:   str        # CLEAR | CAUTION | HIGH_DRIFT | UNRELIABLE
    reason:  str
    rho:     float
    gamma:   float
    delta:   float
    decision: str       # PROCEED | PAUSE | ABORT

    def to_dict(self) -> dict:
        return {
            "label":    self.label,
            "reason":   self.reason,
            "rho":      self.rho,
            "gamma":    self.gamma,
            "delta":    self.delta,
            "decision": self.decision,
        }


def label(rho: float, gamma: float, delta: float, decision: str) -> VELabel:
    """
    Assign an epistemic label to a gate result.

    Usage:
        from ve_labeler import label
        result = label(rho=0.82, gamma=0.75, delta=0.22, decision="PROCEED")
        print(result.label)   # CLEAR
        print(result.reason)  # All signals healthy
    """
    reasons = []

    # Check drift first — most safety-critical
    if delta > DELTA_CEIL + CAUTION_BAND:
        reasons.append(f"delta={delta:.2f} well above ceiling {DELTA_CEIL}")
    elif delta > DELTA_CEIL:
        reasons.append(f"delta={delta:.2f} above ceiling {DELTA_CEIL}")
    elif delta > DELTA_CEIL - CAUTION_BAND:
        reasons.append(f"delta={delta:.2f} near ceiling {DELTA_CEIL}")

    # Check confidence
    if rho < RHO_FLOOR - CAUTION_BAND:
        reasons.append(f"rho={rho:.2f} below floor {RHO_FLOOR}")
    elif rho < RHO_FLOOR:
        reasons.append(f"rho={rho:.2f} just below floor {RHO_FLOOR}")
    elif rho < RHO_FLOOR + CAUTION_BAND:
        reasons.append(f"rho={rho:.2f} near floor {RHO_FLOOR}")

    # Check alignment
    if gamma < GAMMA_FLOOR - CAUTION_BAND:
        reasons.append(f"gamma={gamma:.2f} below floor {GAMMA_FLOOR}")
    elif gamma < GAMMA_FLOOR:
        reasons.append(f"gamma={gamma:.2f} just below floor {GAMMA_FLOOR}")
    elif gamma < GAMMA_FLOOR + CAUTION_BAND:
        reasons.append(f"gamma={gamma:.2f} near floor {GAMMA_FLOOR}")

    weak_count = sum([
        rho < RHO_FLOOR + CAUTION_BAND,
        gamma < GAMMA_FLOOR + CAUTION_BAND,
        delta > DELTA_CEIL - CAUTION_BAND,
    ])

    if weak_count >= 2:
        lbl = "UNRELIABLE"
    elif delta > DELTA_CEIL:
        lbl = "HIGH_DRIFT"
    elif reasons:
        lbl = "CAUTION"
    else:
        lbl = "CLEAR"

    reason = "; ".join(reasons) if reasons else "All signals healthy"

    return VELabel(
        label=lbl,
        reason=reason,
        rho=round(rho, 4),
        gamma=round(gamma, 4),
        delta=round(delta, 4),
        decision=decision,
    )


def run_demo() -> None:
    import json
    cases = [
        (0.92, 0.88, 0.12, "PROCEED"),
        (0.73, 0.72, 0.28, "PROCEED"),   # near thresholds
        (0.65, 0.71, 0.18, "PAUSE"),     # rho weak
        (0.85, 0.85, 0.38, "PAUSE"),     # high drift
        (0.62, 0.63, 0.35, "ABORT"),     # multiple weak
    ]
    print("VELabeler demo")
    print("-" * 50)
    for rho, gamma, delta, decision in cases:
        r = label(rho, gamma, delta, decision)
        print(f"  [{r.label:12}] {decision:8} | ρ={rho} γ={gamma} Δ={delta}")
        print(f"    reason: {r.reason}")


if __name__ == "__main__":
    run_demo()
