"""Build starter + solution notebooks for the mini-projects, execute them, and verify every check."""
import os, re, sys, json, io, contextlib, warnings
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from nbclient import NotebookClient
import matplotlib
matplotlib.use("Agg")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from projects import PROJECTS
OUT = os.path.join(sys.argv[1], "notebooks", "projects")
os.makedirs(OUT, exist_ok=True)

CHECK_FN = (
    "# Run this cell first: it defines check(), which tells you whether each step is right.\n"
    "import numpy as np\n"
    "def check(get, want, hint=''):\n"
    "    try:\n"
    "        got = get()\n"
    "        if isinstance(want, str):\n"
    "            ok = str(got) == want\n"
    "        else:\n"
    "            ok = np.shape(got) == np.shape(want) and np.allclose(np.asarray(got, dtype=float), np.asarray(want, dtype=float), rtol=1e-4, atol=1e-6)\n"
    "    except Exception:\n"
    "        ok = False\n"
    "    print('✅ Correct!' if ok else '❌ Not yet. Hint: ' + hint)\n")
TODO = re.compile(r"^(\s*)(.*?)\s*#TODO:\s*(.*)$")

def solution_code(code):
    return "\n".join(TODO.sub(lambda m: m.group(1) + m.group(2), ln) for ln in code.split("\n"))

def starter_code(code):
    out = []
    for ln in code.split("\n"):
        m = TODO.match(ln)
        if not m: out.append(ln); continue
        ind, stmt, hint = m.groups()
        lhs = re.match(r"^([A-Za-z_][\w\s,\[\]\"']*?)\s*=(?!=)", stmt)
        if lhs:
            names = [x.strip() for x in lhs.group(1).split(",")]
            out.append(ind + lhs.group(1).strip() + " = " + ", ".join(["None"] * len(names)) + "  # TODO: " + hint)
        else:
            out.append(ind + "# TODO: " + hint)
    return "\n".join(out)

def plain(h): return re.sub(r"<[^>]+>", "", h)

RESULTS, ok_all = {}, True
for P in PROJECTS:
    ns, wants = {}, []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for title, md, code, checks in P["steps"]:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(solution_code(code).replace("plt.show()", "plt.close('all')"), ns)
            w = []
            for expr, hint in checks:
                v = eval(expr, ns)
                v = v.tolist() if hasattr(v, "tolist") else v
                if isinstance(v, tuple): v = list(v)
                if not isinstance(v, (int, float, list, str)): v = str(v)
                w.append((expr, v, hint))
            wants.append(w)
    RESULTS[P["id"]] = ns  # keep namespace for summary numbers
    for kind in ("starter", "solution"):
        nb = new_notebook(); nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
        lessons = ", ".join(f"Lesson {l}" for l in P["lessons"])
        intro = (f"# Project: {P['title']}\n\n*ML Academy — {'starter notebook' if kind == 'starter' else 'complete solution'}*\n\n"
                 f"**Goal.** {P['goal']}\n\n**The data.** {plain(P['data'])}\n\n**Uses:** {lessons}.\n\n")
        intro += ("Work through the steps in order. Lines marked `# TODO` are yours to write; each step ends with a check that prints ✅ when you're right "
                  "(and a hint when you're not). Cells that use a step's result will show errors until that step is done — that's expected. The solution notebook is in the same folder."
                  if kind == "starter" else "This notebook contains the full solution with outputs. Try the starter notebook first!")
        intro += "\n\nRequirements: `pip install numpy pandas scikit-learn matplotlib scipy` — " + ("the data is simulated in the first step, so no download is needed." if P.get("simulated") else "the dataset ships with scikit-learn, so no download is needed.")
        nb.cells.append(new_markdown_cell(intro))
        nb.cells.append(new_code_cell(CHECK_FN))
        for k, ((title, md, code, checks), w) in enumerate(zip(P["steps"], wants)):
            nb.cells.append(new_markdown_cell(f"## Step {k+1}. {title}" + (f"\n\n{md}" if md else "")))
            src = starter_code(code) if kind == "starter" else solution_code(code)
            nb.cells.append(new_code_cell(src))
            if w:
                nb.cells.append(new_code_cell("\n".join(f"check(lambda: {e}, {v!r}, hint={h!r})" for e, v, h in w)))
        nb.cells.append(new_markdown_cell("## Go further\n\n" + "\n".join(f"- {plain(x)}" for x in P["further"])))
        client = NotebookClient(nb, timeout=900, kernel_name="python3", allow_errors=(kind == "starter"), resources={"metadata": {"path": OUT}})
        status = "ok"
        try:
            client.execute()
        except Exception as ex:
            status = "FAILED: " + str(ex)[:300]; ok_all = False
        outs = ["".join(o.get("text", "") for o in c.get("outputs", []) if o.get("output_type") == "stream") for c in nb.cells if c.cell_type == "code" and c.source.startswith("check(")]
        n_ok = sum(o.count("✅") for o in outs); n_chk = sum(len(w) for w in wants)
        n_todo = sum(c.source.count("# TODO") for c in nb.cells if c.cell_type == "code")
        if kind == "solution" and n_ok != n_chk: status = f"only {n_ok}/{n_chk} checks passed"; ok_all = False
        if kind == "starter":
            for c in nb.cells:
                if c.cell_type == "code": compile(c.source.replace("%matplotlib inline", ""), "cell", "exec")
            if n_ok == n_chk: status = "starter passes everything?!"; ok_all = False
        nbformat.write(nb, os.path.join(OUT, f"{P['id']}-{kind}.ipynb"))
        print(f"{P['id']:9s} {kind:8s}: {n_chk} checks, {n_ok} passed, {n_todo} TODO lines — {status}")

