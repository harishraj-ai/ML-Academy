sizes = [30, 30]; grp = np.repeat([0, 1], sizes)
P = np.where(grp[:, None] == grp[None, :], 0.25, 0.03)
B = np.triu(rng.random((60, 60)) < P, 1).astype(float); B = B + B.T
L = np.diag(B.sum(axis=1)) - B                                              # graph Laplacian
w, v = np.linalg.eigh(L)
fiedler = v[:, 1]                                                           # second-smallest eigenvector
split = (fiedler > 0).astype(int)
acc = max((split == grp).mean(), (split != grp).mean())
print("smallest Laplacian eigenvalues:", np.round(w[:3], 3).tolist())
print("splitting by the sign of the second eigenvector recovers the groups for", f"{acc:.0%}", "of nodes")
