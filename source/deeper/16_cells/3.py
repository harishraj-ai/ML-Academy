# Choosing k without labels: silhouette score and the mixture's BIC
Xk, _ = make_blobs(n_samples=600, centers=4, cluster_std=1.0, random_state=7)
print(" k   silhouette   BIC")
for k in range(2, 8):
    lab = KMeans(k, n_init=10, random_state=0).fit_predict(Xk)
    bic = GaussianMixture(k, random_state=0).fit(Xk).bic(Xk)
    print(f"{k:2d}   {silhouette_score(Xk, lab):10.3f}   {bic:7.0f}")
