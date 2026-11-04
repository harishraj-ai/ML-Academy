from sklearn.model_selection import cross_val_score

n = len(y)
rng = np.random.default_rng(0)
print("noise cols  train R²  adjusted R²  5-fold CV R²")
for extra in [0, 10, 50, 100]:
    Xe = np.column_stack([X, rng.normal(size=(n, extra))])     # add columns of pure noise
    d = Xe.shape[1]
    r2 = LinearRegression().fit(Xe, y).score(Xe, y)
    adj = 1 - (1 - r2) * (n - 1) / (n - d - 1)
    cv = cross_val_score(LinearRegression(), Xe, y, cv=5, scoring="r2").mean()
    print(f"{extra:10d}  {r2:8.3f}  {adj:11.3f}  {cv:12.3f}")
