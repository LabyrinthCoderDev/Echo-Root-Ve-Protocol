"""
test_ve_schema_check.py — Tests for ledger/ve_schema_check.py
"""
import sys, json, tempfile, os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "ledger"))

def _write_ledger(entries):
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl',
                                    delete=False, encoding='utf-8')
    for e in entries: f.write(json.dumps(e) + '\n')
    f.close()
    return f.name

def _run(path, psi_min=1.38):
    import subprocess, sys
    r = subprocess.run(
        [sys.executable,
         str(Path(__file__).parent.parent / 'ledger' / 've_schema_check.py'),
         '--ledger', path, '--psi-min', str(psi_min)],
        capture_output=True, text=True
    )
    return r.returncode, r.stdout

ZEROS = "0" * 64

def _good_entry(prev="", rho=0.81, gamma=0.77, delta=0.22, psi_min=1.38):
    import hashlib
    e = {"timestamp": "2025-10-31T00:00:00Z", "event": "test",
         "psi_min": psi_min, "hash_prev": prev,
         "rho": rho, "gamma": gamma, "delta": delta}
    payload = json.dumps(e, separators=(',', ':'))
    e["hash_self"] = hashlib.sha256(payload.encode()).hexdigest()
    return e

def test_valid_single_entry():
    e = _good_entry(prev=ZEROS)
    path = _write_ledger([e])
    rc, out = _run(path)
    os.unlink(path)
    assert rc == 0, f"Expected 0 got {rc}: {out}"

def test_missing_required_field():
    e = {"timestamp": "2025-10-31T00:00:00Z", "event": "test",
         "hash_prev": ZEROS, "hash_self": "abc"}
    # missing psi_min
    path = _write_ledger([e])
    rc, out = _run(path)
    os.unlink(path)
    assert rc != 0, "Expected failure for missing psi_min"

def test_empty_ledger_fails():
    path = _write_ledger([])
    rc, out = _run(path)
    os.unlink(path)
    assert rc != 0, "Empty ledger should fail"

def test_psi_below_minimum():
    # psi_min field in entry is 1.20 < required 1.38
    e = _good_entry(prev=ZEROS, psi_min=1.20)
    path = _write_ledger([e])
    rc, out = _run(path)
    os.unlink(path)
    assert rc != 0, f"Low psi should fail: {out}"

def test_invalid_json_line():
    path = _write_ledger([])
    with open(path, 'w') as f:
        f.write('not json\n')
    rc, out = _run(path)
    os.unlink(path)
    assert rc != 0, "Invalid JSON should fail"


if __name__ == "__main__":
    tests = [test_valid_single_entry, test_missing_required_field,
             test_empty_ledger_fails, test_psi_below_minimum,
             test_invalid_json_line]
    passed = failed = 0
    for t in tests:
        try:
            t(); print(f"  ✓ {t.__name__}"); passed += 1
        except Exception as e:
            print(f"  ✗ {t.__name__}: {e}"); failed += 1
    print(f"\n  {passed} passed / {failed} failed")
