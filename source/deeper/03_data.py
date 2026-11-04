# Lesson 3 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("The calculus that explains how well optimisation works: derivatives of whole layers (the Jacobian), "
          "curvature (the Hessian), why some losses have exactly one lowest point (convexity), a faster method that "
          "uses curvature (Newton's method), how to test a hand-written gradient, and how to optimise with a rule "
          "the answer must obey (Lagrange multipliers).")

QUIZ = [
    ("A function takes 4 numbers and returns 3. What shape is its Jacobian?",
     [("a", "4 × 3"), ("b", "3 × 4"), ("c", "3 × 3")], "b",
     "One row per output (3) and one column per input (4)."),
    ("At a point with zero gradient, the Hessian's eigenvalues are 5 and −1. What kind of point is it?",
     [("a", "A minimum"), ("b", "A maximum"), ("c", "A saddle point")], "c",
     "Curving up in one direction and down in another: a saddle."),
    ("Why is a convex loss good news for gradient descent?",
     [("a", "Every local minimum is the global minimum"), ("b", "It always converges in one step"), ("c", "It needs no learning rate")], "a",
     "There is only one valley, so you can't get stuck in a worse one. You still need a sensible learning rate."),
    ("On a quadratic loss, how many steps does Newton's method need to reach the minimum?",
     [("a", "One"), ("b", "About as many as gradient descent"), ("c", "It never reaches it exactly")], "a",
     "A quadratic is exactly its own second-order Taylor approximation, so jumping to the bottom of that bowl lands on the true minimum."),
    ("A gradient check gives a relative error of $0.05$. What should you conclude?",
     [("a", "Everything is fine"), ("b", "There is probably a bug in the gradient"), ("c", "$h$ is too big")], "b",
     "Correct gradients typically agree to about $10^{-7}$ or better. An error of $5\\times 10^{-2}$ points to a mistake, such as a missing chain-rule factor."),
]

IQ = [
    (3, "Why don't we train neural networks with Newton's method, if it converges so much faster?",
     "\"Because it doesn't work on non-convex functions.\"",
     "Cost first: the Hessian has $d^2$ entries and solving with it is about $d^3$ work, which is impossible for millions of weights. It also needs the full dataset's curvature, whereas we train on noisy mini-batches. And on non-convex surfaces the Hessian isn't positive definite, so a raw Newton step can head <em>towards</em> a saddle or maximum. Quasi-Newton methods (L-BFGS) and adaptive methods (Adam) capture some curvature cheaply instead."),
    (2, "What makes a loss function convex, and which common ML losses are convex?",
     "Saying \"it has one minimum\" without the test.",
     "A twice-differentiable function is convex if and only if its Hessian is positive semi-definite everywhere. Equivalently, the chord between any two points lies on or above the graph. Convex: MSE for linear models, log loss for logistic regression, hinge loss for SVMs, and these plus L1 or L2 penalties. Not convex: neural network losses, k-means' objective, mixture-model likelihoods."),
    (3, "What's the difference between the Jacobian and the Hessian?",
     "Mixing up which one holds first derivatives.",
     "The Jacobian holds the <em>first</em> derivatives of a vector-valued function (outputs × inputs). The Hessian holds the <em>second</em> derivatives of a scalar function (inputs × inputs), and it is symmetric. In fact, the Hessian is the Jacobian of the gradient. Backprop multiplies Jacobians; second-order optimisers use the Hessian."),
    (3, "In an SVM or in PCA, where do Lagrange multipliers come in?",
     "Saying they're only a trick for textbook problems.",
     "PCA maximises the variance $\\mathbf{v}^\\top\\Sigma\\mathbf{v}$ subject to $\\lVert\\mathbf{v}\\rVert = 1$. The Lagrange condition gives $\\Sigma\\mathbf{v} = \\lambda\\mathbf{v}$, so the components are eigenvectors and $\\lambda$ is the variance. The SVM maximises the margin subject to inequality constraints. Its Lagrange multipliers (via the KKT conditions) are zero for every point except the support vectors, and its dual form is what makes the kernel trick possible."),
]

EX = [
    ("Intermediate", "Compute the Jacobian of $\\mathbf{f}(x, y) = (xy,\\ x + y^2)$ at $(2, 3)$. Give the entries row by row.",
     "$J = \\begin{pmatrix}y &amp; x\\\\ 1 &amp; 2y\\end{pmatrix}$, so at $(2, 3)$: $\\begin{pmatrix}3 &amp; 2\\\\ 1 &amp; 6\\end{pmatrix}$."),
    ("Intermediate", "For $L(w_1, w_2) = 3w_1^2 + 2w_1w_2 + w_2^2$, find the Hessian and its eigenvalues. Is $L$ convex?",
     "$H = \\begin{pmatrix}6 &amp; 2\\\\ 2 &amp; 2\\end{pmatrix}$. $\\det(H - \\lambda I) = \\lambda^2 - 8\\lambda + 8 = 0$, so $\\lambda = 4 \\pm 2\\sqrt{2} \\approx 1.172$ and $6.828$. Both are positive, so $H$ is positive definite and $L$ is convex."),
    ("Intermediate", "Use one Newton step to minimise $L(w) = w^4$ in one dimension, starting from $w = 2$. Where do you land?",
     "$L' = 4w^3 = 32$ and $L'' = 12w^2 = 48$ at $w = 2$. Step: $w \\leftarrow 2 - 32/48 = 1.333$. (Each Newton step multiplies $w$ by $2/3$ for this function, so it is slower here because the curvature vanishes at the minimum.)"),
    ("Intermediate", "Maximise $f = x + y$ subject to $x^2 + y^2 = 8$ using a Lagrange multiplier. What are $x$, $y$ and the maximum?",
     "$\\nabla f = (1, 1) = \\lambda(2x, 2y)$, so $x = y = 1/(2\\lambda)$. The constraint gives $2x^2 = 8$, so $x = y = 2$ (the positive root gives the maximum) and $f = 4$."),
]

CHECKS = {
    0: [("Jacobian entries (row by row)", [3, 2, 1, 6], "Row 1 is (∂f₁/∂x, ∂f₁/∂y) = (y, x); row 2 is (1, 2y).")],
    1: [("Eigenvalues (smaller, larger)", [1.17157, 6.82843], "Solve λ² − 8λ + 8 = 0.")],
    2: [("w after one step", 1.33333, "w − L′(w)/L″(w).")],
    3: [("x", 2, "x = y at the optimum."), ("y", 2, "Use the constraint 2x² = 8."), ("Maximum of x + y", 4, "Add them.")],
}
