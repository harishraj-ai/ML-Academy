# Lesson 8 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("Logistic regression seen as a probability model: why its loss has a single lowest point, how libraries "
          "solve it in a few Newton steps, what scikit-learn's C setting means, whether its probabilities can be "
          "trusted (calibration), and what to do when the class you care about is rare.")

QUIZ = [
    ("In scikit-learn's <code>LogisticRegression</code>, what does a smaller <code>C</code> do?",
     [("a", "Weakens regularization"), ("b", "Strengthens regularization"), ("c", "Changes the threshold")], "b",
     "$C = 1/\\lambda$: a smaller $C$ means a larger penalty on the weights."),
    ("A model says 0.9 for 100 cases, and 60 of them are actually positive. The model is…",
     [("a", "Over-confident (badly calibrated)"), ("b", "Well calibrated"), ("c", "Under-confident")], "a",
     "Well calibrated would mean about 90 of the 100 were positive."),
    ("Why does logistic regression's Hessian guarantee a single minimum?",
     [("a", "It's $X^\\top S X$ with positive weights, so it is positive semi-definite and the loss is convex"), ("b", "It's always diagonal"), ("c", "It's always the identity")], "a",
     "A PSD Hessian everywhere means the loss is convex."),
    ("<code>class_weight=\"balanced\"</code> on data with 5% positives usually…",
     [("a", "Raises recall and pushes the average predicted probability well above 5%"), ("b", "Leaves predictions unchanged"), ("c", "Makes the probabilities better calibrated")], "a",
     "It trades calibration for recall. Moving the threshold is the alternative that keeps honest probabilities."),
    ("Which metric measures calibration and sharpness together?",
     [("a", "Accuracy"), ("b", "ROC-AUC"), ("c", "Brier score")], "c",
     "AUC and accuracy depend only on how the scores are ordered or thresholded, not on whether the probability values are right."),
]

IQ = [
    (3, "How does scikit-learn solve logistic regression, and why doesn't it use plain gradient descent?",
     "Assuming everything is trained with gradient descent.",
     "The loss is smooth and convex, so second-order methods converge in a few dozen iterations. The default solver, L-BFGS, builds a low-memory approximation of the Hessian; Newton-CG and IRLS use the exact Hessian $X^\\top S X$. Coordinate-descent solvers (liblinear, saga) handle L1 penalties and very large sparse data. Plain gradient descent would need careful learning rates and far more steps."),
    (3, "What is calibration, how do you measure it, and how do you fix a badly calibrated model?",
     "Confusing calibration with accuracy or AUC.",
     "A model is calibrated if predictions of $p$ come true about a fraction $p$ of the time. Measure it with a reliability diagram (binned predictions vs observed rates), the Brier score, or expected calibration error. Fix it on held-out data with Platt scaling (a sigmoid fitted to the scores) or isotonic regression. Random forests, boosted trees, SVM scores and naive Bayes often need it; logistic regression usually doesn't, unless it was class-weighted or heavily regularized."),
    (2, "You have 1% fraud. Would you rather resample the data, reweight the classes, or change the threshold?",
     "Saying resampling is always required.",
     "All three shift the precision–recall trade-off. Reweighting or resampling changes training, which can help the model focus on rare cases but distorts its probabilities. Threshold moving keeps a calibrated model and picks the cut-off from the cost of each error type, which is usually the simplest and most transparent. Whatever you choose, evaluate with precision–recall metrics, not accuracy, and resample only inside training folds."),
    (2, "Why does logistic regression need regularization on perfectly separable data?",
     "\"To prevent overfitting\" with no mechanism.",
     "If a line separates the classes perfectly, making the weights larger always reduces log loss, because the sigmoid becomes steeper and every probability moves closer to 0 or 1. The optimum is at infinity, so training never converges and the probabilities become extreme. An L2 penalty gives a finite, unique answer."),
]

EX = [
    ("Intermediate", "Three training points have predicted probabilities $0.5$, $0.9$ and $0.99$. Compute each point's Hessian weight $p(1-p)$. Which one shapes the curvature most?",
     "$0.5 \\times 0.5 = 0.25$; $0.9 \\times 0.1 = 0.09$; $0.99 \\times 0.01 = 0.0099$. The uncertain point ($p = 0.5$) has the biggest weight, about 25 times the confident one's."),
    ("Intermediate", "Compute the Brier score for predictions $(0.9, 0.2, 0.6, 0.4)$ with true labels $(1, 0, 0, 1)$.",
     "Squared errors: $0.01$, $0.04$, $0.36$, $0.36$. Mean $= 0.77/4 = 0.1925$."),
    ("Intermediate", "Scikit-learn's <code>class_weight=\"balanced\"</code> gives class $c$ the weight $n/(k\\,n_c)$ for $k$ classes. With 1,000 examples, 950 negative and 50 positive, what are the two weights?",
     "Negatives: $1000/(2 \\times 950) \\approx 0.526$. Positives: $1000/(2 \\times 50) = 10$. Each positive counts 19 times as much as a negative."),
    ("Intermediate", "Softmax gives $\\mathbf{p} = (0.7, 0.2, 0.1)$ for an example whose true class is the second, with input $\\mathbf{x} = (1, 2)$. What is $\\mathbf{p} - \\mathbf{y}$, and what is the gradient for the second class's weight column?",
     "$\\mathbf{y} = (0, 1, 0)$, so $\\mathbf{p} - \\mathbf{y} = (0.7, -0.8, 0.1)$. The second column's gradient is $\\mathbf{x}\\times(-0.8) = (-0.8, -1.6)$; gradient descent moves those weights up, raising that class's score."),
]

CHECKS = {
    0: [("Weights (three numbers)", [0.25, 0.09, 0.0099], "Compute p(1 − p) for each point.")],
    1: [("Brier score", 0.1925, "Average of (p − y)².")],
    2: [("Negative-class weight", 0.52632, "1000 / (2 × 950)."), ("Positive-class weight", 10, "1000 / (2 × 50).")],
    3: [("p − y", [0.7, -0.8, 0.1], "Subtract the one-hot label."), ("Gradient for class 2's weights", [-0.8, -1.6], "Multiply x by −0.8.")],
}
