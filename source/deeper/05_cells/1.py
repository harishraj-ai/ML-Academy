import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import GridSearchCV, cross_val_score, KFold
from sklearn.svm import SVC

# A small, noisy problem where tuning can easily "overfit the validation folds"
X, y = make_classification(n_samples=120, n_features=40, n_informative=4, flip_y=0.2, random_state=0)
grid = {"C": [0.01, 0.1, 1, 10, 100], "gamma": [0.0001, 0.001, 0.01, 0.1, 1]}
inner, outer = KFold(5, shuffle=True, random_state=1), KFold(5, shuffle=True, random_state=2)

search = GridSearchCV(SVC(), grid, cv=inner).fit(X, y)
print("best score inside the search (optimistic):", round(search.best_score_, 3))
nested = cross_val_score(GridSearchCV(SVC(), grid, cv=inner), X, y, cv=outer)
print("nested cross-validation (honest):        ", round(nested.mean(), 3))
