# Algorithm decision guide: a small question tree. Questions -> options -> next node; leaves are recommendations.
# Inspired by scikit-learn's "Choosing the right estimator" flowchart (same questions and sample-size thresholds),
# simplified for beginners and mapped to the lessons of this course.
Q = {
 "start": ("What do you want the model to do?", "Start from the question you want answered, not from an algorithm.", [
    ("Predict a number", "a price, a temperature, next month's sales", "reg_type"),
    ("Predict a category", "spam or not, which digit, will the customer leave", "cls_type"),
    ("Find groups in data without labels", "customer segments, similar documents", "clu_k"),
    ("Simplify or visualise many features", "too many columns, or you want a 2D picture", "dim_why"),
 ]),
 "cls_type": ("What does each example look like?", "The type of input matters more than anything else.", [
    ("A row in a table", "numbers and categories in columns", "cls_n"),
    ("Text", "emails, reviews, support tickets", "cls_text"),
    ("Images, audio or video", "raw pixels or sound waves", "R_deep"),
 ]),
 "cls_n": ("How many labelled examples do you have?", "scikit-learn's flowchart uses 50 and 100,000 as rough thresholds.", [
    ("Fewer than 50", "", "R_more_data"),
    ("50 to 100,000", "", "cls_explain"),
    ("More than 100,000", "", "R_cls_big"),
 ]),
 "cls_explain": ("Must people understand why each prediction was made?", "Loans, medicine and hiring often require an explanation.", [
    ("Yes, it must be explainable", "", "R_cls_explain"),
    ("No, accuracy matters most", "", "R_cls_tab"),
 ]),
 "cls_text": ("How much labelled text do you have?", "", [
    ("Up to a few thousand documents", "", "R_text_small"),
    ("Lots, or the meaning is subtle", "sarcasm, long documents, many languages", "R_text_big"),
 ]),
 "reg_type": ("What does each example look like?", "", [
    ("A row in a table", "numbers and categories in columns", "reg_n"),
    ("Images, audio or text", "", "R_deep"),
 ]),
 "reg_n": ("How many examples do you have?", "", [
    ("Fewer than 50", "", "R_more_data"),
    ("50 to 100,000", "", "reg_few"),
    ("More than 100,000", "", "R_reg_big"),
 ]),
 "reg_few": ("Do you expect only a few of the features to really matter?", "For example, 200 measured columns but probably only a handful drive the result.", [
    ("Yes, only a few", "", "R_reg_sparse"),
    ("No, or not sure", "", "R_reg_tab"),
 ]),
 "clu_k": ("Do you know roughly how many groups there should be?", "", [
    ("Yes", "e.g. 'three customer tiers'", "clu_shape"),
    ("No", "", "clu_noise"),
 ]),
 "clu_shape": ("Are the groups likely to be round blobs of similar size?", "Plot two features first if you can.", [
    ("Yes, or I can't tell", "", "R_kmeans"),
    ("No — odd shapes, or very different sizes", "", "R_dbscan"),
 ]),
 "clu_noise": ("Does the data contain outliers or odd shapes?", "", [
    ("Yes", "", "R_dbscan"),
    ("No / not sure — and the dataset is small (< 10,000)", "", "R_hier"),
    ("No / not sure — and the dataset is large", "", "R_kmeans_scan"),
 ]),
 "dim_why": ("Why do you want fewer dimensions?", "", [
    ("To feed a model: fewer, uncorrelated features", "", "R_pca"),
    ("To draw a 2D picture and look for structure", "", "R_tsne"),
 ]),
}
# result: title, [(model, lesson, why)], [lessons to read], watch-out
R = {
 "R_more_data": ("Collect more data first", [("A simple baseline (mean / most common class)", 5, "With under 50 examples, no algorithm can learn reliably — and you can't even measure it reliably."),
                 ("Then the simplest model: linear or logistic regression", 6, "Few parameters means less overfitting.")],
                 [1, 5], "Use leave-one-out cross-validation to evaluate; treat any result as a rough estimate."),
 "R_cls_explain": ("Logistic regression or a small decision tree", [("Logistic regression", 8, "Each weight shows how a feature pushes the odds up or down."),
                 ("Decision tree (limited depth)", 13, "Gives readable if-then rules."),
                 ("Then: random forest + feature importances", 14, "If you need more accuracy, check whether it's worth losing some explainability.")],
                 [8, 9, 13], "Check precision and recall, not just accuracy — especially if one class is rare."),
 "R_cls_tab": ("Start simple, then try tree ensembles", [("Baseline: logistic regression", 8, "Fast, and tells you how much a fancier model really adds."),
                 ("Random forest", 14, "Strong with almost no tuning."),
                 ("Gradient boosting", 14, "Usually the most accurate on tables, with tuning."),
                 ("Also worth a try: SVM (RBF kernel) or kNN", 15, "Good on small-to-medium data once features are scaled (kNN: Lesson 11).")],
                 [5, 8, 9, 14], "Compare all candidates with the same cross-validation folds and metric (Lessons 5 and 9)."),
 "R_cls_big": ("Models that scale to big data", [("Logistic regression with SGD", 7, "Learns from mini-batches, so data size isn't a problem."),
                 ("Gradient boosting (LightGBM / XGBoost)", 14, "Fast, scalable libraries; often the top choice for big tables."),
                 ("Neural network", 18, "Worth it when there are many complex feature interactions.")],
                 [7, 14, 18], "With lots of data, a simple hold-out validation set is usually enough."),
 "R_text_small": ("Naive Bayes or logistic regression on word counts", [("Naive Bayes", 12, "Classic fast baseline for text; works with little data."),
                 ("Logistic regression on TF-IDF features (word counts, down-weighted for very common words)", 8, "Usually a bit more accurate once you have more examples.")],
                 [12, 8, 20], "Fit the vocabulary (CountVectorizer) inside a pipeline so test text never leaks into training (Lesson 20)."),
 "R_text_big": ("Fine-tune a pretrained Transformer", [("Pretrained language model (Transformer)", 19, "Already understands language; you only adapt it to your labels."),
                 ("Keep a word-count + logistic regression baseline", 8, "Shows how much the big model actually adds.")],
                 [12, 19], "Training a Transformer from scratch needs enormous data — fine-tune instead."),
 "R_deep": ("Deep learning — usually starting from a pretrained network", [("Images: convolutional network (CNN)", 19, "Learns edges, textures and shapes from pixels."),
                 ("Text or sequences: Transformer", 19, "Handles word order and long-range context."),
                 ("Fine-tuning a pretrained model", 19, "Needs far less data and compute than training from scratch.")],
                 [18, 19], "Deep learning needs a GPU and plenty of data; check whether a pretrained model already solves your task."),
 "R_reg_sparse": ("Lasso (or elastic net)", [("Lasso regression", 10, "Sets the weights of unhelpful features to exactly zero."),
                 ("Elastic net", 10, "Mixes lasso and ridge; more stable when features are correlated.")],
                 [6, 10], "Standardise features first, and choose the penalty strength by cross-validation."),
 "R_reg_tab": ("Ridge regression, then tree ensembles", [("Baseline: linear / ridge regression", 10, "Fast, explainable, and hard to beat when relationships are roughly linear."),
                 ("Random forest regressor", 14, "Captures non-linear effects and interactions automatically."),
                 ("Gradient boosting regressor", 14, "Often the most accurate on tables."),
                 ("Also worth a try: SVR (RBF kernel) or kNN regression", 15, "Good on small data once features are scaled (kNN: Lesson 11).")],
                 [6, 10, 14], "Report MAE or RMSE in the target's own units so the error is easy to interpret."),
 "R_reg_big": ("Models that scale to big data", [("Linear regression with SGD", 7, "Learns in mini-batches."),
                 ("Gradient boosting (LightGBM / XGBoost)", 14, "Scales well and handles non-linear patterns."),
                 ("Neural network", 18, "For very large, complex problems.")],
                 [7, 14], "Scale numeric features for SGD and neural networks (Lesson 20)."),
 "R_kmeans": ("k-means", [("k-means (with k-means++ starts)", 16, "Fast and simple; finds round clusters around centres."),
                 ("MiniBatchKMeans for millions of points", 16, "scikit-learn's version that updates the centroids from small random batches — much faster, nearly as good.")],
                 [16, 2], "Scale features first, try several values of k, and check them with the elbow method or silhouette score."),
 "R_kmeans_scan": ("k-means over a range of k", [("k-means for k = 2 … 10", 16, "Pick k with the elbow method or the silhouette score."),
                 ("Then inspect the clusters", 16, "Do they make sense to someone who knows the data?")],
                 [16], "There's no 'correct' answer in clustering — judge clusters by whether they're useful."),
 "R_dbscan": ("DBSCAN", [("DBSCAN", 16, "Follows dense regions of any shape and labels sparse points as noise."),
                 ("Tune eps by trying a few values", 16, "Too small and most points become noise; too large and clusters merge. scikit-learn's default min_samples = 5 is a fair start.")],
                 [16], "DBSCAN struggles when clusters have very different densities."),
 "R_hier": ("Hierarchical clustering", [("Agglomerative clustering + dendrogram", 16, "Shows every level of grouping; cut the tree where the gaps are largest."),
                 ("Compare with k-means at the k you pick", 16, "A second opinion on the same data.")],
                 [16], "Memory grows with the square of the number of points — fine for thousands, not millions."),
 "R_pca": ("PCA", [("PCA (keep ~95% of the variance)", 17, "Fast, linear, and the same transform works on new data."),
                 ("Or: lasso / feature selection", 10, "If you'd rather keep original, explainable features.")],
                 [17, 20], "Standardise first, and fit PCA only on the training data (inside a pipeline)."),
 "R_tsne": ("PCA first, then t-SNE or UMAP", [("PCA to ~50 dimensions", 17, "Removes noise and speeds up the next step."),
                 ("t-SNE (or UMAP) to 2D", 17, "Places similar points close together, so clusters become visible.")],
                 [17], "Distances between t-SNE clusters and their sizes mean little; use it for looking, not as model input."),
}
GUIDE_SOURCES = [("scikit-learn — Choosing the right estimator", "https://scikit-learn.org/stable/machine_learning_map.html"),
                 ("scikit-learn — User guide", "https://scikit-learn.org/stable/user_guide.html"),
                 ("Google — Rules of Machine Learning", "https://developers.google.com/machine-learning/guides/rules-of-ml")]

if __name__ == "__main__":
    seen = set()
    def walk(k):
        if k in R: seen.add(k); return
        for _, _, nx in Q[k][2]: assert nx in Q or nx in R, nx; walk(nx)
    walk("start"); print(len(Q), "questions;", len(seen), "of", len(R), "results reachable", set(R) - seen)
