# ML Academy — code

All the Python code from the ML Academy course as plain scripts, with tests.

```
ml-academy-code/
├── lessons/        lesson-00.py … lesson-21.py — every code example from each lesson, in order
│                   lesson-19-pytorch.py — the PyTorch example (needs `pip install torch`)
├── challenges/     lesson-XX-challenges.py — fill in one missing line per challenge; each check prints ✅ or a hint
├── projects/       the four mini-projects: *-starter.py (with TODOs) and *-solution.py
├── data/houses.csv the 12-house "Chennai Homes" dataset used in every lesson
├── tests/          test_code.py and the expected output of every lesson script
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python lessons/lesson-06.py                   # any lesson, from any folder
python challenges/lesson-06-challenges.py     # try the challenges
python projects/wine-starter.py               # work through a project
```

Scripts find `data/` relative to their own location, so they work wherever you unzip the folder.
Plots open in a window; set `MPLBACKEND=Agg` to skip them.

## Test

```bash
pytest -q
```

* **test_lessons** — every lesson script runs and prints the same output as when the course was published
  (`tests/expected/`). Tiny rounding differences are allowed. If a library update changes a result, the test shows the new output.
* **test_projects** — every project solution runs and all its checks pass.
* **test_challenges** — every challenge solution gives the expected answer, and every starter is still unsolved.

The outputs were produced with Python 3.13, NumPy 2.5, pandas 3.0, scikit-learn 1.9 and matplotlib 3.11.
