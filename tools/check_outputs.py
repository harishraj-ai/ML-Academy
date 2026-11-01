#!/usr/bin/env python3
"""ML Academy — output checker.

Re-runs every lesson and project notebook in a temporary copy, compares each code cell's
new output with the output saved in the notebook (and, for lessons, with the output shown
on the lesson page), and writes a report of anything that changed — for example after a
scikit-learn or NumPy update.

Usage (from the course folder):
    python tools/check_outputs.py                # check everything
    python tools/check_outputs.py --only 6 8     # only lessons 6 and 8
    python tools/check_outputs.py --tol 1e-4     # looser numeric tolerance

Needs: numpy, pandas, scikit-learn, matplotlib, nbformat, nbclient, ipykernel.
Nothing in the course is modified; the only file written is tools/check_report.md.
Exit code: 0 = everything matches, 1 = something changed or failed.
"""
import argparse, html, json, os, re, shutil, sys, tempfile, time
from datetime import datetime
from importlib import metadata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")
PKGS = ["numpy", "pandas", "scikit-learn", "matplotlib", "scipy", "nbclient", "nbformat"]


def versions():
    v = {"python": sys.version.split()[0]}
    for p in PKGS:
        try: v[p] = metadata.version(p)
        except metadata.PackageNotFoundError: v[p] = "not installed"
    return v


def text_of(cell):
    """Printed text and results of a code cell (stderr warnings and images are ignored)."""
    out, images = [], 0
    for o in cell.get("outputs", []):
        t = o.get("output_type")
        if t == "stream" and o.get("name") == "stdout":
            out.append(o["text"] if isinstance(o["text"], str) else "".join(o["text"]))
        elif t in ("execute_result", "display_data"):
            d = o.get("data", {})
            if "image/png" in d: images += 1
            elif "text/plain" in d:
                tp = d["text/plain"]; out.append((tp if isinstance(tp, str) else "".join(tp)) + "\n")
        elif t == "error":
            out.append(f"ERROR {o.get('ename')}: {o.get('evalue')}\n")
    return "".join(out), images


def same(a, b, tol):
    """Equal apart from whitespace and tiny numeric differences."""
    ta, tb = a.split(), b.split()
    if len(ta) != len(tb): return False
    for x, y in zip(ta, tb):
        if x == y: continue
        nx, ny = NUM.findall(x), NUM.findall(y)
        if NUM.sub("#", x) != NUM.sub("#", y) or len(nx) != len(ny): return False
        for p, q in zip(nx, ny):
            p, q = float(p), float(q)
            if abs(p - q) > max(tol * max(abs(p), abs(q)), 1e-9): return False
    return True


def norm(s):
    return " ".join(s.split())


