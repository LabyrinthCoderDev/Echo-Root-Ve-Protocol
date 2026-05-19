# Release Process — Vulpine Echo (VE)

## Release Checklist

Before tagging any release:

```
[ ] All tests pass:  python -m pytest Tests/ -v  (42/42)
[ ] Pre-push check:  runners/run_all.ps1 -Quick  (exit 0)
[ ] CHANGELOG.md updated with release entry
[ ] VERSION file bumped
[ ] KNOWN_GAPS.md current
[ ] No runtime files tracked (ve_ledger.jsonl, ledger.jsonl, sysinfo.json)
[ ] run:  git status  — confirm no unexpected files
```

## Tagging a Release

```bash
# Confirm working tree is clean
git status

# Create annotated tag
git tag -a v0.1b -m "VE v0.1b — governed execution harness"

# Generate release hash for RELEASE_HASHES.txt
git rev-parse v0.1b > release_hash.txt
git show v0.1b --stat >> release_hash.txt

# Push tag
git push origin v0.1b
```

## Release Hash Verification

Every release should have a verifiable hash recorded.

```
v0.1b   commit: <sha>   date: 2025-10-xx
```

To verify a downloaded release against the published hash:
```bash
git verify-commit <sha>   # if GPG signing is configured
git show <sha> --stat     # manual verification
```

## Signing (recommended for v0.2+)

```bash
# Set up GPG signing
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true

# Sign a tag
git tag -s v0.2.0 -m "VE v0.2.0"

# Verify
git verify-tag v0.2.0
```

## Semantic Versioning

```
v0.1a   Initial build — PS 5.1 kernel, ledger, gate, guard
v0.1b   Snapshot system, CI, multiple kernel iterations
v0.1b+  Rehabilitation pass — structure, tests, hardening
v0.2.0  Target: Z3 threshold proofs, multi-operator support
```

---

*@BioAnkh84 — sole release authority*
