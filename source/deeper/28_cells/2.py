import numpy as np
data = np.array([2.9, 3.1, 2.4, 3.3, 2.7, 8.5, 2.8])
def log_post(m):
    return -np.sum(np.log1p((data - m) ** 2)) - m ** 2 / 200       # Cauchy likelihood, wide normal prior
def chain(start, step, n=4000, seed=0):
    rng, m, out = np.random.default_rng(seed), start, []
    for _ in range(n):
        prop = m + rng.normal(0, step)
        if np.log(rng.random()) < log_post(prop) - log_post(m):
            m = prop
        out.append(m)
    return np.array(out[n // 2:])                                    # drop the first half as warm-up
def r_hat(chains):
    c = np.array(chains); n = c.shape[1]
    W, B = c.var(axis=1, ddof=1).mean(), n * c.mean(axis=1).var(ddof=1)
    return np.sqrt(((n - 1) / n * W + B / n) / W)
for step in [0.5, 0.005]:
    chains = [chain(s, step, seed=i) for i, s in enumerate([-10, 0, 10, 20])]
    print("step", step, " chain means", [round(float(c.mean()), 2) for c in chains], " R-hat", round(float(r_hat(chains)), 2))
