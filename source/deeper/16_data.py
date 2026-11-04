# Lesson 16 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("Alternatives to k-means and when to use them: Gaussian mixtures (stretched clusters with soft membership, "
          "fitted by the EM algorithm), DBSCAN and single-linkage clustering (any shape, plus outliers), "
          "hierarchical clustering (a tree of groupings), and how to choose the number of clusters with the "
          "silhouette score or BIC.")

QUIZ = [
    ("What does the E-step of EM compute for a Gaussian mixture?",
     [("a", "New cluster means"), ("b", "Each point's probability of belonging to each cluster"), ("c", "The number of clusters")], "b",
     "The E-step computes responsibilities; the M-step then updates the means, covariances and weights."),
    ("Which method can find two interlocking half-moon shapes?",
     [("a", "k-means"), ("b", "DBSCAN"), ("c", "Ward linkage")], "b",
     "DBSCAN follows dense connected regions; k-means and Ward prefer compact blobs."),
    ("A point's silhouette is near −1. What does that suggest?",
     [("a", "It's well clustered"), ("b", "It's probably in the wrong cluster"), ("c", "It's exactly between two clusters")], "b",
     "Its own cluster is farther away on average than the nearest other cluster."),
    ("For Gaussian mixtures, which $k$ does BIC prefer?",
     [("a", "The one with the lowest BIC"), ("b", "The one with the highest BIC"), ("c", "Always the largest")], "a",
     "BIC $= -2\\log L + p\\log n$: fit quality plus a penalty for parameters. Lower is better."),
    ("k-means can be seen as a special case of…",
     [("a", "EM for a Gaussian mixture with equal, round, tiny-variance clusters and hard assignments"), ("b", "DBSCAN"), ("c", "PCA")], "a",
     "With those assumptions the E-step becomes \"nearest centroid\" and the M-step becomes \"average of assigned points\"."),
]

IQ = [
    (3, "Compare k-means and Gaussian mixture models.",
     "Saying they're the same thing.",
     "Both alternate assignment and update steps. k-means makes hard assignments to the nearest centroid, assumes round clusters of similar size, and minimises within-cluster squared distance. A GMM makes soft probabilistic assignments, learns each cluster's covariance (stretched, tilted, different sizes) and maximises likelihood with EM. GMMs give uncertainty and a likelihood (so BIC can choose $k$), but have more parameters, can be unstable in high dimensions, and are slower."),
    (2, "When would you choose DBSCAN over k-means?",
     "Only saying \"for non-round clusters\".",
     "When clusters have arbitrary shapes, when you don't know the number of clusters, and when the data contains noise or outliers that shouldn't be forced into a cluster (DBSCAN labels them $-1$). Avoid it when cluster densities differ a lot (use HDBSCAN) or in high dimensions where distances concentrate (reduce dimensions first)."),
    (3, "How can you evaluate a clustering if you do have labels for a sample?",
     "Using accuracy directly.",
     "Cluster numbers are arbitrary, so use label-invariant measures: the adjusted Rand index (pairs of points grouped consistently, corrected for chance), normalised mutual information, or homogeneity and completeness. A score near 0 means chance-level agreement. Remember the labels may reflect only one of several valid ways to group the data."),
]

EX = [
    ("Intermediate", "A point's average distance to its own cluster is $a = 2$ and to the nearest other cluster is $b = 5$. What is its silhouette?",
     "$s = (5 - 2)/\\max(2, 5) = 3/5 = 0.6$."),
    ("Intermediate", "Two models are fitted to $n = 1000$ points. Model A has log-likelihood $-2400$ with 11 parameters; model B has $-2380$ with 17. Using $\\text{BIC} = -2\\log L + p\\ln n$, which is preferred?",
     "A: $4800 + 11\\ln 1000 = 4800 + 75.99 = 4875.99$. B: $4760 + 17 \\times 6.908 = 4760 + 117.43 = 4877.43$. A has the lower BIC, so it's preferred, narrowly: B's better fit doesn't quite justify 6 extra parameters."),
    ("Intermediate", "In the E-step, a point's weighted densities under three clusters are $0.02$, $0.06$ and $0.12$. What are its responsibilities?",
     "Divide by the total $0.20$: $(0.1, 0.3, 0.6)$."),
]

CHECKS = {
    0: [("Silhouette", 0.6, "(b − a) / max(a, b).")],
    1: [("BIC of A", 4875.99, "−2 log L + p ln n.", 0.1), ("BIC of B", 4877.43, "Same formula with p = 17.", 0.1)],
    2: [("Responsibilities", [0.1, 0.3, 0.6], "Divide each by the sum.")],
}
