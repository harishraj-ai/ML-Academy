from sklearn.metrics import average_precision_score

# Same model quality, rarer positives: scores of positives ~ N(1.5, 1), negatives ~ N(0, 1)
rng = np.random.default_rng(1)
for n_pos in [10000, 1000, 100]:
    s = np.r_[rng.normal(1.5, 1, n_pos), rng.normal(0, 1, 10000)]
    t = np.r_[np.ones(n_pos), np.zeros(10000)]
    print(f"positives {t.mean():6.1%}: ROC-AUC {roc_auc_score(t, s):.3f}   average precision {average_precision_score(t, s):.3f}   (random model's AP {t.mean():.3f})")
