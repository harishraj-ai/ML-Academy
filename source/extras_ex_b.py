# Practice exercises + common mistakes, lessons 11-20. All numeric answers verified with Python.
EX = {}
MISTAKES = {}

EX[11] = [
 ("By hand", "Training points: A $(0,0)$ red, B $(1,1)$ red, C $(4,4)$ blue, D $(5,4)$ blue, E $(1,4)$ blue. Classify $\\mathbf{q} = (2, 1)$ with $k = 1, 3, 5$.",
  "Distances: B $= 1$, A $= \\sqrt5 \\approx 2.236$, E $= \\sqrt{10} \\approx 3.162$, C $= \\sqrt{13} \\approx 3.606$, D $= \\sqrt{18} \\approx 4.243$.<br>$k = 1$: B → <strong>red</strong>. $k = 3$: B, A, E → 2 red, 1 blue → <strong>red</strong>. $k = 5$: 2 red, 3 blue → <strong>blue</strong>."),
 ("By hand", "Compute the Euclidean and Manhattan distances between $(1, 2)$ and $(4, 6)$.",
  "Euclidean: $\\sqrt{3^2 + 4^2} = 5$. Manhattan: $3 + 4 = 7$."),
 ("Concepts", "A dataset has \"age\" (20–70) and \"salary\" (20,000–200,000). Without scaling, which feature will dominate kNN distances? What should you do?",
  "Salary — its differences are thousands of times larger. Standardise both features (fitted on training data) before kNN."),
 ("By hand", "In 5 dimensions, what side length must a cube-shaped neighbourhood have to contain 10% of uniformly spread data?",
  "$0.1^{1/5} \\approx 0.63$ — 63% of each feature's range. Hardly \"local\" any more."),
]
MISTAKES[11] = [
 "Running kNN on unscaled features.",
 "Judging $k = 1$ by its training accuracy (always 100%).",
 "Keeping many irrelevant features, which dilute the meaning of distance.",
]

EX[12] = [
 ("By hand", "With add-one smoothing, a word never seen in the ham class, ham total word count 50, vocabulary size 100. What is $P(\\text{word} \\mid \\text{ham})$?",
  "$(0 + 1)/(50 + 100) = 1/150 \\approx 0.0067$ — small, but not zero."),
 ("By hand", "Priors: spam 0.5, ham 0.5. $P(\\text{cheap} \\mid \\text{spam}) = 0.2$, $P(\\text{cheap} \\mid \\text{ham}) = 0.02$; $P(\\text{meeting} \\mid \\text{spam}) = 0.01$, $P(\\text{meeting} \\mid \\text{ham}) = 0.1$. Classify \"cheap meeting\".",
  "Spam: $0.5\\times0.2\\times0.01 = 0.001$. Ham: $0.5\\times0.02\\times0.1 = 0.001$. A perfect tie: $P(\\text{spam}) = 0.5$. The two words' evidence (×10 for spam, ×10 for ham) cancels out."),
 ("By hand", "Gaussian NB, one feature. Class A: $\\mu = 10$, $\\sigma = 2$. Class B: $\\mu = 14$, $\\sigma = 2$. Equal priors. Classify $x = 11.5$.",
  "Same $\\sigma$, so compare $e^{-z^2/2}$. A: $z = 0.75$ → $e^{-0.281} \\approx 0.755$. B: $z = -1.25$ → $e^{-0.781} \\approx 0.458$.<br>$P(A \\mid x) = 0.755/(0.755 + 0.458) \\approx 0.62$ → <strong>class A</strong>."),
 ("Concepts", "Why does Naive Bayes often classify well even though its probabilities are over-confident?",
  "Classification only needs the <em>right class to score highest</em>. Violated independence distorts the size of the probabilities more than their ranking."),
]
MISTAKES[12] = [
 "Forgetting smoothing, so one unseen word sets a class's probability to zero.",
 "Multiplying many raw probabilities instead of adding log-probabilities (underflow).",
 "Trusting Naive Bayes probabilities as well-calibrated confidence levels.",
]

