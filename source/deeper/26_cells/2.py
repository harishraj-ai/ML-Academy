from sklearn.linear_model import Ridge
X = pd.DataFrame({f"lag_{l}": y.shift(l) for l in [7, 14, 21]}).dropna(); target = y[X.index]
cal, test = X.index[(X.index >= 550) & (X.index < 640)], X.index[X.index >= 640]
model = Ridge(1.0).fit(X[X.index < 550], target[target.index < 550])
resid = target[cal] - model.predict(X.loc[cal])
lo, hi = np.quantile(resid, [0.05, 0.95])            # 90% interval from held-out errors
pred = model.predict(X.loc[test])
inside = ((target[test] >= pred + lo) & (target[test] <= pred + hi)).mean()
print("interval offsets:", round(lo, 1), "to", round(hi, 1), "  coverage on the test period:", round(inside, 3))
