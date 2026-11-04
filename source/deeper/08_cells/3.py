from sklearn.metrics import recall_score, precision_score

# Imbalanced problem: 5% positives
from sklearn.datasets import make_classification
Xi, yi = make_classification(n_samples=4000, n_features=8, weights=[0.95], class_sep=0.8, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(Xi, yi, test_size=0.5, random_state=0, stratify=yi)
for cw in [None, "balanced"]:
    m = LogisticRegression(class_weight=cw).fit(Xtr, ytr)
    pr = m.predict(Xte)
    print(f"class_weight {str(cw):9}: recall {recall_score(yte, pr):.3f}  precision {precision_score(yte, pr):.3f}  average predicted probability {m.predict_proba(Xte)[:, 1].mean():.3f}")
print("true share of positives in the test set:", round(yte.mean(), 3))
