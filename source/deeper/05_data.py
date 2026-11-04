# Lesson 5 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("When the usual validation habits quietly break: tuning makes your best score look better than it really "
          "is (nested cross-validation fixes it), time series and repeated customers need special splits, learning "
          "curves tell you whether more data would help, and adversarial validation detects when new data no longer "
          "looks like your training data.")

QUIZ = [
    ("You try 200 hyperparameter settings and report the best cross-validated score. That score is probably…",
     [("a", "Slightly too optimistic"), ("b", "Exactly right"), ("c", "Too pessimistic")], "a",
     "Picking the best of many includes some luck. Nested cross-validation (or an untouched test set) gives an honest estimate."),
    ("Which split suits forecasting next month's sales?",
     [("a", "Shuffled k-fold"), ("b", "A time-ordered split: train on the past, validate on later dates"), ("c", "Leave-one-out")], "b",
     "Split the way the model will be used: it will always predict the future from the past."),
    ("A learning curve shows training accuracy 0.99 and validation accuracy 0.80, with validation still rising as data grows. What's likely to help?",
     [("a", "More data or more regularization"), ("b", "A more complex model"), ("c", "Nothing will help")], "a",
     "A large gap that is still closing is high variance: more data or a simpler (more regularized) model helps."),
    ("In adversarial validation, a classifier separates training rows from new rows with AUC 0.95. What does that mean?",
     [("a", "Your model is excellent"), ("b", "The new data differs a lot from the training data"), ("c", "There is label leakage")], "b",
     "If train and new rows were alike, telling them apart would be impossible (AUC ≈ 0.5)."),
    ("Your dataset has 10 rows per patient. Which cross-validation should you use?",
     [("a", "KFold with shuffle"), ("b", "GroupKFold with patient as the group"), ("c", "StratifiedKFold")], "b",
     "Keep each patient's rows together, so the model is scored on patients it has never seen."),
]

IQ = [
    (3, "What's nested cross-validation, and when do you need it?",
     "Thinking the best grid-search score is an unbiased estimate.",
     "Two loops: an inner CV chooses hyperparameters using only the training part of each outer fold, and the outer CV scores the whole \"tune then fit\" procedure on data the tuning never saw. You need it when you want an honest performance estimate for a tuned model and don't have a separate test set. The best inner score is biased upwards, more so with many settings and little data."),
    (3, "Your model scores R² = 0.95 in cross-validation but fails badly in production a month later. List likely causes.",
     "Blaming bad luck.",
     "Leakage (a feature that won't exist at prediction time, or preprocessing fitted on all data). A split that doesn't match use, such as shuffled folds on time-ordered data or the same customer on both sides. Distribution shift, where production inputs differ from training (check with adversarial validation). Overfitting to the validation set through many tuning rounds. Fix: time-based or group splits, pipelines, a final untouched test set and drift monitoring."),
    (2, "How do you decide whether collecting more data is worth it?",
     "\"More data always helps.\"",
     "Plot a learning curve: train and validation scores against training-set size. If the validation score is still rising and there's a big gap to training (high variance), more data should help. If both are low and close together (high bias), more data won't, and you need better features or a more flexible model. You can extrapolate the curve's trend to estimate the gain."),
    (3, "What's the difference between covariate shift, label shift and concept drift?",
     "Using \"data drift\" for all three.",
     "Covariate shift: the distribution of inputs $P(x)$ changes but $P(y\\mid x)$ stays the same. Label shift: the class balance $P(y)$ changes but $P(x\\mid y)$ stays. Concept drift: the relationship $P(y\\mid x)$ itself changes. Covariate shift can be detected without labels (adversarial validation, statistical tests on features); concept drift needs fresh labels to detect, and usually retraining to fix."),
]

EX = [
    ("Intermediate", "A grid search tries 3 values of <code>C</code> and 4 values of <code>gamma</code>, with 5-fold inner CV inside a 5-fold outer CV. How many models are trained in total, not counting refits?",
     "Each outer fold runs $3 \\times 4 = 12$ settings × 5 inner folds $= 60$ fits. Five outer folds: $5 \\times 60 = 300$ fits. (Scikit-learn also refits the best setting once per outer fold, making 305.)"),
    ("Intermediate", "<code>TimeSeriesSplit(n_splits=4)</code> on 100 rows uses test blocks of 20 rows each. How many rows are in the training set of the first split, and of the last?",
     "The test blocks are rows 21–40, 41–60, 61–80 and 81–100. The first split trains on rows 1–20 (20 rows); the last trains on rows 1–80 (80 rows). The training window grows, and testing is always on later data."),
    ("Intermediate", "On a learning curve, the training score is 0.72 and the validation score 0.70 at every training size from 1,000 to 50,000 rows. Is the model suffering from high bias or high variance, and would 10 times more data help?",
     "High bias: both scores are low and the gap is tiny, and adding data hasn't moved them. Ten times more data is very unlikely to help. Try richer features or a more flexible model."),
    ("Code · intermediate", "In the time-series code, change the forest to <code>LinearRegression()</code> and re-run both splits. Which split changes more, and why?",
     "Shuffled k-fold drops to about $R^2 = 0.51$ and the time-ordered split collapses to about $-8.26$. A straight line in time extrapolates the wandering trend confidently and badly. Shuffled CV still flatters the model by a huge margin; only the time-ordered split shows that neither model can forecast this trend."),
]

CHECKS = {
    0: [("Total fits (without refits)", 300, "outer folds × settings × inner folds.")],
    3: [("Time-ordered R² for LinearRegression", -8.26, "Use cv=TimeSeriesSplit(5).", 0.05)],
    1: [("Training rows, first split", 20, "Training is everything before the first test block."), ("Training rows, last split", 80, "Everything before rows 81–100.")],
}
