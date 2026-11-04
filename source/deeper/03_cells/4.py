# Gradient check for a tiny model: loss(w) = mean((tanh(Xw) − y)²)
rng = np.random.default_rng(0)
X = rng.normal(size=(20, 3)); y = rng.normal(size=20); w = rng.normal(size=3)
loss = lambda w: np.mean((np.tanh(X @ w) - y) ** 2)

def grad_formula(w):
    p = np.tanh(X @ w)
    return X.T @ (2 * (p - y) * (1 - p**2)) / len(y)   # chain rule: tanh' = 1 − tanh²

def rel_error(a, b):
    return np.linalg.norm(a - b) / (np.linalg.norm(a) + np.linalg.norm(b))

h = 1e-5
numeric = np.array([(loss(w + h * e) - loss(w - h * e)) / (2 * h) for e in np.eye(3)])
print("relative error, correct formula:", f"{rel_error(grad_formula(w), numeric):.1e}")
buggy = lambda w: X.T @ (2 * (np.tanh(X @ w) - y)) / len(y)   # forgot the tanh' factor
print("relative error, buggy formula:  ", f"{rel_error(buggy(w), numeric):.1e}")
