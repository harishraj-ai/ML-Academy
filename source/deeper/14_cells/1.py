import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X, y = load_breast_cancer(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
# max_features controls how different the trees are
for mf in [1.0, 0.5, "sqrt", 1]:
    rf = RandomForestClassifier(n_estimators=300, max_features=mf, oob_score=True, random_state=0, n_jobs=-1).fit(Xtr, ytr)
    preds = np.array([t.predict(Xte) for t in rf.estimators_])
    corr = np.corrcoef(preds)[np.triu_indices(len(preds), 1)].mean()
    print(f"max_features {str(mf):5}: tree-to-tree correlation {corr:.2f}   out-of-bag accuracy {rf.oob_score_:.3f}   test {rf.score(Xte, yte):.3f}")
