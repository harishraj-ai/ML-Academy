from sklearn.linear_model import LassoCV, ElasticNetCV
from sklearn.datasets import load_diabetes
from sklearn.preprocessing import StandardScaler

X, y = load_diabetes(return_X_y=True)
X = StandardScaler().fit_transform(X)
lasso = LassoCV(cv=5, random_state=0).fit(X, y)
enet = ElasticNetCV(l1_ratio=[0.1, 0.5, 0.9], cv=5, random_state=0).fit(X, y)
print("lasso: best alpha", round(lasso.alpha_, 3), " non-zero weights", np.sum(lasso.coef_ != 0), "of 10")
print("elastic net: best alpha", round(enet.alpha_, 3), " l1_ratio", enet.l1_ratio_, " non-zero", np.sum(enet.coef_ != 0))
