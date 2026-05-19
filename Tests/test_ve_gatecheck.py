"""
test_ve_gatecheck.py — Tests for core/ve_gatecheck.py
"""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent / "core"))
from ve_gatecheck import gate


def test_proceed_all_in_range():
    assert gate(0.90, 0.85, 0.15) == "PROCEED"

def test_proceed_at_exact_thresholds():
    assert gate(0.70, 0.70, 0.30) == "PROCEED"

def test_abort_high_delta():
    assert gate(0.90, 0.90, 0.45) == "ABORT"

def test_abort_low_gamma():
    assert gate(0.90, 0.60, 0.20) == "ABORT"

def test_pause_rho_below_floor():
    assert gate(0.65, 0.80, 0.20) == "PAUSE"

def test_pause_gamma_near_abort_but_not_abort():
    # gamma=0.66 — above abort threshold 0.65, below proceed floor 0.70
    assert gate(0.80, 0.66, 0.20) == "PAUSE"

def test_pause_delta_above_ceil_below_abort():
    # delta=0.35 — above proceed ceiling 0.30, below abort threshold 0.40
    assert gate(0.80, 0.80, 0.35) == "PAUSE"

def test_abort_boundary_delta():
    # delta exactly at abort threshold
    assert gate(0.90, 0.90, 0.41) == "ABORT"

def test_proceed_boundary_rho():
    assert gate(0.70, 0.85, 0.20) == "PROCEED"

def test_abort_both_triggers():
    assert gate(0.50, 0.60, 0.50) == "ABORT"


if __name__ == "__main__":
    tests = [
        test_proceed_all_in_range, test_proceed_at_exact_thresholds,
        test_abort_high_delta, test_abort_low_gamma,
        test_pause_rho_below_floor, test_pause_gamma_near_abort_but_not_abort,
        test_pause_delta_above_ceil_below_abort, test_abort_boundary_delta,
        test_proceed_boundary_rho, test_abort_both_triggers,
    ]
    passed = failed = 0
    for t in tests:
        try:
            t(); print(f"  ✓ {t.__name__}"); passed += 1
        except Exception as e:
            print(f"  ✗ {t.__name__}: {e}"); failed += 1
    print(f"\n  {passed} passed / {failed} failed")
