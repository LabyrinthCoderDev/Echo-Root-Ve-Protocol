"""
test_ve_kernel_exec.py — Tests for core/ve_kernel.py exec and safety policy
"""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent / "core"))
from ve_kernel import do_exec, _py_safe, EXIT_OK, EXIT_FAIL


def test_echo_exec():
    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = do_exec("echo: hello world")
    assert rc == EXIT_OK
    assert "hello world" in buf.getvalue()

def test_py_arithmetic():
    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = do_exec("py: (10*2)+5")
    assert rc == EXIT_OK
    assert buf.getvalue().strip() == "25"

def test_py_fstring():
    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = do_exec('py: f"sum={1+2}"')
    assert rc == EXIT_OK
    assert "sum=3" in buf.getvalue()

def test_py_blocked_dunder():
    rc = do_exec("py: __import__('os')")
    assert rc == EXIT_FAIL, "dunder should be blocked"

def test_py_blocked_import():
    rc = do_exec("py: import os")
    assert rc == EXIT_FAIL, "import should be blocked"

def test_py_blocked_getattr():
    rc = do_exec("py: getattr(int, '__bases__')")
    assert rc == EXIT_FAIL, "getattr should be blocked"

def test_py_blocked_open():
    rc = do_exec("py: open('/etc/passwd')")
    assert rc == EXIT_FAIL, "open should be blocked"

def test_empty_payload():
    rc = do_exec("")
    assert rc == EXIT_FAIL

def test_safe_check_passes_arithmetic():
    assert _py_safe("(10*2)+5") is True

def test_safe_check_blocks_dunder():
    assert _py_safe("__import__('os')") is False


if __name__ == "__main__":
    tests = [
        test_echo_exec, test_py_arithmetic, test_py_fstring,
        test_py_blocked_dunder, test_py_blocked_import,
        test_py_blocked_getattr, test_py_blocked_open,
        test_empty_payload, test_safe_check_passes_arithmetic,
        test_safe_check_blocks_dunder,
    ]
    passed = failed = 0
    for t in tests:
        try:
            t(); print(f"  ✓ {t.__name__}"); passed += 1
        except Exception as e:
            print(f"  ✗ {t.__name__}: {e}"); failed += 1
    print(f"\n  {passed} passed / {failed} failed")
