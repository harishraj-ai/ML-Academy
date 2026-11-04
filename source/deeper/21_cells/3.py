# Small groups make fairness metrics noisy: bootstrap interval for a TPR measured on just 400 people
yS, sS = yA[:400], sA[:400]
pos = np.flatnonzero(yS == 1)
boot = [np.mean(sS[rng.choice(pos, len(pos))] >= 0.5) for _ in range(5000)]
print("positives in the small sample:", len(pos), "  TPR:", round(np.mean(sS[pos] >= 0.5), 3),
      "  95% interval:", np.round(np.percentile(boot, [2.5, 97.5]), 3))
