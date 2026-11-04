# Check the matrix-calculus rule  ∇_w ||Xw − y||² = 2 Xᵀ(Xw − y)  with finite differences
rng = np.random.default_rng(3)
Xg = rng.normal(size=(5, 3)); yg = rng.normal(size=5); w = rng.normal(size=3)
f = lambda w: np.sum((Xg @ w - yg) ** 2)
formula = 2 * Xg.T @ (Xg @ w - yg)
h = 1e-6
numeric = np.array([(f(w + h * e) - f(w - h * e)) / (2 * h) for e in np.eye(3)])
print("formula:", formula.round(4))
print("numeric:", numeric.round(4))
