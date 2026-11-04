
# Isolation Forest's intuition: average number of random splits needed to isolate a point
rng = np.random.default_rng(0)
pts = np.vstack([rng.normal(0, 1, (500, 2)), [[6, 6]]])            # 500 normal points and one far away
def splits_to_isolate(i, trials=200):
    total = 0
    for _ in range(trials):
        idx = np.arange(len(pts)); depth = 0
        while len(idx) > 1:
            f = rng.integers(2); lo, hi = pts[idx, f].min(), pts[idx, f].max()
            t = rng.uniform(lo, hi)
            idx = idx[pts[idx, f] < t] if pts[i, f] < t else idx[pts[idx, f] >= t]
            depth += 1
        total += depth
    return total / trials
print("average splits to isolate the far point:   ", round(splits_to_isolate(500), 1))
print("average splits to isolate a typical point: ", round(np.mean([splits_to_isolate(i, 40) for i in range(10)]), 1))