EX[13] = [
 ("By hand", "A node has 3 examples of class A and 1 of class B. Compute its Gini impurity and entropy.",
  "Gini $= 1 - (0.75^2 + 0.25^2) = 0.375$. Entropy $= -(0.75\\log_2 0.75 + 0.25\\log_2 0.25) \\approx 0.811$ bits."),
 ("By hand", "Parent: 5 A / 5 B. A split gives left 4 A / 1 B and right 1 A / 4 B. Compute the Gini impurity decrease.",
  "Parent Gini $= 0.5$. Each child: $1 - (0.8^2 + 0.2^2) = 0.32$. Weighted: $0.32$. Decrease $= 0.5 - 0.32 = 0.18$."),
 ("By hand", "Using the iris tree in this lesson, classify a flower with petal width 2.1 cm, and one with 0.4 cm.",
  "2.1: is $2.1 \\le 0.8$? No → is $2.1 \\le 1.75$? No → <strong>virginica</strong>. 0.4: $0.4 \\le 0.8$ → <strong>setosa</strong>."),
 ("Code", "Train <code>DecisionTreeClassifier(max_depth=2)</code> on iris and print it with <code>export_text</code>. Does it match the tree in this lesson?",
  "<code>from sklearn.datasets import load_iris</code><br><code>from sklearn.tree import DecisionTreeClassifier, export_text</code><br><code>iris = load_iris()</code><br><code>t = DecisionTreeClassifier(max_depth=2, random_state=0).fit(iris.data, iris.target)</code><br><code>print(export_text(t, feature_names=iris.feature_names))</code><br>Yes — splits at petal width 0.80 and 1.75."),
]
MISTAKES[13] = [
 "Letting trees grow without limits and trusting their 100% training accuracy.",
 "Scaling features for trees (harmless, but unnecessary).",
 "Reading impurity-based feature importance as causal, or as fair between correlated features.",
]

EX[14] = [
 ("By hand", "Three independent classifiers, each 70% accurate, vote by majority. How accurate is the vote?",
  "Correct when at least 2 of 3 are right: $0.7^3 + 3\\times0.7^2\\times0.3 = 0.343 + 0.441 = 0.784$."),
 ("By hand", "A bootstrap sample of size 5 is drawn from 5 examples. What's the chance a particular example is never picked?",
  "$(4/5)^5 \\approx 0.328$ — about a third, close to the large-$n$ value $e^{-1} \\approx 0.368$."),
 ("By hand", "An AdaBoost weak learner has weighted error 0.2. What is its vote weight $\\alpha$?",
  "$\\alpha = \\frac12\\ln\\frac{0.8}{0.2} = \\frac12\\ln4 \\approx 0.693$."),
 ("By hand", "Gradient boosting: $y = 10, 20$; $F_0$ is the mean. A stump fits the residuals perfectly; learning rate 0.1. What are the predictions after one round?",
  "$F_0 = 15$; residuals $-5, +5$. $F_1 = 15 + 0.1\\times(-5) = 14.5$ and $15 + 0.1\\times5 = 15.5$."),
]
MISTAKES[14] = [
 "Using too many boosting rounds with a large learning rate, which overfits.",
 "Assuming more random-forest trees causes overfitting — it only costs time.",
 "Ensembling near-identical models, which barely helps.",
]

EX[15] = [
 ("By hand", "An SVM has $\\mathbf{w} = (3, 4)$. How wide is its margin?",
  "$\\|\\mathbf{w}\\| = 5$, so the margin is $2/5 = 0.4$."),
 ("By hand", "Hinge loss for a point with $y = -1$ and score $-2$; and with score $0.3$.",
  "Score $-2$: $\\max(0, 1 - (-1)(-2)) = \\max(0, -1) = 0$ — safely correct.<br>Score $0.3$: $\\max(0, 1 + 0.3) = 1.3$ — wrong side."),
 ("By hand", "For $\\mathbf{x} = (2, 1)$, $\\mathbf{z} = (1, 3)$, compute the polynomial kernel $(\\mathbf{x}\\cdot\\mathbf{z})^2$ and the RBF kernel with $\\gamma = 0.5$.",
  "$\\mathbf{x}\\cdot\\mathbf{z} = 5$ → $25$. $\\|\\mathbf{x} - \\mathbf{z}\\|^2 = 1 + 4 = 5$ → $e^{-0.5\\times5} = e^{-2.5} \\approx 0.082$."),
 ("Concepts", "An RBF SVM underfits: training 75%, test 74%, with a very smooth boundary. Which way should $C$ and $\\gamma$ move?",
  "Increase $\\gamma$ (more local, flexible boundary) and/or increase $C$ (fewer margin violations allowed) — then check with cross-validation."),
]
MISTAKES[15] = [
 "Forgetting to scale features before an SVM.",
 "Tuning $C$ and $\\gamma$ separately instead of together.",
 "Using kernel SVMs on hundreds of thousands of examples (use LinearSVC or SGD).",
]

