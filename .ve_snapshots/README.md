# .ve_snapshots/

Snapshot system for Vulpine Echo — captures `ve_data/` state at key moments.

## Structure

Each snapshot is a numbered folder: `seq-NNNN/`
Contains: `hello.txt`, `manifest.json` (file hashes), `meta.json` (metadata)

## Sequence History

| Seq | Status | Notes |
|-----|--------|-------|
| seq-0001 | ABSENT | Early experiment — deleted before first stable build |
| seq-0002 | ABSENT | Early experiment — deleted before first stable build |
| seq-0003 | ABSENT | Early experiment — deleted before first stable build |
| seq-0004 | PRESENT | First stable snapshot |
| seq-0005+ | PRESENT | Normal sequence continues |

seq-0001 through seq-0003 were early development snapshots taken during
initial VE kernel construction in October 2025. They were intentionally
deleted as the system stabilised. The gap is expected and documented.

## How Snapshots Are Verified

```powershell
python verify\ve_manifest_verify.py --snap-root .ve_snapshots --seq 4 --data-root ve_data
```

## How New Snapshots Are Created

```powershell
.\release\ve_make_artifacts.ps1
```
