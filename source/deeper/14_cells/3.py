from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

base = [("forest", RandomForestClassifier(n_estimators=300, random_state=0)),
        ("boost", HistGradientBoostingClassifier(random_state=0)),
        ("knn", make_pipeline(StandardScaler(), KNeighborsClassifier(15)))]
for name, m in base:
    print(f"{name:7}: test accuracy {m.fit(Xtr, ytr).score(Xte, yte):.3f}")
stack = StackingClassifier(base, final_estimator=LogisticRegression(max_iter=1000), cv=5).fit(Xtr, ytr)
print(f"stacked: test accuracy {stack.score(Xte, yte):.3f}   blender weights {stack.final_estimator_.coef_.round(2)}")
