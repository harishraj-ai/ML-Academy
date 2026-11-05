import numpy as np
rng = np.random.default_rng(0)
n_users, n_items, k = 200, 40, 3
P_true, Q_true = rng.normal(0, 1, (n_users, k)), rng.normal(0, 1, (n_items, k))
R = P_true @ Q_true.T + rng.normal(0, 0.3, (n_users, n_items))
mask = rng.random((n_users, n_items)) < 0.2            # only 20% of ratings observed
test = (rng.random((n_users, n_items)) < 0.25) & mask
train = mask & ~test
P, Q, lam = rng.normal(0, 0.1, (n_users, k)), rng.normal(0, 0.1, (n_items, k)), 1.0
for sweep in range(1, 9):
    for u in range(n_users):                           # fix Q, solve a small ridge problem per user
        Qi = Q[train[u]]
        P[u] = np.linalg.solve(Qi.T @ Qi + lam * np.eye(k), Qi.T @ R[u, train[u]])
    for i in range(n_items):                           # fix P, solve per item
        Pu = P[train[:, i]]
        Q[i] = np.linalg.solve(Pu.T @ Pu + lam * np.eye(k), Pu.T @ R[train[:, i], i])
    if sweep in (1, 2, 4, 8):
        rmse = np.sqrt(np.mean((R - P @ Q.T)[test] ** 2))
        print("sweep", sweep, " test RMSE", round(rmse, 3))
