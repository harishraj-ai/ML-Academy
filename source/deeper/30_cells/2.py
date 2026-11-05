from sklearn.metrics import roc_auc_score
m = 3000
y = rng.integers(0, 2, m)
champion = y * 1.0 + rng.normal(0, 1.2, m)                          # current model's scores
challenger = y * 1.0 + rng.normal(0, 1.1, m)                        # new model, slightly better
diffs = []
for _ in range(1000):                                               # bootstrap the AUC difference
    idx = rng.integers(0, m, m)
    diffs.append(roc_auc_score(y[idx], challenger[idx]) - roc_auc_score(y[idx], champion[idx]))
lo, hi = np.percentile(diffs, [2.5, 97.5])
print("AUC champion", round(roc_auc_score(y, champion), 3), " challenger", round(roc_auc_score(y, challenger), 3))
print("95% interval for the improvement:", round(lo, 3), "to", round(hi, 3))
