"""
test_ve_quickcheck.py — Tests for ledger/ve_quickcheck.py
"""
import sys, json, hashlib, tempfile, os, subprocess
from pathlib import Path

LEDGER_DIR = Path(__file__).parent.parent / 'ledger'
SCRIPT     = str(LEDGER_DIR / 've_quickcheck.py')

def sha256(s): return hashlib.sha256(s.encode()).hexdigest()

def _make_entry(prev_hash, rho=0.81, gamma=0.77, delta=0.22, type_="RUN"):
    e = {"ts": "2025-10-31T00:00:00Z", "type": type_,
         "rho": rho, "gamma": gamma, "delta": delta,
         "hash_prev": prev_hash}
    payload = json.dumps({k: v for k, v in e.items() if k != "hash_self"},
                         separators=(',', ':'))
    e["hash_self"] = sha256(payload)
    return e

def _write(entries):
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl',
                                    delete=False, encoding='utf-8')
    for e in entries: f.write(json.dumps(e) + '\n')
    f.close()
    return f.name

def _run(path, psi_min=1.38):
    r = subprocess.run(
        [sys.executable, SCRIPT, '--ledger', path, '--psi-min', str(psi_min)],
        capture_output=True, text=True
    )
    return r.returncode, r.stdout + r.stderr

ZEROS = "0" * 64

def test_valid_chain():
    g = _make_entry(ZEROS, type_="GENESIS")
    e = _make_entry(g["hash_self"])
    path = _write([g, e])
    rc, out = _run(path)
    os.unlink(path)
    assert rc == 0, f"Expected 0 got {rc}: {out}"

def test_broken_chain():
    g = _make_entry(ZEROS, type_="GENESIS")
    e = _make_entry("badhash" + "0" * 57)  # wrong prev_hash
    path = _write([g, e])
    rc, out = _run(path)
    os.unlink(path)
    assert rc != 0, f"Broken chain should fail: {out}"

def test_tampered_entry():
    g = _make_entry(ZEROS, type_="GENESIS")
    # Tamper after building — change rho
    g["rho"] = 0.99
    path = _write([g])
    rc, out = _run(path)
    os.unlink(path)
    assert rc != 0, f"Tampered entry should fail: {out}"

def test_missing_ledger():
    rc, out = _run("/tmp/nonexistent_ledger_xyz.jsonl")
    assert rc != 0, "Missing ledger should fail"

def test_empty_ledger():
    path = _write([])
    rc, out = _run(path)
    os.unlink(path)
    # quickcheck on empty = no entries = pass (nothing to fail)
    # This is consistent with ve_quickcheck.py behavior
    assert rc == 0, f"Empty ledger rc={rc}: {out}"

def test_single_genesis():
    g = _make_entry(ZEROS, type_="GENESIS")
    path = _write([g])
    rc, out = _run(path)
    os.unlink(path)
    assert rc == 0, f"Single genesis should pass: {out}"


if __name__ == "__main__":
    tests = [test_valid_chain, test_broken_chain, test_tampered_entry,
             test_missing_ledger, test_empty_ledger, test_single_genesis]
    passed = failed = 0
    for t in tests:
        try:
            t(); print(f"  ✓ {t.__name__}"); passed += 1
        except Exception as e:
            print(f"  ✗ {t.__name__}: {e}"); failed += 1
    print(f"\n  {passed} passed / {failed} failed")
