import numpy as np
from sklearn.linear_model import LinearRegression
rng = np.random.default_rng(0); n = 20000
discount = rng.integers(0, 2, n)                               # randomised
visits = 2 + 3 * discount + rng.normal(0, 1, n)                 # the discount brings people back (a mediator)
spend = 50 + 4 * visits + rng.normal(0, 5, n)                   # all of the effect goes through visits: 4 × 3 = 12
total = LinearRegression().fit(np.c_[discount], spend).coef_[0]
blocked = LinearRegression().fit(np.c_[discount, visits], spend).coef_[0]
print("effect of the discount, not adjusting:", round(total, 2), "  'adjusting' for visits:", round(blocked, 2))
