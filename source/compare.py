# Side-by-side comparison pages. Every illustration is computed here with real models.
import os, warnings
import numpy as np, pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.datasets import make_moons, load_digits
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from walks import T, axes
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(HERE, "data", "houses.csv"))

def svg(w, h, body, label):
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'

FACTS = {}

# 1 ---- linear vs logistic (Chennai Homes)
def fig_lin_log():
    x, y = df["size_m2"].to_numpy(float), df["price_lakh"].to_numpy(float)
    m = LinearRegression().fit(x[:, None], y)
    d, s = df["dist_km"].to_numpy(float), df["sold_fast"].to_numpy()
    lg = LogisticRegression().fit(d[:, None], s)
    FACTS["linlog"] = (m.coef_[0], m.intercept_, lg.coef_[0][0], lg.intercept_[0])
    px = lambda v: 50 + (v - 40) * 1.6; py = lambda v: 246 - (v - 30) * 2.6
    L = axes(px, py, 40, 200, 30, 110, [50, 100, 150, 200], [40, 60, 80, 100], "size (m²)", "price (lakh)")
    L += "".join(f'<circle cx="{px(a):.1f}" cy="{py(b):.1f}" r="5" class="wp1"/>' for a, b in zip(x, y))
    L += f'<line x1="{px(40):.1f}" y1="{py(m.predict([[40]])[0]):.1f}" x2="{px(200):.1f}" y2="{py(m.predict([[200]])[0]):.1f}" class="la"/>'
    L += T(178, 14, "Linear regression: a number", "t h", "c")
    qx = lambda v: 360 + v * 10.5; qy = lambda v: 246 - v * 180
    R = f'<line x1="{qx(0)}" y1="{qy(0)}" x2="{qx(25)}" y2="{qy(0)}" class="ax"/><line x1="{qx(0)}" y1="{qy(0)}" x2="{qx(0)}" y2="{qy(1.05):.1f}" class="ax"/>'
    for v in (0, 5, 10, 15, 20, 25): R += T(qx(v), 262, str(v), "t s", "c")
    for v in (0, 0.5, 1): R += T(qx(0) - 6, qy(v) + 4, f"{v:g}", "t s", "e")
    R += T(qx(12.5), 278, "distance to centre (km)", "t s", "c") + T(qx(0) - 30, qy(1.05) - 8, "P(sold fast)", "t s")
    R += f'<line x1="{qx(0)}" y1="{qy(.5):.1f}" x2="{qx(25)}" y2="{qy(.5):.1f}" class="dash"/>'
    R += "".join(f'<circle cx="{qx(a):.1f}" cy="{qy(b):.1f}" r="5" class="wp{b}"/>' for a, b in zip(d, s))
    xs = np.linspace(0, 25, 80); ps = lg.predict_proba(xs[:, None])[:, 1]
    R += '<polyline points="' + " ".join(f"{qx(a):.1f},{qy(b):.1f}" for a, b in zip(xs, ps)) + '" class="lv" fill="none"/>'
    R += T(491, 14, "Logistic regression: a probability", "t h", "c")
    return svg(640, 288, L + R, "Linear regression fits a straight line to prices; logistic regression fits an S-curve of probabilities")

