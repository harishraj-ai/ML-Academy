# Lesson 17 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("How to decide how many components to keep (variance kept and reconstruction error), kernel PCA for "
          "curved structure, and t-SNE and UMAP maps: what they keep (neighbourhoods), what they don't (distances "
          "between clusters, cluster sizes), and why they're for looking at data rather than for model features.")

QUIZ = [
    ("PCA with $k$ components keeps 93% of the variance. What is the relative reconstruction error?",
     [("a", "0.93"), ("b", "0.07"), ("c", "It can't be known")], "b",
     "The reconstruction error equals the variance in the dropped components: $1 - 0.93 = 0.07$."),
    ("Why can kernel PCA separate concentric circles when PCA can't?",
     [("a", "It finds principal components in a kernel feature space, where the curved structure becomes straight"), ("b", "It uses more data"), ("c", "It standardises the features")], "a",
     "It's PCA plus the kernel trick."),
    ("In a t-SNE map, two clusters are far apart. You can conclude that…",
     [("a", "They're very different in the original space"), ("b", "Not much: t-SNE preserves neighbourhoods, not distances between clusters"), ("c", "They have different sizes")], "b",
     "Global distances and cluster sizes on a t-SNE map are not reliable."),
    ("What does t-SNE's perplexity roughly control?",
     [("a", "The number of output dimensions"), ("b", "How many neighbours each point pays attention to"), ("c", "The learning rate")], "b",
     "Low perplexity focuses on very local structure; high perplexity on broader structure."),
    ("Which method should you use to create features for a downstream model?",
     [("a", "t-SNE"), ("b", "PCA (inside a pipeline)"), ("c", "Neither")], "b",
     "PCA has a <code>transform</code> for new data and stable, meaningful axes; t-SNE is for visualisation."),
]

IQ = [
    (3, "How do you choose the number of principal components?",
     "\"Always keep 95%.\"",
     "Look at the cumulative explained-variance curve and the reconstruction error (they're the same information: error = variance dropped). A variance threshold (90–99%) or an elbow is a reasonable start. When PCA feeds a model, the best answer is to treat $k$ as a hyperparameter and pick it by cross-validating the whole pipeline. For visualisation, 2 or 3 components, accepting that much variance is lost."),
    (2, "What are the main pitfalls of interpreting t-SNE plots?",
     "Reading cluster distances and sizes as meaningful.",
     "t-SNE preserves local neighbourhoods, so between-cluster distances and cluster sizes are unreliable; results depend on perplexity and the random seed; noise can look clustered at low perplexity; and the axes mean nothing. Try several settings, colour by known labels, and confirm structure with other methods. It has no out-of-sample transform, so don't use it to create model features."),
    (3, "How can PCA be used for anomaly detection?",
     "Only mentioning dimensionality reduction.",
     "Fit PCA on normal data and keep enough components to describe typical variation. For each new point, project and reconstruct it; the reconstruction error measures how badly it fits the usual pattern. A threshold on that error (chosen on validation data) flags anomalies. It works well when normal data really does lie near a lower-dimensional subspace."),
]

EX = [
    ("Intermediate", "Eigenvalues of a covariance matrix are $5, 3, 1.5, 0.3, 0.2$. What fraction of the variance do 2 components keep, and how many are needed for at least 95%?",
     "Total $= 10$. Two components: $8/10 = 0.8$. Three: $9.5/10 = 0.95$, so 3 components are needed."),
    ("Intermediate", "With the eigenvalues above, what is the relative reconstruction error with 3 components?",
     "The dropped variance: $(0.3 + 0.2)/10 = 0.05$."),
    ("Code · intermediate", "Using the digits code, keep enough components for 90% of the variance with <code>PCA(0.90)</code>. How many components does it choose?",
     "<code>PCA(0.90).fit(X).n_components_</code> gives 21 components (from 64 pixels)."),
]

CHECKS = {
    0: [("Fraction kept by 2 components", 0.8, "Sum of the top 2 eigenvalues ÷ total."), ("Components needed for 95%", 3, "Add eigenvalues until you reach 95%.")],
    1: [("Relative reconstruction error", 0.05, "Dropped eigenvalues ÷ total.")],
    2: [("Components for 90%", 21, "Read n_components_.")],
}
