import html, os, re, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import json
from diagrams import D as DIAGRAMS
from extras_ex_a import EX as EXA, MISTAKES as MA
from extras_ex_b import EX as EXB, MISTAKES as MB
from reference import GLOSSARY, CHEAT
from context import DEPS, REFRESH, FIT, USE, FAQ
from understanding import STEPS, DECODE, MYTHS
from running_code import CODE as RUN_CODE
from running_text import INTRO as RUN_INTRO
from levels import SIMPLE
from walks import WALKS, walk_html
from compare import COMPARE, FIGS as CMP_FIGS, CAPS as CMP_CAPS, SEE_ALSO
from guide import Q as GQ, R as GR, GUIDE_SOURCES
from checks import CHECKS
from tests import TESTS
from projects import PROJECTS
from routes import ROUTES
from advanced import ADV
from rai import RAI
import recent as RECENT
import nextpage as NEXTP
from sense import SENSE, SCENE, WHATIF
from iq import QI, PI, LEVELS as IQ_LEVELS
from exboxes import boxes as _exboxes
from lesson0_data import LESSON0, OBJ0, SRC0, FIT0, FAQ0, MIST0, EX0, CHECKS0
from lesson21_data import L21, OBJ21, SRC21
PROJ_RES = json.load(open(os.path.join(HERE, 'project_results.json')))
PROJ_BY_PART = {P['part']: P for P in PROJECTS}
import io, contextlib, tempfile, warnings
EXERCISES = {**EXA, **EXB}; MISTAKES = {**MA, **MB}
OUT = sys.argv[1]
e = html.escape

PARTS = [
    ("Part 1", "Foundations", "The ideas and the little bit of maths you need — explained from zero."),
    ("Part 2", "Learning from labelled data", "Your first real models, how they are trained, and how to judge them honestly."),
    ("Part 3", "Classic algorithms", "The toolbox every ML practitioner knows, from nearest neighbours to support vector machines."),
    ("Part 4", "Finding structure without labels", "Discover groups and patterns in data that nobody has labelled."),
    ("Part 5", "Neural networks & real projects", "Build a neural network from scratch, meet modern deep learning, and ship a complete project."),
]

# (num, part_index, title, summary, minutes)
LESSONS = [
    (1, 0, "What Is Machine Learning?", "Rules vs learning, the core vocabulary, the types of ML, and how a model learns by minimising a loss.", 35),
    (2, 0, "Vectors & Matrices", "Lists and tables of numbers, the dot product, distances, and why predictions are matrix multiplications.", 45),
    (3, 0, "Derivatives & Gradients", "Slopes, derivatives, the chain rule, partial derivatives and the gradient — the maths of learning.", 50),
    (4, 0, "Probability & Statistics", "Probability rules, Bayes' theorem, mean and variance, z-scores and the normal distribution.", 50),
    (5, 1, "Data, Features & Generalization", "Datasets, train/validation/test splits, overfitting vs underfitting, and cross-validation.", 45),
    (6, 1, "Linear Regression", "Fit a line (and a plane) to data, derive the least-squares solution, and interpret the weights.", 55),
    (7, 1, "Gradient Descent", "Train any model by walking downhill: learning rates, batch vs stochastic, and convergence.", 50),
    (8, 1, "Logistic Regression", "Classification with the sigmoid, probabilities, log loss and decision boundaries.", 55),
    (9, 1, "Evaluating Models", "Confusion matrices, precision, recall, F1, ROC curves and regression metrics.", 50),
    (10, 1, "Overfitting, Regularization & Bias–Variance", "Why models overfit and how L1/L2 penalties and the bias–variance trade-off help.", 50),
    (11, 2, "k-Nearest Neighbours", "Classify by asking the neighbours: distances, choosing k, scaling and the curse of dimensionality.", 40),
    (12, 2, "Naive Bayes", "Bayes' theorem as a classifier — the classic spam filter, built step by step.", 40),
    (13, 2, "Decision Trees", "Twenty questions for data: Gini impurity, entropy, information gain and pruning.", 50),
    (14, 2, "Random Forests & Boosting", "Combine many trees: bagging, random forests, AdaBoost and gradient boosting.", 50),
    (15, 2, "Support Vector Machines", "Maximum margins, the hinge loss, and the kernel trick for curved boundaries.", 55),
    (16, 3, "Clustering", "Group data without labels: k-means, choosing k, hierarchical clustering and DBSCAN.", 50),
    (17, 3, "Dimensionality Reduction & PCA", "Compress many features into a few: variance, principal components and t-SNE.", 55),
    (18, 4, "Neural Networks from Scratch", "Neurons, layers, activations and backpropagation — built by hand in NumPy.", 70),
    (19, 4, "Deep Learning Architectures", "Training deep nets, CNNs for images, RNNs for sequences, and Transformers.", 65),
    (20, 4, "Feature Engineering, Pipelines & Final Project", "Clean and encode data, build leak-proof pipelines, and complete an end-to-end project.", 70),
]

OBJECTIVES = {
    1: ["Explain how machine learning differs from traditional programming", "Use the words feature, label, model, parameter, training and inference correctly",
        "Tell regression, classification and clustering problems apart", "Compute the mean squared error of a simple model by hand"],
    2: ["Add, scale and measure vectors", "Compute a dot product by hand and explain what it means geometrically",
        "Read a dataset as a matrix and multiply a matrix by a vector", "Use NumPy for the same operations"],
    3: ["Explain a derivative as a slope and compute it from the definition", "Apply the power, sum and chain rules",
        "Compute partial derivatives and assemble a gradient", "Explain why gradient descent moves against the gradient"],
    4: ["Apply the basic probability rules and conditional probability", "Use Bayes' theorem on a real-world problem",
        "Compute mean, variance, standard deviation and z-scores by hand", "Describe the normal distribution and the 68–95–99.7 rule"],
    5: ["Explain generalization and why training error can mislead", "Recognise underfitting and overfitting from training and test errors",
        "Split data correctly into training, validation and test sets", "Run and interpret k-fold cross-validation, and avoid data leakage"],
    6: ["Write the linear regression model for one or many features", "Derive the least-squares formulas for the slope and intercept",
        "Fit a line by hand and with the normal equation", "Measure fit with R² and interpret the weights carefully"],
    7: ["Explain the gradient descent update rule and why it works", "Derive the gradient of the MSE loss and run steps by hand",
        "Choose a learning rate and recognise divergence", "Compare batch, stochastic and mini-batch gradient descent"],
    8: ["Explain why classification needs the sigmoid function", "Turn model scores into probabilities, decisions and odds",
        "Compute log loss and explain why it punishes confident mistakes", "Derive the gradient and train a classifier with gradient descent"],
    9: ["Build and read a confusion matrix", "Compute accuracy, precision, recall, specificity and F1 by hand",
        "Explain the threshold trade-off, ROC curves and AUC", "Choose suitable metrics for classification and regression problems"],
    10: ["Explain bias, variance and the trade-off between them", "Diagnose underfitting vs overfitting and pick a fix",
        "Write and compute ridge (L2) and lasso (L1) penalties", "Choose the regularization strength with cross-validation"],
    11: ["Classify and regress with the k-nearest neighbours algorithm by hand", "Compute Euclidean and Manhattan distances",
        "Explain how k controls the bias–variance trade-off", "Explain why feature scaling and the curse of dimensionality matter"],
    12: ["Turn Bayes' theorem into a classifier", "Explain the naive independence assumption and its limits",
        "Build a spam filter by hand with Laplace smoothing", "Choose between Multinomial, Bernoulli and Gaussian Naive Bayes"],
    13: ["Read and follow a decision tree to make a prediction", "Compute Gini impurity, entropy and information gain by hand",
        "Explain how the CART algorithm chooses splits", "Control overfitting with depth limits and pruning"],
    14: ["Explain mathematically why combining diverse models reduces error", "Describe bagging, bootstrap samples and out-of-bag evaluation",
        "Explain how random forests decorrelate trees", "Run AdaBoost and gradient boosting rounds by hand"],
    15: ["Explain the maximum-margin idea and support vectors", "Compute a margin and hinge losses by hand",
        "Explain how C trades margin width against errors", "Use the kernel trick and tune C and gamma for an RBF SVM"],
    16: ["Run the k-means algorithm by hand", "Choose k with the elbow method and silhouette score",
        "Explain hierarchical clustering and the different linkages", "Use DBSCAN to find clusters of any shape and flag outliers"],
    17: ["Explain why reducing dimensions helps", "Compute a covariance matrix and its eigenvalues by hand for 2D data",
        "Find principal components, explained variance and projections", "Choose the number of components and read t-SNE plots safely"],
    18: ["Explain neurons, layers and why activation functions are needed", "Run a forward pass through a small network by hand",
        "Run backpropagation by hand and update the weights", "Implement and train a neural network from scratch in NumPy"],
    19: ["Explain vanishing gradients and the techniques that fix them", "Compute a convolution, output sizes and max pooling by hand",
        "Describe how RNNs and LSTMs process sequences", "Compute scaled dot-product attention for a small example"],
    20: ["Scale, transform and encode features correctly", "Handle missing values without leaking information",
        "Build leak-proof pipelines with ColumnTransformer", "Complete an end-to-end ML project from raw data to a saved model"],
}

