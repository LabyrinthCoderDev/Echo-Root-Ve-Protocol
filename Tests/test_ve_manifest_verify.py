"""
test_ve_manifest_verify.py — Tests for verify/ve_manifest_verify.py

API: python ve_manifest_verify.py --snap-root <dir> --seq <n> --data-root <dir>
Reads snapshot from <snap-root>/seq-NNNN/manifest.json
Compares against live files in <data-root>
"""
import sys, json, hashlib, tempfile, shutil, os, subprocess
from pathlib import Path

SCRIPT = str(Path(__file__).parent.parent / 'verify' / 've_manifest_verify.py')

def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''): h.update(chunk)
    return h.hexdigest()

def _make_snapshot(snap_root, seq, data_root, files):
    snap_dir = Path(snap_root) / f'seq-{seq:04d}'
    snap_dir.mkdir(parents=True, exist_ok=True)
    Path(data_root).mkdir(exist_ok=True)
    manifest = []
    for name, content in files.items():
        p = Path(data_root) / name
        p.write_text(content, encoding='utf-8')
        manifest.append({"path": name, "size": p.stat().st_size,
                          "sha256": _sha256_file(str(p))})
    (snap_dir / 'manifest.json').write_text(json.dumps(manifest))
    (snap_dir / 'meta.json').write_text('{}')

def _run(snap_root, seq, data_root):
    r = subprocess.run(
        [sys.executable, SCRIPT,
         '--snap-root', snap_root, '--seq', str(seq), '--data-root', data_root],
        capture_output=True, text=True
    )
    return r.returncode, r.stdout + r.stderr

def test_valid_snapshot():
    tmp = tempfile.mkdtemp()
    _make_snapshot(tmp+'/s', 1, tmp+'/d', {"hello.txt": "hello world"})
    rc, out = _run(tmp+'/s', 1, tmp+'/d')
    shutil.rmtree(tmp)
    assert rc == 0, f"Expected 0 got {rc}: {out}"

def test_tampered_file():
    tmp = tempfile.mkdtemp()
    _make_snapshot(tmp+'/s', 1, tmp+'/d', {"hello.txt": "hello world"})
    (Path(tmp+'/d') / 'hello.txt').write_text("TAMPERED")
    rc, out = _run(tmp+'/s', 1, tmp+'/d')
    shutil.rmtree(tmp)
    assert rc != 0, f"Tampered file should fail: {out}"

def test_missing_file():
    tmp = tempfile.mkdtemp()
    _make_snapshot(tmp+'/s', 1, tmp+'/d', {"a.txt": "a", "b.txt": "b"})
    (Path(tmp+'/d') / 'b.txt').unlink()
    rc, out = _run(tmp+'/s', 1, tmp+'/d')
    shutil.rmtree(tmp)
    assert rc != 0, f"Missing file should fail: {out}"

def test_multiple_files():
    tmp = tempfile.mkdtemp()
    _make_snapshot(tmp+'/s', 1, tmp+'/d', {f"f{i}.txt": f"c{i}" for i in range(5)})
    rc, out = _run(tmp+'/s', 1, tmp+'/d')
    shutil.rmtree(tmp)
    assert rc == 0, f"Multiple files should pass: {out}"

def test_missing_snapshot_seq():
    tmp = tempfile.mkdtemp()
    Path(tmp+'/s').mkdir()
    Path(tmp+'/d').mkdir()
    rc, out = _run(tmp+'/s', 99, tmp+'/d')
    shutil.rmtree(tmp)
    assert rc != 0, f"Missing seq should fail: {out}"


if __name__ == "__main__":
    tests = [test_valid_snapshot, test_tampered_file, test_missing_file,
             test_multiple_files, test_missing_snapshot_seq]
    passed = failed = 0
    for t in tests:
        try:
            t(); print(f"  ✓ {t.__name__}"); passed += 1
        except Exception as e:
            print(f"  ✗ {t.__name__}: {e}"); failed += 1
    print(f"\n  {passed} passed / {failed} failed")
