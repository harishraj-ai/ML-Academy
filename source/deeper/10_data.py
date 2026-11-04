# Lesson 10 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("Regularization in practice: bias and variance measured by simulation, the simple rule that makes lasso "
          "set weights to exactly zero, choosing the penalty automatically with cross-validation, why lasso is "
          "unstable with correlated features (elastic net fixes it), why stopping training early acts like a "
          "penalty, and why very large models can generalise well again (double descent).")

QUIZ = [
    ("With $\\lambda = 2$, what does lasso's soft-thresholding turn a least-squares value of $1.5$ into?",
     [("a", "0"), ("b", "0.5"), ("c", "0.75")], "a",
     "$|1.5| - 2 &lt; 0$, so the weight becomes exactly 0. (Ridge would give $1.5/3 = 0.5$.)"),
    ("As $\\lambda$ grows, what happens to bias² and variance?",
     [("a", "Both fall"), ("b", "Bias² rises and variance falls"), ("c", "Bias² falls and variance rises")], "b",
     "A stronger penalty makes models simpler and more alike: more bias, less variance."),
    ("Why prefer elastic net over lasso when features come in correlated groups?",
     [("a", "It's faster"), ("b", "Its L2 part spreads weight across correlated features instead of picking one arbitrarily"), ("c", "It never sets weights to zero")], "b",
     "Lasso's choice within a correlated group is unstable; elastic net tends to keep the group together."),
    ("How is early stopping related to ridge regression?",
     [("a", "It isn't"), ("b", "Fewer gradient steps from zero keep weights small, much like a stronger L2 penalty"), ("c", "It's the same as lasso")], "b",
     "Roughly, $k$ steps with learning rate $\\eta$ act like ridge with $\\lambda \\approx 1/(k\\eta)$."),
    ("In double descent, where does test error peak?",
     [("a", "Near the point where the model can just fit the training data exactly"), ("b", "At the simplest model"), ("c", "At the largest model")], "a",
     "At the interpolation threshold there's a single, usually wild, exact fit. With many more parameters, the smoothest exact fit is chosen."),
]

IQ = [
    (3, "Describe how coordinate descent solves the lasso.",
     "Saying it uses gradient descent (the L1 penalty isn't differentiable at 0).",
     "Cycle through the weights one at a time. For weight $j$, compute the least-squares value it would take given the current residuals (with the other weights fixed), then apply soft-thresholding: shrink it towards 0 by $\\lambda$ and set it to exactly 0 if it would cross. Update the residuals and move on. Repeat until the weights stop changing. Each step is closed-form, so it's fast, and warm starts make fitting a whole path of $\\lambda$ values cheap."),
    (3, "How would you check whether the features lasso selected are trustworthy?",
     "Trusting a single fit's non-zero weights.",
     "Refit on many bootstrap samples (or CV folds) and record how often each feature is selected. This is the idea of stability selection. Features chosen in, say, over 80% of fits are robust; ones that flip are usually members of a correlated group. Check correlations or VIFs, and consider elastic net or reporting the group rather than one member."),
    (2, "Can you show that bias and variance trade off, rather than just asserting it?",
     "Only drawing the U-curve.",
     "Simulate: draw many training sets from the same distribution, fit the model to each, and evaluate at fixed test points. Bias² is the squared gap between the average prediction and the truth; variance is the spread of the predictions across fits. Sweeping model complexity or $\\lambda$ shows bias² falling and variance rising as the model becomes more flexible, with the total error minimised in between."),
    (3, "Is early stopping really a form of regularization? Explain.",
     "\"It just saves time.\"",
     "Yes. Starting from small weights, gradient descent first fits the strongest, smoothest patterns (large-eigenvalue directions) and only later the weak, noisy ones. Stopping early leaves the weights small along those weak directions, which is the same effect ridge has. For linear least squares the equivalence is approximately $\\lambda \\approx 1/(k\\eta)$ for $k$ steps. The number of epochs (or of boosting rounds) is therefore a regularization hyperparameter, chosen on validation data."),
]

EX = [
    ("Intermediate", "With $\\lambda = 0.5$ and standardised features, apply lasso soft-thresholding and ridge shrinkage $z/(1+\\lambda)$ to the least-squares values $z = 2$, $0.4$ and $-1$. Give the lasso values.",
     "Lasso: $2 - 0.5 = 1.5$; $0.4 &lt; 0.5$ so $0$; $-1 + 0.5 = -0.5$. Ridge: $2/1.5 = 1.333$, $0.4/1.5 = 0.267$, $-1/1.5 = -0.667$."),
    ("Intermediate", "In a simulation, the average prediction at a test point is 4.2, the true value is 5.0, and predictions across training sets have standard deviation 0.6. The noise variance is 0.25. Compute bias², variance and the expected squared error at that point.",
     "Bias² $= (4.2 - 5.0)^2 = 0.64$. Variance $= 0.6^2 = 0.36$. Expected error $= 0.64 + 0.36 + 0.25 = 1.25$."),
    ("Intermediate", "Elastic net with $\\lambda = 2$ and <code>l1_ratio</code> $\\rho = 0.25$: what are the effective L1 and L2 penalty strengths, using $\\lambda\\rho\\lVert\\mathbf{w}\\rVert_1 + \\lambda\\frac{1-\\rho}{2}\\lVert\\mathbf{w}\\rVert_2^2$?",
     "L1: $2 \\times 0.25 = 0.5$. L2: $2 \\times 0.75/2 = 0.75$."),
    ("Code · intermediate", "In the correlated-features code, change <code>Lasso(alpha=1.0)</code> to <code>ElasticNet(alpha=1.0, l1_ratio=0.5)</code> inside the bootstrap loop. How often is each pattern chosen now?",
     "Elastic net keeps both features in essentially all 200 bootstrap samples, with similar weights each time. The L2 part removes the arbitrary choice between near-duplicates."),
]

CHECKS = {
    0: [("Lasso values", [1.5, 0, -0.5], "Shrink each towards 0 by 0.5; stop at 0.")],
    1: [("Bias²", 0.64, "(average prediction − truth)²."), ("Variance", 0.36, "Square the standard deviation."), ("Expected error", 1.25, "Add the noise variance too.")],
    3: [("Samples where both features are kept (of 200)", 200, "Count the 'both' entry.")],
    2: [("L1 strength", 0.5, "λ × ρ."), ("L2 strength", 0.75, "λ × (1 − ρ) / 2.")],
}
