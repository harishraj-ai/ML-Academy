import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = load_breast_cancer(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
path = DecisionTreeClassifier(random_state=0).cost_complexity_pruning_path(Xtr, ytr)
print(" ccp_alpha   leaves   train acc   test acc")
for a in path.ccp_alphas[::3]:
    t = DecisionTreeClassifier(random_state=0, ccp_alpha=a).fit(Xtr, ytr)
    print(f"{a:9.4f}   {t.get_n_leaves():6d}   {t.score(Xtr, ytr):9.3f}   {t.score(Xte, yte):8.3f}")
