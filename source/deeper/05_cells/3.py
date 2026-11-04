from sklearn.model_selection import learning_curve
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

Xb, yb = load_breast_cancer(return_X_y=True)
sizes, tr, va = learning_curve(make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)), Xb, yb,
                               train_sizes=[0.05, 0.1, 0.25, 0.5, 1.0], cv=5, shuffle=True, random_state=0)
for s, a, b in zip(sizes, tr.mean(axis=1), va.mean(axis=1)):
    print(f"{s:4d} training examples: train accuracy {a:.3f}   validation accuracy {b:.3f}")
