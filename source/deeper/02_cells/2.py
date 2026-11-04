# Three features, but the third is the sum of the first two
X = np.array([[1, 2, 3],
              [2, 0, 2],
              [0, 1, 1],
              [3, 1, 4]], dtype=float)
print("columns:", X.shape[1], " rank:", np.linalg.matrix_rank(X))
print("det(XᵀX):", round(np.linalg.det(X.T @ X), 6))

A = np.array([[2.0, 1.0], [1.0, 3.0]])
print("det(A):", round(np.linalg.det(A), 3), "-> A scales areas by this factor")
