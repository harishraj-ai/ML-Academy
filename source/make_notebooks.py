"""Build one Jupyter notebook per lesson from its code blocks, then execute it so outputs are included."""
import html, os, re, sys, tempfile, io, contextlib
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from nbclient import NotebookClient

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(sys.argv[1], "notebooks")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, HERE)
import importlib.util
spec = importlib.util.spec_from_file_location("b", os.path.join(HERE, "build.py"))
src = open(os.path.join(HERE, "build.py")).read()
LESSONS = eval(re.search(r"LESSONS = (\[.*?\n\])", src, re.S).group(1))
import lesson21_data; LESSONS.append(lesson21_data.L21)

CODE_RE = re.compile(r"^\s*(import |from \S+ import )|\bprint\(|\bdef | = ", re.M)

def plain(h):
    h = re.sub(r"<[^>]+>", "", h)
    return html.unescape(h).strip()

CHECK_FN = (
    "# Checker used by the challenges below — run this cell first.\n"
    "import numpy as np\n"
    "def check(got, want, hint='', atol=1e-6):\n"
    "    try:\n"
    "        ok = got is not None and np.shape(got) == np.shape(want) and np.allclose(np.asarray(got, dtype=float), np.asarray(want, dtype=float), rtol=1e-4, atol=atol)\n"
    "    except Exception:\n"
    "        ok = False\n"
    "    print('✅ Correct!' if ok else '❌ Not yet. Hint: ' + hint)\n")
from challenges import C as CHAL
_WORK = tempfile.mkdtemp(); os.makedirs(os.path.join(_WORK, "notebooks")); os.makedirs(os.path.join(_WORK, "data"))
import shutil as _sh; _sh.copy(os.path.join(HERE, "data", "houses.csv"), os.path.join(_WORK, "data", "houses.csv")); os.chdir(os.path.join(_WORK, "notebooks"))   # challenge code reads ../data/houses.csv
def starter_of(ch):
    name, sol = ch[3], ch[4]
    return ch[6] if len(ch) > 6 and ch[6] else (re.match(r"\s*", sol).group(0) + name + " = None  # ← your code here")
def fill(code, line):
    return code.replace("    ##BLANK##", line) if "    ##BLANK##" in code else code.replace("##BLANK##", line.strip())
