# Threat Model — Vulpine Echo (VE)
## v0.1b | May 2026

Explicit definition of what VE protects against, what it assumes,
and what is explicitly out of scope.

---

## System Roles

| Role | Trust Level | Description |
|------|------------|-------------|
| **Operator** | Trusted | The human deploying and configuring VE. Has read/write access to config, secrets/, policy.ve.psl |
| **Payload** | Untrusted | Input arriving at the gate for evaluation (ρ/γ/Δ scoring) |
| **Execution surface** | Bounded | Commands that pass the gate — constrained to allowlisted executables only |
| **Ledger** | Tamper-evident | Append-only JSONL with SHA-256 chain — operator can read, system can append, nobody can silently modify |
| **Snapshot system** | Integrity-verified | .ve_snapshots/ — manifest-verified against live ve_data/ |

---

## Trust Assumptions

```
1. The operator is a single trusted party (not adversarial)
2. The execution host is a trusted environment (not actively compromised)
3. Python 3.8+ interpreter on PATH is the legitimate system interpreter
4. Secrets directory is readable only by the operator
5. ve_ledger.jsonl is append-only once initialized (no external process truncates it)
6. The operator's HMAC key (ve_shared.key) is kept secret
```

If any assumption breaks, re-evaluate the deferred items in KNOWN_GAPS.md.

---

## What VE Protects Against

### P1 — Execution without gate decision
Every payload passes through the ρ/γ/Δ gate before execution.
ABORT and PAUSE decisions prevent execution unconditionally.
PROCEED is required before `Invoke-Exec` fires.
**Mechanism:** gate check in `core/ve_gatecheck.py` + `core/ve_kernel.ps1` flow

### P2 — Arbitrary executable dispatch
Only allowlisted executables can be dispatched via `Invoke-Exec`:
`powershell`, `python`, `python3`, `py`, `bash`, `sh`, `pwsh`
**Mechanism:** allowlist check in `core/ve_kernel.ps1` before `&` dispatch

### P3 — Dangerous Python expression evaluation
`py:` payloads are evaluated with `_PY_SAFE_BUILTINS` only.
`__dunder__`, `import`, `open`, `getattr`, `globals`, `exec` are blocked.
**Mechanism:** `_py_safe()` blocker + `_PY_SAFE_BUILTINS` allowlist in `core/ve_kernel.py`

### P4 — Silent ledger tampering
Any modification to a ledger entry breaks the SHA-256 chain.
`ledger/ve_quickcheck.py` detects the break immediately.
**Mechanism:** `hash_prev` / `hash_self` chain in every JSONL entry

### P5 — Writes outside ve_data/
`core/ve_guard.ps1` (VE.Guard module) blocks Set-Content/Add-Content
to any path outside `ve_data/`. Blast radius is bounded.
**Mechanism:** `VE.Guard.psm1` regex allowlist on write commands

### P6 — Credential exfiltration via envelope
All cross-talk envelopes are HMAC-signed with `ve_shared.key`.
Unsigned or tampered envelopes will fail signature verification.
**Mechanism:** `New-VECrossTalkEnvelope` in `core/ve_kernel.ps1`

### P7 — Snapshot drift (ve_data/ modified without record)
`verify/ve_manifest_verify.py` verifies file hashes against snapshot manifest.
Unrecorded changes to `ve_data/` are detectable.
**Mechanism:** SHA-256 per-file verification against `.ve_snapshots/seq-NNNN/manifest.json`

---

## What VE Does NOT Protect Against

### N1 — Compromised operator
VE cannot protect against a malicious operator.
The operator has root-level access to policy, secrets, and the ledger.
This is by design — VE is a single-operator system.

### N2 — Kernel-level or hypervisor-level attacks
VE runs in userspace. A compromised OS or hypervisor bypasses all controls.

### N3 — Timing attacks on HMAC verification
VE uses standard string comparison for HMAC verification.
Not constant-time. Not hardened against timing side-channels.
Acceptable for v0.1 single-operator use. Not acceptable for distributed/multi-party.

### N4 — Formal verification of ρ/γ/Δ sufficiency
Thresholds are set by design intuition with documented reasoning (THRESHOLDS.md).
No Z3 or TLA+ proof that these values are sufficient for all threat models.
This is deferred to v0.2.

### N5 — Multi-operator trust and key rotation coordination
Current key rotation (`core/ve_key_rotate.ps1`) generates and archives keys locally.
No protocol exists for distributing keys to multiple operators simultaneously.
Single-operator deployment only.

### N6 — Adversarial payload crafting
VE's gate evaluates ρ/γ/Δ scores. How those scores are derived from input
is the operator's responsibility. VE trusts the scores it receives.
An adversary who can control the scoring system can bypass the gate.

### N7 — Python sandbox escape via attribute chain
`_py_safe()` is a string-based blocker, not a formal sandbox.
Sufficiently creative attribute access chains may bypass it.
For this threat level, remove `py:` exec entirely and use `echo:` only.

---

## Security Posture Summary

```
VE is designed for:
  Single trusted operator
  Trusted execution environment
  Audit-first deployment
  Governance of AI execution pipelines

VE is NOT designed for:
  Hostile multi-party environments
  Untrusted execution hosts
  Formal security certification
  High-value adversarial targets
```

This is a v0.1b governance substrate.
It is substantially more defensible than an ungoverned system.
It is not a replacement for formal security engineering.

---

*@BioAnkh84 — sole authority on all threat model decisions.*
*External review: @LabyrinthCoder, May 2026*
