# ML Academy — source and how to rebuild

Everything in the published course (the HTML pages, notebooks, code zip and workbook PDF) is **generated** from the files in this `source/` folder. To change the course, edit the source and rebuild — don't hand-edit the generated pages in the top-level folder.

## Where things are

| To change… | Edit |
|---|---|
| A lesson's main text, maths, worked examples, quiz | `lessons/NN.html` (Lesson 0 is built by `lesson0_build.py` from `lesson0_data.py`) |
| Lesson titles, objectives, sources, home page, navigation, page layout | `build.py` |
| "Make sense of it" boxes, "Picture it" openers, which calculator goes where | `sense.py` |
| Interactive demos / what-if calculators | `assets/demos.js` / `assets/whatif.js` |
| Hidden interview questions / confused terms | `interview_a.py`, `interview_b.py`, `interview_c.py` / `confused.py` |
| Exercises, answer checkers, common mistakes | `extras_ex_a.py`, `extras_ex_b.py`, `checks.py` (practice generators: `assets/practice.js`) |
| Notebook coding challenges | `challenges.py` |
| Part tests, projects, learning routes | `tests.py`, `projects.py` + `make_projects.py`, `routes.py` |
| Context boxes, FAQs, myths, responsible-AI notes, advanced boxes | `context.py`, `understanding.py`, `rai.py`, `advanced.py` |
| Running example (Chennai Homes) | `running_code.py`, `running_text.py`, `data/houses.csv` |
| Lesson 21 data, What next page, Recent developments, changelog | `lesson21_data.py`, `nextpage.py`, `recent.py`, `changelog.py` |
| "Going deeper" (intermediate) sections | `deeper/NN.html` (text), `deeper/NN_cells/K.py` (code), `deeper/NN_data.py` (quiz, interview questions, exercises). After editing a code cell run `python source/deeper.py NN` to refresh its saved output. |
| Styles | `assets/base.css` |
| Top-level README / requirements / .gitignore | `site_README.md`, `site_requirements.txt`, `site_gitignore` |
| README and requirements inside the code zip | `code_README.md`, `code_requirements.txt` |

## Setup (once)

```bash
pip install numpy pandas scikit-learn matplotlib scipy joblib nbformat nbclient ipykernel pytest pikepdf
npm install playwright        # only needed to rebuild the workbook PDF
npx playwright install chromium
```

## Rebuild

Run these from the course's top-level folder (the one containing `index.html` and `source/`). The `.` means "write the output here".

```bash
python source/deeper.py                  # only if you changed a Going deeper code cell: refreshes its outputs
python source/build.py .                 # all HTML pages, search index, assets (about 10 s)
python source/make_notebooks.py .        # lesson notebooks, executed with real outputs (a few minutes)
python source/make_projects.py .         # project notebooks (only if you changed projects)
python source/build.py .                 # again, so the notebook download helpers are refreshed
python source/make_code_zip.py .         # downloads/ml-academy-code.zip (runs and records every script)
node source/make_workbook.js .           # workbook/ML-Academy-workbook.pdf (about 1 minute)
python source/fix_pdf_links.py .         # makes the PDF's links work from any copy
python tools/check_outputs.py            # optional: re-run every notebook and compare outputs
```

For a text-only change to one lesson, `python source/build.py .` is usually enough; rebuild the notebooks, zip and PDF when code, exercises or printed content change.

Then publish:

```bash
git add .
git commit -m "Describe what you changed"
git push
```

GitHub Pages rebuilds the live site about a minute after the push.

## Before publishing

* Open a few changed pages in a browser and check the maths renders (no red KaTeX errors).
* Add a line to `changelog.py` describing the release.
* Every number quoted in the text should come from running the code — the notebooks and the code zip's tests will catch outputs that drift.
