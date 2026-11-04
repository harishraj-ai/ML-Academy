from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True)
for metric in ["euclidean", "manhattan", "cosine"]:
    for weights in ["uniform", "distance"]:
        m = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=15, metric=metric, weights=weights))
        print(f"{metric:9} {weights:8}: accuracy {cross_val_score(m, X, y, cv=10).mean():.3f}")
