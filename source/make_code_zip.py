# Builds downloads/ml-academy-code.zip: every lesson's code, the projects and the challenges as plain .py scripts,
# with pytest tests and expected outputs. Run after make_notebooks.py.   Usage: python make_code_zip.py OUT_DIR
import ast, io, json, os, re, shutil, subprocess, sys, tempfile, textwrap, zipfile
import nbformat

OUT = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lesson21_data  # noqa: F401  (adds Lesson 21 to the shared dictionaries)
from challenges import C as CHAL
src = open(os.path.join(HERE, "build.py")).read()
LESSONS = eval(re.search(r"LESSONS = (\[.*?\n\])", src, re.S).group(1)) + [lesson21_data.L21]
from lesson0_data import LESSON0
TITLE = {n: t for (n, p, t, s, m) in [LESSON0] + LESSONS}
spec = __import__("importlib.util").util.spec_from_file_location("mk", os.path.join(HERE, "make_notebooks.py"))
MK = open(os.path.join(HERE, "make_notebooks.py")).read()
CHECK_FN = re.search(r'CHECK_FN = \((.*?)\)\n', MK, re.S).group(1)
CHECK_FN = eval("(" + CHECK_FN + ")")
def starter_of(ch):
    name, sol = ch[3], ch[4]
    return ch[6] if len(ch) > 6 and ch[6] else (re.match(r"\s*", sol).group(0) + name + " = None  # ← your code here")
def fill(code, line):
    return code.replace("    ##BLANK##", line) if "    ##BLANK##" in code else code.replace("##BLANK##", line.strip())

DATA_HDR = 'from pathlib import Path\nDATA = Path(__file__).resolve().parent.parent / "data"   # the course\'s data folder\n'

def comment(md):
    lines = []
    for ln in md.strip().splitlines():
        ln = re.sub(r"[*`]", "", ln).replace("$", "")
        ln = re.sub(r"^#+\s*", "", ln)
        lines += textwrap.wrap(ln, 96) or [""]
    return "\n".join(("# " + l).rstrip() for l in lines)

def scriptify(code):
    """Make a notebook cell work as a script: print a bare final expression, fix data paths."""
    code = code.replace('pd.read_csv("../data/houses.csv")', 'pd.read_csv(DATA / "houses.csv")')
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        last = tree.body[-1]
        if not (isinstance(last.value, ast.Call) and getattr(last.value.func, "id", "") in ("print", "check")) and not isinstance(last.value, ast.Constant):
            lines = code.splitlines(); a, b = last.lineno - 1, last.end_lineno
            expr = "\n".join(lines[a:b])
            lines[a:b] = [f"print({expr})"]
            code = "\n".join(lines)
    return code

TMP = tempfile.mkdtemp(); ROOT = os.path.join(TMP, "ml-academy-code")
for d in ["lessons", "challenges", "projects", "tests/expected", "data"]: os.makedirs(os.path.join(ROOT, d))
shutil.copy(os.path.join(HERE, "data", "houses.csv"), os.path.join(ROOT, "data", "houses.csv"))

