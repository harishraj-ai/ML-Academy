# Lesson 15 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("The mathematics underneath SVMs: the dual problem shows that only the support vectors matter and that "
          "data appears only through dot products (which is why kernels work), a check that a kernel equals a dot "
          "product of hidden features, how C and gamma interact, and why a linear SVM behaves much like logistic "
          "regression.")

QUIZ = [
    ("In the SVM dual, a training point safely outside the margin has…",
     [("a", "$\\alpha_i = 0$, so it doesn't affect the boundary"), ("b", "$\\alpha_i = C$"), ("c", "The largest $\\alpha_i$")], "a",
     "Only support vectors (on or inside the margin) have non-zero $\\alpha_i$."),
    ("Why can the SVM use kernels?",
     [("a", "In the dual, the data appears only through dot products"), ("b", "Kernels make training faster in every case"), ("c", "Because of the hinge loss")], "a",
     "Swap every $\\mathbf{x}_i\\cdot\\mathbf{x}_j$ for $K(\\mathbf{x}_i, \\mathbf{x}_j)$."),
    ("An RBF SVM has 100% training accuracy and much lower test accuracy. Which change is most likely to help?",
     [("a", "Increase gamma"), ("b", "Decrease gamma and/or C"), ("c", "Remove feature scaling")], "b",
     "Large gamma and C give a wiggly, overfit boundary."),
    ("The hinge loss for a point with $y\\,f(\\mathbf{x}) = 2$ is…",
     [("a", "0"), ("b", "1"), ("c", "2")], "a",
     "$\\max(0, 1 - 2) = 0$: confidently correct points cost nothing."),
    ("Which statement about linear SVMs and logistic regression is true?",
     [("a", "They usually give very similar boundaries; logistic regression also gives probabilities"), ("b", "They're unrelated"), ("c", "The SVM always gives probabilities")], "a",
     "Both minimise a regularized loss; log loss is a smooth version of the hinge."),
]

IQ = [
    (3, "Explain the SVM dual problem and why it matters.",
     "Saying it's \"just another way to write it\".",
     "Introducing Lagrange multipliers $\\alpha_i$ for the margin constraints and eliminating $\\mathbf{w}$ gives a problem over the $\\alpha_i$ with box constraints $0 \\le \\alpha_i \\le C$. It matters for two reasons: the KKT conditions make most $\\alpha_i$ zero, so the solution depends only on the support vectors; and the data enters only through dot products, which can be replaced by any valid kernel, giving non-linear boundaries without computing high-dimensional features."),
    (3, "What makes a function a valid kernel?",
     "\"Any similarity function works.\"",
     "Mercer's condition: it must be symmetric, and for any set of points the matrix of its values must be positive semi-definite. Then it equals a dot product in some (possibly infinite-dimensional) feature space. Sums, positive multiples and products of valid kernels are valid. Arbitrary similarity scores can fail this, making the SVM optimisation ill-posed."),
    (2, "Linear SVM or logistic regression: how do you choose?",
     "Claiming one is always more accurate.",
     "Accuracy is usually very close, because both are linear models with a regularized convex loss (hinge vs log loss). Choose logistic regression when you need calibrated probabilities or easy interpretation of odds; a linear SVM when you only need decisions and want a pure max-margin boundary, or in very high-dimensional sparse text where it's a strong default. Kernel SVMs are a different choice, for small to medium data with non-linear boundaries."),
]

EX = [
    ("Intermediate", "Compute the polynomial kernel $(\\mathbf{x}\\cdot\\mathbf{z} + 1)^2$ for $\\mathbf{x} = (2, 0)$ and $\\mathbf{z} = (1, 3)$, and check it with $\\phi$ from the code.",
     "$\\mathbf{x}\\cdot\\mathbf{z} = 2$, so $K = 3^2 = 9$. With $\\phi(\\mathbf{x}) = (1, 2\\sqrt2, 0, 4, 0, 0)$ and $\\phi(\\mathbf{z}) = (1, \\sqrt2, 3\\sqrt2, 1, 9, 3\\sqrt2)$, the dot product is $1 + 4 + 0 + 4 + 0 + 0 = 9$."),
    ("Intermediate", "Compute the hinge loss $\\max(0, 1 - y f)$ for three points with $y f = 1.5$, $0.4$ and $-0.5$.",
     "$0$; $0.6$; $1.5$. The first is beyond the margin (free), the second is inside it, and the third is misclassified."),
    ("Intermediate", "An RBF kernel with $\\gamma = 0.5$: compute $K$ for two points at distance 2, and for two points at distance 0.5.",
     "$e^{-0.5 \\times 4} = e^{-2} \\approx 0.135$; $e^{-0.5 \\times 0.25} = e^{-0.125} \\approx 0.882$."),
]

CHECKS = {
    0: [("Kernel value", 9, "(x·z + 1)².")],
    1: [("Hinge losses", [0, 0.6, 1.5], "max(0, 1 − yf) for each.")],
    2: [("K at distance 2", 0.13534, "exp(−γ d²)."), ("K at distance 0.5", 0.8825, "exp(−0.5 × 0.25).")],
}
