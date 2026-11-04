# Lesson 23: Hyperparameter Tuning & Model Selection. Patches the shared per-lesson dictionaries on import.
import context, extras_ex_b, checks, running_code, running_text, challenges, reference, understanding, rai

L23 = (23, 5, "Hyperparameter Tuning & Model Selection", "Validation curves, grid and random search, Bayesian optimisation, successive halving, nested CV and choosing the simplest good model.", 55)

OBJ23 = ["Tell parameters from hyperparameters and read a validation curve",
         "Run grid and random search over a pipeline, and explain why random search usually wins",
         "Describe Bayesian optimisation and successive halving, and when to use them",
         "Report a tuned model's performance honestly and pick the simplest good model"]

SRC23 = [("scikit-learn — Tuning the hyper-parameters of an estimator", "https://scikit-learn.org/stable/modules/grid_search.html"),
         ("Bergstra & Bengio (2012) — Random Search for Hyper-Parameter Optimization, JMLR", "https://www.jmlr.org/papers/v13/bergstra12a.html"),
         ("Snoek, Larochelle & Adams (2012) — Practical Bayesian Optimization of Machine Learning Algorithms", "https://arxiv.org/abs/1206.2944"),
         ("Li et al. (2018) — Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization, JMLR", "https://jmlr.org/papers/v18/16-558.html"),
         ("Cawley & Talbot (2010) — On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation, JMLR", "https://www.jmlr.org/papers/v11/cawley10a.html"),
         ("Hastie, Tibshirani & Friedman — The Elements of Statistical Learning, section 7.10 (the one-standard-error rule)", "https://hastie.su.domains/ElemStatLearn/"),
         ("Optuna — documentation", "https://optuna.readthedocs.io/")]

context.DEPS[23] = [5, 10, 15]
context.REFRESH[23] = "Hyperparameters are chosen by cross-validation on training data; random search covers them better than grids, and nested CV gives the honest score."
context.FIT[23] = "Turns the scattered advice on choosing k, λ, depth, C and γ from Lessons 10–15 into one systematic, honest procedure for any model."
context.USE[23] = (["Getting the most out of gradient boosting, SVMs and neural networks",
                    "Fair comparisons between candidate models before deployment",
                    "AutoML systems, which automate exactly this search"],
                   "Whenever a model has settings that strongly affect its accuracy, which is almost always.",
                   "the dataset is tiny: heavy tuning on little data mostly fits noise, so prefer simple models with sensible defaults.")
