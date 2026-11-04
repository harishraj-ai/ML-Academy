from sklearn.model_selection import GridSearchCV
search = GridSearchCV(DecisionTreeClassifier(random_state=0), {"ccp_alpha": path.ccp_alphas}, cv=5).fit(Xtr, ytr)
best = search.best_estimator_
print("alpha chosen by CV:", round(search.best_params_["ccp_alpha"], 4), " leaves:", best.get_n_leaves(), " test accuracy:", round(best.score(Xte, yte), 3))
