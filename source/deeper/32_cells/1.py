import numpy as np
from sklearn.semi_supervised import LabelSpreading
from sklearn.linear_model import LogisticRegression
rng = np.random.default_rng(0)
# The label depends on feature 1; feature 2 is irrelevant noise on a scale 50 times larger.
X = np.c_[rng.normal(0, 1, 600), rng.normal(0, 50, 600)]
y = (X[:, 0] > 0).astype(int)
lab = rng.choice(600, 20, replace=False)
yp = np.full(600, -1); yp[lab] = y[lab]
test = np.setdiff1d(np.arange(600), lab)
sup = LogisticRegression().fit(X[lab], y[lab]).score(X[test], y[test])
spread = (LabelSpreading(kernel="knn", n_neighbors=10).fit(X, yp).transduction_[test] == y[test]).mean()
Xs = X / X.std(axis=0)
spread_s = (LabelSpreading(kernel="knn", n_neighbors=10).fit(Xs, yp).transduction_[test] == y[test]).mean()
print("labelled only:", round(sup, 3), "  label spreading, raw features:", round(spread, 3), "  after scaling:", round(spread_s, 3))
