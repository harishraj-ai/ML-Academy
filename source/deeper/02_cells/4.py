# A ratings table: 50 users × 40 films, built from 3 hidden "tastes" plus noise
rng = np.random.default_rng(0)
R = rng.normal(size=(50, 3)) @ rng.normal(size=(3, 40)) + rng.normal(0, 0.3, size=(50, 40))
U, s, Vt = np.linalg.svd(R, full_matrices=False)
print("largest singular values:", s[:6].round(1))
for k in [1, 2, 3, 5, 10]:
    approx = U[:, :k] @ np.diag(s[:k]) @ Vt[:k]          # keep only the k largest
    err = np.linalg.norm(R - approx) / np.linalg.norm(R)
    print(f"rank {k:2d}: stores {k * (50 + 40 + 1):4d} of 2000 numbers, relative error {err:.3f}")
