# Inverted dropout: drop units with probability p during training and scale the rest by 1/(1−p)
p = 0.5
h = np.ones(100000)
mask = rng.random(h.shape) > p
train_out = h * mask / (1 - p)
print("share of units kept:", round(mask.mean(), 3), "  average activation, training:", round(train_out.mean(), 3), "  at prediction time (no dropout):", h.mean())

# Batch normalisation: standardise each feature over the batch, then rescale with learned gamma and beta
z = rng.normal(5, 3, size=(64, 4))
gamma, beta = np.array([1.0, 2.0, 1.0, 0.5]), np.array([0.0, 1.0, -1.0, 0.0])
bn = gamma * (z - z.mean(0)) / np.sqrt(z.var(0) + 1e-5) + beta
print("after batch norm, per-feature mean:", (bn.mean(0).round(3) + 0.0), " std:", bn.std(0).round(3))
