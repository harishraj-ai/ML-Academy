# Lasso with two almost identical features, on bootstrap samples: which one does it keep?
rng = np.random.default_rng(1)
from sklearn.linear_model import Lasso
n = 200
z = rng.normal(size=n)                                    # one underlying quantity…
a = z + rng.normal(0, 0.05, n); b = z + rng.normal(0, 0.05, n)   # …measured twice
yy = 3 * z + rng.normal(0, 1, n)
picks = {"only a": 0, "only b": 0, "both": 0}
for _ in range(200):
    i = rng.integers(0, n, n)
    w = Lasso(alpha=1.0).fit(np.column_stack([a, b])[i], yy[i]).coef_
    key = "both" if (w != 0).all() else ("only a" if w[0] != 0 else "only b")
    picks[key] += 1
print("lasso, 200 bootstrap samples:", picks)
from sklearn.linear_model import ElasticNet
w = ElasticNet(alpha=1.0, l1_ratio=0.5).fit(np.column_stack([a, b]), yy).coef_
print("elastic net weights on the full data:", w.round(2))