# 2 ---- ridge vs lasso coefficient paths (Chennai Homes)
def fig_ridge_lasso():
    cols = ["size_m2", "bedrooms", "dist_km", "age_yrs"]
    Z = StandardScaler().fit_transform(df[cols]); y = df["price_lakh"].to_numpy(float)
    al = np.logspace(-2, 2, 40)
    rp = np.array([Ridge(alpha=a).fit(Z, y).coef_ for a in al * 3])
    lp = np.array([Lasso(alpha=a, max_iter=100000).fit(Z, y).coef_ for a in al])
    FACTS["rl"] = (rp[-1].round(2), lp[-1].round(2), [int(np.argmax(np.abs(lp[:, j]) < 1e-9)) for j in range(4)])
    lo, hi = min(rp.min(), lp.min()) - 1, max(rp.max(), lp.max()) + 1
    out = ""
    names = ["size", "bedrooms", "distance", "age"]; cls = ["la", "lv", "lw", "lv2"]
    for k, (P, title, x0) in enumerate([(rp, "Ridge (L2): shrinks, never exactly 0", 50), (lp, "Lasso (L1): switches features off", 370)]):
        px = lambda i, x0=x0: x0 + i * 6.2; py = lambda v: 30 + (hi - v) / (hi - lo) * 200
        out += f'<line x1="{px(0)}" y1="{py(0):.1f}" x2="{px(39):.1f}" y2="{py(0):.1f}" class="dash"/>'
        out += f'<line x1="{px(0)}" y1="230" x2="{px(39):.1f}" y2="230" class="ax"/><line x1="{px(0)}" y1="230" x2="{px(0)}" y2="30" class="ax"/>'
        out += T(px(0), 18, title, "t h") + T(px(19.5), 248, "penalty strength →", "t s", "c")
        for v in (-10, 0, 10): out += T(px(0) - 5, py(v) + 4, str(v), "t s", "e")
        for j in range(4):
            out += '<polyline points="' + " ".join(f"{px(i):.1f},{py(P[i, j]):.1f}" for i in range(40)) + f'" class="{cls[j]}" fill="none"/>'
    out += "".join(f'<line x1="{60 + j * 140}" y1="266" x2="{84 + j * 140}" y2="266" class="{cls[j]}"/>' + T(90 + j * 140, 270, names[j], "t s") for j in range(4))
    return svg(640, 280, out, "Coefficient paths: ridge weights shrink smoothly towards zero, lasso weights hit exactly zero one by one")

# 3 ---- bagging vs boosting schematic
def fig_bag_boost():
    def bx(x, y, w, h, t, c="b"): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" class="{c}"/>' + T(x + w / 2, y + h / 2 + 5, t, "t", "c")
    a = lambda x1, y1, x2, y2: f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="ln" marker-end="url(#ah)"/>'
    s = '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="fa"/></marker></defs>'
    s += T(20, 20, "Bagging (e.g. random forest): in parallel", "t h")
    s += bx(20, 90, 80, 40, "Data")
    for i in range(3):
        y = 40 + i * 50
        s += a(100, 110, 140, y + 18) + bx(145, y, 110, 36, f"sample {i + 1}", "b") + a(255, y + 18, 285, y + 18) + bx(290, y, 70, 36, f"tree {i + 1}", "b2") + a(360, y + 18, 400, 110)
    s += bx(405, 90, 110, 40, "vote / average", "b3")
    s += T(20, 222, "Boosting (e.g. gradient boosting): in sequence", "t h")
    for i in range(4):
        x = 20 + i * 150
        s += bx(x, 240, 100, 40, f"tree {i + 1}", "b2")
        if i < 3: s += a(x + 100, 260, x + 148, 260) + T(x + 124, 300, "fix errors", "t s", "c")
    s += T(20, 330, "Each new tree is trained on what the trees before it still got wrong; the final model adds them all up.", "t s")
    return svg(640, 340, s, "Bagging trains independent trees on random samples and votes; boosting trains trees one after another, each correcting the previous ones")

# 4 ---- k-means vs DBSCAN on moons
def fig_km_db():
    X, _ = make_moons(n_samples=200, noise=0.06, random_state=0)
    X = np.vstack([X, [[-1.1, 1.1], [2.2, 1.0], [0.5, -0.7], [-0.9, -0.5], [1.6, 1.15]]])   # five stray points
    km = KMeans(n_clusters=2, n_init=10, random_state=0).fit_predict(X)
    db = DBSCAN(eps=0.2, min_samples=5).fit_predict(X)
    FACTS["kmdb"] = (len(set(db) - {-1}), int((db == -1).sum()))
    out = ""
    for k, (lab, title, x0) in enumerate([(km, "k-means (k = 2): cuts straight across", 20), (db, "DBSCAN: follows the dense shapes", 340)]):
        px = lambda v, x0=x0: x0 + 20 + (v + 1.2) * 85; py = lambda v: 230 - (v + 0.75) * 100
        out += T(x0, 20, title, "t h")
        out += "".join(f'<circle cx="{px(a):.1f}" cy="{py(b):.1f}" r="3.6" class="{"wn" if l == -1 else "wc" + str(l)}"/>' for (a, b), l in zip(X, lab))
    return svg(640, 240, out, "On two interleaving half-moons, k-means splits the data with a straight boundary while DBSCAN recovers each moon")

