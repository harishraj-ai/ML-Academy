from scipy import stats

# McNemar's test: do the two models make different numbers of mistakes on the SAME cases?
right_lr, right_tr = logreg.predict(Xte) == yte, tree.predict(Xte) == yte
b = np.sum(right_lr & ~right_tr)          # logistic right, tree wrong
c = np.sum(~right_lr & right_tr)          # tree right, logistic wrong
print("accuracy: logistic", round(right_lr.mean(), 3), " tree", round(right_tr.mean(), 3))
print("cases only logistic got right:", b, "  only the tree got right:", c)
print("McNemar exact p-value:", round(stats.binomtest(b, b + c, 0.5).pvalue, 4))
