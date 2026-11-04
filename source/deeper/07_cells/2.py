from sklearn.datasets import load_diabetes

# Mini-batch SGD on the diabetes data: constant learning rate vs a decaying schedule
Xd, yd = load_diabetes(return_X_y=True)
Xd = (Xd - Xd.mean(0)) / Xd.std(0); yd = (yd - yd.mean()) / yd.std()
w_best = np.linalg.lstsq(Xd, yd, rcond=None)[0]
best = np.mean((Xd @ w_best - yd) ** 2)

def sgd(schedule, epochs=60, batch=16, seed=0):
    rng = np.random.default_rng(seed); w = np.zeros(10); step = 0; tail = []
    for ep in range(epochs):
        for idx in np.array_split(rng.permutation(len(yd)), len(yd) // batch):
            g = 2 * Xd[idx].T @ (Xd[idx] @ w - yd[idx]) / len(idx)
            w -= schedule(step) * g; step += 1
        if ep >= epochs - 10: tail.append(np.mean((Xd @ w - yd) ** 2))
    return np.mean(tail) - best, np.std(tail)

for name, sch in [("constant 0.05", lambda t: 0.05),
                  ("decay 0.05/(1 + t/200)", lambda t: 0.05 / (1 + t / 200))]:
    gap, wobble = sgd(sch)
    print(f"{name:24}: extra loss above the best {gap:.4f}, wobble between epochs {wobble:.4f}")
