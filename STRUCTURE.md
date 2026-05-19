# Structure — Vulpine Echo (VE)

---

## Root Level

```
README.md                   primary documentation
WHAT_THIS_IS.md             one-page orientation
CHANGELOG.md                version history
KNOWN_GAPS.md               honest open issues
JOURNAL.md                  project session log
STRUCTURE.md                this file
RELEASE_NOTES.md            release notes
CONTRIBUTING.md             contribution guide
CODE_OF_CONDUCT.md          conduct policy
SECURITY.md                 security policy
CITATION.cff                academic citation
LICENSE                     MIT
.gitignore / .gitattributes / .editorconfig

# CI compatibility shims (thin wrappers → call into core/)
ve_kernel.ps1           shim → core/ve_kernel.ps1
ve_kernel.sh            shim → core/ve_kernel.sh
ve_parse.sh             shim → core/ve_parse.sh
ve_quickcheck_stub.py   shim → ledger/ve_quickcheck.py (expected by ve_fullstack)
```

---

## core/ — Kernel, Gate, Guard, Policy

```
ve_kernel.ps1       Primary entrypoint — HMAC-signed envelope, ledger write
ve_kernel.py        Python bridge — echo:, py:, audit, quickcheck
ve_kernel.sh        Linux/Mac shell entry
ve_parse.sh         Shell parser for Linux CI
ve.ps1              Thin wrapper
ve_launch.cmd       Windows launcher (double-click safe)
ve_guard.ps1        Write guard — limits writes to ve_data/ only
ve_gatecheck.py     Gate logic — ρ/γ/Δ → PROCEED/PAUSE/ABORT (20 lines)
policy.ve.psl       Policy spec — operator-readable TOML-like config
ve_atomic_io.ps1    Atomic I/O operations
ve_fastpath.ps1     Fast execution path
```

---

## ledger/ — Hash-Chained Audit Trail

```
ve_ledger_append.ps1          Append entry to JSONL ledger
ve_ledger_append_atomic.ps1   Atomic append (race-safe)
ve_ledger_pin.ps1             Write genesis entry (WARNING: destructive — see KNOWN_GAPS)
ve_schema_check.py            Full chain validator (hash_prev verification)
ve_quickcheck.py              Fast integrity checker
ve_genesis_ii.jsonl           Genesis record
ve_guard_log.jsonl            Guard decision log
```

---

## verify/ — Handshake, Manifest, Self-Test

```
ve_handshake.ps1        PS↔Python handshake protocol
ve_handshake.py         Python handshake
ve_handshake_file.py    File-based handshake
ve_manifest_verify.py   File manifest verification against snapshot hashes
ve_selftest.ps1         Self-test suite
ve_prepush_check.ps1    Pre-push gate (run before every push)
```

---

## runners/ — How to Run the System

```
run_all.ps1       TOP-LEVEL ENTRY POINT → delegates to ve_fullstack.ps1
                  Accepts -Quick flag for fast dev loop
ve_fullstack.ps1  Complete pipeline: unblock → handshake → gate → ledger → sysinfo → quickcheck
ve_stable_run.ps1 Stable/demo runner
VE_Demo_Run.ps1   Demo script (starts local server)
Enter-VE.ps1      Environment entry point
```

**Start here:** `.\runners\run_all.ps1`

---

## diag/ — Diagnostics, Status, Tools

```
ve_audit.ps1      Audit the ledger
ve_diag.ps1       Environment diagnostics
ve_status.ps1     Repo health check (uses $PSScriptRoot — portable)
ve_syscheck.ps1   System check
ve_sysinfo.ps1    System information collector
ve_tools.ps1      Helper utilities
```

---

## release/ — Release and Artifact Tooling

```
ve_release_prep.ps1      Prepare a release
ve_make_artifacts.ps1    Generate test artifact sets
patch_ve_kernel_exec.ps1 Kernel patch utility
```

---

## Standard Folders

```
Modules/          PowerShell modules
  VE.Guard/       Write guard module
  VE.FastPath/    Fast path module
Tests/            Test files (VE.Guard.Tests.ps1)
egs/              Example payloads (hello2.txt, payload.json, payload_diag.json)
.ve_snapshots/    Snapshot system — seq-0004 through seq-0021
  seq-NNNN/       Each has hello.txt + manifest.json + meta.json
ve_data/          Runtime data (gitignored in production)
.github/          CI workflows + issue templates + CODEOWNERS
```

---

## History and Archives

```
dev-history/      26 kernel development snapshots (.bak files from Oct 2025)
                  Development history of ve_kernel.ps1 evolution.
                  Safe to delete once git branch history covers this period.
                  Gitignored from tracking — present for local reference only.
archive/
  test_runs/      3 artifact test run folders (evidence of test history)
  runtime/        ve_ledger.lock + ve_run_20251028_051438.log
```

---

## bonus/ — Philosophy, Theory, Metaphor, Poetry

```
bonus/
  labyrinth-reflections/   External analysis and philosophical writing
                           about what VE means and why it matters.
                           Read it or don't — the code works without it.
```

---

*Structure by @LabyrinthCoder | May 2026*
