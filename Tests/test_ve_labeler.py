"""
test_ve_labeler.py — Tests for ve_labeler.py
"""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent / "core"))
from ve_labeler import label


def test_clear():
    r = label(rho=0.90, gamma=0.85, delta=0.15, decision="PROCEED")
    assert r.label == "CLEAR", f"Expected CLEAR got {r.label}"
    assert r.decision == "PROCEED"

def test_caution_rho_near_floor():
    r = label(rho=0.72, gamma=0.85, delta=0.10, decision="PROCEED")
    assert r.label in ("CAUTION", "UNRELIABLE"), f"Expected CAUTION/UNRELIABLE got {r.label}"

def test_high_drift():
    r = label(rho=0.90, gamma=0.85, delta=0.35, decision="PAUSE")
    assert r.label == "HIGH_DRIFT", f"Expected HIGH_DRIFT got {r.label}"

def test_unreliable_multiple_weak():
    r = label(rho=0.65, gamma=0.63, delta=0.28, decision="ABORT")
    assert r.label == "UNRELIABLE", f"Expected UNRELIABLE got {r.label}"

def test_to_dict_keys():
    r = label(rho=0.80, gamma=0.80, delta=0.20, decision="PROCEED")
    d = r.to_dict()
    for key in ("label", "reason", "rho", "gamma", "delta", "decision"):
        assert key in d, f"Missing key: {key}"

def test_abort_high_delta():
    r = label(rho=0.60, gamma=0.60, delta=0.45, decision="ABORT")
    assert r.label == "UNRELIABLE"

if __name__ == "__main__":
    tests = [test_clear, test_caution_rho_near_floor, test_high_drift,
             test_unreliable_multiple_weak, test_to_dict_keys, test_abort_high_delta]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {t.__name__}: {e}")
            failed += 1
    print(f"\n  {passed} passed / {failed} failed")
