import numpy as np
import pandas as pd
rng = np.random.default_rng(3)
t = np.arange(730)
y = pd.Series((200 + 0.15 * t) * np.array([0.85, 0.9, 0.95, 1.0, 1.05, 1.25, 1.1])[t % 7] * rng.lognormal(0, 0.08, 730))
change = y.diff(1)                                   # remove the trend first
acf = {lag: round(float(change.autocorr(lag)), 2) for lag in [1, 2, 3, 6, 7, 14, 21]}
print("autocorrelation of daily changes by lag:", acf)