# 5 ---- PCA vs t-SNE on digits
def fig_pca_tsne():
    d = load_digits(); keep = np.isin(d.target, [0, 1, 4, 7]); X, y = d.data[keep], d.target[keep]
    lab = np.searchsorted([0, 1, 4, 7], y)
    P = PCA(n_components=2).fit_transform(X)
    S = TSNE(n_components=2, random_state=0, init="pca", perplexity=30).fit_transform(X)
    FACTS["pt"] = (len(y),)
    out = ""
    for k, (E, title, x0) in enumerate([(P, "PCA: a linear projection", 20), (S, "t-SNE: keeps neighbours together", 340)]):
        mn, mx = E.min(0), E.max(0)
        px = lambda v, x0=x0, mn=mn, mx=mx: x0 + 15 + (v - mn[0]) / (mx[0] - mn[0]) * 270
        py = lambda v, mn=mn, mx=mx: 225 - (v - mn[1]) / (mx[1] - mn[1]) * 190
        out += T(x0, 20, title, "t h")
        out += "".join(f'<circle cx="{px(a):.1f}" cy="{py(b):.1f}" r="2.6" class="wc{l}"/>' for (a, b), l in zip(E, lab))
    out += "".join(f'<circle cx="{200 + j * 70}" cy="252" r="5" class="wc{j}"/>' + T(210 + j * 70, 256, f"digit {dgt}", "t s") for j, dgt in enumerate([0, 1, 4, 7]))
    return svg(640, 265, out, "Handwritten digits projected to 2D: PCA overlaps the classes, t-SNE separates them into tight groups")

FIGS = {"linear-vs-logistic": fig_lin_log(), "ridge-vs-lasso": fig_ridge_lasso(), "bagging-vs-boosting": fig_bag_boost(),
        "kmeans-vs-dbscan": fig_km_db(), "pca-vs-tsne": fig_pca_tsne()}

a_, b_, c_, d_ = FACTS["linlog"]
CAPS = {
 "linear-vs-logistic": f"Chennai Homes. Left: price against size, fitted line price = {a_:.3f}·size + {b_:.1f}. Right: sold fast (1) or not (0) against distance, with the logistic curve; it crosses 50% at {-d_ / c_:.1f} km.",
 "ridge-vs-lasso": "Chennai Homes, four standardised features. As the penalty grows (left to right), ridge shrinks all four weights smoothly; lasso drives them to exactly zero one at a time.",
 "bagging-vs-boosting": "Bagging builds independent models and combines them; boosting builds each model to repair the previous ones.",
 "kmeans-vs-dbscan": f"200 points in two half-moons (scikit-learn's make_moons) plus 5 stray points. k-means puts every point in a cluster; DBSCAN (eps = 0.2, min_samples = 5) found {FACTS['kmdb'][0]} clusters and marked {FACTS['kmdb'][1]} points as noise (grey).",
 "pca-vs-tsne": f"{FACTS['pt'][0]} handwritten digits (0, 1, 4, 7) from scikit-learn's digits dataset, 64 pixels each, squeezed to 2D.",
}

