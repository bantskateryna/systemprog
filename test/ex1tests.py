import os
import sys
import subprocess
import tempfile

SCRIPT = os.path.abspath("lab2ex1.py")
PY = sys.executable

def run_args(args, input_bytes=None):
    proc = subprocess.run([PY, SCRIPT] + args, input=input_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout.decode('utf-8', errors='replace'), proc.stderr.decode('utf-8', errors='replace')

def make_temp_file(content):
    fd, path = tempfile.mkstemp(text=True)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def test_help_exits_without_filepath():
    code, out, err = run_args(["--help"])
    assert code == 0
    assert "usage" in out.lower() or "usage" in err.lower()

def test_reads_default_10_lines():
    content = "\n".join(str(i) for i in range(1, 21)) + "\n"
    path = make_temp_file(content)
    try:
        code, out, err = run_args([path])
        assert code == 0
        lines = out.strip().splitlines()
        assert len(lines) == 10
        assert lines[0] == "1"
        assert lines[-1] == "10"
    finally:
        os.remove(path)

def test_reads_n_lines_flag():
    content = "\n".join(["a","b","c","d"]) + "\n"
    path = make_temp_file(content)
    try:
        code, out, err = run_args(["-n", "2", path])
        assert code == 0
        lines = out.strip().splitlines()
        assert lines == ["a", "b"]
    finally:
        os.remove(path)

def test_reads_bytes_flag():
    content = "абвгде"
    path = make_temp_file(content)
    try:
        code, out, err = run_args(["-c", "4", path])
        assert code == 0
        assert len(out) >= 1
    finally:
        os.remove(path)

def test_verbose_shows_header_when_color_off():
    content = "one\ntwo\n"
    path = make_temp_file(content)
    try:
        code, out, err = run_args(["-v", path])
        assert code == 0
        assert "==>" in out
        assert path in out
    finally:
        os.remove(path)

def test_line_numbers_flag_prefixes_numbers():
    content = "x\ny\nz\n"
    path = make_temp_file(content)
    try:
        code, out, err = run_args(["--line-numbers", "-n", "2", path])
        assert code == 0
        lines = out.strip().splitlines()
        assert lines[0].strip().startswith("1:")
        assert lines[1].strip().startswith("2:")
    finally:
        os.remove(path)

def test_reads_from_stdin_when_no_filepath_and_pipe():
    content = "\n".join(str(i) for i in range(1, 6)) + "\n"
    proc = subprocess.run([PY, SCRIPT], input=content.encode("utf-8"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = proc.stdout.decode("utf-8", errors="replace")
    assert proc.returncode == 0
    lines = out.strip().splitlines()
    assert lines[0] == "1"
    assert lines[-1] == "5"

def test_error_when_filepath_missing_and_bytes_flag():
    code, out, err = run_args(["-c", "5"])
    assert code != 0
    assert "required" in err.lower() or "required" in out.lower()
