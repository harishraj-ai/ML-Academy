# Part 6 (intermediate) lessons. Add a lesson by creating lessonNN_data.py and lessons/NN.html, then listing NN here.
import importlib
NUMS = [22, 23, 24, 25]
MODULES = [importlib.import_module(f"lesson{n}_data") for n in NUMS]
LESSONS = [getattr(m, f"L{n}") for n, m in zip(NUMS, MODULES)]
OBJ = {n: getattr(m, f"OBJ{n}") for n, m in zip(NUMS, MODULES)}
SRC = {n: getattr(m, f"SRC{n}") for n, m in zip(NUMS, MODULES)}
