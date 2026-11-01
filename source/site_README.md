# ML Academy — machine learning from zero

**Start learning: https://harishraj07022004-cpu.github.io/ML-Academy/**

A free, beginner-first machine-learning course that runs entirely in the browser: 22 lessons (Lesson 0 to Lesson 21) with plain-English explanations, the maths step by step, worked examples, interactive demos and "what if?" calculators, real code with real outputs, quizzes, exercises that check your answers, end-of-part tests, spaced review, mini-projects, hidden interview questions and a printable workbook.

No build step, no server code, no tracking, no external requests: everything — fonts, maths rendering, demos — is in this folder.

## Open it

* **Online:** https://harishraj07022004-cpu.github.io/ML-Academy/
* **On your computer:** download or clone the repository and open `index.html` in a browser. Everything works from a local folder, offline.
  If your browser blocks something when opening files directly, serve the folder instead:

  ```bash
  python -m http.server 8000      # then open http://localhost:8000
  ```

## Publish on GitHub Pages

1. Push this folder to a GitHub repository (the files at the top level: `index.html`, `assets/`, …).
2. In the repository: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, choose your branch (e.g. `main`) and the `/ (root)` folder, and save.
3. After a minute the course is live at `https://<your-user>.github.io/<repository>/`.

All links are relative, so the site works at any address or sub-folder.

## What's inside

| Path | What it is |
|---|---|
| `index.html` | Home page and learning path |
| `lesson-00.html` … `lesson-21.html` | The lessons |
| `interview.html`, `confused.html` | Hidden interview questions and commonly confused terms |
| `tests.html`, `review.html`, `projects.html`, `progress.html`, `notes.html` | Part tests, spaced review, mini-projects, progress dashboard, your notes |
| `glossary.html`, `cheatsheet.html`, `compare.html`, `guide.html`, `map.html` | Reference pages |
| `recent.html`, `next.html`, `changelog.html` | Recent developments, what to learn next, version history |
| `notebooks/` | A Jupyter notebook for every lesson and project, with outputs |
| `downloads/ml-academy-code.zip` | All the code as plain `.py` scripts, with a `pytest` test suite |
| `workbook/ML-Academy-workbook.pdf` | Printable workbook with space for working and answers |
| `data/houses.csv` | The small "Chennai Homes" dataset used in every lesson |
| `tools/check_outputs.py` | Re-runs every notebook and reports any output that changed |
| `assets/` | Styles, scripts, fonts and the KaTeX maths library |

Your progress, quiz scores, notes and settings are saved only in your own browser (`localStorage`); nothing is sent anywhere.
"Listen to this lesson" uses your browser's built-in speech voices, so the available voices depend on your system.

## Run the code

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab                         # then open a notebook in notebooks/
```

Or download `downloads/ml-academy-code.zip`, unzip it anywhere, and follow its README (`pytest -q` runs all the tests).

## Check the outputs after a library update

```bash
python tools/check_outputs.py          # all notebooks (about 2 minutes)
python tools/check_outputs.py --only 6 # just Lesson 6
```

The report is written to `tools/check_report.md`. The library versions used for the published outputs are listed in `tools/versions.json` and on `changelog.html`.

## Changing the course

The pages, notebooks, code zip and workbook are generated from the files in [`source/`](source/). See [`source/BUILD.md`](source/BUILD.md) for what to edit and how to rebuild.

## Feedback

Found a mistake or have a suggestion? Please open an issue or comment on this repository.
