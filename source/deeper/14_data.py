# Lesson 14 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("Why averaging many trees works only if they disagree (correlation sets the limit), how to tune boosting "
          "with a learning rate and early stopping, what XGBoost, LightGBM and CatBoost add to plain gradient "
          "boosting, and when combining different models (stacking) is worth it.")

QUIZ = [
    ("Averaging 1,000 trees that are perfectly correlated ($\\rho = 1$) reduces variance by…",
     [("a", "A factor of 1,000"), ("b", "Nothing"), ("c", "Half")], "b",
     "$\\rho\\sigma^2 + (1-\\rho)\\sigma^2/B = \\sigma^2$ when $\\rho = 1$. Identical trees give no benefit."),
    ("In a random forest, lowering <code>max_features</code>…",
     [("a", "Makes trees more alike"), ("b", "Makes trees less correlated but each one weaker"), ("c", "Has no effect")], "b",
     "Fewer candidate features per split means more disagreement between trees, at the cost of individual accuracy."),
    ("If you halve gradient boosting's learning rate, you usually need about…",
     [("a", "Half as many trees"), ("b", "Twice as many trees"), ("c", "The same number of trees")], "b",
     "Each tree corrects half as much. Let early stopping pick the exact number."),
    ("XGBoost's leaf value $w^* = -\\sum g_i / (\\sum h_i + \\lambda)$ uses…",
     [("a", "Only gradients"), ("b", "Gradients and second derivatives (curvature), plus an L2 penalty"), ("c", "Random numbers")], "b",
     "It's a regularized Newton step for each leaf."),
    ("Why must a stacking blender be trained on out-of-fold predictions?",
     [("a", "It's faster"), ("b", "Predictions on training rows are over-optimistic, so the blender would learn from leaked information"), ("c", "Scikit-learn requires it")], "b",
     "Base models fit their own training rows too well; the blender needs predictions like those on new data."),
]

IQ = [
    (3, "What does XGBoost do differently from classic gradient boosting?",
     "\"It's just faster.\"",
     "It optimises a regularized objective with a second-order (Newton) approximation: each point contributes a gradient $g_i$ and curvature $h_i$, leaf values have the closed form $-\\sum g/(\\sum h + \\lambda)$, and a split's gain must exceed $\\gamma$ (a cost per leaf). It also learns default directions for missing values, uses column and row subsampling, and is engineered for parallel, sparse and out-of-core data."),
    (2, "How would you tune a gradient-boosted model in limited time?",
     "Grid-searching everything at once.",
     "Fix a moderate learning rate (0.05–0.1) and use early stopping on a validation set to pick the number of trees. Then tune tree complexity (max_depth or num_leaves, min samples per leaf), then subsampling (rows and columns) and L2 regularization, using random or Bayesian search with cross-validation. Finally, lower the learning rate, raise the tree limit, and refit with early stopping for a small final gain."),
    (3, "Why does a random forest choose features randomly at each split, in terms of the variance formula?",
     "\"To be random.\"",
     "The variance of an average of $B$ trees is $\\rho\\sigma^2 + (1-\\rho)\\sigma^2/B$. Adding trees only shrinks the second term; the first, set by the correlation $\\rho$ between trees, remains. Bootstrap samples alone leave trees highly correlated, because the strongest features dominate every tree's top splits. Random feature subsets lower $\\rho$, and so the floor, at the cost of slightly weaker individual trees."),
]

EX = [
    ("Intermediate", "Trees have variance $\\sigma^2 = 1$ and pairwise correlation $\\rho = 0.3$. What is the variance of the average of 10 trees, and the limit as the number of trees grows without bound?",
     "$0.3 + 0.7/10 = 0.37$. As $B \\to \\infty$: $0.3$."),
    ("Intermediate", "A leaf contains points with gradients $g = (0.4, -0.2, 0.6)$ and curvatures $h = (0.24, 0.16, 0.24)$. With $\\lambda = 1$, compute XGBoost's leaf value.",
     "$\\sum g = 0.8$, $\\sum h = 0.64$. $w^* = -0.8/(0.64 + 1) = -0.488$."),
    ("Intermediate", "Gradient boosting with learning rate 0.1 stops early at 300 trees. Roughly how many trees would you expect at learning rate 0.05?",
     "About twice as many, around 600. Each tree's contribution is halved."),
]

CHECKS = {
    0: [("Variance with 10 trees", 0.37, "ρσ² + (1 − ρ)σ²/B."), ("Limit", 0.3, "Let B grow without bound.")],
    1: [("Leaf value", -0.4878, "−Σg / (Σh + λ).")],
    2: [("Expected trees", 600, "Halving the rate roughly doubles the trees.", 60)],
}