EX[16] = [
 ("By hand", "Run k-means with $k = 2$ on $1, 2, 6, 7, 8$, starting from centroids 1 and 8. Give the final centroids and inertia.",
  "Assign: $\\{1, 2\\}$ and $\\{6, 7, 8\\}$ (6 is 5 from 1 but 2 from 8). Update: $1.5$ and $7$. Re-assigning changes nothing → converged.<br>Inertia $= 0.25 + 0.25 + 1 + 0 + 1 = 2.5$."),
 ("By hand", "A point has $a = 2$ (own cluster) and $b = 5$ (nearest other cluster). What is its silhouette value?",
  "$(5 - 2)/\\max(2, 5) = 3/5 = 0.6$."),
 ("By hand", "1D points $1, 2, 3, 6, 10$; DBSCAN with $\\varepsilon = 1$ and <code>min_samples</code> $= 3$ (counting the point itself). Label each point core, border or noise.",
  "2 has $\\{1, 2, 3\\}$ within 1 → <strong>core</strong>. 1 and 3 have only 2 points each, but are within 1 of point 2 → <strong>border</strong>. 6 and 10 → <strong>noise</strong>. One cluster: $\\{1, 2, 3\\}$."),
 ("Concepts", "Which method fits? (a) Segment customers into exactly 5 groups for 5 marketing teams; (b) find unusual GPS traces among millions of normal ones; (c) see how species group at every level of similarity.",
  "(a) k-means with $k = 5$. (b) DBSCAN (its noise points are the unusual traces). (c) Hierarchical clustering with a dendrogram."),
]
MISTAKES[16] = [
 "Picking $k$ by minimising inertia (it always prefers more clusters).",
 "Running k-means on unscaled features or on non-round cluster shapes.",
 "Treating cluster labels as ground truth without checking they're meaningful.",
]

EX[17] = [
 ("By hand", "Covariance matrix $\\begin{bmatrix}4 & 2\\\\2 & 1\\end{bmatrix}$. Find the eigenvalues and the share of variance on PC1.",
  "$\\lambda = 2.5 \\pm \\sqrt{1.5^2 + 2^2} = 2.5 \\pm 2.5$: $\\lambda_1 = 5$, $\\lambda_2 = 0$. PC1 explains 100% — the data lies exactly on a line."),
 ("By hand", "Eigenvalues $8, 4, 2, 1, 1$. What share do the first two explain? How many components are needed for at least 90%?",
  "Total 16. First two: $12/16 = 75\\%$. Three: $14/16 = 87.5\\%$. Four: $15/16 \\approx 93.8\\%$ → <strong>4 components</strong>."),
 ("By hand", "A centred point $(3, 1)$ is projected onto PC1 $= \\frac{1}{\\sqrt2}(1, 1)$. What is its new coordinate?",
  "$(3 + 1)/\\sqrt2 = 4/\\sqrt2 \\approx 2.83$."),
 ("Code", "Standardise the wine dataset (13 features) and fit <code>PCA()</code>. How many components are needed for 90% of the variance?",
  "<code>from sklearn.datasets import load_wine</code> … <code>PCA().fit(StandardScaler().fit_transform(X))</code>, then <code>np.argmax(np.cumsum(pca.explained_variance_ratio_) >= 0.9) + 1</code> → <strong>8</strong>. (The first 2 explain about 55%.)"),
]
MISTAKES[17] = [
 "Running PCA on unstandardised features measured in different units.",
 "Fitting PCA on all data before the train/test split.",
 "Reading cluster sizes or gaps in a t-SNE plot as real distances.",
]

EX[18] = [
 ("By hand", "Inputs $\\mathbf{x} = (2, 1)$. Hidden ReLU neurons with weights $(1, -1)$ and $(-1, 2)$, biases 0. Output sigmoid with weights $(2, 3)$, bias $-1$. Compute the output.",
  "$h_1 = \\text{ReLU}(2 - 1) = 1$; $h_2 = \\text{ReLU}(-2 + 2) = 0$. $z = 2\\cdot1 + 3\\cdot0 - 1 = 1$; $p = \\sigma(1) \\approx 0.731$."),
 ("By hand", "Continue exercise 1 with label $y = 0$. Compute $\\partial L/\\partial v_1$ and $\\partial L/\\partial v_2$ (sigmoid + log loss).",
  "$\\delta_{\\text{out}} = p - y = 0.731$. $\\partial L/\\partial v_1 = 0.731\\times h_1 = 0.731$; $\\partial L/\\partial v_2 = 0.731\\times0 = 0$ (neuron 2 was inactive)."),
 ("By hand", "How many parameters has a network with 10 inputs, hidden layers of 32 and 16 neurons, and 3 outputs?",
  "$(10\\cdot32 + 32) + (32\\cdot16 + 16) + (16\\cdot3 + 3) = 352 + 528 + 51 = 931$."),
 ("Code", "In the XOR code, change the hidden size from 4 to 1 (<code>(2, 1)</code> and <code>(1, 1)</code>) and run it. Can it learn XOR? Why?",
  "No — the loss stays high and at least one point is misclassified. One hidden neuron draws one line, and XOR needs two."),
]
MISTAKES[18] = [
 "Initialising all weights to the same value (usually zero).",
 "Forgetting non-linear activations between layers.",
 "Not scaling inputs, which slows or stalls training.",
]

