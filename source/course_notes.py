"""Build course-notes.html: handwritten-style study notes for every lesson.

The notes themselves are written by hand, one file per lesson, in
source/notes/NN.html (styled by assets/study-notes.css). This script wraps them
in the site's page shell with a contents list.

Run from the ML folder:   python source/course_notes.py .
PDF:                      node source/course_notes_pdf.js .
"""
import os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(ROOT, *a)

files = sorted(f for f in os.listdir(os.path.join(HERE, "notes")) if re.fullmatch(r"\d\d\.html", f))
toc, arts = [], []
for f in files:
    n = int(f[:2])
    a = open(os.path.join(HERE, "notes", f), encoding="utf-8").read().strip()
    title = re.sub(r"<[^>]+>", "", re.search(r"<h2>(.*?)</h2>", a, re.S).group(1))
    toc.append(f'<li><a href="#n{n:02d}"><span class="sn-n">{n}</span>{title}</a></li>')
    lesson = f"lesson-{n:02d}.html"
    a = a.replace("</article>", f'<p class="sn-back"><a href="{lesson}">open the full lesson →</a></p>\n</article>')
    # draw each sketch at its natural size (never wider than the page)
    a = re.sub(r'<svg class="sk" viewBox="0 0 (\d+) (\d+)"', lambda m: f'<svg class="sk" width="{m.group(1)}" viewBox="0 0 {m.group(1)} {m.group(2)}"', a)
    arts.append(a)

main = ('<main id="main">\n<div class="module-hero"><div class="container"><div class="eyebrow">Reference</div>'
        f'<h1>Study notes</h1><p>Notebook-style revision notes for all {len(files)} lessons: every section explained simply, '
        'plus each lesson&#39;s Going deeper, with small sketches and worked numbers. Your own highlights and notes stay on '
        '<a href="notes.html">My notes</a>.</p></div></div>\n'
        '<div class="container ref-page"><div class="prose wide">'
        '<div class="sn-top"><a class="btn" href="workbook/ML-Academy-study-notes.pdf" download>Download the PDF</a>'
        '</div>'
        f'<div class="sn-contents"><h2 style="margin-top:0">Contents</h2><ol class="sn-toc">{"".join(toc)}</ol></div>\n'
        + "\n".join(arts) + "\n</div></div>\n</main>")

tpl = open(P("cheatsheet.html"), encoding="utf-8").read()
a, b = tpl.index('<main id="main">'), tpl.index("</main>") + len("</main>")
out = tpl[:a] + main + tpl[b:]
out = out.replace('<link rel="stylesheet" href="assets/base.css">',
                  '<link rel="stylesheet" href="assets/base.css"><link rel="stylesheet" href="assets/study-notes.css">', 1)
out = re.sub(r"<title>.*?</title>", "<title>Study notes — ML Academy</title>", out, count=1, flags=re.S)
out = re.sub(r'(<meta name="description" content=")[^"]*', r"\1Notebook-style study notes for every ML Academy lesson, covering every section and Going deeper, with sketches and worked examples.", out, count=1)
out = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\1Study notes — ML Academy", out, count=1)
open(P("course-notes.html"), "w", encoding="utf-8").write(out)
print("study notes:", len(files), "lessons")
