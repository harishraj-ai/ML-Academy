import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance

# Two copies of the same signal: how do importance methods share the credit?
rng = np.random.default_rng(0)
n = 2000
a = rng.normal(size=n); b = a + rng.normal(0, 0.05, n)        # b is almost a copy of a
c = rng.normal(size=n)
X = np.column_stack([a, b, c]); y = 3 * a + 1 * c + rng.normal(0, 0.5, n)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, random_state=0)
rf = RandomForestRegressor(n_estimators=200, random_state=0).fit(X_tr, y_tr)
perm = permutation_importance(rf, X_te, y_te, n_repeats=10, random_state=0, scoring="r2").importances_mean
print("permutation importance (a, b, c):", perm.round(3))

# Drop-column importance: retrain without each feature and measure the loss
full = rf.score(X_te, y_te)
drop = [full - RandomForestRegressor(n_estimators=200, random_state=0).fit(np.delete(X_tr, j, 1), y_tr).score(np.delete(X_te, j, 1), y_te) for j in range(3)]
print("drop-column importance (a, b, c):", np.round(drop, 3))
