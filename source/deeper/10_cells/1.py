import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline

# Measure bias² and variance directly: refit on 300 fresh training sets
rng = np.random.default_rng(0)
f = lambda x: np.sin(2 * np.pi * x)                   # the true curve
x_test = np.linspace(0, 1, 50)
for lam in [1e-6, 1e-3, 1e-1, 10]:
    preds = []
    for _ in range(300):
        x = rng.uniform(0, 1, 20); y = f(x) + rng.normal(0, 0.3, 20)
        m = make_pipeline(PolynomialFeatures(9), Ridge(alpha=lam)).fit(x[:, None], y)
        preds.append(m.predict(x_test[:, None]))
    preds = np.array(preds)
    bias2 = np.mean((preds.mean(axis=0) - f(x_test)) ** 2)
    var = np.mean(preds.var(axis=0))
    print(f"lambda {lam:7.0e}: bias² {bias2:.3f}   variance {var:.3f}   expected error {bias2 + var + 0.09:.3f}")
