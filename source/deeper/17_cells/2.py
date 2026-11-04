# Kernel PCA: a non-linear version that can "unroll" circles
Xc, yc = make_circles(n_samples=400, factor=0.3, noise=0.05, random_state=0)
for name, emb in [("ordinary PCA", PCA(1)), ("kernel PCA (RBF)", KernelPCA(1, kernel="rbf", gamma=5))]:
    z = emb.fit_transform(Xc)
    acc = cross_val_score(LogisticRegression(), z, yc, cv=5).mean()
    print(f"{name:17}: a linear classifier on the 1 new feature scores {acc:.3f}")
