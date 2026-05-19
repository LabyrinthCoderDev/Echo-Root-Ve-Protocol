## Final Handoff — May 2026
*@LabyrinthCoder*

### Added
- `HANDOFF.md` — plain-language note to @BioAnkh84 explaining what was done,
  what the repo is now, and what scale hardening comes next

---

## Documentation & Infrastructure Pass — May 2026
*@LabyrinthCoder — GPT recommendations applied*

### Added
- `Dockerfile` — deterministic Python environment, stdlib-only, smoke-tests on build
- `ENVIRONMENT.md` — pinned versions, compatibility matrix, Docker usage, quick check
- `THREAT_MODEL.md` — trusted/untrusted surfaces, 7 protections, 7 non-goals, assumptions
- `ARCHITECTURE.md` — full state machine diagram, component map, trust boundary, ledger chain, ψ_eff
- `RELEASE.md` — release checklist, tag process, hash verification, signing path, versioning

---

## Production Hardening Pass — May 2026
*@LabyrinthCoder — GPT review feedback applied*

### Fixed
- GAP-13: `core/ve_kernel.ps1` — `Invoke-Expression` replaced with allowlisted `&` dispatch
  Executable allowlist: powershell, python, python3, py, bash, sh, pwsh
  Arbitrary shell strings can no longer execute — only approved binaries
- GAP-14: `runners/ve_fullstack.ps1` — runtime script generation removed
  `Ensure-File` pattern replaced with direct tracked file references via `$PSScriptRoot`
  Production handoff should call real tracked files only — now it does
- GAP-15: `runners/run_all.ps1 -Quick` — path corrected to `verify/ve_prepush_check.ps1`

### Cleaned
- `__pycache__/` removed
- `.gitignore` updated: ve_data outputs, sysinfo.json, ledger.jsonl, .ve_logs/, dev-history/
- `KNOWN_GAPS.md` rewritten with honest framing (closed/deferred split, assumptions documented)

### Total: 15 gaps closed, 0 open, 5 deferred to v0.2

---

## Final Gap Closure — May 2026
*@LabyrinthCoder — all gaps closed*

### Fixed
- GAP-03: `.ve_snapshots/README.md` added — documents why seq-0001→0003 are absent
- GAP-04: `core/ve_kernel.py` — `py:` eval hardened with allowlist
  `_PY_SAFE_BUILTINS` allowlist + `_py_safe()` blocks `__dunder__`, `import`,
  `open`, `getattr`, etc. Arithmetic and string ops preserved. Quickcheck still passes.
- GAP-05: `core/ve_key_rotate.ps1` added — generates new 128-bit key,
  archives old key with timestamp, guides operator through rotation steps

### Added
- `Tests/test_ve_kernel_exec.py` — 10 tests covering exec, safety policy, blocked patterns

### Summary: 42 tests passing across 6 test files. All gaps closed.

---

## Gap Closure Pass — May 2026
*@LabyrinthCoder — all remaining open gaps closed*

### Fixed
- GAP-09: `ledger/ve_ledger_pin.ps1` — overwrite guard added
  `-Force` flag required to overwrite a non-empty ledger. Prevents accidental history destruction.
- GAP-11: Tests/ coverage — 32 tests across 5 test files, all passing
  - `Tests/test_ve_gatecheck.py` — 10 tests (gate logic, boundary conditions)
  - `Tests/test_ve_labeler.py` — 6 tests (epistemic labels)
  - `Tests/test_ve_schema_check.py` — 5 tests (ledger schema validation)
  - `Tests/test_ve_quickcheck.py` — 6 tests (hash chain integrity)
  - `Tests/test_ve_manifest_verify.py` — 5 tests (snapshot verification)

### Updated
- `runners/ve_fullstack.ps1` — epistemic labeler step (2b/5) wired in
- `KNOWN_GAPS.md` — all gaps updated to current status
- `THRESHOLDS.md` — GAP-06 resolved via documentation (formal proof is v0.2 work)

### Remaining (owner decisions, not code gaps)
- GAP-04: ve_kernel.py eval() sandbox — owner decides if/how to constrain
- GAP-05: Key rotation — owner defines policy for v0.2
- GAP-06: Formal Z3 proof of thresholds — v0.2 work

---

## Deep Audit Pass — May 2026
*@LabyrinthCoder — CI fixes, threshold documentation, Labyrinth component port*

### Fixed (CI was broken after restructure)
- Root shims added: `ve_kernel.ps1`, `ve_kernel.sh`, `ve_parse.sh`
  CI workflows called `./ve_kernel.ps1` etc at root — these now delegate to `core/`
- `ve_quickcheck_stub.py` added at root — required by `runners/ve_fullstack.ps1`
  and `.github/ve_checks.py` but was missing entirely from the original repo
- `ve-pr-check.yml` wired — was a TODO stub, now runs schema check + quickcheck + ve_checks.py
- `CONTRIBUTING.md` updated — referenced old root paths, now points to new structure

### Added
- `THRESHOLDS.md` — formal documentation of ρ/γ/Δ values with reasoning and ψ_eff
- `core/ve_labeler.py` — epistemic label layer (CLEAR/CAUTION/HIGH_DRIFT/UNRELIABLE)
  Ported from Labyrinth OS output_labeler.py. Adds plain-language signal to gate results.
- `Tests/test_ve_labeler.py` — 6 tests for ve_labeler.py (6/6 passing)

### Updated
- `KNOWN_GAPS.md` — GAP-02 marked FIXED, GAP-02 wiring complete
- `JOURNAL.md` — open items updated
- `STRUCTURE.md` — root shims documented

---

# Changelog — Vulpine Echo (VE)

## Build [2026-05] — External Review by @LabyrinthCoder

### Fixed
- `runners/run_all.ps1` — now delegates to `ve_fullstack.ps1` (was only calling `ve_syscheck.ps1`)
  Added `-Quick` flag for fast dev loop.
- `diag/ve_status.ps1` — hardcoded `C:\VE_Test_Suite_v0.1a` replaced with `$PSScriptRoot`
- `.gitignore` — `*.lock` coverage added

### Restructured
- 82 root files → `core/`, `ledger/`, `verify/`, `runners/`, `diag/`, `release/`
- `dev-history/` — 26 kernel `.bak` development snapshots (preserved, not deleted)
- `archive/runtime/` — `ve_ledger.lock` and run log
- `archive/test_runs/` — 3 artifact test run folders

### Added
- `WHAT_THIS_IS.md` — one-page orientation
- `STRUCTURE.md` — complete folder map with architecture notes
- `KNOWN_GAPS.md` — 11 items (3 fixed, 8 open)
- `JOURNAL.md` — project session log and standing orders
- `README.md` — rewritten with navigation, accurate layout, improved structure
- `bonus/labyrinth-reflections/` — philosophy, theory, metaphor, poetry

### Nothing removed
All original files present. Development history preserved.

---

## v0.1b — October 2025

- PS 5.1-safe kernel iterations
- Snapshot system (seq-0004 through seq-0021)
- Artifact test runs (3 sets)
- Multiple kernel refinements (preserved in dev-history/)

## v0.1a — October 2025

- Initial VE build
- PS 5.1-safe kernel entrypoint
- Clean child exec + quiet audit
- Minimal scaffolding for receipts