nbdir = os.path.join(OUT, "notebooks")
for n in sorted(TITLE):
    nb = nbformat.read(os.path.join(nbdir, f"lesson-{n:02d}.ipynb"), as_version=4)
    body, torch = [], []
    for c in nb.cells[1:]:
        if c.cell_type == "markdown" and c.source.startswith("## Coding challenges"): break
        if c.cell_type == "markdown":
            if "```python" in c.source and "import torch" in c.source:
                torch.append(re.search(r"```python\n(.*?)```", c.source, re.S).group(1))
                body.append("# (The PyTorch example for this section is in lesson-19-pytorch.py — it needs PyTorch installed.)")
            elif c.source.startswith("## "):
                body.append("\n" + "#" * 78 + "\n" + comment(c.source) + "\n" + "#" * 78)
            else:
                body.append(comment(c.source))
        else:
            body.append(scriptify(c.source))
    text = f'"""Lesson {n}: {TITLE[n]} — all the code from the lesson, as one script.\n\nPart of the ML Academy course. Run it with:  python lesson-{n:02d}.py\n(works from any folder; the data is read from ../data/)\n"""\n'
    uses_data = any("DATA /" in b for b in body)
    text += (DATA_HDR if uses_data else "") + "\n".join(body) + "\n"
    open(os.path.join(ROOT, "lessons", f"lesson-{n:02d}.py"), "w").write(text)
    for k, t in enumerate(torch):
        open(os.path.join(ROOT, "lessons", f"lesson-{n:02d}-pytorch.py"), "w").write(
            f'"""Lesson {n}: the PyTorch example. Needs PyTorch:  pip install torch  (see pytorch.org)\nNot run by the tests.\n"""\n' + t)
    if n in CHAL:
        ch = f'"""Lesson {n} coding challenges. Each block has ONE missing line marked "your code here" or "replace".\nWrite the line, run this file, and each check prints ✅ or a hint.  Solutions: the SOLUTIONS list in tests/test_code.py\n"""\n' + (DATA_HDR if any("houses.csv" in x[2] for x in CHAL[n]) else "") + CHECK_FN
        for k, c in enumerate(CHAL[n]):
            ch += f"\n\n# ---- Challenge {k + 1}: {c[0]} ----\n# {c[1]}\n" + scriptify(fill(c[2], starter_of(c))) + f"\ncheck({c[3]}, EXPECTED_{k + 1}, hint={c[5]!r})\n"
        # expected values computed from the solutions
        exp = []
        for k, c in enumerate(CHAL[n]):
            cwd = os.getcwd(); os.chdir(os.path.join(ROOT, "lessons"))
            try:
                ns = {}
                with __import__("contextlib").redirect_stdout(io.StringIO()):
                    exec(scriptify(fill(c[2], c[4])).replace('DATA / "houses.csv"', '"../data/houses.csv"'), ns)
            finally: os.chdir(cwd)
            v = ns[c[3]]; v = v.tolist() if hasattr(v, "tolist") else (float(v) if not isinstance(v, (int, float)) else v)
            exp.append(f"EXPECTED_{k + 1} = {v!r}")
        ch = ch.replace(CHECK_FN, CHECK_FN + "\n" + "\n".join(exp) + "\n", 1)
        open(os.path.join(ROOT, "challenges", f"lesson-{n:02d}-challenges.py"), "w").write(ch)

# projects
for f in sorted(os.listdir(os.path.join(nbdir, "projects"))):
    if not f.endswith(".ipynb"): continue
    nb = nbformat.read(os.path.join(nbdir, "projects", f), as_version=4)
    kind = "solution" if "solution" in f else "starter"
    body = []
    for c in nb.cells:
        body.append(comment(c.source) if c.cell_type == "markdown" else scriptify(c.source))
    head = (f'"""Mini-project ({kind}). ' + ("Fill in each TODO from top to bottom and run the file again; it stops at the first unfinished step, and each check() prints ✅ or a hint." if kind == "starter" else "The complete worked solution.") + '\nRun with:  python ' + f.replace(".ipynb", ".py") + '\n"""\n')
    open(os.path.join(ROOT, "projects", f.replace(".ipynb", ".py")), "w").write(head + "\n".join(body) + "\n")