# numbers for the website (taken from the executed solutions)
d, t, wn, dg = RESULTS["diabetes"], RESULTS["tumours"], RESULTS["wine"], RESULTS["digits"]
fc, rt = RESULTS["forecast"], RESULTS["retention"]
import numpy as np
def fc_r(v): return f"{v:+.3f}"
SUMMARY = {
 "diabetes": [("Baseline MAE (predict the average)", f"{d['baseline_mae']:.1f}"), ("BMI only", f"MAE {d['bmi_mae']:.1f} · R² {d['bmi_r2']:.2f}"),
              ("All ten features", f"MAE {d['full_mae']:.1f} · R² {d['full_r2']:.2f}"), ("Ridge (α by CV)", f"α = {d['ridge'][-1].alpha_:g} · MAE {d['ridge_mae']:.1f}")],
 "tumours": [("Best by 5-fold CV", f"{t['best_name']} ({t['cv_acc'][t['best_name']]:.3f})"), ("Test set, threshold 0.5", f"precision {t['precision']:.2f} · recall {t['recall']:.2f}"),
             ("Threshold 0.1", f"recall {t['recall_low']:.2f} — no malignant tumour missed"), ("Most important feature", t['importances'].index[0])],
 "wine": [("PC1 + PC2 explain", f"{100 * (wn['ratio'][0] + wn['ratio'][1]):.0f}% of the variance"), ("Best k by silhouette", str(wn['best_k'])),
          ("Agreement with the real cultivars", f"ARI {wn['ari']:.2f}")],
 "forecast": [("Seasonal naive MAE (test)", f"{fc['naive_mae']:.1f}"), ("Ridge on lag features", f"MAE {fc['model_mae']:.1f} · MASE {fc['mase']:.2f}"),
              ("Backtest (5 windows)", f"average MAE {fc['backtest_mae']:.1f}"), ("Anomaly detector (robust z > 4)", f"precision {fc['precision']:.2f} · recall {fc['recall']:.2f}")],
 "retention": [("Naive churn difference", f"{fc_r(rt['naive_diff'])}"), ("Still subscribed at 12 months", f"no coupon {rt['s12'][0]:.3f} · coupon {rt['s12'][1]:.3f}"),
               ("Coupon hazard ratio", f"{float(np.exp(rt['naive_fit'].x[0])):.2f} unadjusted · {rt['hr'][0]:.2f} adjusted (true 0.7)"), ("Concordance index", f"{rt['c_index']:.3f}")],
 "digits": [("Logistic regression", f"{100 * dg['baseline_acc']:.1f}%"), ("Neural network (64 hidden)", f"{100 * dg['mlp_acc']:.1f}%"),
            ("SVM (RBF)", f"{100 * dg['svm_acc']:.1f}%"), ("Most common mistake", f"{dg['true_d']} read as {dg['pred_d']}")],
}
json.dump(SUMMARY, open(os.path.join(HERE, "project_results.json"), "w"), indent=1)
print(json.dumps(SUMMARY, indent=1))
print("ALL OK" if ok_all else "SOME FAILED")
