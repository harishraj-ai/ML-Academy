from sklearn.inspection import permutation_importance

# Add a column of pure noise with many distinct values (like an ID number)
rng = np.random.default_rng(0)
Xn_tr = np.column_stack([Xtr, rng.permutation(len(ytr))])
Xn_te = np.column_stack([Xte, rng.permutation(len(yte))])
tree = DecisionTreeClassifier(random_state=0).fit(Xn_tr, ytr)
imp = tree.feature_importances_
perm = permutation_importance(tree, Xn_te, yte, n_repeats=30, random_state=0).importances_mean
print("noise column: impurity importance", round(imp[-1], 3), " rank", int((imp > imp[-1]).sum()) + 1, "of 31")
print("noise column: permutation importance on test data", round(perm[-1], 3))
