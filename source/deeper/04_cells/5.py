# Bootstrap: a confidence interval for the median house price (simulated, lakh)
rng = np.random.default_rng(2)
prices = rng.lognormal(mean=4.2, sigma=0.5, size=60)
boot = [np.median(rng.choice(prices, size=len(prices), replace=True)) for _ in range(10000)]
print("sample median:", round(np.median(prices), 1))
print("95% bootstrap interval:", np.round(np.percentile(boot, [2.5, 97.5]), 1))
