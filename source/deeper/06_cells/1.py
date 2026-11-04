import numpy as np
from scipy import stats
from sklearn.datasets import load_diabetes

def ols(X, y):
    """Least squares plus standard errors, t, p-values and 95% intervals."""
    n, d = X.shape
    A = np.column_stack([np.ones(n), X])            # add the bias column
    w = np.linalg.solve(A.T @ A, A.T @ y)           # the usual weights
    resid = y - A @ w
    dof = n - d - 1                                 # data points minus parameters
    sigma2 = resid @ resid / dof                    # estimated noise variance
    se = np.sqrt(np.diag(sigma2 * np.linalg.inv(A.T @ A)))
    t = w / se                                      # how many SEs away from zero
    p = 2 * stats.t.sf(np.abs(t), dof)              # two-sided p-values
    tc = stats.t.ppf(0.975, dof)                    # 95% critical value
    return w, se, t, p, w - tc * se, w + tc * se

data = load_diabetes()
X, y, names = data.data, data.target, data.feature_names
w, se, t, p, lo, hi = ols(X, y)
print(f"{'':6}{'weight':>8}{'SE':>7}{'t':>7}{'p':>7}   95% interval")
for row in zip(["bias"] + names, w, se, t, p, lo, hi):
    print("{:6}{:8.1f}{:7.1f}{:7.2f}{:7.3f}   [{:7.1f}, {:7.1f}]".format(*row))
