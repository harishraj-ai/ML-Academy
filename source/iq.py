# Gathers hidden interview questions and confused pairs; assigns stable ids.
import importlib
QS = []
for mod in ["interview_a", "interview_b", "interview_c", "interview_d"]:
    try: QS += importlib.import_module(mod).Q
    except ModuleNotFoundError: pass
import deeper as _deeper
QS += _deeper.interview_questions()      # intermediate questions from the Going deeper sections
from confused import PAIRS
_seen = {}
QI = []   # (id, lesson, level, q, trap, a)
for (n, lvl, q, trap, a) in QS:
    _seen[n] = _seen.get(n, 0) + 1
    QI.append((f"q{n}-{_seen[n]}", n, lvl, q, trap, a))
PI = []   # (id, lesson, title, diff, hook)
_ps = {}
for (n, t, d, h) in PAIRS:
    _ps[n] = _ps.get(n, 0) + 1
    PI.append((f"p{n}-{_ps[n]}", n, t, d, h))
LEVELS = {1: "Basics", 2: "Interview", 3: "Deep-dive"}
