from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier

# Adversarial validation: can a model tell training rows from "production" rows?
rng = np.random.default_rng(1)
train_rows = rng.normal(0, 1, size=(500, 3))
prod_same = rng.normal(0, 1, size=(500, 3))
prod_shift = rng.normal(0, 1, size=(500, 3)); prod_shift[:, 0] += 0.8   # one feature has drifted

cv = StratifiedKFold(5, shuffle=True, random_state=0)
for name, prod in [("no shift", prod_same), ("feature 0 drifted", prod_shift)]:
    Xa = np.vstack([train_rows, prod]); ya = np.r_[np.zeros(500), np.ones(500)]
    clf = RandomForestClassifier(n_estimators=200, min_samples_leaf=10, random_state=0)
    p = cross_val_predict(clf, Xa, ya, cv=cv, method="predict_proba")[:, 1]
    imp = clf.fit(Xa, ya).feature_importances_
    print(f"{name:18}: AUC {roc_auc_score(ya, p):.3f}   feature importances {imp.round(2)}")
