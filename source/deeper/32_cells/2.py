from sklearn.datasets import load_digits
from sklearn.ensemble import BaggingClassifier
Xd, yd = load_digits(return_X_y=True); Xd = Xd / 16
pool, test2 = np.arange(1200), np.arange(1200, len(yd))
def run(strategy, seed):
    r = np.random.default_rng(seed); lab = list(r.choice(pool, 20, replace=False))
    for _ in range(10):
        rest = np.setdiff1d(pool, lab)
        if strategy == "committee":
            com = BaggingClassifier(LogisticRegression(max_iter=1000), n_estimators=5, random_state=seed).fit(Xd[lab], yd[lab])
            votes = np.array([est.predict(Xd[rest]) for est in com.estimators_])
            disagree = np.array([len(set(v)) for v in votes.T])           # number of distinct votes
            pick = rest[np.argsort(-disagree + 1e-3 * r.random(len(rest)))[:15]]
        else:
            pick = r.choice(rest, 15, replace=False)
        lab += list(pick)
    return LogisticRegression(max_iter=1000).fit(Xd[lab], yd[lab]).score(Xd[test2], yd[test2])
for s in ["random", "committee"]:
    print(f"{s:9s}: test accuracy with 170 labels {np.mean([run(s, k) for k in range(3)]):.3f}")
