from sklearn.manifold import TSNE
from sklearn.neighbors import KNeighborsClassifier

# Compare 2-D maps: how well do a point's map neighbours share its digit label?
maps = {"PCA, 2-D": PCA(2).fit_transform(X),
        "t-SNE, 2-D": TSNE(2, perplexity=30, random_state=0, init="pca").fit_transform(X)}
for name, Z in maps.items():
    acc = cross_val_score(KNeighborsClassifier(5), Z, y, cv=5).mean()
    print(f"{name:10}: 5-nearest-neighbour accuracy in the map {acc:.3f}")
