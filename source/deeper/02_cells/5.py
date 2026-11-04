rng = np.random.default_rng(2)
n = 100
size = rng.uniform(50, 150, n)
size2 = size + rng.normal(0, 0.5, n)                 # a second, almost identical measurement
Xc = np.column_stack([size, size2]); Xc = Xc - Xc.mean(axis=0)
y = 0.6 * Xc[:, 0] + rng.normal(0, 5, n)
y_nudged = y + rng.normal(0, 1, n)                   # a small change in the targets

G = Xc.T @ Xc
print("condition number of XᵀX:", round(np.linalg.cond(G)))
print("weights:            ", np.linalg.solve(G, Xc.T @ y).round(2))
print("after a tiny change:", np.linalg.solve(G, Xc.T @ y_nudged).round(2))
Gr = G + 100 * np.eye(2)                             # ridge: add λI with λ = 100
print("condition number with ridge:", round(np.linalg.cond(Gr)))
print("ridge weights:      ", np.linalg.solve(Gr, Xc.T @ y).round(2))
print("after a tiny change:", np.linalg.solve(Gr, Xc.T @ y_nudged).round(2))
