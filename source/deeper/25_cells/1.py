import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss

X, y = make_classification(n_samples=40000, n_features=10, n_informative=5, weights=[0.98], flip_y=0, random_state=1)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.5, random_state=0, stratify=y)
pi = y_tr.mean()                                                    # true positive rate in training data
p_bal = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X_tr, y_tr).predict_proba(X_te)[:, 1]

# Undo the reweighting: the model behaves as if positives were as common as negatives
odds = p_bal / (1 - p_bal) * (pi / (1 - pi))
p_fixed = odds / (1 + odds)
p_plain = LogisticRegression(max_iter=1000).fit(X_tr, y_tr).predict_proba(X_te)[:, 1]
for name, p in [("balanced weights", p_bal), ("balanced, corrected", p_fixed), ("plain model", p_plain)]:
    print(f"{name:20}: average predicted risk {p.mean():.3f} (true rate {y_te.mean():.3f})   Brier score {brier_score_loss(y_te, p):.4f}")
