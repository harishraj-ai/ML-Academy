# Multiple testing: 20 features with no real effect, each tested at the 5% level, in 5,000 experiments
rng = np.random.default_rng(4)
groups = rng.normal(size=(5000, 20, 2, 30))              # two groups of 30, no true difference
p = stats.ttest_ind(groups[:, :, 0], groups[:, :, 1], axis=2).pvalue
print("share of single tests below 0.05:", round((p < 0.05).mean(), 3))
print("share of experiments with at least one 'significant' feature:", round((p < 0.05).any(axis=1).mean(), 3))
print("theory, 1 − 0.95^20:", round(1 - 0.95**20, 3))
print("with Bonferroni (p < 0.05/20):", round((p < 0.05 / 20).any(axis=1).mean(), 3))
