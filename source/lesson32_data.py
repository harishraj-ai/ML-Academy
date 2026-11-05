# Lesson 32: Semi-supervised & Active Learning. Patches the shared per-lesson dictionaries on import.
import context, extras_ex_b, checks, running_code, running_text, challenges, reference, understanding, rai

L32 = (32, 6, "Semi-supervised & Active Learning", "Learning with few labels: self-training and pseudo-labels, label spreading on a graph, and active learning with uncertainty sampling.", 50)

OBJ32 = ["Explain the smoothness, cluster and manifold assumptions behind semi-supervised learning",
         "Apply self-training with a confidence threshold and recognise confirmation bias",
         "Use label spreading to propagate labels along a nearest-neighbour graph",
         "Run active learning with uncertainty sampling and compare it with random labelling"]

SRC32 = [("Settles (2009) — Active Learning Literature Survey", "https://burrsettles.com/pub/settles.activelearning.pdf"),
         ("Zhou et al. (2004) — Learning with Local and Global Consistency, NeurIPS", "https://proceedings.neurips.cc/paper/2003/hash/87682805257e619d49b8e0dfdc14affa-Abstract.html"),
         ("van Engelen & Hoos (2020) — A survey on semi-supervised learning, Machine Learning", "https://link.springer.com/article/10.1007/s10994-019-05855-6"),
         ("Ratner et al. (2017) — Snorkel: Rapid Training Data Creation with Weak Supervision", "https://arxiv.org/abs/1711.10160"),
         ("scikit-learn — Semi-supervised learning", "https://scikit-learn.org/stable/modules/semi_supervised.html"),
         ("Chapelle, Schölkopf & Zien (eds.) — Semi-Supervised Learning", "https://mitpress.mit.edu/9780262514125/semi-supervised-learning/")]

context.DEPS[32] = [8, 11, 16]
context.REFRESH[32] = "Unlabelled data helps when nearby points share labels; self-training and label spreading use it, and active learning picks the labels worth paying for."
context.FIT[32] = "Combines classification (Lesson 8), nearest-neighbour graphs (Lesson 11) and cluster structure (Lesson 16) to learn from mostly unlabelled data."
context.USE[32] = (["Medical imaging and document classification with few expert labels",
                    "Tagging support tickets, products or content with a small labelling budget",
                    "Building training sets faster with a human in the loop"],
                   "Whenever unlabelled data is plentiful and labels are expensive.",
                   "labels are cheap or the unlabelled data doesn't share the structure of the labels: then simply label more.")
context.FAQ[32] = [
    ("How many labels do I need to start?",
     "Enough for every class to appear several times and for a rough first model: often a few dozen to a few hundred. Start random, then switch to active learning."),
    ("Is semi-supervised learning always better than using labels alone?",
     "No. When its assumptions fail it can hurt. Always compare with the labelled-only baseline on a labelled test set."),
    ("What's weak supervision?",
     "Writing several rough labelling rules (keywords, heuristics, other models), combining their noisy votes into probabilistic labels, and training on those."),
    ("How is this related to self-supervised learning?",
     "Self-supervised learning creates tasks from unlabelled data itself (predict a missing word or patch) to learn features, then fine-tunes on a few labels. It's the deep-learning route to the same goal."),
]
understanding.MYTHS[32] = [
    ("Unlabelled data always helps.", "Only if similar points share labels; otherwise it can mislead the model."),
    ("More pseudo-labels are always better.", "Low-confidence pseudo-labels add errors, and the model reinforces its own mistakes."),
    ("Active learning always picks the best examples.", "Pure uncertainty sampling can chase outliers and noise; mix in random and diverse picks."),
]
extras_ex_b.MISTAKES[32] = [
    "Evaluating on pseudo-labels instead of a properly labelled test set.",
    "Setting the self-training threshold too low.",
    "Running label spreading on unscaled features.",
    "Using only uncertainty sampling, so the labelled set is full of odd outliers.",
    "Starting active learning with a labelled set that misses some classes.",
]
extras_ex_b.EX[32] = [
    ("By hand", "A model gives class probabilities (0.55, 0.40, 0.05) for one image and (0.48, 0.47, 0.05) for another. Using the margin between the top two, which is more uncertain?",
     "Margins: 0.55 − 0.40 = 0.15 and 0.48 − 0.47 = 0.01. The second is more uncertain, so label it first."),
    ("By hand", "Self-training adds 800 pseudo-labels, 6% of them wrong. How many wrong labels enter the training set?",
     "0.06 × 800 = 48."),
    ("By hand", "Random labelling needs 400 labels to reach 94.6% accuracy; active learning needs 170. What percentage of labelling effort does active learning save?",
     "(400 − 170)/400 = 0.575, about 57.5%."),
    ("By hand", "An unlabelled point's 3 nearest neighbours have labels A, A and B (unweighted). Which label would simple propagation give it?",
     "A, the majority among its neighbours."),
    ("Code", "In the active-learning code, change the batch size from 15 to 1 (and the rounds to 150). Does accuracy at 170 labels improve?",
     "Usually a little, because each choice uses the latest model, but it needs 150 rounds of retraining and labelling. Batches trade a small loss in efficiency for practicality."),
]
checks.CHECKS[(32, 1)] = [("Wrong labels", 48, "Share wrong × number added.")]
checks.CHECKS[(32, 2)] = [("Saving", 57.5, "Labels saved ÷ random labels, as a percentage.", 0.1)]

