from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import brier_score_loss

Xa, ya = load_breast_cancer(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(Xa, ya, test_size=0.5, random_state=0, stratify=ya)
sc = StandardScaler().fit(Xtr)
models = {"logistic regression": LogisticRegression(max_iter=1000).fit(sc.transform(Xtr), ytr),
          "naive Bayes": GaussianNB().fit(sc.transform(Xtr), ytr)}
bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
for name, m in models.items():
    p = m.predict_proba(sc.transform(Xte))[:, 1]
    print(f"{name}: Brier score {brier_score_loss(yte, p):.3f}")
    idx = np.digitize(p, bins[1:-1])
    for b in range(5):
        sel = idx == b
        if sel.sum(): print(f"   predicted {bins[b]:.1f}–{bins[b+1]:.1f}: {sel.sum():3d} cases, average prediction {p[sel].mean():.2f}, actually positive {yte[sel].mean():.2f}")
