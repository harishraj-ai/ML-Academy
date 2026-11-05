import numpy as np
from scipy import stats
rng = np.random.default_rng(1)
train = rng.normal(0, 1, 50000)
for n in [500, 5000, 50000]:
    live = rng.normal(0.03, 1, n)                                    # a tiny, harmless shift
    ks = stats.ks_2samp(train, live)
    edges = np.quantile(train, np.linspace(0, 1, 11)); edges[0], edges[-1] = -np.inf, np.inf
    e, a = np.histogram(train, edges)[0] / len(train), np.histogram(live, edges)[0] / n
    psi = float(np.sum((a - e) * np.log(a / e)))
    print(f"live sample {n:6d}: KS p-value {ks.pvalue:.3g}   PSI {psi:.4f}")