SOURCES = {
    1: [("Google for Developers — What is Machine Learning?", "https://developers.google.com/machine-learning/intro-to-ml/what-is-ml"),
        ("scikit-learn — LinearRegression / Linear Models", "https://scikit-learn.org/stable/modules/linear_model.html"),
        ("Google ML Crash Course", "https://developers.google.com/machine-learning/crash-course")],
    2: [("Deisenroth, Faisal & Ong — Mathematics for Machine Learning (Cambridge University Press, 2020)", "https://mml-book.github.io/"),
        ("Wikipedia — Dot product", "https://en.wikipedia.org/wiki/Dot_product"),
        ("NumPy — the absolute basics for beginners", "https://numpy.org/doc/stable/user/absolute_beginners.html"),
        ("3Blue1Brown — visual maths lessons (see “Essence of linear algebra”)", "https://www.3blue1brown.com/")],
    3: [("Deisenroth, Faisal & Ong — Mathematics for Machine Learning, ch. 5 Vector Calculus", "https://mml-book.github.io/"),
        ("Wikipedia — Chain rule", "https://en.wikipedia.org/wiki/Chain_rule"),
        ("Google MLCC — Gradient descent", "https://developers.google.com/machine-learning/crash-course/linear-regression/gradient-descent"),
        ("3Blue1Brown — visual maths lessons (see “Essence of calculus”)", "https://www.3blue1brown.com/")],
    4: [("Seeing Theory — a visual introduction to probability and statistics (Brown University)", "https://seeing-theory.brown.edu/"),
        ("Wikipedia — Bayes' theorem", "https://en.wikipedia.org/wiki/Bayes%27_theorem"),
        ("Wikipedia — Normal distribution", "https://en.wikipedia.org/wiki/Normal_distribution"),
        ("Deisenroth, Faisal & Ong — Mathematics for Machine Learning, ch. 6 Probability", "https://mml-book.github.io/")],
    5: [("Google MLCC — Datasets, generalization, and overfitting", "https://developers.google.com/machine-learning/crash-course/overfitting"),
        ("Google MLCC — Dividing the original dataset", "https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets"),
        ("scikit-learn — Cross-validation: evaluating estimator performance", "https://scikit-learn.org/stable/modules/cross_validation.html"),
        ("scikit-learn — Common pitfalls and recommended practices", "https://scikit-learn.org/stable/common_pitfalls.html")],
    6: [("scikit-learn — Linear Models (Ordinary Least Squares)", "https://scikit-learn.org/stable/modules/linear_model.html"),
        ("Google MLCC — Linear regression", "https://developers.google.com/machine-learning/crash-course/linear-regression"),
        ("Deisenroth, Faisal & Ong — Mathematics for Machine Learning, ch. 9 Linear Regression", "https://mml-book.github.io/")],
    7: [("Google MLCC — Linear regression: Gradient descent", "https://developers.google.com/machine-learning/crash-course/linear-regression/gradient-descent"),
        ("scikit-learn — Stochastic Gradient Descent", "https://scikit-learn.org/stable/modules/sgd.html"),
        ("Wikipedia — Gradient descent", "https://en.wikipedia.org/wiki/Gradient_descent"),
        ("Goodfellow, Bengio & Courville — Deep Learning (ch. 4 & 8 on optimisation)", "https://www.deeplearningbook.org/")],
    8: [("Google MLCC — Logistic regression", "https://developers.google.com/machine-learning/crash-course/logistic-regression"),
        ("scikit-learn — Linear Models (Logistic regression)", "https://scikit-learn.org/stable/modules/linear_model.html"),
        ("scikit-learn — Stochastic Gradient Descent (log loss)", "https://scikit-learn.org/stable/modules/sgd.html"),
        ("Deisenroth, Faisal & Ong — Mathematics for Machine Learning", "https://mml-book.github.io/")],
    9: [("scikit-learn — Metrics and scoring", "https://scikit-learn.org/stable/modules/model_evaluation.html"),
        ("Google MLCC — Accuracy, recall, precision and related metrics", "https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall"),
        ("scikit-learn — Common pitfalls and recommended practices", "https://scikit-learn.org/stable/common_pitfalls.html")],
    10: [("Wikipedia — Bias–variance tradeoff", "https://en.wikipedia.org/wiki/Bias%E2%80%93variance_tradeoff"),
        ("scikit-learn — Linear Models (Ridge, Lasso, ElasticNet)", "https://scikit-learn.org/stable/modules/linear_model.html"),
        ("Google MLCC — Datasets, generalization, and overfitting", "https://developers.google.com/machine-learning/crash-course/overfitting"),
        ("scikit-learn — Tuning the hyper-parameters of an estimator", "https://scikit-learn.org/stable/modules/grid_search.html")],
    11: [("scikit-learn — Nearest Neighbors", "https://scikit-learn.org/stable/modules/neighbors.html"),
        ("scikit-learn — Preprocessing data (StandardScaler)", "https://scikit-learn.org/stable/modules/preprocessing.html"),
        ("Deisenroth, Faisal & Ong — Mathematics for Machine Learning", "https://mml-book.github.io/")],
    12: [("scikit-learn — Naive Bayes", "https://scikit-learn.org/stable/modules/naive_bayes.html"),
        ("Wikipedia — Bayes' theorem", "https://en.wikipedia.org/wiki/Bayes%27_theorem"),
        ("Seeing Theory — Bayesian inference (Brown University)", "https://seeing-theory.brown.edu/")],
    13: [("scikit-learn — Decision Trees (CART, impurity, pruning)", "https://scikit-learn.org/stable/modules/tree.html"),
        ("scikit-learn — Ensembles (for what comes next)", "https://scikit-learn.org/stable/modules/ensemble.html")],
    14: [("scikit-learn — Ensembles: gradient boosting, random forests, bagging, voting, stacking", "https://scikit-learn.org/stable/modules/ensemble.html"),
        ("XGBoost — Introduction to Boosted Trees", "https://xgboost.readthedocs.io/en/stable/tutorials/model.html"),
        ("Chen & Guestrin (2016) — XGBoost: A Scalable Tree Boosting System", "https://arxiv.org/abs/1603.02754")],
    15: [("scikit-learn — Support Vector Machines", "https://scikit-learn.org/stable/modules/svm.html"),
        ("Wikipedia — Support vector machine", "https://en.wikipedia.org/wiki/Support_vector_machine"),
        ("LIBSVM — the library behind scikit-learn's SVC", "https://www.csie.ntu.edu.tw/~cjlin/libsvm/")],
    16: [("scikit-learn — Clustering (k-means, hierarchical, DBSCAN)", "https://scikit-learn.org/stable/modules/clustering.html"),
        ("scikit-learn — Metrics and scoring", "https://scikit-learn.org/stable/modules/model_evaluation.html")],
    17: [("scikit-learn — Decomposing signals in components (PCA)", "https://scikit-learn.org/stable/modules/decomposition.html"),
        ("scikit-learn — Manifold learning (t-SNE)", "https://scikit-learn.org/stable/modules/manifold.html"),
        ("Wattenberg, Viégas & Johnson — How to Use t-SNE Effectively (Distill, 2016)", "https://distill.pub/2016/misread-tsne/"),
        ("Deisenroth, Faisal & Ong — Mathematics for Machine Learning, ch. 10 PCA", "https://mml-book.github.io/")],
    18: [("scikit-learn — Neural network models (supervised)", "https://scikit-learn.org/stable/modules/neural_networks_supervised.html"),
        ("Google MLCC — Neural networks", "https://developers.google.com/machine-learning/crash-course/neural-networks"),
        ("Goodfellow, Bengio & Courville — Deep Learning (ch. 6, Deep Feedforward Networks)", "https://www.deeplearningbook.org/")],
    19: [("Stanford CS231n — Convolutional Neural Networks", "https://cs231n.github.io/convolutional-networks/"),
        ("Olah — Understanding LSTM Networks", "https://colah.github.io/posts/2015-08-Understanding-LSTMs/"),
        ("Vaswani et al. (2017) — Attention Is All You Need", "https://arxiv.org/abs/1706.03762"),
        ("Kingma & Ba — Adam: A Method for Stochastic Optimization", "https://arxiv.org/abs/1412.6980"),
        ("Goodfellow, Bengio & Courville — Deep Learning", "https://www.deeplearningbook.org/")],
    20: [("scikit-learn — Preprocessing data", "https://scikit-learn.org/stable/modules/preprocessing.html"),
        ("scikit-learn — Pipelines and composite estimators", "https://scikit-learn.org/stable/modules/compose.html"),
        ("scikit-learn — Imputation of missing values", "https://scikit-learn.org/stable/modules/impute.html"),
        ("scikit-learn — Feature selection", "https://scikit-learn.org/stable/modules/feature_selection.html"),
        ("scikit-learn — Model persistence (and its security risks)", "https://scikit-learn.org/stable/model_persistence.html"),
        ("Zinkevich — Rules of Machine Learning (Google)", "https://developers.google.com/machine-learning/guides/rules-of-ml")],
}

LESSONS.append(L21); OBJECTIVES[21] = OBJ21; SOURCES[21] = SRC21
OBJECTIVES[0] = OBJ0; SOURCES[0] = SRC0; FIT[0] = FIT0; FAQ[0] = FAQ0; EXERCISES[0] = EX0; MISTAKES[0] = MIST0; CHECKS.update(CHECKS0)
def ready(n): return os.path.exists(os.path.join(HERE, "lessons", f"{n:02d}.html"))
def fname(n): return f"lesson-{n:02d}.html"

# copy assets
if os.path.exists(os.path.join(OUT, "assets")): shutil.rmtree(os.path.join(OUT, "assets"))
shutil.copytree(os.path.join(HERE, "assets"), os.path.join(OUT, "assets"))
os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
shutil.copy(os.path.join(HERE, "data", "houses.csv"), os.path.join(OUT, "data", "houses.csv"))

FONTS = ('<link rel="stylesheet" href="assets/webfonts.css">'
         '<script>try{var s_=JSON.parse(localStorage.getItem("mla-a11y")||"{}"),r_=document.documentElement;if(s_.contrast==="high")r_.classList.add("hc");if(s_.font==="dyslexic")r_.classList.add("dys");'
         'if(s_.size)r_.style.setProperty("--ts",s_.size/100);if((s_.size||100)>=130||s_.font==="dyslexic")r_.classList.add("big");if(s_.motion==="reduce"||(s_.motion!=="allow"&&window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches))r_.classList.add("rm");}catch(e){}</script>')
LOGO = ('<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<circle cx="5" cy="6" r="2"/><circle cx="5" cy="18" r="2"/><circle cx="19" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><path d="M7 6.8 10.3 11M7 17.2l3.3-4.2M14 12h3"/></svg>')
THEME_BTN = ('<button class="icon-btn" id="theme-toggle" type="button" aria-label="Toggle light/dark theme">'
             '<svg class="theme-icon-dark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
             '<svg class="theme-icon-light" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button>')
