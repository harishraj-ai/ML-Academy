# For a linear model the exact SHAP value of feature j is w_j * (x_j - mean_j); averaging |SHAP| gives a global ranking
lin = LinearRegression().fit(X_tr, y_tr)
shap_vals = lin.coef_ * (X_te - X_tr.mean(axis=0))
print("weights (a, b, c):            ", lin.coef_.round(2))
print("mean |SHAP| per feature:      ", np.abs(shap_vals).mean(axis=0).round(3))
print("check, first row: baseline + contributions", round(lin.predict(X_tr).mean() + shap_vals[0].sum(), 4), "vs prediction", round(lin.predict(X_te[:1])[0], 4))
