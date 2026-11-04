Xm, ym = make_moons(n_samples=500, noise=0.06, random_state=0)
results = {
    "k-means":            KMeans(2, n_init=10, random_state=0).fit_predict(Xm),
    "Gaussian mixture":   GaussianMixture(2, random_state=0).fit(Xm).predict(Xm),
    "DBSCAN":             DBSCAN(eps=0.2, min_samples=5).fit_predict(Xm),
    "agglomerative, single linkage": AgglomerativeClustering(2, linkage="single").fit_predict(Xm),
    "agglomerative, Ward linkage":   AgglomerativeClustering(2, linkage="ward").fit_predict(Xm),
}
for name, lab in results.items():
    print(f"{name:30}: ARI {adjusted_rand_score(ym, lab):.3f}")
