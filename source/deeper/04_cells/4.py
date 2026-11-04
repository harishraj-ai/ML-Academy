# Central limit theorem: averages of a skewed variable become bell-shaped
rng = np.random.default_rng(1)
for n in [1, 5, 30, 200]:
    means = rng.exponential(scale=1.0, size=(50000, n)).mean(axis=1)
    print(f"n {n:3d}: skewness {stats.skew(means):5.2f}   spread of the means {means.std():.3f}   1/sqrt(n) {1 / np.sqrt(n):.3f}")
