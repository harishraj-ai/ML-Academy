import numpy as np

# Two groups with different base rates; a model whose scores are perfectly calibrated in both groups
rng = np.random.default_rng(0)
def make_group(n, a, b):
    risk = rng.beta(a, b, n)                 # each person's true probability
    return risk, (rng.random(n) < risk).astype(int)
groups = {"group A": make_group(20000, 2, 5), "group B": make_group(20000, 4, 4)}

print("group     base rate   calibration (pred 0.6–0.7: actual)   TPR     FPR     PPV")
for g, (score, y) in groups.items():
    flag = score >= 0.5
    sel = (score >= 0.6) & (score < 0.7)
    tpr = flag[y == 1].mean(); fpr = flag[y == 0].mean(); ppv = y[flag].mean()
    print(f"{g:8}   {y.mean():9.3f}   {y[sel].mean():33.3f}   {tpr:.3f}   {fpr:.3f}   {ppv:.3f}")
