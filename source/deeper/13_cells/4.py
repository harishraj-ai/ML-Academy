# Instability: which feature does the root split use on bootstrap samples?
names = load_breast_cancer().feature_names
roots = {}
for _ in range(100):
    i = rng.integers(0, len(ytr), len(ytr))
    r = names[DecisionTreeClassifier(random_state=0).fit(Xtr[i], ytr[i]).tree_.feature[0]]
    roots[str(r)] = roots.get(str(r), 0) + 1
print(sorted(roots.items(), key=lambda kv: -kv[1]))
