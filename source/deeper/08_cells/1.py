import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

X, y = load_breast_cancer(return_X_y=True)
X = StandardScaler().fit_transform(X[:, :5])          # 5 features keep the example small
A = np.column_stack([np.ones(len(y)), X])
lam = 1.0                                             # L2 penalty, same as sklearn's C = 1

w = np.zeros(A.shape[1])
for it in range(1, 11):                               # Newton's method (IRLS)
    p = 1 / (1 + np.exp(-A @ w))
    grad = A.T @ (p - y) + lam * np.r_[0, w[1:]]      # don't penalise the bias
    S = p * (1 - p)                                   # each point's weight
    H = A.T @ (A * S[:, None]) + lam * np.diag(np.r_[0, np.ones(5)])
    step = np.linalg.solve(H, grad)
    w -= step
    print(f"iteration {it}: step size {np.linalg.norm(step):.2e}")
    if np.linalg.norm(step) < 1e-8: break

sk = LogisticRegression(C=1.0, tol=1e-10, max_iter=1000).fit(X, y)   # tight tolerance
print("ours:   ", w.round(4))
print("sklearn:", np.r_[sk.intercept_, sk.coef_[0]].round(4))
