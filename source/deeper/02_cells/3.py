vals, vecs = np.linalg.eigh(A)            # eigh: for symmetric matrices
print("eigenvalues:", vals.round(3))
print("eigenvectors (columns):")
print(vecs.round(3))
v1 = vecs[:, 1]
print("A @ v:     ", (A @ v1).round(3))
print("lambda * v:", (vals[1] * v1).round(3))
print("dot product of the two eigenvectors:", abs(round(vecs[:, 0] @ vecs[:, 1], 10)))
