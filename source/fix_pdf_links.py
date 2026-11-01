# Make the workbook PDF's links portable: Chromium writes absolute file:// links to the build folder;
# rewrite them relative to workbook/ (e.g. ../lesson-06.html) so they work on GitHub Pages and in any copy.
import sys, os, pikepdf
out = os.path.abspath(sys.argv[1]); p = os.path.join(out, "workbook", "ML-Academy-workbook.pdf")
prefix = "file://" + out.rstrip("/") + "/"
pdf = pikepdf.open(p, allow_overwriting_input=True); n = left = 0
for pg in pdf.pages:
    for a in pg.get("/Annots") or []:
        A = a.get("/A")
        if A is not None and A.get("/URI") is not None:
            u = str(A.URI)
            if u.startswith(prefix): A.URI = pikepdf.String("../" + u[len(prefix):]); n += 1
            elif u.startswith("file:"): left += 1
pdf.docinfo["/Title"] = "ML Academy — Printable workbook"; pdf.docinfo["/Author"] = "ML Academy"
for k in ["/Creator", "/Producer"]:
    if k in pdf.docinfo: del pdf.docinfo[k]
import re, html as _h
titles = {int(m.group(1)): _h.unescape(m.group(2)) for m in re.finditer(r'data-n="(\d+)" data-title="([^"]*)"', open(os.path.join(out, "workbook.html"), encoding="utf-8").read())}
with pdf.open_outline() as ol:
    for it in ol.root:
        t = str(it.title); m = re.match(r"Lesson (\d+):", t)
        if m and int(m.group(1)) in titles: it.title = f"Lesson {m.group(1)}: {titles[int(m.group(1))]}"
        elif t.startswith("Answers"): it.title = "Answers"
pdf.save(p); print(f"rewrote {n} links, {left} other file: links left")