ok = True
from lesson0_data import LESSON0
for (n, p, title, summary, mins) in [LESSON0] + LESSONS:
    body = open(os.path.join(HERE, "lessons", f"{n:02d}.html")).read()
    nb = new_notebook()
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nb.cells.append(new_markdown_cell(
        f"# Lesson {n}: {title}\n\n*ML Academy — companion notebook*\n\n{summary}\n\n"
        f"Run each cell in order with **Shift+Enter**. The explanations, maths and worked examples are in `lesson-{n:02d}.html`; "
        "this notebook contains every code example from the lesson so you can run and modify it.\n\n"
        "Requirements: `pip install numpy pandas scikit-learn matplotlib`"))
    parts = re.split(r'(<h2 id="[^"]+">.*?</h2>)', body)
    sec = 0
    for i in range(1, len(parts), 2):
        sec += 1
        heading = plain(parts[i])
        content = parts[i + 1] if i + 1 < len(parts) else ""
        blocks = [html.unescape(c) for c in re.findall(r"<pre><code>(.*?)</code></pre>", content, re.S)]
        code = [b for b in blocks if CODE_RE.search(b)]
        if not code:
            continue
        nb.cells.append(new_markdown_cell(f"## {sec}. {heading}"))
        for b in code:
            if "import torch" in b:
                nb.cells.append(new_markdown_cell("The PyTorch example below needs PyTorch installed (see pytorch.org), so it's shown as text rather than a runnable cell:\n\n```python\n" + b + "\n```"))
            else:
                nb.cells.append(new_code_cell(b.replace('pd.read_csv("houses.csv")', 'pd.read_csv("../data/houses.csv")')))
    from running_code import CODE as RUN_CODE
    if n in RUN_CODE:
        nb.cells.append(new_markdown_cell("## Running example: Chennai Homes\n\nThe same 12-house dataset used in every lesson (`data/houses.csv` in the course folder)."))
        nb.cells.append(new_code_cell(RUN_CODE[n].replace('pd.read_csv("houses.csv")   # download it from Lesson 1', 'pd.read_csv("../data/houses.csv")')))
    sols = []
    if n in CHAL:
        nb.cells.append(new_markdown_cell("## Coding challenges\n\nEach cell below has **one missing line**, marked `# ← your code here` (or `# ← replace`). Write the line, run the cell, and the check at the bottom tells you whether you got it right. "
                                          "Stuck? A wrong answer prints a hint, and the solutions are at the very end of this notebook."))
        nb.cells.append(new_code_cell(CHECK_FN))
        for k, ch in enumerate(CHAL[n]):
            title_, task, code, name, sol, hint = ch[:6]
            atol = ch[7] if len(ch) > 7 else None
            ns = {}
            with contextlib.redirect_stdout(io.StringIO()): exec(fill(code, sol), ns)
            want = ns[name]
            want_src = repr(want.tolist() if hasattr(want, "tolist") else (float(want) if not isinstance(want, (int, float)) else want))
            chk = f"check({name}, {want_src}, hint={hint!r}" + (f", atol={atol}" if atol else "") + ")"
            nb.cells.append(new_markdown_cell(f"### Challenge {k+1}: {title_}\n\n{task}"))
            nb.cells.append(new_code_cell(fill(code, starter_of(ch)) + "\n" + chk))
            sols.append((title_, sol.strip(), fill(code, sol) + "\n" + chk))
    nb.cells.append(new_markdown_cell("## Your turn\n\nTry the **practice exercises** at the end of the lesson page. Many of them ask you to change one of the cells above and re-run it."))
    if sols:
        nb.cells.append(new_markdown_cell("## Challenge solutions\n\n*Spoilers — try the challenges first!*\n\n" + "\n\n".join(f"**{k+1}. {t}** — the missing line:\n\n```python\n{sl}\n```" for k, (t, sl, _) in enumerate(sols))))
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "notebooks")); os.makedirs(os.path.join(tmp, "data"))
        import shutil; shutil.copy(os.path.join(HERE, "data", "houses.csv"), os.path.join(tmp, "data", "houses.csv"))
        try:
            NotebookClient(nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": os.path.join(tmp, "notebooks")}}).execute()
            status = "ok"
        except Exception as ex:
            status = "FAILED: " + str(ex)[:300]
            ok = False
    errs = [o for c in nb.cells if c.cell_type == "code" for o in c.get("outputs", []) if o.get("output_type") == "error"]
    starter_outs = ["".join(o.get("text", "") for o in c.get("outputs", []) if o.get("output_type") == "stream") for c in nb.cells if c.cell_type == "code" and "\ncheck(" in c.source]
    if sols and (len(starter_outs) != len(sols) or any("Not yet" not in o for o in starter_outs)): status = f"STARTER CHECK PROBLEM {starter_outs}"; ok = False
    for k, (_, _, full) in enumerate(sols):          # every solution must pass its own check
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            ns = {}; exec(CHECK_FN, ns); exec(full, ns)
        if "Correct" not in buf.getvalue(): status = f"SOLUTION {k+1} FAILED: {buf.getvalue()[:100]}"; ok = False
    if errs:
        status = f"{len(errs)} error output(s)"; ok = False
    nbformat.write(nb, os.path.join(OUT, f"lesson-{n:02d}.ipynb"))
    print(f"lesson {n:2d}: {sum(c.cell_type == 'code' for c in nb.cells)} code cells — {status}")
print("ALL OK" if ok else "SOME FAILED")
