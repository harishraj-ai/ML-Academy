import numpy as np
rng = np.random.default_rng(5); n = 4000
g = rng.integers(0, 2, n)
# Group 1's benefit fades: hazard ratio 0.4 in the first 6 months, 1.0 afterwards.
t_early = rng.exponential(1 / (0.15 * np.where(g == 1, 0.4, 1.0)))
t = np.where(t_early < 6, t_early, 6 + rng.exponential(1 / 0.15, n))
e = (t < 24).astype(int); t = np.minimum(t, 24)
def hazard(grp, lo, hi):                       # events per month at risk, between months lo and hi
    m = g == grp
    events = ((e[m] == 1) & (t[m] >= lo) & (t[m] < hi)).sum()
    exposure = np.clip(np.minimum(t[m], hi) - lo, 0, None).sum()
    return events / exposure
for lo, hi in [(0, 6), (6, 24)]:
    print(f"months {lo}–{hi}: hazard ratio, group 1 vs group 0, {hazard(1, lo, hi) / hazard(0, lo, hi):.2f}")
