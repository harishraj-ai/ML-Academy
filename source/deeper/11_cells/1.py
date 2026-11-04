import numpy as np

# Distance concentration: in high dimensions the nearest and farthest points are almost equally far
rng = np.random.default_rng(0)
for d in [2, 10, 100, 1000]:
    pts = rng.uniform(size=(1000, d)); q = rng.uniform(size=d)
    dist = np.linalg.norm(pts - q, axis=1)
    print(f"{d:4d} dimensions: nearest {dist.min():6.2f}   farthest {dist.max():6.2f}   ratio {dist.max() / dist.min():5.2f}")
