# Bayesian updating: prior Beta(2, 2), then observe 7 heads and 3 tails
a, b = 2 + 7, 2 + 3
post = stats.beta(a, b)
print(f"posterior: Beta({a}, {b})")
print("posterior mean:", round(post.mean(), 3), " MAP (most likely value):", round((a - 1) / (a + b - 2), 3))
print("95% credible interval:", np.round(post.ppf([0.025, 0.975]), 3))