EX[19] = [
 ("By hand", "Output width: (a) input 32, kernel 5, padding 0, stride 1; (b) input 28, 2×2 pooling, stride 2.",
  "(a) $(32 - 5)/1 + 1 = 28$. (b) $(28 - 2)/2 + 1 = 14$."),
 ("By hand", "Convolve $\\begin{bmatrix}1&2&0\\\\0&1&3\\\\2&1&0\\end{bmatrix}$ with the 2×2 kernel $\\begin{bmatrix}1&0\\\\0&-1\\end{bmatrix}$ (no padding, stride 1).",
  "Each output = top-left − bottom-right of the window: $1 - 1 = 0$, $2 - 3 = -1$, $0 - 1 = -1$, $1 - 0 = 1$. Result $\\begin{bmatrix}0 & -1\\\\-1 & 1\\end{bmatrix}$."),
 ("By hand", "A conv layer has 32 filters of size 5×5 on a 3-channel input. How many parameters?",
  "$(5\\cdot5\\cdot3 + 1)\\times32 = 76\\times32 = 2{,}432$."),
 ("By hand", "A token's attention scores (already divided by $\\sqrt{d_k}$) are $2$ and $0$. What are its attention weights?",
  "Softmax: $e^2/(e^2 + 1) \\approx 0.881$ and $1/(e^2 + 1) \\approx 0.119$."),
]
MISTAKES[19] = [
 "Training a large network from scratch when a pretrained model could be fine-tuned.",
 "Forgetting to switch dropout off when evaluating (in PyTorch: <code>model.eval()</code>).",
 "Using sigmoid in every layer of a deep network (vanishing gradients) — prefer ReLU in hidden layers.",
]

EX[20] = [
 ("By hand", "Training values of a feature are $10, 20, 30$. Standardise the new value 40 (divide by $n$).",
  "$\\mu = 20$, $\\sigma = \\sqrt{(100 + 0 + 100)/3} \\approx 8.165$. $z = (40 - 20)/8.165 \\approx 2.45$. Training statistics are reused — never recomputed on new data."),
 ("By hand", "One-hot encode the sizes small, large, medium, small (categories in alphabetical order: large, medium, small).",
  "small → $(0, 0, 1)$; large → $(1, 0, 0)$; medium → $(0, 1, 0)$; small → $(0, 0, 1)$."),
 ("Concepts", "What's wrong? <code>X = StandardScaler().fit_transform(X)</code>, then <code>train_test_split(X, y)</code>, then <code>cross_val_score(model, X_train, y_train)</code>.",
  "The scaler was fitted on all data (including test rows) — leakage. Split first and put the scaler inside a <code>Pipeline</code> so it's re-fitted on each fold."),
 ("Project", "Extend the churn project: add a feature <code>is_new_customer</code> (tenure ≤ 6 months) inside <code>add_features</code>, add it to the numeric list, and re-run Steps 4–6. Did it help?",
  "Add <code>X[\"is_new_customer\"] = (X[\"tenure_months\"] &lt;= 6).astype(int)</code>. Compare the cross-validated ROC-AUC with the earlier 0.771. When we ran it, logistic regression stayed at exactly 0.771 — no gain. Tenure is already a feature, and the new column only repeats part of it. A useful lesson: a new feature must add <em>new</em> information. Any change smaller than the ± spread (about 0.01) isn't a real improvement."),
]
MISTAKES[20] = [
 "Fitting any preprocessing step on the full dataset before splitting.",
 "Label-encoding unordered categories as 1, 2, 3 for linear or distance-based models.",
 "Deploying without monitoring, so silent data changes go unnoticed.",
]