# tests
TESTS = r'''"""Tests for the ML Academy code.   Run from the ml-academy-code folder:   pytest -q

* test_lessons     — every lesson script runs and prints the same output as when the course was published
                     (numbers may differ by tiny rounding; library updates can change them — see tests/expected/).
* test_projects    — every project solution runs and all its checks pass.
* test_challenges  — every challenge solution produces the expected answer, and every starter does not (yet).
"""
import os, re, subprocess, sys, pathlib, pytest
ROOT = pathlib.Path(__file__).resolve().parent.parent
NUM = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")
ENV = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8", PYTHONWARNINGS="ignore")

def run(path):
    return subprocess.run([sys.executable, str(path)], cwd=path.parent, env=ENV, capture_output=True, text=True, encoding="utf-8", timeout=900)

def same(a, b, tol=1e-6):
    ta, tb = a.split(), b.split()
    if len(ta) != len(tb): return False
    for x, y in zip(ta, tb):
        if x == y: continue
        nx, ny = NUM.findall(x), NUM.findall(y)
        if NUM.sub("#", x) != NUM.sub("#", y) or len(nx) != len(ny): return False
        if any(abs(float(p) - float(q)) > max(tol * max(abs(float(p)), abs(float(q))), 1e-9) for p, q in zip(nx, ny)): return False
    return True

@pytest.mark.parametrize("script", sorted((ROOT / "lessons").glob("lesson-??.py")), ids=lambda p: p.name)
def test_lessons(script):
    r = run(script)
    assert r.returncode == 0, r.stderr[-2000:]
    expected = (ROOT / "tests" / "expected" / (script.stem + ".txt")).read_text(encoding="utf-8")
    assert same(r.stdout, expected), "output changed — compare with tests/expected/" + script.stem + ".txt\n" + r.stdout[-2000:]

@pytest.mark.parametrize("script", sorted((ROOT / "projects").glob("*-solution.py")), ids=lambda p: p.name)
def test_projects(script):
    r = run(script)
    assert r.returncode == 0, r.stderr[-2000:]
    assert "Not yet" not in r.stdout and "✅" in r.stdout, r.stdout[-2000:]

SOLUTIONS = __SOLUTIONS__

@pytest.mark.parametrize("lesson,k,code,name,want", SOLUTIONS, ids=[f"lesson{s[0]}-challenge{s[1]}" for s in SOLUTIONS])
def test_challenges(lesson, k, code, name, want):
    import numpy as np, contextlib, io
    cwd = os.getcwd(); os.chdir(ROOT / "lessons")
    try:
        ns = {"DATA": ROOT / "data"}
        with contextlib.redirect_stdout(io.StringIO()): exec(code, ns)
    finally: os.chdir(cwd)
    got = ns[name]
    assert np.shape(got) == np.shape(want) and np.allclose(np.asarray(got, dtype=float), np.asarray(want, dtype=float), rtol=1e-4, atol=1e-6)

@pytest.mark.parametrize("script", sorted((ROOT / "challenges").glob("*.py")), ids=lambda p: p.name)
def test_challenge_starters_are_unsolved(script):
    r = run(script)
    assert "Not yet" in r.stdout or r.returncode != 0
'''
sols = []
for n in sorted(CHAL):
    for k, c in enumerate(CHAL[n]):
        code = scriptify(fill(c[2], c[4]))
        cwd = os.getcwd(); os.chdir(os.path.join(ROOT, "lessons"))
        try:
            ns = {"DATA": __import__("pathlib").Path(os.path.join(ROOT, "data"))}
            with __import__("contextlib").redirect_stdout(io.StringIO()): exec(code, ns)
        finally: os.chdir(cwd)
        v = ns[c[3]]; v = v.tolist() if hasattr(v, "tolist") else (float(v) if not isinstance(v, (int, float)) else v)
        sols.append((n, k + 1, code, c[3], v))
open(os.path.join(ROOT, "tests", "test_code.py"), "w").write(TESTS.replace("__SOLUTIONS__", "[\n" + ",\n".join("    " + repr(s) for s in sols) + "\n]"))

# expected outputs for the lesson scripts
env = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8", PYTHONWARNINGS="ignore")
for f in sorted(os.listdir(os.path.join(ROOT, "lessons"))):
    if not re.match(r"lesson-\d\d\.py$", f): continue
    r = subprocess.run([sys.executable, f], cwd=os.path.join(ROOT, "lessons"), env=env, capture_output=True, text=True, encoding="utf-8", timeout=900)
    if r.returncode: print("SCRIPT FAILED", f, r.stderr[-800:]); sys.exit(1)
    open(os.path.join(ROOT, "tests", "expected", f.replace(".py", ".txt")), "w", encoding="utf-8").write(r.stdout)
for leftover in ["churn_model.joblib"]:
    p = os.path.join(ROOT, "lessons", leftover)
    if os.path.exists(p): os.remove(p)

open(os.path.join(ROOT, "requirements.txt"), "w").write(open(os.path.join(HERE, "code_requirements.txt")).read())
open(os.path.join(ROOT, "README.md"), "w").write(open(os.path.join(HERE, "code_README.md")).read())

os.makedirs(os.path.join(OUT, "downloads"), exist_ok=True)
zp = os.path.join(OUT, "downloads", "ml-academy-code.zip")
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for d, _, fs in sorted(os.walk(ROOT)):
        for f in sorted(fs):
            if "__pycache__" in d or f.endswith((".pyc", ".joblib")): continue
            full = os.path.join(d, f); arc = os.path.relpath(full, TMP)
            zi = zipfile.ZipInfo(arc, date_time=(2026, 11, 2, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16
            z.writestr(zi, open(full, "rb").read())
print("zip:", zp, os.path.getsize(zp), "bytes;", sum(1 for _ in zipfile.ZipFile(zp).namelist()), "files; work dir", ROOT)
