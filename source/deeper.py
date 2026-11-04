"""'Going deeper' (intermediate) sections for the lessons.

Each lesson NN that has one keeps its material in the deeper/ folder:
  deeper/NN.html        the section text (HTML, KaTeX maths); <!--cell K--> marks where code cell K goes
  deeper/NN_cells/K.py  code cell K (cells run in order, sharing variables, like a notebook)
  deeper/NN_cells/K.out its printed output, pasted under the code on the page
  deeper/NN_data.py     QUIZ, IQ (interview questions), EX (exercises), CHECKS, SIMPLE (plain-words summary)

After changing a code cell, refresh the saved outputs with:
  python source/deeper.py 6          (or several lesson numbers, or no number for all)
"""
import glob, html, io, os, contextlib, re, runpy, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "deeper")


def lessons():
    return sorted(int(os.path.basename(p)[:2]) for p in glob.glob(os.path.join(DIR, "[0-9][0-9].html")))


def data(n):
    p = os.path.join(DIR, f"{n:02d}_data.py")
    return runpy.run_path(p) if os.path.exists(p) else {}


def cells(n):
    d = os.path.join(DIR, f"{n:02d}_cells")
    ks = sorted(int(os.path.basename(p)[:-3]) for p in glob.glob(os.path.join(d, "*.py")))
    return [(k, open(os.path.join(d, f"{k}.py")).read().rstrip() + "\n", os.path.join(d, f"{k}.out")) for k in ks]


def _quiz(n, qs):
    out = ['<div class="quiz deep-quiz">']
    for i, (q, opts, correct, why) in enumerate(qs, 1):
        out.append(f'<div class="q" data-correct="{correct}"><p class="q-text">{i}. {q}</p>' +
                   "".join(f'<button data-opt="{k}">{t}</button>' for k, t in opts) +
                   f'<div class="q-explain">{why}</div></div>')
    return "".join(out) + "</div>"


def _iq(qs):
    return ('<div class="box hidden-q deep-iq"><div class="box-title">Interview corner · intermediate</div>'
            '<p class="hq-sub"><strong>Hidden questions</strong> — answer in your head first, then open.</p>' +
            "".join(f'<details class="hq"><summary>{q}</summary><p class="iq-trap"><strong>The trap:</strong> {trap}</p><p>{a}</p></details>'
                    for _lvl, q, trap, a in qs) + '</div>')


def section(n):
    """The finished HTML of lesson n's deeper section ('' if it has none)."""
    p = os.path.join(DIR, f"{n:02d}.html")
    if not os.path.exists(p):
        return ""
    s = open(p).read()
    for k, code, outp in cells(n):
        block = f'<pre><code>{html.escape(code.rstrip(), quote=False)}</code></pre>'
        if os.path.exists(outp) and open(outp).read().strip():
            block += f'<p>Output:</p><pre><code>{html.escape(open(outp).read().rstrip(), quote=False)}</code></pre>'
        s = s.replace(f"<!--cell {k}-->", block)
    d = data(n)
    if d.get("IQ"):
        s = s.replace("<!--interview-->", _iq(d["IQ"]))
    if d.get("QUIZ"):
        s = s.replace("<!--quiz-->", '<h3 id="deeper-quiz">Check your understanding: going deeper</h3>' + _quiz(n, d["QUIZ"]))
    return s


def inject(n, body):
    """Append lesson n's deeper section to the raw lesson body (after the beginner quiz)."""
    return body + section(n)


def interview_questions():
    """(lesson, level, question, trap, answer) for the interview page."""
    return [(n, lvl, q, trap, a) for n in lessons() for (lvl, q, trap, a) in data(n).get("IQ", [])]


def run_cells(n):
    """Run lesson n's cells in order (sharing variables) and save each cell's output."""
    import shutil, tempfile
    tmp = tempfile.mkdtemp()
    shutil.copy(os.path.join(HERE, "data", "houses.csv"), tmp)
    cwd = os.getcwd(); os.chdir(tmp)
    ns = {"__name__": "__main__"}
    try:
        for k, code, outp in cells(n):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                exec(compile(code, f"{n:02d}_cells/{k}.py", "exec"), ns)
            open(outp, "w").write(buf.getvalue())
            if re.search(r"^\s*(import |from \S+ import )|\bprint\(|\bdef | = ", buf.getvalue(), re.M):
                print(f"  WARNING: cell {k}'s output contains ' = ' or code-like text, so the notebook builder would treat it as code. Reword the print.")
            print(f"lesson {n} cell {k}: {len(buf.getvalue().splitlines())} output lines")
    finally:
        os.chdir(cwd)


if __name__ == "__main__":
    for n in ([int(a) for a in sys.argv[1:]] or lessons()):
        run_cells(n)
