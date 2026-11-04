import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score

X, y = load_breast_cancer(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
logreg = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(Xtr, ytr)
tree = DecisionTreeClassifier(max_depth=3, random_state=0).fit(Xtr, ytr)
p_lr, p_tr = logreg.predict_proba(Xte)[:, 1], tree.predict_proba(Xte)[:, 1]

rng = np.random.default_rng(0)
boot = []
for _ in range(2000):
    i = rng.integers(0, len(yte), len(yte))            # resample test cases with replacement
    if len(np.unique(yte[i])) == 2:
        boot.append(roc_auc_score(yte[i], p_lr[i]) - roc_auc_score(yte[i], p_tr[i]))
print("AUC: logistic", round(roc_auc_score(yte, p_lr), 3), " tree", round(roc_auc_score(yte, p_tr), 3))
print("95% bootstrap interval for the difference:", np.round(np.percentile(boot, [2.5, 97.5]), 3))
