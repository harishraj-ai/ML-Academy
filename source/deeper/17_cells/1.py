import numpy as np
from sklearn.datasets import load_digits, make_circles
from sklearn.decomposition import PCA, KernelPCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

# How many components? Variance kept and reconstruction error on the digits (64 pixels)
X, y = load_digits(return_X_y=True)
pca = PCA().fit(X)
cum = np.cumsum(pca.explained_variance_ratio_)
for k in [2, 10, 20, 30, 40]:
    p = PCA(k).fit(X)
    rec = p.inverse_transform(p.transform(X))
    err = np.mean((X - rec) ** 2) / np.mean((X - X.mean(0)) ** 2)
    print(f"{k:2d} components: variance kept {cum[k - 1]:.3f}   relative reconstruction error {err:.3f}")
print("components needed for 95% of the variance:", int(np.searchsorted(cum, 0.95) + 1))
