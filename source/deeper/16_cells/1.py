import numpy as np
from sklearn.datasets import make_blobs, make_moons
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import adjusted_rand_score, silhouette_score

# Stretched clusters: k-means assumes round blobs, a Gaussian mixture doesn't
Xb, yb = make_blobs(n_samples=600, centers=3, random_state=170)
Xs = Xb @ np.array([[0.6, -0.6], [-0.4, 0.8]])          # stretch and shear the blobs
km = KMeans(3, n_init=10, random_state=0).fit_predict(Xs)
gmm = GaussianMixture(3, covariance_type="full", random_state=0).fit(Xs)
print("stretched blobs: ARI k-means", round(adjusted_rand_score(yb, km), 3), "  ARI Gaussian mixture", round(adjusted_rand_score(yb, gmm.predict(Xs)), 3))
p = gmm.predict_proba(Xs)
print("share of points the mixture is unsure about (max probability < 0.9):", round(np.mean(p.max(axis=1) < 0.9), 3))
