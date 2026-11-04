import numpy as np

v = np.array([3.0, -4.0, 1.0])
print("L1 norm (sum of sizes):    ", np.linalg.norm(v, 1))
print("L2 norm (straight line):   ", round(np.linalg.norm(v), 3))
print("L-infinity (biggest entry):", np.linalg.norm(v, np.inf))

M = np.array([[1.0, 2.0], [3.0, 4.0]])
print("Frobenius norm of M:       ", round(np.linalg.norm(M), 3))