context.FAQ[23] = [
    ("Which hyperparameters should I tune first?",
     "The ones with the biggest effect: regularization strength (λ, C), learning rate and the number of iterations or trees (with early stopping), and model capacity (depth, number of leaves, k, γ). Library defaults for the rest are usually fine."),
    ("How many random-search trials do I need?",
     "A useful fact: with 60 random trials, there's a 95% chance at least one lands in the best 5% of the search space (because $1 - 0.95^{60} \\approx 0.95$). Start with 20–60 and increase if results are still improving."),
    ("Is it OK to tune on the test set if I'm careful?",
     "No. Any decision based on test results makes them optimistic. Tune with cross-validation on training data and look at the test set once, at the end."),
    ("Should I tune the preprocessing too?",
     "Yes, if it matters: imputation strategy, the number of PCA components or polynomial degree can all go in the same search, using pipeline names like <code>pca__n_components</code>."),
]
understanding.MYTHS[23] = [
    ("The best cross-validated score from a search is what the model will achieve.", "It's the best of many tries, so it's optimistic. Report nested CV or an untouched test set."),
    ("Grid search is more thorough than random search.", "It's exhaustive only over the few values you listed. For the same budget random search tests many more values of each hyperparameter."),
    ("More tuning always helps.", "On small datasets heavy tuning fits the noise in the validation folds. Gains below the CV standard error are usually not real."),
]
extras_ex_b.MISTAKES[23] = [
    "Choosing hyperparameters by looking at test-set scores.",
    "Searching learning rates or penalties on a linear scale instead of a log scale.",
    "Scaling or selecting features outside the cross-validation loop, so tuning leaks.",
    "Reporting the best search score as the final performance.",
    "Picking a complex model for a gain smaller than the score's standard error.",
]
extras_ex_b.EX[23] = [
    ("By hand", "A grid has 5 values of $C$, 4 of $\\gamma$ and 2 kernels, with 10-fold cross-validation. How many fits does it run, including the final refit?",
     "$5 \\times 4 \\times 2 = 40$ settings $\\times 10 = 400$ fits, plus 1 refit: 401."),
    ("By hand", "How many random trials do you need for a 90% chance that at least one lands in the best 5% of the space? (Solve $1 - 0.95^n \\ge 0.9$.)",
     "$0.95^n \\le 0.1$ gives $n \\ge \\ln 0.1/\\ln 0.95 = 44.9$, so 45 trials."),
    ("By hand", "Successive halving starts 81 candidates with factor 3, each on 10 rows. How many candidates and rows per candidate are there in rounds 2, 3 and 4?",
     "Round 2: 27 candidates on 30 rows; round 3: 9 on 90; round 4: 3 on 270."),
    ("By hand", "Cross-validated scores: depth 2: 0.90, depth 3: 0.93, depth 5: 0.94 (the best, standard error 0.015), depth 8: 0.935. Which depth does the one-standard-error rule pick?",
     "Threshold $0.94 - 0.015 = 0.925$. The simplest depth at or above it is depth 3 (0.93)."),
    ("Code", "Change the lesson's tuning recipe to optimise accuracy instead of ROC-AUC (<code>scoring=\"accuracy\"</code>). Does the chosen $C$ change?",
     "It can: different metrics reward different trade-offs, so the best $C$ often moves. Always tune on the metric you'll actually report and use (Lesson 9)."),
]
checks.CHECKS[(23, 0)] = [("Fits including refit", 401, "settings × folds + 1.")]
checks.CHECKS[(23, 1)] = [("Trials needed", 45, "Round ln(0.1)/ln(0.95) up.")]
checks.CHECKS[(23, 2)] = [("Candidates in rounds 2, 3, 4", [27, 9, 3], "Divide by 3 each round."), ("Rows per candidate in rounds 2, 3, 4", [30, 90, 270], "Multiply by 3 each round.")]
checks.CHECKS[(23, 3)] = [("Depth chosen", 3, "Find the simplest depth scoring at least best − SE.")]

challenges.C[23] = [
    ("Count the grid", "Compute how many model fits a 5-fold grid search over this grid performs (not counting the refit).",
     'grid = {"C": [0.1, 1, 10], "gamma": [0.01, 0.1, 1, 10], "kernel": ["rbf", "sigmoid"]}\nfolds = 5\n##BLANK##',
     'fits', 'fits = len(grid["C"]) * len(grid["gamma"]) * len(grid["kernel"]) * folds', "Multiply the number of values of each hyperparameter, then by the number of folds.",
     'fits = len(grid) * folds  # ← replace: count every combination'),
    ("Log-scale samples", "Draw 5 learning rates spread evenly on a log scale from 0.001 to 1.",
     'import numpy as np\n##BLANK##\nresult = [round(float(v), 4) for v in rates]',
     'result', 'rates = np.logspace(-3, 0, 5)', "np.logspace(start, stop, num) uses powers of ten: 10**-3 to 10**0.",
     'rates = np.linspace(0.001, 1, 5)  # ← replace with a log-spaced version'),
]

reference.GLOSSARY += [
    ("Hyperparameter", "A setting chosen before training that controls how a model learns, such as λ, k, tree depth or the learning rate.", 23, "why"),
    ("Validation curve", "A plot of training and cross-validated scores against one hyperparameter, showing underfitting and overfitting.", 23, "curves"),
    ("Random search", "Hyperparameter search that samples settings from distributions; usually more efficient than a grid for the same budget.", 23, "random"),
    ("Bayesian optimisation", "Hyperparameter search that fits a surrogate model of the score and chooses each next setting to balance exploration and exploitation.", 23, "smarter"),
    ("Successive halving", "A search that trains many candidates on a small budget and repeatedly keeps the best fraction with a larger budget.", 23, "smarter"),
    ("One-standard-error rule", "Choose the simplest model whose cross-validated score is within one standard error of the best.", 23, "choosing"),
]

rai.RAI[23] = ("Tune for the right objective",
    "<p>A search optimises exactly the metric you give it and nothing else. If the overall score improves while performance for a small group gets worse, the search won't notice. Include subgroup metrics and calibration in the final comparison (Lesson 21), and record what was tried, so results can be reproduced and checked.</p>")