running_code.CODE[32] = '''import pandas as pd
import numpy as np
df = pd.read_csv("houses.csv")   # download it from Lesson 1
from sklearn.semi_supervised import LabelSpreading
from sklearn.preprocessing import StandardScaler
X = StandardScaler().fit_transform(df[["size_m2", "dist_km", "age_yrs", "price_lakh"]])
known = np.array([True, False, False, True, False, True, False, False, True, False, True, False])
y = np.where(known, df.sold_fast, -1)
ls = LabelSpreading(kernel="knn", n_neighbors=3).fit(X, y)
hidden = ~known
print("labels known for", known.sum(), "homes; inferred for", hidden.sum())
print("inferred correctly:", int((ls.transduction_[hidden] == df.sold_fast[hidden]).sum()), "of", hidden.sum())'''
running_text.INTRO[32] = ("Suppose only 5 of the 12 homes are known to have sold fast or not. Label spreading connects each home to its 3 most similar homes (size, distance, age and price, standardised) and lets the 5 known labels flow to the other 7. "
    "It infers 4 of the 7 correctly: better than nothing, but with this few homes the neighbourhoods are rough. Semi-supervised methods shine with hundreds of unlabelled points that reveal the shape of the classes.")

challenges.C[32] = [
    ("Margin uncertainty", "Compute the margin between the two highest probabilities.",
     'import numpy as np\np = np.array([0.2, 0.45, 0.35])\n##BLANK##',
     'margin', 'margin = round(float(np.sort(p)[-1] - np.sort(p)[-2]), 2)', "Sort descending, then subtract the second from the first.",
     'margin = p.max()  # ← subtract the second-highest probability'),
    ("Pick the most uncertain", "Return the index of the row with the smallest margin.",
     'import numpy as np\nP = np.array([[0.9, 0.1], [0.55, 0.45], [0.7, 0.3]])\n##BLANK##',
     'pick', 'pick = int(np.argmin(np.abs(P[:, 0] - P[:, 1])))', "The margin is the gap between the two probabilities; take the argmin.",
     'pick = int(np.argmax(P[:, 0]))  # ← that is the most confident'),
]

reference.GLOSSARY += [
    ("Semi-supervised learning", "Learning from a small labelled set together with a large unlabelled set.", 32, "assumptions"),
    ("Pseudo-label", "A model's confident prediction for an unlabelled example, used as if it were a label.", 32, "self"),
    ("Label spreading", "A graph method that propagates known labels to unlabelled neighbours until they settle.", 32, "spread"),
    ("Active learning", "Choosing which examples to label next, to learn most from each label.", 32, "active"),
    ("Uncertainty sampling", "An active-learning strategy that labels the examples the model is least sure about.", 32, "active"),
]

rai.RAI[32] = ("Whose examples get labelled?",
    "<p>Semi-supervised and active learning decide which data a model learns from. If the starting labels under-represent a group, pseudo-labels for that group are likelier to be wrong and errors compound; uncertainty sampling may also over-sample unusual cases while ignoring others. Check label quality and performance by group, and seed the labelled set deliberately to cover the population.</p>")
