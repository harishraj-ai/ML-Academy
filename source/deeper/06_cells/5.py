from sklearn.linear_model import HuberRegressor

rng = np.random.default_rng(1)
x = np.arange(1, 21, dtype=float)
y_ = 2 * x + 5 + rng.normal(0, 2, size=20)         # true line: y = 2x + 5
x = np.append(x, 40.0); y_ = np.append(y_, 20.0)   # one unusual point far to the right

A = np.column_stack([np.ones_like(x), x])
lev = np.diag(A @ np.linalg.inv(A.T @ A) @ A.T)    # leverage = diagonal of the hat matrix
w_ = np.linalg.solve(A.T @ A, A.T @ y_)
e = y_ - A @ w_
p_ = A.shape[1]
s2 = e @ e / (len(y_) - p_)
cooks = e**2 / (p_ * s2) * lev / (1 - lev) ** 2     # Cook's distance

print("slope, least squares with the point:   ", round(w_[1], 2))
print("slope, least squares without the point:", round(LinearRegression().fit(x[:-1, None], y_[:-1]).coef_[0], 2))
print("slope, Huber with the point:           ", round(HuberRegressor().fit(x[:, None], y_).coef_[0], 2))
print("leverage: median", round(np.median(lev), 3), "| unusual point", round(lev[-1], 3))
print("Cook's D: largest other", round(cooks[:-1].max(), 3), "| unusual point", round(cooks[-1], 2))
