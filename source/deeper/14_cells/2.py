from sklearn.ensemble import HistGradientBoostingClassifier

for lr in [1.0, 0.3, 0.1, 0.03]:
    gb = HistGradientBoostingClassifier(learning_rate=lr, max_iter=2000, early_stopping=True,
                                        validation_fraction=0.2, n_iter_no_change=30, random_state=0).fit(Xtr, ytr)
    print(f"learning rate {lr:4}: trees used {gb.n_iter_:4d}   test accuracy {gb.score(Xte, yte):.3f}")
