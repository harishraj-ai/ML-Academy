import numpy as np
rng = np.random.default_rng(3)
n = 60
A = (rng.random((n, n)) < 0.08).astype(float); np.fill_diagonal(A, 0)      # a directed graph
out = A.sum(axis=1, keepdims=True)
M = np.where(out > 0, A / np.maximum(out, 1), 1 / n)
G = 0.15 / n + 0.85 * M                                                     # the "Google matrix"
vals, vecs = np.linalg.eig(G.T)
lead = np.real(vecs[:, np.argmax(np.real(vals))]); lead = lead / lead.sum()
r = np.full(n, 1 / n)
for it in range(1, 101):
    r_new = r @ G
    if np.abs(r_new - r).sum() < 1e-10: break
    r = r_new
print("largest eigenvalue:", round(float(np.max(np.real(vals))), 6), "  power iteration converged in", it, "steps")
print("max difference from the eigenvector:", f"{np.abs(r - lead).max():.1e}")
print("correlation with in-degree:", round(np.corrcoef(r, A.sum(axis=0))[0, 1], 3), "  with out-degree:", round(np.corrcoef(r, A.sum(axis=1))[0, 1], 3))
