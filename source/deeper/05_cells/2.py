from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor

# Daily sales that drift slowly over time: neighbouring days look alike
rng = np.random.default_rng(0)
t = np.arange(600)
trend = np.cumsum(rng.normal(0, 1, 600))                  # a slow random walk
Xt = np.column_stack([t, np.sin(2 * np.pi * t / 7)])      # day number and weekday pattern
yt = trend + 3 * Xt[:, 1] + rng.normal(0, 1, 600)

model = RandomForestRegressor(n_estimators=100, random_state=0)
shuffled = cross_val_score(model, Xt, yt, cv=KFold(5, shuffle=True, random_state=0), scoring="r2")
forward = cross_val_score(model, Xt, yt, cv=TimeSeriesSplit(5), scoring="r2")
print("shuffled k-fold R²:   ", round(shuffled.mean(), 3))
print("time-ordered split R²:", round(forward.mean(), 3))
