# Lesson 13 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("How to cut a tree back properly (cost-complexity pruning, chosen by cross-validation), why the feature "
          "importances that tree libraries print can rank pure noise highly (use permutation importance instead), "
          "and why a small change in the data can produce a completely different tree, which is the weakness "
          "random forests fix.")

QUIZ = [
    ("In cost-complexity pruning, what does a larger $\\alpha$ do?",
     [("a", "Grows a bigger tree"), ("b", "Charges more per leaf, so the tree becomes smaller"), ("c", "Changes the impurity measure")], "b",
     "$R_\\alpha(T) = R(T) + \\alpha|\\text{leaves}|$: a higher price per leaf favours smaller trees."),
    ("Why can impurity-based importance rank a random ID column highly?",
     [("a", "IDs are always useful"), ("b", "Features with many distinct values offer many split points, some of which fit training noise"), ("c", "It's computed on test data")], "b",
     "It's measured on training data and favours high-cardinality features."),
    ("Permutation importance measures…",
     [("a", "How much the held-out score drops when one feature's values are shuffled"), ("b", "How many splits use the feature"), ("c", "The feature's correlation with the target")], "a",
     "Shuffling breaks the feature's link to the target; a useful feature's absence hurts the score."),
    ("Two strongly correlated features are both useful. What can permutation importance show for each?",
     [("a", "Both look very important"), ("b", "Both can look unimportant, because the model falls back on the partner"), ("c", "It always picks the right one")], "b",
     "Shuffling one leaves the other, so the score barely drops. Group correlated features or use other methods."),
    ("Why are single decision trees unstable?",
     [("a", "Greedy top splits change with small data changes, and everything below depends on them"), ("b", "They use random numbers"), ("c", "They need feature scaling")], "a",
     "This high variance is exactly what bagging and random forests average away."),
]

IQ = [
    (3, "How would you prune a decision tree, and how do you choose how much?",
     "Only mentioning max_depth.",
     "Grow the full tree, then apply cost-complexity (weakest-link) pruning: minimise training error + $\\alpha$ × number of leaves. Increasing $\\alpha$ gives a nested sequence of subtrees. Pick $\\alpha$ by cross-validation (often the simplest tree within one standard error of the best score). Pre-pruning limits (max_depth, min_samples_leaf) are cheaper alternatives, but they can stop before a useful deeper split."),
    (3, "Your stakeholder asks which features drive the model. What do you report, and what caveats do you give?",
     "Pasting the default feature_importances_ bar chart.",
     "Use permutation importance on held-out data (or SHAP values for per-prediction explanations), with error bars from repeats. Caveats: correlated features share or hide importance, so group them; importance describes what the model uses, not what causes the outcome; and results depend on the model, so a different good model might rank features differently."),
    (2, "Why do people say random forests fix the weaknesses of decision trees?",
     "\"Because more trees is better.\"",
     "A deep tree has low bias but high variance: small data changes give very different trees. Averaging many trees trained on bootstrap samples (bagging), with random feature subsets at each split to make them less correlated, cancels much of that variance while keeping low bias. The price is interpretability and some speed."),
]

EX = [
    ("Intermediate", "A tree with 10 leaves has training error 0.05. Pruning one branch gives 7 leaves with training error 0.08. For which values of $\\alpha$ is the pruned tree preferred?",
     "Compare $0.05 + 10\\alpha$ with $0.08 + 7\\alpha$. The pruned tree wins when $0.08 + 7\\alpha &lt; 0.05 + 10\\alpha$, i.e. $\\alpha &gt; 0.03/3 = 0.01$."),
    ("Intermediate", "A node holds 40 positives and 60 negatives. A split sends 30 positives and 10 negatives left, and 10 positives and 50 negatives right. Compute the Gini impurity before the split and the weighted Gini after it.",
     "Before: $1 - (0.4^2 + 0.6^2) = 0.48$. Left (40 cases): $1 - (0.75^2 + 0.25^2) = 0.375$. Right (60 cases): $1 - ((1/6)^2 + (5/6)^2) = 0.2778$. Weighted: $0.4 \\times 0.375 + 0.6 \\times 0.2778 = 0.3167$. The decrease is $0.163$."),
    ("Intermediate", "A model scores 0.90 on test data. After shuffling feature A it scores 0.84, and after shuffling feature B, 0.90. What are the two permutation importances, and what might B's value mean?",
     "A: $0.90 - 0.84 = 0.06$. B: $0$. B may be useless, or it may be correlated with another feature the model can use instead."),
]

CHECKS = {
    0: [("Smallest α at which pruning wins", 0.01, "Set 0.05 + 10α equal to 0.08 + 7α.")],
    1: [("Gini before", 0.48, "1 − (p₊² + p₋²)."), ("Weighted Gini after", 0.31667, "Weight each child by its share of cases.")],
    2: [("Importance of A", 0.06, "Score drop."), ("Importance of B", 0, "Score drop.")],
}
