from sklearn.linear_model import LinearRegression

# VIF of feature j = 1 / (1 - R²) when feature j is predicted from all the other features
for j, name in enumerate(names):
    others = np.delete(X, j, axis=1)
    r2_j = LinearRegression().fit(others, X[:, j]).score(others, X[:, j])
    print(f"{name:4} VIF {1 / (1 - r2_j):5.1f}")

# Drop s2 and refit: s1's standard error shrinks, the fit barely changes
keep = [j for j, name in enumerate(names) if name != "s2"]
w2, se2, *_ = ols(X[:, keep], y)
print("s1 with s2:    weight", round(w[5], 1), " SE", round(se[5], 1))
print("s1 without s2: weight", round(w2[5], 1), " SE", round(se2[5], 1))
print("R² with s2:   ", round(LinearRegression().fit(X, y).score(X, y), 4))
print("R² without s2:", round(LinearRegression().fit(X[:, keep], y).score(X[:, keep], y), 4))