SEARCH_BTN = ('<button class="icon-btn" type="button" data-search-open aria-label="Search the course (press /)" title="Search ( / )">'
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg></button>')
A11Y_BTN = '<button class="icon-btn a11y-btn" type="button" aria-label="Reading settings: contrast, font, text size, motion" aria-expanded="false" title="Reading settings">Aa</button>'
UP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"/></svg>'


ALL_LINKS = [("PATH", "Learning path"), ("map.html", "Course map"), ("review.html", "Review"), ("tests.html", "Tests"), ("projects.html", "Projects"), ("progress.html", "My progress"), ("notes.html", "My notes"), ("recent.html", "Recent developments"), ("next.html", "What next"), ("interview.html", "Interview questions"), ("confused.html", "Confused terms"), ("changelog.html", "Changelog"),
             ("guide.html", "Which model?"), ("compare.html", "Compare"), ("glossary.html", "Glossary"), ("cheatsheet.html", "Cheat sheet")]
def nav_html(path_href, primary, cls="nav"):
    links = [(path_href if h == "PATH" else h, t) for h, t in ALL_LINKS]
    prim = [l for l in links if l[1] in primary]
    rest = [l for l in links if l[1] not in primary]
    menu = "".join(f'<a class="more-dup" href="{h}">{t}</a>' for h, t in prim) + "".join(f'<a href="{h}">{t}</a>' for h, t in rest)
    return (f'<nav class="{cls}" aria-label="Main">' + "".join(f'<a href="{h}">{t}</a>' for h, t in prim) +
            f'<details class="nav-more"><summary>More <span aria-hidden="true">▾</span></summary><div class="nav-menu">{menu}</div></details></nav>')

SITE_URL = "https://harishraj07022004-cpu.github.io/ML-Academy/"   # change this if you publish the course elsewhere
def head(title, desc, math=False, demos=True):
    m = ('<link rel="stylesheet" href="assets/katex.min.css"><script defer src="assets/katex.min.js"></script>'
         '<script defer src="assets/auto-render.min.js"></script>' + ('<script defer src="assets/demos.js"></script><script defer src="assets/whatif.js"></script>' if demos else '')) if math else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:site_name" content="ML Academy"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="{SITE_URL}assets/social-preview.png"><meta property="og:image:width" content="1280"><meta property="og:image:height" content="640"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="assets/icon-32.png" sizes="32x32" type="image/png"><link rel="alternate icon" href="assets/favicon.ico"><link rel="apple-touch-icon" href="assets/icon-180.png"><meta name="theme-color" content="#0f2e1d">
{FONTS}<link rel="stylesheet" href="assets/base.css">{m}<script defer src="assets/app.js"></script><script defer src="assets/search-index.js"></script><script defer src="assets/search.js"></script><script defer src="assets/terms.js"></script><script defer src="assets/understand.js"></script><script defer src="assets/practice.js"></script><script defer src="assets/review.js"></script><script defer src="assets/a11y.js"></script><script defer src="assets/listen.js"></script><script defer src="assets/routes.js"></script><script defer src="assets/progress.js"></script><script defer src="assets/notes.js"></script>
</head>
"""
FOOTER = """<footer class="site-footer"><div class="container">
<div>ML Academy · A free, beginner-first machine learning course.</div>
<div class="footer-links"><a href="index.html#path">Learning path</a><a href="map.html">Course map</a><a href="tests.html">Part tests</a><a href="review.html">Review</a><a href="projects.html">Projects</a><a href="compare.html">Compare</a><a href="guide.html">Which model?</a><a href="glossary.html">Glossary</a><a href="cheatsheet.html">Cheat sheet</a><a href="workbook/ML-Academy-workbook.pdf">Printable workbook (PDF)</a><a href="index.html#setup">Setup</a><a href="changelog.html">Changelog &amp; versions</a></div>
</div></footer>"""
def ext(u, t): return f'<a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a>'

# ---------------- index ----------------
n_ready = sum(1 for L in LESSONS if ready(L[0]))
parts_html = ""
for pi, (plabel, ptitle, pdesc) in enumerate(PARTS):
    cards = ""
    for (n, p, t, s, mins) in LESSONS:
        if p != pi: continue
        if ready(n):
            cards += f'''<a class="lesson-card" data-lesson="{n}" href="{fname(n)}"><span class="check">✓</span><span class="num">LESSON {n:02d}</span><h4>{e(t)}</h4><p>{e(s)}</p><div class="meta"><span class="tag">~{mins} min</span><span class="tag level-Beginner">Available</span></div></a>'''
        else:
            cards += f'''<div class="lesson-card soon" data-lesson="{n}"><span class="check">✓</span><span class="num">LESSON {n:02d}</span><h4>{e(t)}</h4><p>{e(s)}</p><div class="meta"><span class="tag">~{mins} min</span><span class="tag">Coming soon</span></div></div>'''
    if pi == 0:
        cards = f'''<a class="lesson-card lesson-zero" data-lesson="0" href="lesson-00.html"><span class="check">✓</span><span class="num">LESSON 00 · OPTIONAL</span><h4>{e(LESSON0[2])}</h4><p>{e(LESSON0[3])}</p><div class="meta"><span class="tag">~{LESSON0[4]} min</span><span class="tag level-Beginner">Start here if you've never coded</span></div></a>''' + cards
    parts_html += f'''<div class="part"><div class="part-head"><span class="eyebrow">{plabel}</span><h3>{e(ptitle)}</h3><p>{e(pdesc)}</p><a class="part-test" href="tests.html?part={pi+1}">Take the {plabel} test →</a>{(' <a class="part-test" href="projects.html#' + PROJ_BY_PART[pi]['id'] + '">Project: ' + e(PROJ_BY_PART[pi]['title']) + ' →</a>') if pi in PROJ_BY_PART else ''}</div><div class="lessons-grid">{cards}</div></div>'''


routes_html = "".join(f'<a class="route-card" href="map.html?route={rid}"><span class="eyebrow">{len(ls)} lessons · ~{round(sum(LESSONS[l-1][4] for l in ls)/60)} h</span><h3>{e(name)}</h3><p>{e(blurb)}</p><span class="route-go">See it on the map →</span></a>' for rid, name, blurb, ls in ROUTES)
total_min = sum(L[4] for L in LESSONS)
index = head("ML Academy — Learn Machine Learning from Zero", "A free, self-contained machine learning course for complete beginners: intuition, step-by-step maths, interactive demos, code and quizzes.") + f"""<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="container">
<a class="brand" href="index.html"><span class="brand-mark">{LOGO}</span>ML Academy</a>
{nav_html("#path", ["Learning path", "Course map", "Review", "Tests", "Projects"])}
{A11Y_BTN}{SEARCH_BTN}{THEME_BTN}</div></header>
<main id="main">
<section class="hero"><div class="container"><div class="hero-grid">
<div>
<span class="badge">● Free · For complete beginners · No prior maths needed</span>
<h1>Learn machine learning<br><span>from zero.</span></h1>
<p class="lead">A complete, self-contained course. Every idea is explained in plain English first, then with step-by-step maths, worked examples you can follow by hand, interactive demos, Python code and a quiz. You won't need to look anywhere else.</p>
<div class="hero-actions"><a class="btn btn-primary" href="{fname(1)}">Start Lesson 1 →</a><a class="btn" href="#path">See the learning path</a><a class="btn" href="lesson-00.html">Never coded? Start with Lesson 0</a></div>
</div>
<div class="terminal" aria-hidden="true"><div class="terminal-bar"><i></i><i></i><i></i></div>
<pre><span class="t-dim"># what you'll be able to do by Lesson 7</span>
<span class="t-key">model</span>   ŷ = w·x + b
<span class="t-key">loss</span>    L = (1/n) Σ (ŷᵢ − yᵢ)²
<span class="t-key">grad</span>    ∂L/∂w = (2/n) Σ (ŷᵢ − yᵢ)·xᵢ
<span class="t-key">update</span>  w ← w − η · ∂L/∂w

<span class="t-prompt">for</span> step <span class="t-prompt">in</span> range(1000):
    w -= lr * grad(w)
<span class="t-ok">✓ and you'll understand every symbol</span></pre></div>
</div>
<div class="stats">
<div class="stat"><b>21</b><span>Lessons in 5 parts</span></div>
<div class="stat"><b>~{round(total_min/60)} h</b><span>Total study time</span></div>
<div class="stat"><b>0</b><span>Prerequisites beyond basic algebra</span></div>
<div class="stat"><b>{n_ready}/21</b><span>Lessons available now</span></div>
</div></div></section>

<section class="block" id="how"><div class="container">
<div class="eyebrow">How every lesson works</div>
<h2>Understand it, see it, do it.</h2>
<p class="sub">Each lesson follows the same rhythm so you always know where you are.</p>
<div class="flow">
<div><b>1 · Intuition</b>What you need from earlier lessons, where it fits, and a plain-English explanation.</div>
<div><b>2 · Maths</b>Formulas rendered clearly, every symbol explained.</div>
<div><b>3 · Worked example</b>Real numbers, step by step, by hand.</div>
<div><b>4 · Interactive demo</b>Drag sliders and watch the idea move.</div>
<div><b>5 · Code</b>Python from scratch and with scikit-learn.</div>
<div><b>6 · Quiz &amp; practice</b>A quiz, then exercises with worked solutions.</div>
</div></div></section>

<section class="block" id="routes"><div class="container">
<div class="eyebrow">Choose your route</div>
<h2>Short on time? Pick a goal.</h2>
<p class="sub">Every route is a subset of the 21 lessons in a sensible order. Skipped prerequisites are covered by the "Before you start" box at the top of each lesson.</p>
<div class="route-grid">{routes_html}</div>
<p class="sub" style="margin-top:14px">Track everything you've done — lessons, quiz scores, exercises, tests, time and badges — on <a href="progress.html">your progress dashboard</a>.</p>
</div></section>

<section class="block" id="path"><div class="container">
<div class="eyebrow">Learning path</div>
<h2>21 lessons, in order.</h2>
<p class="sub">Each lesson builds on the ones before it. Mark lessons complete as you go — your progress is saved in this browser.</p>
<div class="overall"><div class="overall-bar"><i></i></div><span class="overall-label"></span><a class="btn" href="map.html" style="margin-left:auto">See how the lessons connect →</a><a class="btn" href="guide.html">Which model should I use? →</a><a class="btn" href="compare.html">Side-by-side comparisons →</a></div>
{parts_html}
</div></section>

<section class="block" id="setup"><div class="container">
<div class="eyebrow">Setup</div>
<h2>Run the code yourself</h2>
<p class="sub">You can read every lesson without installing anything. To run the code examples, install Python 3, then in a terminal:</p>
<pre class="code"><code>python3 -m venv ml-env
source ml-env/bin/activate        # on Windows: ml-env\\Scripts\\activate
pip install numpy pandas scikit-learn matplotlib jupyterlab
jupyter lab</code></pre>
<p class="sub">JupyterLab opens in your browser. Every lesson has a <strong>ready-made notebook</strong> with all its code (and the expected outputs): use the <em>Download Jupyter notebook</em> button at the top of a lesson, open the file in JupyterLab, and press Shift+Enter to run each cell. All 21 are in the <code>notebooks</code> folder.</p>
<p class="sub"><strong>Prefer paper?</strong> The <a href="workbook/ML-Academy-workbook.pdf">printable workbook (PDF, about 410 pages)</a> has every lesson with space to work the exercises by hand, and all answers at the back. Each lesson page also prints cleanly on its own.</p>
<p class="sub"><strong>Prefer plain Python scripts?</strong> <a class="btn" href="downloads/ml-academy-code.zip" download>⬇ Download all the code (.zip)</a> — every lesson as a <code>.py</code> file, the coding challenges, the four projects (starter and solution), the dataset and a <code>pytest</code> test suite that checks every script still gives the published results. Unzip it anywhere and see its README.</p>
</div></section>

<section class="block" id="about"><div class="container">
<div class="eyebrow">About</div>
<h2>Accurate by design</h2>
<p class="sub">Lessons are written to be complete on their own, and checked against trusted sources — the scikit-learn documentation, Google's Machine Learning Crash Course, <em>Mathematics for Machine Learning</em> and original papers. Every code example has been run and its output verified. Each lesson lists the sources used at the bottom.</p>
</div></section>
</main>
{FOOTER}
</body></html>"""
open(os.path.join(OUT, "index.html"), "w").write(index)


def end_of_section(body, sid):
    i = body.index(f'<h2 id="{sid}">')
    j = body.find('<h2 ', i + 5)
    return len(body) if j == -1 else j

def stepper_html(title, steps):
    lis = "".join(f'<li class="st"><div class="st-math">$${m}$$</div><p class="st-why">{why}</p></li>' for m, why in steps)
    return ('<div class="stepper"><div class="stepper-head"><span class="stepper-tag">Step-by-step derivation</span>'
            f'<span class="stepper-title">{title}</span></div><ol class="st-list">{lis}</ol>'
            '<div class="st-controls"><button type="button" data-act="next">Next step →</button>'
            '<button type="button" data-act="all">Show all</button><button type="button" data-act="reset">Start again</button>'
            '<span class="st-count"></span></div></div>')

def decode_html(title, tex, parts):
    lis = "".join(f'<li data-p="{k+1}" tabindex="0"><span class="sw sw-{k+1}"></span><b>{e(lbl)}</b> — {mean}</li>' for k, (lbl, mean) in enumerate(parts))
    return (f'<div class="decode"><div class="decode-head"><span class="decode-tag">Read the formula</span><span class="decode-title">{title}</span></div>'
            f'<div class="decode-math">$${tex}$$</div><ul class="decode-legend">{lis}</ul>'
            '<p class="decode-hint">Hover over (or tap) a part to highlight it in the formula.</p></div>')

_RUN_OUT = {}
def run_output(n):
    if n not in _RUN_OUT:
        warnings.filterwarnings("ignore")
        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copy(os.path.join(HERE, "data", "houses.csv"), os.path.join(tmp, "houses.csv"))
            os.chdir(tmp)
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    exec(RUN_CODE[n], {"__name__": "__main__"})
            finally:
                os.chdir(cwd)
        _RUN_OUT[n] = buf.getvalue().rstrip()
    return _RUN_OUT[n]

def running_html(n):
    if n not in RUN_CODE: return ""
    import pandas as _pd
    h = '<h2 id="running-example">Running example: Chennai Homes</h2><div class="run-box">'
    h += f'<p>{RUN_INTRO[n]}</p>'
    if n == 1:
        d = _pd.read_csv(os.path.join(HERE, "data", "houses.csv"))
        h += '<div class="run-table"><table class="tbl"><thead><tr>' + "".join(f"<th>{e(c)}</th>" for c in d.columns) + '</tr></thead><tbody>'
        h += "".join("<tr>" + "".join(f"<td>{e(str(v))}</td>" for v in row) + "</tr>" for row in d.itertuples(index=False)) + '</tbody></table></div>'
        h += '<p><a class="btn" href="data/houses.csv" download>⬇ Download houses.csv</a> Save it next to your notebook (it\'s also already in the course\'s <code>data</code> folder).</p>'
    else:
        h += '<p class="run-note">Same 12 houses as <a href="lesson-01.html#running-example">Lesson 1</a>. With so little data, treat the numbers as an illustration of the method, not as reliable estimates.</p>'
    h += f'<pre><code>{e(RUN_CODE[n])}</code></pre><p class="run-out-label">Output:</p><pre><code>{e(run_output(n))}</code></pre></div>'
    return h

def apply_levels(n, body):
    for sid, summary in SIMPLE.get(n, {}).items():
        hs = body.index(f'<h2 id="{sid}">')
        he = body.index('</h2>', hs) + 5
        end = end_of_section(body, sid)
        inner = body[he:end]
        wrapped = (f'<div class="simple-sum"><p><span class="lvl-tag">In plain words</span>{summary}</p>'
                   f'<button type="button" class="adv-toggle" aria-expanded="false" data-target="adv-{sid}">Show the full maths ▾</button></div>'
                   f'<div class="adv-body" id="adv-{sid}">{inner}</div>')
        body = body[:he] + wrapped + body[end:]
    return body

def sense_html(n, k):
    d = SENSE.get((n, k)); h = ""
    if d:
        h = ('<div class="box sense"><div class="box-title">Make sense of it</div>'
             f'<p><strong>The situation:</strong> {d["s"]}</p><p><strong>What the result tells you:</strong> {d["m"]}</p>'
             '<p class="sense-wi"><strong>What if…?</strong></p><ul>' + "".join(f"<li>{w}</li>" for w in d["w"]) + '</ul>'
             f'<p><strong>Why it matters in ML:</strong> {d["ml"]}</p></div>')
    if (n, k) in WHATIF:
        h += f'<div class="whatif" data-whatif="{WHATIF[(n, k)]}"><noscript>This calculator needs JavaScript.</noscript></div>'
    return h

def enrich(n, body):
    for k, (i0, j0, _sid, _b) in reversed(list(enumerate(_exboxes(body)))):
        body = body[:j0] + sense_html(n, k) + body[j0:]
    inserts = []
    for sid, title, steps in STEPS.get(n, []):
        inserts.append((sid, stepper_html(title, steps)))
    if n == 19:
        inserts.append(("transformers", '<div class="box tip recent-link"><div class="box-title">Where things stand now</div><p>Large language models, reasoning models, agents and diffusion image generators are all built from the ideas in this lesson. For a dated overview of recent developments — and how each connects back to this course — see <a href="recent.html">Recent developments in LLMs and generative AI</a>.</p></div>'))
    for sid, at, ah in ADV.get(n, []):
        inserts.append((sid, f'<details class="adv-box"><summary><span class="adv-tag">Advanced · optional</span>{e(at)}</summary><div class="adv-content">{ah}</div></details>'))
    if n in WALKS:
        sid, wt, W_, H_, st_, frs_ = WALKS[n]
        inserts.append((sid, walk_html(wt, W_, H_, st_, frs_, n)))
    if n in DECODE:
        sid, title, tex, parts = DECODE[n]
        inserts.append((sid, decode_html(title, tex, parts)))
    for sid, html_ in inserts:
        k_ = end_of_section(body, sid)
        body = body[:k_] + html_ + body[k_:]
    if n in DIAGRAMS:
        sid, svgc, cap = DIAGRAMS[n]
        i = body.index(f'<h2 id="{sid}">')
        j = body.find('</p>', i)
        nxt = body.find('<h2 ', i + 5)
        pos = j + 4 if j != -1 and (nxt == -1 or j < nxt) else body.index('</h2>', i) + 5
        body = body[:pos] + f'<figure class="fig">{svgc}<figcaption>Figure {n}. {e(cap)}</figcaption></figure>' + body[pos:]
    top = '<div class="box context-box"><div class="box-title">Before you start</div>'
    if DEPS.get(n):
        top += '<p class="ctx-lead">This lesson builds on:</p><ul class="ctx-deps">' + "".join(f'<li><a href="{fname(d)}">Lesson {d}: {e(LESSONS[d-1][2])}</a> — {REFRESH.get(d, "")}</li>' for d in DEPS[n]) + '</ul>'
    else:
        top += '<p class="ctx-lead">No prerequisites — this is the starting point.' + (' Never written code? <a href="lesson-00.html">Lesson 0</a> teaches just enough Python, NumPy and pandas for the whole course.' if n == 1 else '') + '</p>'
    top += f'<p class="ctx-fit"><strong>Where this fits:</strong> {FIT[n]}</p></div>'
    body = top + body
    pre = running_html(n)
    if n in SEE_ALSO:
        pre += '<p class="see-also">⇄ Compare side by side: ' + "".join(f'<a href="compare.html#{c}">{e(next(x[1] for x in COMPARE if x[0] == c))}</a>' for c in SEE_ALSO[n]) + '</p>'
    if n in USE:
        uses, when, avoid = USE[n]
        pre += '<div class="box use-box"><div class="box-title">Where this is used</div><ul>' + "".join(f"<li>{u}</li>" for u in uses) + '</ul>'
        pre += f'<p><strong>Choose it when:</strong> {when}</p>' + (f'<p><strong>Think twice when:</strong> {avoid}</p>' if avoid != "—" else '') + '</div>'
    if n in MYTHS:
        pre += '<div class="box myths"><div class="box-title">Misconceptions to unlearn</div>' + "".join(f'<div class="myth"><p class="myth-m"><span class="lbl">Myth</span>{m}</p><p class="myth-r"><span class="lbl">Reality</span>{r}</p></div>' for m, r in MYTHS[n]) + '</div>'
    if n in RAI:
        rt, rh = RAI[n]
        pre += f'<div class="box rai"><div class="box-title">Responsible AI · {e(rt)}</div>{rh}</div>'
    if n in FAQ:
        pre += '<h2 id="faq">Questions beginners often ask</h2><div class="faq">' + "".join(f'<div class="faq-item"><p class="faq-q">{q}</p><p class="faq-a">{a}</p></div>' for q, a in FAQ[n]) + '</div>'
    if pre:
        k0 = body.index('<h2 id="summary">')
        body = body[:k0] + pre + body[k0:]
    if n in MISTAKES:
        box = '<div class="box warn mistakes"><div class="box-title">Common mistakes to avoid</div><ul>' + "".join(f"<li>{m}</li>" for m in MISTAKES[n]) + '</ul></div>'
        k = body.index('<h2 id="summary">')
        body = body[:k] + box + body[k:]
    iqs = [q for q in QI if q[1] == n]; pps = [p for p in PI if p[1] == n]
    if iqs or pps:
        box = '<div class="box hidden-q"><div class="box-title">Interview corner</div>'
        if pps:
            box += '<p class="hq-sub"><strong>Don\'t confuse</strong></p><ul class="hq-pairs">' + "".join(f'<li><a href="confused.html#{pid}"><strong>{t}</strong></a> — {h}</li>' for pid, _, t, d, h in pps) + '</ul>'
        if iqs:
            box += '<p class="hq-sub"><strong>Hidden questions</strong> — answer in your head first, then open.</p>' + "".join(
                f'<details class="hq"><summary>{q}</summary><p class="iq-trap"><strong>The trap:</strong> {trap}</p><p>{a}</p></details>' for qid, _, lvl, q, trap, a in iqs[:4])
            box += f'<p class="hq-more"><a href="interview.html#l{n}">All {len(iqs)} hidden questions for this lesson →</a></p>'
        box += '</div>'
        k = body.index('<h2 id="summary">')
        body = body[:k] + box + body[k:]
    if n in EXERCISES:
        def chk(i):
            if (n, i) not in CHECKS: return ""
            fl = [{"label": c[0], "ans": c[1], "hint": c[2], **({"tol": c[3]} if len(c) > 3 else {})} for c in CHECKS[(n, i)]]
            rows = "".join(f'<div class="chk-row"><label><span>{e(c[0])}</span><input type="text" inputmode="decimal" autocomplete="off" spellcheck="false" aria-label="{e(c[0])}"></label><span class="chk-res" aria-live="polite"></span></div>' for c in CHECKS[(n, i)])
            return (f'<div class="chk" data-key="ex-{n}-{i}" data-fields="{e(json.dumps(fl, ensure_ascii=False))}"><p class="chk-lead">Check your answer{"s" if len(fl) > 1 else ""}' +
                    (' — for several numbers, separate them with commas' if any(isinstance(c[1], list) for c in CHECKS[(n, i)]) else '') + ':</p>' + rows +
                    '<button type="button" class="chk-btn">Check</button><p class="chk-hint" aria-live="polite"></p></div>')
        items = "".join(f'<div class="ex"><div class="ex-head"><span class="ex-num">Exercise {i+1}</span><span class="tag">{tag}</span></div><p>{q}</p>{chk(i)}<details><summary>Show solution</summary><div class="ex-sol">{a}</div></details></div>' for i, (tag, q, a) in enumerate(EXERCISES[n]))
        gen = ('<div class="gen" data-gen="' + str(n) + '"><div class="gen-head"><span class="gen-tag">Practice with new numbers</span><span class="gen-title"></span><span class="gen-stats"></span></div>'
               '<p class="gen-q"><noscript>This practice problem needs JavaScript.</noscript></p><div class="gen-fields"></div>'
               '<div class="gen-actions"><button type="button" class="chk-btn">Check</button><button type="button" class="gen-new">New numbers ↻</button><button type="button" class="gen-show">Show worked solution</button></div>'
               '<p class="chk-hint" aria-live="polite"></p><div class="gen-sol" hidden></div></div>')
        body += ('<h2 id="exercises">Practice exercises</h2><p>Work each exercise on paper (or in the lesson notebook), type your answer into the box to check it, and open the solution to compare your working. '
                 'Answers can be decimals (round to 3 places), fractions like <code>2/3</code> or percentages like <code>75%</code>. Every answer has been checked with Python. '
                 f'For hands-on coding practice, the <a href="notebooks/lesson-{n:02d}.ipynb" download>lesson notebook</a> ends with two <strong>coding challenges</strong>: fill in one missing line and an automatic check tells you whether it\'s right.</p><div class="exercises">' + items + '</div>' + gen)
    body = apply_levels(n, body)
    for (ln, sid), sh in SCENE.items():
        if ln == n:
            i = body.index(f'<h2 id="{sid}">'); i = body.index('</h2>', i) + 5
            body = body[:i] + sh + body[i:]
    return body

# ---------------- lessons ----------------
for (n, p, t, s, mins) in [LESSON0] + LESSONS:
    if not ready(n): continue
    body = enrich(n, open(os.path.join(HERE, "lessons", f"{n:02d}.html")).read())
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    k = [0]
    def number(m):
        k[0] += 1
        return f'<h2 id="{m.group(1)}"><span class="sec-num">{k[0]}.</span>{m.group(2)}</h2>'
    body = re.sub(r'<h2 id="([^"]+)">(.*?)</h2>', number, body)
    def tocText(h):
        h = re.sub("<[^>]+>", "", h)
        return re.sub(r"\$([^$]+)\$", lambda m: m.group(1).replace("^2", "²").replace("\\lambda", "λ").replace("\\", ""), h)
    toc = "".join(f'<li><a href="#{i}">{j+1}. {tocText(h)}</a></li>' for j, (i, h) in enumerate(heads))
    obj = "".join(f"<li>{e(o)}</li>" for o in OBJECTIVES.get(n, []))
    srcs = "".join(f"<li>{ext(u, tt)}</li>" for tt, u in SOURCES.get(n, []))
    prev_l = LESSONS[n - 2] if n > 1 else (LESSON0 if n == 1 else None)
    next_l = LESSONS[n] if n < len(LESSONS) else None
    pager = ""
    if prev_l: pager += f'<a class="prev" href="{fname(prev_l[0])}"><small>← Previous</small>Lesson {prev_l[0]}: {e(prev_l[2])}</a>'
    if next_l:
        if ready(next_l[0]): pager += f'<a class="next" href="{fname(next_l[0])}"><small>Next →</small>Lesson {next_l[0]}: {e(next_l[2])}</a>'
        else: pager += f'<a class="next soon"><small>Next (coming soon)</small>Lesson {next_l[0]}: {e(next_l[2])}</a>'
    plabel, ptitle, _ = PARTS[p]
    last_in_part = max(L[0] for L in LESSONS if L[1] == p) == n
    part_end = (f'<div class="box tip part-end"><div class="box-title">You\'ve finished {plabel}: {e(ptitle)}</div><p>Check how well it has stuck with a 15-question mixed test. You\'ll get a score and a list of sections to revisit.</p>'
                f'<p><a class="btn btn-primary" href="tests.html?part={p+1}">Take the {plabel} test →</a> ' + (f'<a class="btn" href="projects.html#{PROJ_BY_PART[p]["id"]}">Do the project: {e(PROJ_BY_PART[p]["title"])}</a> ' if p in PROJ_BY_PART else '') + '<a class="btn" href="review.html">Open spaced review</a></p></div>') if last_in_part else ""
    page = head(f"Lesson {n}: {t} — ML Academy", s, math=True) + f"""<body>
<div class="progress" aria-hidden="true"></div>
<a class="skip" href="#content">Skip to content</a>
<header class="site-header"><div class="container">
<a class="brand" href="index.html" aria-label="ML Academy home"><span class="brand-mark">{LOGO}</span></a>
<a class="back-link" href="index.html#path">‹ Learning path</a>
<span class="page-title-sm">Lesson {n}: {e(t)}</span><span style="margin-left:auto"></span><div class="level-switch" role="group" aria-label="Reading level"><button type="button" data-level="simple" title="Plain-words summaries instead of heavy maths">Simple</button><button type="button" data-level="detailed" title="Everything, including derivations">Detailed</button></div>{nav_html("index.html#path", ["Course map", "Review"], "nav nav-sm")}{A11Y_BTN}{SEARCH_BTN}{THEME_BTN}
</div></header>
<main>
<div class="module-hero"><div class="container">
<div class="eyebrow">{("Before you begin · Optional" if n == 0 else plabel + " · " + e(ptitle))} · Lesson {n:02d} · ~{mins} min</div>
<h1>{e(t)}</h1><p>{e(s)}</p>
<div class="objectives"><h2 class="obj-h">By the end of this lesson you can</h2><ul>{obj}</ul></div>
<div class="lesson-actions"><a class="btn" href="notebooks/lesson-{n:02d}.ipynb" download>⬇ Download Jupyter notebook</a><a class="btn" href="#exercises">Jump to practice exercises</a></div><div class="listen" role="group" aria-label="Listen to this lesson"></div>
</div></div>
<div class="container layout">
<nav class="toc" aria-label="On this page"><div class="toc-title">On this page</div><ol>{toc}</ol></nav>
<article class="prose" id="content">
<div class="route-banner" hidden></div>
{body}
{part_end}<div class="complete-row"><button class="complete-btn" type="button" data-lesson="{n}">Mark lesson as complete</button><span style="color:var(--muted);font-size:.9rem">Saved in this browser.</span></div>
<section class="sources"><h2>Sources used for this lesson</h2><ol>{srcs}</ol></section>
<div class="route-next" hidden></div><nav class="pager" aria-label="Lesson navigation">{pager}</nav>
</article></div></main>
<button class="to-top" type="button" aria-label="Back to top">{UP}</button>
{FOOTER}
</body></html>"""
    open(os.path.join(OUT, fname(n)), "w").write(page)
print("built", n_ready, "lessons")

# ---------------- glossary page ----------------
def page_shell(title, desc, eyebrow, h1, lead, inner, math=False, extra=""):
    return head(title, desc, math=math, demos=False).replace("</head>", extra + "</head>") + f"""<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="container">
<a class="brand" href="index.html"><span class="brand-mark">{LOGO}</span>ML Academy</a>
{nav_html("index.html#path", ["Learning path", "Course map", "Review", "Tests", "Projects"])}
{A11Y_BTN}{SEARCH_BTN}{THEME_BTN}</div></header>
<main id="main">
<div class="module-hero"><div class="container"><div class="eyebrow">{eyebrow}</div><h1>{h1}</h1><p>{lead}</p></div></div>
<div class="container ref-page"><div class="prose wide">{inner}</div></div>
</main>
<button class="to-top" type="button" aria-label="Back to top">{UP}</button>
{FOOTER}
</body></html>"""

letters = sorted({g[0][0].upper() for g in GLOSSARY})
gl = '<div class="az">' + "".join(f'<a href="#g-{L}">{L}</a>' for L in letters) + '</div>'
gl += '<input class="gl-filter" id="gl-filter" type="search" placeholder="Filter terms…" aria-label="Filter glossary terms">'
for L in letters:
    gl += f'<h2 id="g-{L}" class="gl-letter">{L}</h2><dl class="glossary">'
    for term, d, n, sid in sorted([g for g in GLOSSARY if g[0][0].upper() == L], key=lambda g: g[0].lower()):
        gl += f'<div class="gl-item"><dt>{e(term)}</dt><dd>{e(d)} <a class="gl-link" href="{fname(n)}#{sid}">Lesson {n} →</a></dd></div>'
    gl += '</dl>'
gl += """<script>(function(){var f=document.getElementById('gl-filter');f.addEventListener('input',function(){var q=f.value.toLowerCase();document.querySelectorAll('.gl-item').forEach(function(it){it.style.display=it.textContent.toLowerCase().indexOf(q)>-1?'':'none';});document.querySelectorAll('.glossary').forEach(function(dl){var vis=[].some.call(dl.children,function(c){return c.style.display!=='none';});dl.style.display=vis?'':'none';dl.previousElementSibling.style.display=vis?'':'none';});});})();</script>"""
open(os.path.join(OUT, "glossary.html"), "w").write(page_shell("Glossary — ML Academy", "Plain-English definitions of every machine learning term used in the course.", "Reference", "Glossary", f"{len(GLOSSARY)} terms in plain English. Each one links to the lesson section where it's explained in full.", gl))

# ---------------- cheat sheet ----------------
cs = '<p class="no-print"><button class="btn" onclick="window.print()">🖨 Print / save as PDF</button></p><div class="cheat-grid">'
for group, rows in CHEAT:
    cs += f'<section class="cheat"><h2 id="c-{re.sub("[^a-z]+", "-", group.lower())}">{e(group)}</h2><table class="cheat-tbl">'
    for name, tex, note, n in rows:
        cs += f'<tr><th>{e(name)}<a class="gl-link" href="{fname(n)}">L{n}</a></th><td>${tex}$' + (f'<div class="cheat-note">{e(note)}</div>' if note else '') + '</td></tr>'
    cs += '</table></section>'
cs += '</div>'
open(os.path.join(OUT, "cheatsheet.html"), "w").write(page_shell("Cheat sheet — ML Academy", "Every key formula from the course on one printable page.", "Reference", "Formula cheat sheet", "Every key formula from the 21 lessons on one page. Click a lesson tag (L6) to jump to the full explanation. Prints neatly on paper or to PDF.", cs, math=True))

# ---------------- search index ----------------
def plain(h):
    h = re.sub(r'<(svg|script|style)[\s\S]*?</\1>', ' ', h)
    h = re.sub(r'<[^>]+>', ' ', h)
    h = html.unescape(h)
    return re.sub(r'\s+', ' ', h).strip()
IDX = []
for (n, p, t, s_, mins) in [LESSON0] + LESSONS:
    if not ready(n): continue
    body = enrich(n, open(os.path.join(HERE, "lessons", f"{n:02d}.html")).read())
    parts_ = re.split(r'(<h2 id="[^"]+">.*?</h2>)', body)
    IDX.append({"t": f"Lesson {n}: {t}", "s": s_, "u": fname(n), "k": "lesson", "x": (t + " " + s_).lower()})
    for i in range(1, len(parts_), 2):
        m = re.match(r'<h2 id="([^"]+)">(.*?)</h2>', parts_[i])
        sid, title = m.group(1), plain(m.group(2))
        txt = plain(parts_[i + 1]) if i + 1 < len(parts_) else ""
        IDX.append({"t": title, "s": f"Lesson {n} · " + txt[:140], "u": f"{fname(n)}#{sid}", "k": "section", "x": (title + " " + txt[:2500]).lower()})
QUAL = {"error", "parameter", "statistics", "cnn", "svm", "k-fold"}
def aliases(term):
    out = []
    for part in term.split(" / "):
        m = re.match(r"^(.*?)\s*\((.*?)\)\s*$", part)
        if m:
            out.append(m.group(1).strip())
            if m.group(2).lower() not in QUAL: out.append(m.group(2).strip())
        else:
            out.append(part.strip())
    return out
_counts = {}
for term, *_ in GLOSSARY:
    for a in aliases(term): _counts[a.lower()] = _counts.get(a.lower(), 0) + 1
for term, d, n, sid in GLOSSARY:
    al = [a for a in aliases(term) if _counts[a.lower()] == 1 and len(a) >= 3]
    IDX.append({"t": term, "s": "Glossary · " + d, "u": f"glossary.html", "k": "term", "x": (term + " " + d).lower(), "l": f"{fname(n)}#{sid}", "a": al, "d": d, "n": n})
for cid, ct, core, *_ in COMPARE:
    IDX.append({"t": ct, "s": "Comparison · " + plain(core)[:140], "u": f"compare.html#{cid}", "k": "section", "x": (ct + " compare vs versus difference " + plain(core)).lower()})
for P_ in PROJECTS:
    IDX.append({"t": "Project: " + P_["title"], "s": "Project · " + P_["goal"], "u": "projects.html#" + P_["id"], "k": "section", "x": ("project " + P_["title"] + " " + P_["goal"] + " " + plain(P_["data"])).lower()})
IDX.append({"t": "My progress", "s": "Dashboard: lessons completed, quiz scores, exercises, tests, time and badges per part.", "u": "progress.html", "k": "lesson", "x": "progress dashboard badges score time statistics stats completed"})
for rid_, name_, blurb_, ls_ in ROUTES:
    IDX.append({"t": "Route: " + name_, "s": f"{len(ls_)} lessons · " + blurb_, "u": f"map.html?route={rid_}", "k": "section", "x": ("route path learning path " + name_ + " " + blurb_).lower()})
IDX.append({"t": "Printable workbook (PDF)", "s": f"All {len(LESSONS)} lessons with exercises, space for working and answers at the back.", "u": "workbook/ML-Academy-workbook.pdf", "k": "lesson", "x": "workbook pdf print printable paper offline book exercises answers"})
IDX.append({"t": "End-of-part tests", "s": "Practice · a 15-question mixed test for each part, with explanations and links to weak areas.", "u": "tests.html", "k": "lesson", "x": "test exam end of part practice score quiz"})
IDX.append({"t": "Spaced review", "s": "Practice · quiz questions from earlier lessons come back at growing intervals.", "u": "review.html", "k": "lesson", "x": "review spaced repetition revise revision flashcards remember quiz"})
IDX.append({"t": "Which model should I use?", "s": "Decision guide · answer a few questions and get a recommended algorithm and the lessons to read.", "u": "guide.html", "k": "lesson", "x": "which model should i use algorithm decision guide choose choosing estimator flowchart recommend"})
open(os.path.join(OUT, "assets", "search-index.js"), "w").write("window.MLA_INDEX=" + json.dumps(IDX, ensure_ascii=False, separators=(",", ":")) + ";")
print("search entries", len(IDX))

# ---------------- course map ----------------
COLW, ROWH, NW, NH = 230, 92, 196, 70
pos = {}
for pi in range(len(PARTS)):
    ls = [L for L in LESSONS if L[1] == pi]
    for k, L in enumerate(ls):
        pos[L[0]] = (20 + pi * COLW, 70 + k * ROWH)
Wmap, Hmap = 20 + len(PARTS) * COLW, 70 + 6 * ROWH + 10
edges = ""
for n, ds in DEPS.items():
    x2, y2 = pos[n]
    for d in ds:
        x1, y1 = pos[d]
        if x1 == x2:   # same column: curve on the left
            edges += f'<path class="m-edge" data-from="{d}" data-to="{n}" d="M{x1},{y1+NH/2} C{x1-30},{y1+NH/2} {x2-30},{y2+NH/2} {x2},{y2+NH/2}"/>'
        else:
            sx, sy, ex, ey = x1 + NW, y1 + NH / 2, x2, y2 + NH / 2
            edges += f'<path class="m-edge" data-from="{d}" data-to="{n}" d="M{sx},{sy} C{sx+40},{sy} {ex-40},{ey} {ex},{ey}"/>'
SHORT = ["Foundations", "Supervised basics", "Classic algorithms", "Unsupervised", "Neural nets & projects"]
nodes = "".join(f'<text x="{20 + i * COLW + NW/2}" y="40" class="m-part">{i+1} · {e(SHORT[i])}</text>' for i in range(len(PARTS)))
for (n, p, t, s_, mins) in LESSONS:
    x, y = pos[n]
    words, lines, cur = t.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > 24 and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    lines.append(cur)
    if len(lines) > 2: lines = [lines[0], " ".join(lines[1:])[:22] + "…"]
    tl = "".join(f'<tspan x="{x+14}" dy="{0 if k == 0 else 16}">{e(L)}</tspan>' for k, L in enumerate(lines))
    nodes += f'<a href="{fname(n)}" class="m-node" data-lesson="{n}"><rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="12"/><text x="{x+14}" y="{y+20}" class="m-num">LESSON {n:02d}</text><text x="{x+14}" y="{y+40}" class="m-title">{tl}</text><title>{e(t)} — {e(s_)}</title></a>'
mapsvg = f'<div class="map-wrap"><svg class="course-map" viewBox="0 0 {Wmap} {Hmap}" role="group" aria-label="Map of the 21 lessons and how they depend on each other">{edges}{nodes}</svg></div>'
legend = '<p class="map-legend"><span class="lg lg-done"></span> completed <span class="lg lg-todo"></span> not yet <span class="lg-line"></span> "builds on" — hover a lesson to highlight its connections.</p>'
tbl = '<h2 id="dependencies">Every lesson and what it builds on</h2><table class="tbl"><thead><tr><th>Lesson</th><th>Builds on</th></tr></thead><tbody>' + "".join(
    f'<tr><td><a href="{fname(n)}">{n}. {e(t)}</a></td><td>' + (", ".join(f'<a href="{fname(d)}">{d}. {e(LESSONS[d-1][2])}</a>' for d in DEPS[n]) or "— (start here)") + '</td></tr>' for (n, p, t, s_, m) in LESSONS) + '</tbody></table>'
mapjs = """<script>(function(){var done=[];try{done=JSON.parse(localStorage.getItem('mla-done')||'[]');}catch(e){}
document.querySelectorAll('.m-node').forEach(function(a){var n=a.getAttribute('data-lesson');if(done.indexOf(n)>-1)a.classList.add('done');
a.addEventListener('mouseenter',function(){document.querySelectorAll('.m-edge').forEach(function(p){if(p.getAttribute('data-from')===n||p.getAttribute('data-to')===n)p.classList.add('hot');});});
a.addEventListener('mouseleave',function(){document.querySelectorAll('.m-edge.hot').forEach(function(p){p.classList.remove('hot');});});});})();</script>"""
routepick = '<div class="route-pick" role="group" aria-label="Highlight a learning route"><span>Highlight a route:</span><button type="button" class="btn" data-route="">All lessons</button>' + "".join(f'<button type="button" class="btn" data-route="{rid}">{e(name)} ({len(ls)})</button>' for rid, name, blurb, ls in ROUTES) + '</div>'
intro = '<p>Read the map left to right: each column is one part of the course, and each line means "this lesson builds on that one". The suggested order is simply 1 → 21, but if you want to jump to a topic, follow the lines back to see what to review first.</p>'
open(os.path.join(OUT, "map.html"), "w").write(page_shell("Course map — ML Academy", "How the 21 lessons connect: a visual map of prerequisites.", "Reference", "Course map", "All 21 lessons and how they build on each other. Click any lesson to open it.", intro + routepick + legend + mapsvg + '<div class="route-panel" aria-live="polite"></div>' + tbl + mapjs))
print("map built")

# ---------------- comparison page ----------------
chips = '<nav class="cmp-chips" aria-label="Comparisons">' + "".join(f'<a href="#{c[0]}">{e(c[1])}</a>' for c in COMPARE) + '</nav>'
cmp = '<p>Beginners often mix up pairs of ideas that look alike. Each section below puts two of them side by side: the one-sentence difference, a picture computed with real models, a comparison table and when to choose each.</p>' + chips
for cid, ct, core, (an, bn), rows, ca, cb, ls in COMPARE:
    cmp += f'<section class="cmp" id="{cid}"><h2>{e(ct)}</h2><p class="core">{core}</p>'
    if cid in CMP_FIGS:
        cmp += f'<figure class="fig">{CMP_FIGS[cid]}<figcaption>{e(CMP_CAPS[cid])}</figcaption></figure>'
    cmp += f'<div class="table-scroll"><table class="tbl cmp-tbl"><thead><tr><td></td><th>{e(an)}</th><th>{e(bn)}</th></tr></thead><tbody>'
    cmp += "".join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows) + '</tbody></table></div>'
    cmp += f'<div class="cmp-choose"><div><b>Choose {e(an.split(" (")[0])} when…</b>{ca}</div><div><b>Choose {e(bn.split(" (")[0])} when…</b>{cb}</div></div>'
    cmp += '<p class="cmp-lessons">Learn more: ' + " · ".join(f'<a href="{fname(l)}">Lesson {l}: {e(LESSONS[l-1][2])}</a>' for l in ls) + '</p></section>'
open(os.path.join(OUT, "compare.html"), "w").write(page_shell("Compare — ML Academy", "Side-by-side comparisons of machine learning ideas beginners often confuse.", "Understanding", "Side-by-side comparisons", "Eight pairs of ideas that are easy to mix up, compared point by point.", cmp, math=True))

# ---------------- decision guide ----------------
gdata = {"q": GQ, "r": GR, "titles": [L[2] for L in LESSONS]}
gall = '<div class="g-all"><h2 id="all">Every recommendation at a glance</h2><p>The same advice as the questions above, as one list you can scan or print.</p>'
labels = {}
def trail(k, path):
    if k in GR: labels.setdefault(k, []).append(path); return
    for opt, _, nx in GQ[k][2]: trail(nx, path + [opt])
trail("start", [])
for rk, (rt, models, read, watch) in GR.items():
    gall += f'<h3>{e(rt)}</h3><p class="cmp-lessons">When: ' + " <em>or</em> ".join(" → ".join(e(x) for x in p) for p in labels[rk]) + '</p><ul>' + "".join(f'<li><strong>{e(m)}</strong> — {e(w)} (<a href="{fname(l)}">Lesson {l}</a>)</li>' for m, l, w in models) + f'</ul><p><strong>Watch out:</strong> {e(watch)}</p>'
gall += '</div>'
gsrc = '<section class="sources"><h2>Sources</h2><p>The questions and the sample-size thresholds follow scikit-learn\'s estimator flowchart, simplified for beginners and linked to this course\'s lessons.</p><ol>' + "".join(f"<li>{ext(u, t)}</li>" for t, u in GUIDE_SOURCES) + '</ol></section>'
ginner = ('<div class="box tip"><div class="box-title">How to use this</div><p>Answer a few questions about your problem and you\'ll get a short list of algorithms to try, in order, with the lessons that explain them. '
          'It is a starting point, not a rule: in practice you try two or three candidates and let cross-validation decide.</p></div>'
          '<div id="guide" aria-live="polite"><noscript><p>The interactive guide needs JavaScript; every recommendation is listed below.</p></noscript></div>' + gall + gsrc)
gextra = '<script>window.MLA_GUIDE=' + json.dumps(gdata, ensure_ascii=False) + ';</script><script defer src="assets/guide.js"></script>'
open(os.path.join(OUT, "guide.html"), "w").write(page_shell("Which model should I use? — ML Academy", "An interactive guide that recommends a machine learning algorithm for your problem.", "Understanding", "Which model should I use?", "A few questions about your data and goal lead to the algorithms worth trying first.", ginner, extra=gextra))
print("compare + guide built")

# ---------------- question bank, tests and review pages ----------------
QB = {}
def sec_title(n, sid):
    b = open(os.path.join(HERE, "lessons", f"{n:02d}.html")).read()
    m = re.search(r'<h2 id="' + re.escape(sid) + r'">(.*?)</h2>', b)
    return re.sub(r"<[^>]+>", "", m.group(1)).replace("$R^2$", "R²").replace("$k$", "k").replace("$", "") if m else sid
for (n, p, t, s_, mins) in LESSONS:
    b = open(os.path.join(HERE, "lessons", f"{n:02d}.html")).read()
    for k, m in enumerate(re.finditer(r'<div class="q" data-correct="([a-d])"><p class="q-text">(.*?)</p>(.*?)<div class="q-explain">(.*?)</div></div>', b, re.S)):
        opts = re.findall(r'<button data-opt="([a-d])">(.*?)</button>', m.group(3), re.S)
        QB[f"L{n}-{k}"] = {"n": n, "s": "quiz", "st": "Check your understanding", "q": re.sub(r"^\d+\.\s*", "", m.group(2).strip()),
                           "o": [o[1] for o in opts], "c": [o[0] for o in opts].index(m.group(1)), "x": m.group(4).strip()}
for p_, qs in TESTS.items():
    for k, (n, sid, q, opts, c, x) in enumerate(qs):
        QB[f"P{p_+1}-{k}"] = {"n": n, "s": sid, "st": sec_title(n, sid), "q": q, "o": opts, "c": c, "x": x}
assert sum(1 for k in QB if k[0] == "L") == 105, sum(1 for k in QB if k[0] == "L")
open(os.path.join(OUT, "assets", "qbank.js"), "w").write("window.MLA_QBANK=" + json.dumps(QB, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + ";")
parts_js = [{"label": pl, "title": pt, "lessons": [L[0] for L in LESSONS if L[1] == i]} for i, (pl, pt, _) in enumerate(PARTS)]
qextra = '<script defer src="assets/qbank.js"></script><script>window.MLA_PARTS=' + json.dumps(parts_js, ensure_ascii=False) + ';</script>'
tinner = ('<div class="box tip"><div class="box-title">How the tests work</div><p>Each part ends with a 15-question test mixing all of its lessons. The questions are new — not the ones from the lesson quizzes — and the answer order is shuffled every time. '
          'After you submit you get your score, an explanation for every question, and links to the exact sections to re-read. Your best score is saved in this browser.</p></div>'
          '<div id="tests-app" aria-live="polite"><noscript><p>The tests need JavaScript.</p></noscript></div>')
open(os.path.join(OUT, "tests.html"), "w").write(page_shell("End-of-part tests — ML Academy", "A 15-question mixed test for each of the five parts of the course, with explanations and links to weak areas.", "Practice", "End-of-part tests", "Five mixed tests, one per part. Find out what has stuck and what to revisit.", tinner, math=True, extra=qextra))
rinner = ('<div class="box tip"><div class="box-title">Why spaced review?</div><p>We forget most new material within days unless we recall it again — and recalling it just as it starts to fade makes it stick much longer. '
          'This page brings back quiz questions at growing intervals: questions you answer correctly return less and less often; ones you miss come back the next day. '
          'Everything is saved in this browser only.</p></div><div id="review-app" aria-live="polite"><noscript><p>Spaced review needs JavaScript.</p></noscript></div>')
open(os.path.join(OUT, "review.html"), "w").write(page_shell("Spaced review — ML Academy", "Review quiz questions from earlier lessons at growing intervals so they stick.", "Practice", "Spaced review", "A few minutes a day of recalling earlier lessons, scheduled so you review each idea just before you'd forget it.", rinner, math=True, extra=qextra))
print("tests + review built,", len(QB), "questions in the bank")

# ---------------- projects page ----------------
pj = ('<p>Four guided projects on real datasets — one at the end of each part from Part 2 on. Each comes as two Jupyter notebooks: a <strong>starter</strong> where you write the key lines '
      '(marked <code># TODO</code>, with an automatic check after every step) and a complete <strong>solution</strong> with all outputs. '
      'The datasets ship with scikit-learn, so nothing needs downloading.</p>')
pj += '<div class="box tip"><div class="box-title">All the code in one download</div><p>Prefer plain Python scripts to notebooks? <a class="btn" href="downloads/ml-academy-code.zip" download>⬇ Download all the code (.zip)</a> — the four projects as starter and solution <code>.py</code> files, every lesson\'s code, the coding challenges and a <code>pytest</code> suite that checks everything runs and gives the published results.</p></div>'
pj += '<nav class="cmp-chips" aria-label="Projects">' + "".join(f'<a href="#{P["id"]}">{e(P["title"])}</a>' for P in PROJECTS) + '</nav>'
for P in PROJECTS:
    pl, pt, _ = PARTS[P["part"]]
    pj += f'<section class="proj" id="{P["id"]}"><p class="eyebrow">{pl} · {e(pt)}</p><h2>{e(P["title"])}</h2><p class="core">{e(P["goal"])}</p>'
    pj += f'<p><strong>The data.</strong> {P["data"]}</p>'
    pj += '<div class="proj-grid"><div><h3>You will practise</h3><ul>' + "".join(f"<li>{e(x)}</li>" for x in P["skills"]) + '</ul>'
    pj += '<p class="cmp-lessons">Uses: ' + " · ".join(f'<a href="{fname(l)}">Lesson {l}</a>' for l in P["lessons"]) + '</p></div>'
    pj += '<div><h3>Steps</h3><ol class="proj-steps">' + "".join(f"<li>{e(st[0])}</li>" for st in P["steps"]) + '</ol></div></div>'
    pj += '<details class="proj-res"><summary>What the solution finds (open after you\'ve tried)</summary><table class="tbl"><tbody>' + "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in PROJ_RES[P["id"]]) + '</tbody></table></details>'
    pj += f'<p class="proj-dl"><a class="btn btn-primary" href="notebooks/projects/{P["id"]}-starter.ipynb" download>⬇ Starter notebook</a> <a class="btn" href="notebooks/projects/{P["id"]}-solution.ipynb" download>⬇ Solution notebook</a></p>'
    pj += '<p class="cmp-lessons"><strong>Go further:</strong> ' + " ".join(P["further"]) + '</p></section>'
pj += ('<section class="sources"><h2>Dataset sources</h2><ol>'
       '<li>Efron, Hastie, Johnstone &amp; Tibshirani (2004), "Least Angle Regression", <em>Annals of Statistics</em> — diabetes data. ' + ext("https://scikit-learn.org/stable/datasets/toy_dataset.html#diabetes-dataset", "scikit-learn: diabetes dataset") + '</li>'
       '<li>Street, Wolberg &amp; Mangasarian (1993), Wisconsin Diagnostic Breast Cancer. ' + ext("https://scikit-learn.org/stable/datasets/toy_dataset.html#breast-cancer-wisconsin-diagnostic-dataset", "scikit-learn: breast cancer dataset") + '</li>'
       '<li>Forina et al., wine recognition data (UCI). ' + ext("https://scikit-learn.org/stable/datasets/toy_dataset.html#wine-recognition-dataset", "scikit-learn: wine dataset") + '</li>'
       '<li>Alpaydin &amp; Kaynak, optical recognition of handwritten digits (UCI). ' + ext("https://scikit-learn.org/stable/datasets/toy_dataset.html#optical-recognition-of-handwritten-digits-dataset", "scikit-learn: digits dataset") + '</li></ol></section>')
open(os.path.join(OUT, "projects.html"), "w").write(page_shell("Projects — ML Academy", "Four guided machine learning projects on real datasets, with starter and solution notebooks.", "Practice", "Mini-projects", "Put each part of the course to work on a real dataset, step by step, with automatic checks.", pj))
print("projects page built")

# ---------------- notebook download helpers (work on file:// too) ----------------
import glob as _glob
_n = 0
for _f in _glob.glob(os.path.join(OUT, "notebooks", "**", "*.ipynb"), recursive=True):
    _rel = os.path.relpath(_f, OUT).replace(os.sep, "/")
    _txt = open(_f, encoding="utf-8").read()
    open(_f + ".js", "w", encoding="utf-8").write("window.MLA_NB=window.MLA_NB||{};window.MLA_NB[" + json.dumps(_rel) + "]=" + json.dumps(_txt).replace("</", "<\\/") + ";\n")
    _n += 1
print("notebook download helpers:", _n)

# ---------------- accessibility post-pass: name every figure's SVG after its caption ----------------
def _label_figs(h):
    def fix(m):
        fig = m.group(0)
        cap = re.search(r"<figcaption>(.*?)</figcaption>", fig, re.S)
        if not cap: return fig
        label = html.escape(re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", cap.group(1)))).strip(), quote=True)
        def svgfix(sm):
            tag = sm.group(0)
            if "aria-label" in tag or "aria-labelledby" in tag: return tag
            if 'role="img"' not in tag: tag = tag.replace("<svg", '<svg role="img"', 1)
            return tag.replace("<svg", f'<svg aria-label="{label}"', 1)
        return re.sub(r"<svg\b[^>]*>", svgfix, fig, count=1)
    return re.sub(r'<figure class="fig(?! walk)[^"]*">.*?</figure>', fix, h, flags=re.S)
_c = 0
for _f in _glob.glob(os.path.join(OUT, "*.html")):
    _h = open(_f, encoding="utf-8").read(); _h2 = _label_figs(_h)
    if _h2 != _h: open(_f, "w", encoding="utf-8").write(_h2); _c += 1
print("figure labels added in", _c, "pages")

# ---------------- printable workbook (HTML source for the PDF) ----------------
def _wb_body(n):
    b = enrich(n, open(os.path.join(HERE, "lessons", f"{n:02d}.html")).read())
    k = [0]
    def num(m):
        k[0] += 1; return f'<h2 id="l{n}-{m.group(1)}"><span class="sec-num">{k[0]}.</span>{m.group(2)}</h2>'
    b = re.sub(r'<h2 id="([^"]+)">(.*?)</h2>', num, b)
    b = re.sub(r'\sid="(?!l\d+-)([^"]+)"', lambda m: f' id="l{n}-{m.group(1)}"', b)
    b = re.sub(r'href="#([^"]+)"', lambda m: f'href="#l{n}-{m.group(1)}"', b)
    b = b.replace('url(#', f'url(#l{n}-').replace('aria-labelledby="', f'aria-labelledby="l{n}-')
    return b
wb_toc = "".join(f'<li><a href="#lesson-{n}">Lesson {n}: {e(t)}</a></li>' for (n, p, t, s_, m) in [LESSON0] + LESSONS)
wb = []
for (n, p, t, s_, mins) in [LESSON0] + LESSONS:
    pl, pt, _ = ("Before you begin", "Optional", "") if n == 0 else PARTS[p]
    obj = "".join(f"<li>{e(o)}</li>" for o in OBJECTIVES.get(n, []))
    wb.append(f'<section class="wb-lesson prose" id="lesson-{n}" data-n="{n}" data-title="{e(t)}"><p class="eyebrow">{pl} · {e(pt)} · ~{mins} min</p>'
              f'<h1>Lesson {n}: {e(t)}</h1><p class="lead">{e(s_)}</p><div class="objectives"><h4>By the end of this lesson you can</h4><ul>{obj}</ul></div>{_wb_body(n)}</section>')
wb_html = f"""<!doctype html>
<html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ML Academy — Printable workbook</title><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="assets/icon-32.png" sizes="32x32" type="image/png"><link rel="alternate icon" href="assets/favicon.ico"><link rel="apple-touch-icon" href="assets/icon-180.png"><meta name="theme-color" content="#0f2e1d">
<link rel="stylesheet" href="assets/webfonts.css"><link rel="stylesheet" href="assets/base.css"><link rel="stylesheet" href="assets/katex.min.css"><link rel="stylesheet" href="assets/workbook.css">
<script defer src="assets/katex.min.js"></script><script defer src="assets/auto-render.min.js"></script><script defer src="assets/workbook.js"></script>
</head><body class="wb-body">
<section class="wb-cover"><p class="eyebrow">ML Academy</p><h1>Machine learning from zero</h1><p class="lead">The printable workbook: Lesson 0 and all {len(LESSONS)} lessons with maths, worked examples, code, quizzes and exercises — with space to work by hand. Answers are at the back.</p>
<div class="box tip"><div class="box-title">How to use this workbook</div><ul><li>Read a lesson, then try its quiz and exercises in the boxes provided before checking the answers at the back.</li><li>Interactive demos, animations and automatic answer checking live on the website (open <i>index.html</i> in the course folder); the workbook points to them.</li><li>Every code example can be run from the lesson's Jupyter notebook in the <i>notebooks</i> folder.</li></ul></div>
<h2>Contents</h2><ol class="wb-toc">{wb_toc}<li><a href="#wb-answers">Answers to quizzes and exercises</a></li></ol></section>
{''.join(wb)}
<section class="wb-appendix" id="wb-answers"><h1>Answers</h1></section>
</body></html>"""
open(os.path.join(OUT, "workbook.html"), "w", encoding="utf-8").write(wb_html)
print("workbook page built")

# ---------------- data for routes and the progress dashboard ----------------
from context import DEPS as _DEPS
_routes = []
for rid, name, blurb, ls in ROUTES:
    skipped = sorted({d for l in ls for d in _DEPS.get(l, []) if d not in ls})
    _routes.append({"id": rid, "name": name, "blurb": blurb, "lessons": ls, "skipped": skipped, "mins": sum(LESSONS[l-1][4] for l in ls)})
_data = {"lessons": [{"n": n, "t": t, "p": p, "mins": m, "ex": [f"ex-{n}-{i}" for i in range(len(EXERCISES.get(n, []))) if (n, i) in CHECKS], "nex": len(EXERCISES.get(n, []))} for (n, p, t, s_, m) in LESSONS],
         "parts": [{"label": pl, "title": pt} for pl, pt, _ in PARTS], "routes": _routes,
         "deps": {str(k): v for k, v in _DEPS.items()}}
open(os.path.join(OUT, "assets", "routes.js"), "w").write("window.MLA_DATA=" + json.dumps(_data, ensure_ascii=False) + ";")

# ---------------- progress dashboard page ----------------
pg_inner = ('<div id="progress-app" aria-live="polite"><noscript><p>The dashboard needs JavaScript.</p></noscript></div>')
open(os.path.join(OUT, "progress.html"), "w").write(page_shell("My progress — ML Academy", "Your lessons, quiz scores, exercises, tests, time and badges, saved in this browser.", "Progress", "My progress", "Everything you've done in the course, part by part. Saved only in this browser — download it below to keep a copy.", pg_inner))
print("progress page built")

# ---------------- my notes page ----------------
open(os.path.join(OUT, "notes.html"), "w").write(page_shell("My notes — ML Academy", "Your highlights and notes from every lesson, saved in this browser.", "Notes", "My notes", "Everything you've highlighted or written, lesson by lesson. Click a quote to jump back to it.", '<div id="notes-app" aria-live="polite"><noscript><p>Notes need JavaScript.</p></noscript></div>'))
IDX.append({"t": "My notes", "s": "Your highlights and lesson notes, with a Markdown export.", "u": "notes.html", "k": "lesson", "x": "notes highlights highlight annotate my notes markdown"})
open(os.path.join(OUT, "assets", "search-index.js"), "w").write("window.MLA_INDEX=" + json.dumps(IDX, ensure_ascii=False, separators=(",", ":")) + ";")
print("notes page built")

# ---------------- recent developments page ----------------
_rb = RECENT.BODY.replace('\\"', '"').replace("{REVIEWED}", RECENT.REVIEWED)
_rb += '<section class="sources"><h2>Sources</h2><ol>' + "".join(f"<li>{ext(u, t)}</li>" for t, u in RECENT.SOURCES) + '</ol></section>'
open(os.path.join(OUT, "recent.html"), "w").write(page_shell("Recent developments — ML Academy", "A dated overview of large language models and generative AI, connected back to the course.", "Beyond the course · last reviewed " + RECENT.REVIEWED, "Recent developments in LLMs and generative AI", "How today's language models, reasoning models, agents and image generators work — and how each idea connects to what you've learned.", _rb))
IDX.append({"t": "Recent developments in LLMs and generative AI", "s": "Dated overview (" + RECENT.REVIEWED + "): LLMs, reasoning models, agents, RAG, diffusion, risks, EU AI Act.", "u": "recent.html", "k": "lesson", "x": "recent developments llm large language model generative ai chatgpt reasoning agents rag diffusion eu ai act regulation transformer gpt"})
open(os.path.join(OUT, "assets", "search-index.js"), "w").write("window.MLA_INDEX=" + json.dumps(IDX, ensure_ascii=False, separators=(",", ":")) + ";")
print("recent page built")

# ---------------- what next page ----------------
_nb = NEXTP.BODY + '<section class="sources"><h2>Resources mentioned</h2><ol>' + "".join(f"<li>{ext(u, t)}</li>" for t, u in NEXTP.SOURCES) + '</ol></section>'
open(os.path.join(OUT, "next.html"), "w").write(page_shell("What next — ML Academy", "Your learning plan after the course: directions, a 12-week plan, project ideas and free resources.", "Beyond the course", "What next: your learning plan", "You've learned the foundations. Here's how to turn them into real skill: choose a direction, follow a 12-week plan, build projects and keep learning.", _nb))
IDX.append({"t": "What next: your learning plan", "s": "Career directions, a 12-week plan, project ideas and free books and courses.", "u": "next.html", "k": "lesson", "x": "what next learning plan career path roadmap projects books courses resources after the course study plan"})
open(os.path.join(OUT, "assets", "search-index.js"), "w").write("window.MLA_INDEX=" + json.dumps(IDX, ensure_ascii=False, separators=(",", ":")) + ";")
print("next page built")

# ---------------- interview questions & confused terms ----------------
_ALL_L = [LESSON0] + LESSONS
def _ltitle(n): return next(x[2] for x in _ALL_L if x[0] == n)
iqh = ('<div class="iq-tools" role="group" aria-label="Filter questions">'
       '<label>Part <select id="iq-part"><option value="">All parts</option>' + "".join(f'<option value="{i}">{e(p[0])}: {e(p[1])}</option>' for i, p in enumerate(PARTS)) + '<option value="g">General &amp; production</option></select></label>'
       '<label>Level <select id="iq-lvl"><option value="">All levels</option>' + "".join(f'<option value="{k}">{v}</option>' for k, v in IQ_LEVELS.items()) + '</select></label>'
       '<label class="iq-chk"><input type="checkbox" id="iq-hide"> Hide the ones I know</label>'
       '<span class="iq-count" aria-live="polite"></span></div>'
       '<p class="iq-how">Read each question and answer it out loud or on paper <em>before</em> opening the answer. Each answer starts with <strong>the trap</strong> — the tempting wrong answer — then the real one. Tick <em>I know this</em> to track your progress (saved in this browser).</p>')
_part_of = {x[0]: x[1] for x in _ALL_L}
for n in sorted({q[1] for q in QI}, key=lambda v: (v if isinstance(v, int) else 99)):
    qs = [q for q in QI if q[1] == n]
    head_ = f"Lesson {n}: {e(_ltitle(n))}" if isinstance(n, int) else "General &amp; production"
    part = _part_of.get(n, "g") if isinstance(n, int) else "g"
    iqh += f'<section class="iq-sec" data-part="{part}"><h2 id="l{n}">{head_}</h2>'
    for qid, _, lvl, q, trap, a in qs:
        link = f'<a href="{fname(n)}">Revisit Lesson {n} →</a>' if isinstance(n, int) else ''
        iqh += (f'<div class="iq" id="{qid}" data-lvl="{lvl}"><div class="iq-top"><span class="iq-lvl lvl-{lvl}">{IQ_LEVELS[lvl]}</span>'
                f'<label class="iq-known"><input type="checkbox" data-q="{qid}"> I know this</label></div><p class="iq-q">{q}</p>'
                f'<details><summary>Show answer</summary><p class="iq-trap"><strong>The trap:</strong> {trap}</p><div class="iq-a"><p>{a}</p>{("<p class=iq-link>" + link + "</p>") if link else ""}</div></details></div>')
    iqh += '</section>'
iqh += '<script defer src="assets/interview.js"></script>'
open(os.path.join(OUT, "interview.html"), "w").write(page_shell("Hidden interview questions — ML Academy", "Tricky machine-learning interview questions with the trap explained and the real answer.", "Interview practice", "Hidden interview questions",
     f"{len(QI)} questions that sound simple but hide a trap — the ones you only discover in an interview. Think first, then reveal.", iqh, math=True))
cfh = '<input class="gl-filter" id="cf-filter" type="search" placeholder="Filter terms…" aria-label="Filter confused terms">'
for i, p in enumerate(PARTS):
    ps = [x for x in PI if isinstance(x[1], int) and _part_of.get(x[1]) == i]
    if not ps: continue
    cfh += f'<h2 id="part{i+1}">{e(p[0])}: {e(p[1])}</h2><div class="cf-grid">'
    for pid, n, t, d, h in ps:
        cfh += f'<div class="cf" id="{pid}"><h3>{t}</h3><p>{d}</p><p class="cf-hook"><span>Remember:</span> {h}</p><p class="cf-link"><a href="{fname(n)}">Lesson {n} →</a></p></div>'
    cfh += '</div>'
_gp = [x for x in PI if not isinstance(x[1], int)]
if _gp:
    cfh += '<h2 id="general">General &amp; production</h2><div class="cf-grid">' + "".join(f'<div class="cf" id="{pid}"><h3>{t}</h3><p>{d}</p><p class="cf-hook"><span>Remember:</span> {h}</p></div>' for pid, n, t, d, h in _gp) + '</div>'
cfh += """<script>(function(){var f=document.getElementById('cf-filter');f.addEventListener('input',function(){var q=f.value.toLowerCase();document.querySelectorAll('.cf').forEach(function(c){c.style.display=c.textContent.toLowerCase().indexOf(q)>-1?'':'none';});document.querySelectorAll('.cf-grid').forEach(function(g){var v=[].some.call(g.children,function(c){return c.style.display!=='none';});g.style.display=v?'':'none';g.previousElementSibling.style.display=v?'':'none';});});})();</script>"""
open(os.path.join(OUT, "confused.html"), "w").write(page_shell("Commonly confused terms — ML Academy", "Pairs of machine-learning terms that are easy to mix up, with the difference and a way to remember it.", "Interview practice", "Commonly confused terms",
     f"{len(PI)} pairs of terms that people mix up — even experienced practitioners. Each has the difference in plain words and a one-line way to remember it.", cfh, math=True))
_strip = lambda h: re.sub(r"<[^>]+>|\$", "", h)
IDX.append({"t": "Hidden interview questions", "s": f"{len(QI)} tricky questions with the trap explained.", "u": "interview.html", "k": "lesson", "x": "interview questions tricky hidden trap gotcha job prepare"})
IDX.append({"t": "Commonly confused terms", "s": f"{len(PI)} easily mixed-up pairs of terms.", "u": "confused.html", "k": "lesson", "x": "confused terms difference versus vs mix up"})
for qid, n, lvl, q, trap, a in QI: IDX.append({"t": _strip(q)[:140], "s": "Interview question" + (f" · Lesson {n}" if isinstance(n, int) else ""), "u": f"interview.html#{qid}", "k": "iq", "x": _strip(a)[:200].lower()})
for pid, n, t, d, h in PI: IDX.append({"t": _strip(t), "s": "Confused terms" + (f" · Lesson {n}" if isinstance(n, int) else ""), "u": f"confused.html#{pid}", "k": "iq", "x": _strip(d)[:200].lower()})
open(os.path.join(OUT, "assets", "search-index.js"), "w").write("window.MLA_INDEX=" + json.dumps(IDX, ensure_ascii=False, separators=(",", ":")) + ";")
print("interview pages built:", len(QI), "questions,", len(PI), "pairs")

# ---------------- tools, versions & changelog ----------------
import changelog as CHANGELOG
from importlib import metadata as _md
os.makedirs(os.path.join(OUT, "tools"), exist_ok=True)
shutil.copy(os.path.join(HERE, "tools", "check_outputs.py"), os.path.join(OUT, "tools", "check_outputs.py"))
_vers = {"python": sys.version.split()[0]}
for _p in ["numpy", "pandas", "scikit-learn", "matplotlib", "scipy", "nbclient", "nbformat"]:
    try: _vers[_p] = _md.version(_p)
    except _md.PackageNotFoundError: _vers[_p] = "not installed"
_vp = os.path.join(OUT, "tools", "versions.json")
_old = json.load(open(_vp)) if os.path.exists(_vp) else {}
if _old.get("versions") != _vers or _old.get("release") != CHANGELOG.RELEASES[0][0]:
    json.dump({"release": CHANGELOG.RELEASES[0][0], "date": CHANGELOG.RELEASES[0][1], "versions": _vers}, open(_vp, "w"), indent=1)
_rep = os.path.join(OUT, "tools", "check_report.md")
_chk = ""
if os.path.exists(_rep):
    _l = open(_rep, encoding="utf-8").read().splitlines()
    _when = _l[0].replace("# Output check — ", "") if _l else ""
    _sum = re.sub(r"\*\*", "", _l[2]) if len(_l) > 2 else ""
    _chk = f'<p><strong>Last output check:</strong> {e(_when)} — {e(_sum)}</p>'
ch = '<h2 id="versions">Library versions</h2><p>Every code output and notebook in the course was produced with these versions, in a Linux environment:</p>'
ch += '<div class="table-scroll"><table class="tbl"><thead><tr><th>Package</th><th>Version</th></tr></thead><tbody>' + "".join(f"<tr><td>{e(k)}</td><td><code>{e(v)}</code></td></tr>" for k, v in _vers.items()) + '</tbody></table></div>'
ch += ('<p>Newer versions usually give the same results, but defaults and random-number details occasionally change. If your numbers differ slightly from a lesson, compare these versions with yours '
       '(<code>import sklearn; print(sklearn.__version__)</code>).</p>')
ch += ('<h2 id="checks">Automated output checks</h2>' + _chk +
       '<p>The course folder includes <code>tools/check_outputs.py</code>. It re-runs all 22 lesson notebooks and 8 project notebooks in a temporary copy, compares every printed output with the published one (allowing for tiny rounding differences), checks that lesson outputs still match what the lesson page shows, and writes <code>tools/check_report.md</code>. '
       'It also compares your library versions with the ones above. Nothing in the course is changed.</p>'
       '<pre><code>cd ML\npython tools/check_outputs.py            # everything, about 2 minutes\npython tools/check_outputs.py --only 6 8   # just Lessons 6 and 8</code></pre>'
       '<p>Run it after upgrading scikit-learn, NumPy or pandas. It needs <code>numpy pandas scikit-learn matplotlib nbformat nbclient ipykernel</code>.</p>')
ch += '<h2 id="history">What changed and when</h2>' + "".join(f'<section class="rel"><h3 id="v{e(v)}">Version {e(v)} <span class="rel-date">{e(d)}</span></h3><ul>' + "".join(f"<li>{x}</li>" for x in items) + '</ul></section>' for v, d, items in CHANGELOG.RELEASES)
ch += '<h2 id="known">Known gaps</h2><ul>' + "".join(f"<li>{x}</li>" for x in CHANGELOG.NOTES) + '</ul>'
open(os.path.join(OUT, "changelog.html"), "w").write(page_shell("Changelog & versions — ML Academy", "What changed in the course and when, the library versions the outputs were produced with, and how to re-check them.", "About the course", "Changelog &amp; versions",
     f"Version {CHANGELOG.RELEASES[0][0]}, {CHANGELOG.RELEASES[0][1]}. What changed and when, the exact library versions behind every output, and an automated way to re-check them.", ch))
IDX.append({"t": "Changelog & versions", "s": "What changed and when, library versions and the automated output checker.", "u": "changelog.html", "k": "lesson", "x": "changelog version history what changed library versions scikit-learn numpy check outputs"})
open(os.path.join(OUT, "assets", "search-index.js"), "w").write("window.MLA_INDEX=" + json.dumps(IDX, ensure_ascii=False, separators=(",", ":")) + ";")
print("changelog built, release", CHANGELOG.RELEASES[0][0])

shutil.copy(os.path.join(HERE, "site_README.md"), os.path.join(OUT, "README.md"))
shutil.copy(os.path.join(HERE, "site_requirements.txt"), os.path.join(OUT, "requirements.txt"))
print("README and requirements copied")

shutil.copy(os.path.join(HERE, "site_gitignore"), os.path.join(OUT, ".gitignore"))