# id, title, one-line core difference, (A name, B name), rows [(aspect, A, B)], choose A, choose B, lessons
COMPARE = [
 ("linear-vs-logistic", "Linear regression vs logistic regression",
  "Same recipe — a weighted sum of the features — but linear regression outputs that number directly, while logistic regression squashes it into a probability between 0 and 1.",
  ("Linear regression", "Logistic regression"),
  [("Task", "Regression: predict a number", "Classification: predict a class (via a probability)"),
   ("Model", "$\\hat{y} = \\mathbf{w}\\cdot\\mathbf{x} + b$", "$p = \\sigma(\\mathbf{w}\\cdot\\mathbf{x} + b)$"),
   ("Output range", "Any real number", "Between 0 and 1"),
   ("Loss it minimises", "Mean squared error", "Log loss (cross-entropy)"),
   ("How it's solved", "Exact formula (normal equation) or gradient descent", "Gradient descent only — no closed-form answer"),
   ("Reading a weight", "Change in $y$ per unit of the feature", "Change in log-odds; $e^{w}$ multiplies the odds"),
   ("Typical metrics", "MAE, RMSE, $R^2$", "Accuracy, precision, recall, ROC AUC, log loss"),
   ("Chennai Homes", "Price from size, distance and age", "Will it sell within 30 days?")],
  "the answer is a quantity: a price, a temperature, a number of sales.",
  "the answer is a category, or you need a probability to set your own threshold.",
  [6, 7, 8, 9]),
 ("ridge-vs-lasso", "Ridge (L2) vs lasso (L1) regularisation",
  "Both add a penalty on large weights to fight overfitting. Ridge penalises squared weights and shrinks them all; lasso penalises absolute weights and sets some exactly to zero.",
  ("Ridge (L2)", "Lasso (L1)"),
  [("Penalty added to the loss", "$\\lambda\\sum_j w_j^2$", "$\\lambda\\sum_j |w_j|$"),
   ("Effect on weights", "All shrink towards 0, none become exactly 0", "Many become exactly 0"),
   ("Feature selection", "No — keeps every feature", "Yes — automatically drops weak features"),
   ("Correlated features", "Shares the weight between them", "Tends to keep one and drop the others"),
   ("Solution", "Closed form exists", "Iterative (coordinate descent)"),
   ("Geometry", "Circle-shaped constraint", "Diamond-shaped constraint — corners lie on the axes")],
  "you believe most features help a little, or features are strongly correlated.",
  "you suspect only a few features really matter and want a simpler, more explainable model. (Elastic net mixes both.)",
  [10]),
 ("bagging-vs-boosting", "Bagging vs boosting",
  "Both combine many trees. Bagging trains them independently on random samples and averages them, which reduces variance. Boosting trains them one after another, each fixing the previous errors, which reduces bias.",
  ("Bagging / random forest", "Boosting / gradient boosting"),
  [("How trees are built", "Independently, in parallel", "One after another"),
   ("Data each tree sees", "A bootstrap sample (random rows, plus random features in a forest)", "All the data, focused on what's still wrong (residuals or reweighted points)"),
   ("Individual trees", "Deep, low bias, high variance", "Shallow, high bias, low variance"),
   ("Mainly reduces", "Variance (overfitting)", "Bias (underfitting)"),
   ("Combining", "Majority vote or average", "Weighted sum, scaled by a learning rate"),
   ("Overfitting risk with more trees", "Low — more trees don't hurt", "Grows if you add too many — use early stopping"),
   ("Tuning effort", "Little: works well with defaults", "More: learning rate, number of trees, depth"),
   ("Famous versions", "Random forest, extra trees", "AdaBoost, gradient boosting, XGBoost, LightGBM, CatBoost")],
  "you want a strong model quickly with little tuning, or you can train in parallel.",
  "you want the highest accuracy on tabular data and can spend time tuning.",
  [13, 14]),
 ("kmeans-vs-dbscan", "k-means vs hierarchical clustering vs DBSCAN",
  "Three ways to find groups. k-means looks for k round blobs around centres; hierarchical clustering builds a tree of merges you can cut at any level; DBSCAN grows clusters through dense regions and leaves sparse points as noise.",
  ("k-means", "DBSCAN"),
  [("You must choose", "$k$, the number of clusters", "eps (neighbourhood radius) and min_samples"),
   ("Cluster shapes", "Round, similar-sized blobs", "Any shape, as long as it's dense"),
   ("Outliers", "Forced into some cluster", "Labelled as noise"),
   ("Speed on large data", "Very fast (MiniBatch for millions of points)", "Fast with a spatial index; struggles when densities vary"),
   ("Result is", "Same $k$ every time; may vary with the start", "Deterministic for core points"),
   ("Hierarchical clustering (third option)", "Builds a dendrogram of nested merges; choose the number of clusters afterwards by cutting it", "Good for small datasets and when the hierarchy itself is interesting")],
  "groups are roughly round and similar in size, and you know (or can test) how many there are.",
  "clusters have odd shapes, the data contains noise or outliers, or you don't know how many clusters to expect.",
  [16]),
 ("pca-vs-tsne", "PCA vs t-SNE",
  "PCA finds the straight directions of greatest variance and projects onto them. t-SNE moves points around in 2D so that neighbours stay neighbours — good for pictures, not for features.",
  ("PCA", "t-SNE (and UMAP)"),
  [("Type", "Linear projection", "Non-linear embedding"),
   ("Preserves", "Global structure and large distances (variance)", "Local neighbourhoods; distances between clusters mean little"),
   ("Deterministic?", "Yes", "No — depends on the random seed and perplexity"),
   ("New data", "Transform it with the same projection", "No direct transform in t-SNE (UMAP can)"),
   ("Speed", "Very fast", "Slower; usually run on a PCA-reduced version"),
   ("Interpretable axes", "Yes — each component is a weighted mix of features", "No — the axes have no meaning"),
   ("Main use", "Compressing features before modelling, removing correlation", "Visualising high-dimensional data in 2D")],
  "you need fewer features for a model, want to understand which features vary together, or need a fast, repeatable transform.",
  "you only want to <em>see</em> whether your data has clusters. Never feed t-SNE output to a model.",
  [17]),
 ("precision-vs-recall", "Precision vs recall",
  "Precision asks: of everything I flagged, how much was right? Recall asks: of everything I should have flagged, how much did I catch? Raising the threshold usually trades recall for precision.",
  ("Precision", "Recall"),
  [("Formula", "$\\dfrac{TP}{TP + FP}$", "$\\dfrac{TP}{TP + FN}$"),
   ("Question it answers", "When the model says yes, how often is it right?", "Of all the real yeses, how many did it find?"),
   ("Hurt by", "False alarms (false positives)", "Misses (false negatives)"),
   ("Higher threshold", "Usually goes up", "Goes down"),
   ("Chennai Homes (Lesson 9)", "0.86 — one false alarm out of 7 flagged", "1.0 — all 6 fast sellers were caught"),
   ("Combined into", "F1 score = harmonic mean of the two", "F1 score = harmonic mean of the two")],
  "false alarms are costly: a spam filter hiding real email, recommending a bad investment.",
  "misses are costly: screening for a disease, detecting fraud.",
  [9]),
 ("naive-bayes-vs-logistic", "Naive Bayes vs logistic regression",
  "Two classic classifiers for text and simple tables. Naive Bayes models how each class generates the features (generative); logistic regression learns the boundary between classes directly (discriminative).",
  ("Naive Bayes", "Logistic regression"),
  [("Approach", "Generative: learns $P(\\mathbf{x}\\mid y)$ and $P(y)$, then uses Bayes' rule", "Discriminative: learns $P(y\\mid\\mathbf{x})$ directly"),
   ("Key assumption", "Features are independent within each class", "Log-odds are a linear function of the features"),
   ("Training", "Counting — one pass over the data, instant", "Gradient descent — iterative"),
   ("Small datasets", "Often better — needs little data", "Can overfit without regularisation"),
   ("Large datasets", "Usually overtaken", "Usually more accurate"),
   ("Probabilities", "Often over-confident (too close to 0 or 1)", "Usually well calibrated")],
  "you need a fast baseline, especially for text, or you have very little data.",
  "you have more data and want better accuracy and trustworthy probabilities.",
  [8, 12]),
 ("classical-vs-deep", "Classical machine learning vs deep learning",
  "Classical models learn from features you design; deep networks learn the features themselves from raw data, at the price of much more data and computing power.",
  ("Classical ML (trees, linear models, SVMs…)", "Deep learning (neural networks)"),
  [("Best data type", "Tables of numbers and categories", "Images, audio, text, video"),
   ("Features", "Designed by you (feature engineering)", "Learned automatically from raw input"),
   ("Data needed", "Hundreds to millions of rows", "Usually many thousands to billions of examples — or a pretrained model"),
   ("Hardware", "A laptop CPU", "Often GPUs"),
   ("Training time", "Seconds to minutes", "Minutes to weeks"),
   ("Interpretability", "Often good (weights, tree rules, importances)", "Hard — needs special explanation tools"),
   ("Tabular data champion", "Gradient-boosted trees usually win", "Rarely beats boosting on ordinary tables")],
  "your data is a table, the dataset is modest, or you need to explain decisions.",
  "the input is images, sound or language, you have lots of data or can fine-tune a pretrained model.",
  [14, 18, 19]),
]
SEE_ALSO = {6: ["linear-vs-logistic"], 8: ["linear-vs-logistic", "naive-bayes-vs-logistic"], 9: ["precision-vs-recall"], 10: ["ridge-vs-lasso"],
            12: ["naive-bayes-vs-logistic"], 14: ["bagging-vs-boosting", "classical-vs-deep"], 16: ["kmeans-vs-dbscan"], 17: ["pca-vs-tsne"],
            18: ["classical-vs-deep"], 19: ["classical-vs-deep"]}

if __name__ == "__main__":
    print(FACTS); print(CAPS)
