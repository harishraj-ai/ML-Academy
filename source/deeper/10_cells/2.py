# Lasso's key step: soft-thresholding, used by coordinate descent
soft = lambda z, t: np.sign(z) * np.maximum(np.abs(z) - t, 0)
for z in [3.0, 0.8, -0.3, -2.5]:
    print(f"least-squares value {z:5.1f} -> lasso value {soft(z, 1.0) + 0.0:5.1f}    ridge value {z / (1 + 1.0):5.2f}")
