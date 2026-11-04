import numpy as np

# The kernel trick: (x·z + 1)² equals the dot product of explicit degree-2 features
def phi(v):
    a, b = v
    return np.array([1, np.sqrt(2) * a, np.sqrt(2) * b, a * a, b * b, np.sqrt(2) * a * b])

x, z = np.array([1.0, 2.0]), np.array([3.0, -1.0])
print("kernel (x·z + 1)²:     ", (x @ z + 1) ** 2)
print("explicit φ(x)·φ(z):    ", round(phi(x) @ phi(z), 10))