def page_outputs(path):
    if not os.path.exists(path): return ""
    blocks = re.findall(r"<pre[^>]*><code>(.*?)</code></pre>", open(path, encoding="utf-8").read(), re.S)
    return "\n".join(norm(html.unescape(re.sub(r"<[^>]+>", "", b))) for b in blocks)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--only", nargs="*", type=int, help="lesson numbers to check (default: all, plus projects)")
    ap.add_argument("--tol", type=float, default=1e-6, help="relative tolerance for numbers (default 1e-6)")
    ap.add_argument("--timeout", type=int, default=600, help="seconds allowed per cell")
    args = ap.parse_args()
    try:
        import nbformat
        from nbclient import NotebookClient
    except ImportError:
        sys.exit("Please install the checker's requirements: pip install numpy pandas scikit-learn matplotlib nbformat nbclient ipykernel")

    nbdir = os.path.join(ROOT, "notebooks")
    names = sorted(f for f in os.listdir(nbdir) if re.match(r"lesson-\d\d\.ipynb$", f))
    if args.only: names = [f for f in names if int(f[7:9]) in args.only]
    else: names += ["projects/" + f for f in sorted(os.listdir(os.path.join(nbdir, "projects"))) if f.endswith(".ipynb")]

    now, rec = versions(), {}
    vp = os.path.join(ROOT, "tools", "versions.json")
    if os.path.exists(vp): rec = json.load(open(vp)).get("versions", {})
    results, t0 = [], time.time()
    for name in names:
        src = nbformat.read(os.path.join(nbdir, name), as_version=4)
        fresh = nbformat.read(os.path.join(nbdir, name), as_version=4)
        for c in fresh.cells:
            if c.cell_type == "code": c.outputs = []; c.execution_count = None
        status, diffs, notpage = "ok", [], []
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "notebooks", "projects")); shutil.copytree(os.path.join(ROOT, "data"), os.path.join(tmp, "data"))
            path = os.path.join(tmp, "notebooks", os.path.dirname(name))
            try:
                NotebookClient(fresh, timeout=args.timeout, kernel_name="python3", allow_errors=True, resources={"metadata": {"path": path}}).execute()
            except Exception as ex:
                status = "failed to run: " + str(ex).splitlines()[0][:200]
        page_text = page_outputs(os.path.join(ROOT, name.replace(".ipynb", ".html"))) if name.startswith("lesson-") else ""
        code_old = [c for c in src.cells if c.cell_type == "code"]
        code_new = [c for c in fresh.cells if c.cell_type == "code"]
        for k, (a, b) in enumerate(zip(code_old, code_new)):
            ta, ia = text_of(a); tb, ib = text_of(b)
            if "ERROR " in tb and "ERROR " not in ta:
                diffs.append((k + 1, a.source, ta, tb, "new error"))
            elif not same(ta, tb, args.tol):
                diffs.append((k + 1, a.source, ta, tb, "output changed"))
            elif ia != ib:
                diffs.append((k + 1, a.source, f"{ia} image(s)", f"{ib} image(s)", "image count changed"))
            if page_text and tb.strip() and "\ncheck(" not in a.source and norm(tb) not in page_text:
                miss = [ln.strip() for ln in tb.splitlines() if norm(ln) and norm(ln) not in page_text]
                if miss: notpage.append((k + 1, miss))
        if diffs and status == "ok": status = f"{len(diffs)} cell(s) changed"
        results.append((name, status, diffs, notpage, len(code_new)))
        print(f"{name:40s} {status}" + (f"  (output lines not shown on the page: cells {[k for k, _ in notpage]})" if notpage else ""))

    bad = [r for r in results if r[1] != "ok"]
    L = [f"# Output check — {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M (UTC%z)')}", "",
         f"Checked {len(results)} notebooks ({sum(r[4] for r in results)} code cells) in {time.time() - t0:.0f} s. "
         + ("**Everything matches.**" if not bad else f"**{len(bad)} notebook(s) need attention.**"), "",
         "## Library versions", "", "| package | published with | this run |", "|---|---|---|"]
    for k in ["python"] + PKGS:
        L.append(f"| {k} | {rec.get(k, '—')} | {now.get(k)}{' ⚠️' if rec.get(k) and rec.get(k) != now.get(k) else ''} |")
    L += ["", "## Results", "", "| notebook | result |", "|---|---|"] + [f"| {n} | {s} |" for n, s, _, _, _ in results]
    for n, s, diffs, notpage, _ in results:
        if not diffs and not notpage: continue
        L += ["", f"## {n}"]
        for k, srcc, old, new, why in diffs:
            L += ["", f"### Code cell {k}: {why}", "", "```python", srcc.strip()[:800], "```", "Published output:", "```", old.strip()[:1500] or "(none)", "```", "New output:", "```", new.strip()[:1500] or "(none)", "```"]
        if notpage:
            L += ["", "Output lines not found word-for-word on the lesson page (often fine: the page may describe them in words or round them — but worth a look):", ""]
            L += [f"- cell {k}: " + "; ".join(f"`{m[:80]}`" for m in miss[:4]) + (" …" if len(miss) > 4 else "") for k, miss in notpage]
    L += ["", "If an output changed after a library update, decide whether the lesson text still holds, then regenerate the notebooks and pages."]
    open(os.path.join(ROOT, "tools", "check_report.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"\nReport written to tools/check_report.md — {'all good' if not bad else str(len(bad)) + ' notebook(s) changed'}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
