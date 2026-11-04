# Maximum likelihood for a coin: 7 heads in 10 flips
p_grid = np.linspace(0.01, 0.99, 99)
loglik = 7 * np.log(p_grid) + 3 * np.log(1 - p_grid)
print("p with the highest likelihood:", round(p_grid[np.argmax(loglik)], 2))

# MLE for a normal distribution divides by n, which underestimates the variance
rng = np.random.default_rng(0)
samples = rng.normal(0, 2, size=(100000, 5))            # 100,000 small samples, true variance 4
print("average variance, divide by n:    ", round(samples.var(axis=1, ddof=0).mean(), 3))
print("average variance, divide by n − 1:", round(samples.var(axis=1, ddof=1).mean(), 3))
