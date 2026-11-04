from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.datasets import load_breast_cancer
from scipy.stats import loguniform, randint

Xb, yb = load_breast_cancer(return_X_y=True)
gb = HistGradientBoostingClassifier(random_state=0)
grid = GridSearchCV(gb, {"learning_rate": [0.03, 0.1, 0.3], "max_leaf_nodes": [7, 15, 31],
                         "l2_regularization": [0.0, 1.0]}, cv=5).fit(Xb, yb)
rand = RandomizedSearchCV(gb, {"learning_rate": loguniform(0.01, 0.5), "max_leaf_nodes": randint(4, 64),
                               "l2_regularization": loguniform(1e-3, 10)}, n_iter=18, cv=5, random_state=0).fit(Xb, yb)
print(f"grid search:   {len(grid.cv_results_['params'])} settings, best CV accuracy {grid.best_score_:.3f}")
print(f"random search: {len(rand.cv_results_['params'])} settings, best CV accuracy {rand.best_score_:.3f}")
