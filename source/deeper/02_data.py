# Lesson 2 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("The linear algebra that explains how algorithms behave: different ways to measure size (norms), when a "
          "set of features carries duplicate information (rank), the special directions a matrix only stretches "
          "(eigenvectors, the heart of PCA), the SVD that finds hidden structure in a data table, and why nearly "
          "duplicate features make weights unstable (the condition number).")

QUIZ = [
    ("What is the L1 norm of $(2, -3, 1)$?",
     [("a", "$\\sqrt{14}$"), ("b", "6"), ("c", "3")], "b",
     "L1 adds the sizes of the entries: $2 + 3 + 1 = 6$. ($\\sqrt{14}$ is the L2 norm and 3 is the L∞ norm.)"),
    ("A data matrix has 5 columns but rank 4. What does that tell you?",
     [("a", "One column can be built from the others, so $X^\\top X$ can't be inverted"), ("b", "One row is missing"), ("c", "The model will be 80% accurate")], "a",
     "Rank counts independent columns. With one redundant column, ordinary least squares has no unique answer."),
    ("$A\\mathbf{v} = 3\\mathbf{v}$. What does the matrix $A$ do to the direction of $\\mathbf{v}$?",
     [("a", "Rotates it by 3 degrees"), ("b", "Keeps the direction and stretches it 3 times"), ("c", "Flips it")], "b",
     "That's the definition of an eigenvector with eigenvalue 3: same direction, three times as long."),
    ("The singular values of a data table are 90, 60, 2, 1 and 0.5. A good low-rank summary keeps about…",
     [("a", "1 component"), ("b", "2 components"), ("c", "All 5 components")], "b",
     "The values drop sharply after the second. The remaining ones are tiny and mostly describe noise."),
    ("Ridge regression adds $\\lambda I$ to $X^\\top X$. What does that do to its eigenvalues?",
     [("a", "Multiplies each by $\\lambda$"), ("b", "Adds $\\lambda$ to each, so none is near zero"), ("c", "Nothing")], "b",
     "$(X^\\top X + \\lambda I)\\mathbf{v} = (\\mu + \\lambda)\\mathbf{v}$ for each eigenvector. The smallest eigenvalue rises, so the condition number falls."),
]

IQ = [
    (3, "Why does L1 regularization produce exactly-zero weights, while L2 only shrinks them?",
     "\"Because L1 is stronger.\"",
     "It's about shape, not strength. The L1 ball $|w_1| + |w_2| \\le t$ is a diamond with corners on the axes. When the loss's contours first touch it, they usually touch at a corner, where some weights are exactly 0. The L2 ball is round, so the touching point is almost never on an axis. Equivalently, the L1 penalty's slope stays the same size right up to zero, so it keeps pushing until a weight reaches 0. The L2 penalty's slope $2\\lambda w$ fades as $w$ shrinks."),
    (2, "What is an eigenvector, and where do eigenvectors appear in ML?",
     "Giving only the equation, with no meaning.",
     "A direction that a matrix only stretches, $A\\mathbf{v} = \\lambda\\mathbf{v}$. In ML: PCA's components are the eigenvectors of the covariance matrix, with eigenvalues equal to the variance in each direction. The eigenvalues of the Hessian describe a loss surface's curvature (and so how fast gradient descent converges). Spectral clustering and Google's PageRank are also eigenvector methods."),
    (3, "What's the relationship between PCA and the SVD?",
     "Treating them as unrelated algorithms.",
     "Centre the data matrix $X$ and take its SVD, $X = U\\Sigma V^\\top$. The columns of $V$ are the principal components (the eigenvectors of $X^\\top X$), and $\\sigma_i^2/(n-1)$ is the variance along each one. Libraries compute PCA through the SVD because it's more accurate than forming $X^\\top X$, which squares the condition number."),
    (3, "Your linear regression's weights change wildly when you add a few rows of data. What's going on, and how do you fix it?",
     "Blaming the optimiser or the random seed.",
     "Probably ill-conditioning: some features are nearly linear combinations of others, so $X^\\top X$ has a tiny eigenvalue and a huge condition number. Small data changes then cause big swings along that weak direction. Check the VIFs or the condition number. Fix it by removing or combining redundant features, using PCA, or adding ridge regularization, which adds $\\lambda$ to every eigenvalue."),
    (2, "Why is $X^\\top X$ never negative definite, and when is it invertible?",
     "\"It's always invertible because it's square.\"",
     "$\\mathbf{w}^\\top X^\\top X\\mathbf{w} = \\lVert X\\mathbf{w}\\rVert^2 \\ge 0$, so it is always positive semi-definite. It is invertible (positive definite) exactly when the columns of $X$ are linearly independent, which requires at least as many rows as columns. With more features than examples ($d &gt; n$) it is always singular."),
]

EX = [
    ("Intermediate", "For $\\mathbf{v} = (1, -2, 2)$, compute the L1, L2 and L∞ norms.",
     "L1 $= 1 + 2 + 2 = 5$; L2 $= \\sqrt{1 + 4 + 4} = 3$; L∞ $= 2$."),
    ("Intermediate", "Find the eigenvalues of $A = \\begin{pmatrix}4 &amp; 1\\\\ 2 &amp; 3\\end{pmatrix}$. Give the smaller one first.",
     "$\\det(A - \\lambda I) = (4-\\lambda)(3-\\lambda) - 2 = \\lambda^2 - 7\\lambda + 10 = (\\lambda - 2)(\\lambda - 5)$, so $\\lambda = 2$ and $5$. Check: they add up to the trace $4 + 3 = 7$ and multiply to the determinant $12 - 2 = 10$."),
    ("Intermediate", "A matrix has singular values $10, 4, 1$. Keeping only the largest, what fraction of the squared Frobenius norm $\\sum \\sigma_i^2$ does the rank-1 approximation capture?",
     "$\\sum\\sigma_i^2 = 100 + 16 + 1 = 117$. Rank 1 keeps $100/117 \\approx 0.855$ (85.5%). The leftover error is $\\sqrt{16 + 1}/\\sqrt{117} \\approx 0.381$ in relative Frobenius norm."),
    ("Intermediate", "A symmetric matrix has eigenvalues $200$ and $0.5$. What is its condition number? After adding $\\lambda I$ with $\\lambda = 9.5$, what is it?",
     "Before: $200/0.5 = 400$. After: $(200 + 9.5)/(0.5 + 9.5) = 209.5/10 = 20.95$."),
    ("Code · intermediate", "Use <code>np.linalg.svd</code> on the ratings table <code>R</code> from the \"Going deeper\" code. What fraction of $\\sum\\sigma_i^2$ do the first 3 singular values capture?",
     "<code>(s[:3]**2).sum() / (s**2).sum()</code> gives about $0.975$: the 3 hidden tastes explain 97.5% of the table's squared size. The rest is noise."),
]

CHECKS = {
    0: [("L1", 5, "Add the absolute values."), ("L2", 3, "Square, add, square root."), ("L∞", 2, "The biggest absolute value.")],
    1: [("Eigenvalues (smaller, larger)", [2, 5], "Solve λ² − 7λ + 10 = 0.")],
    2: [("Fraction captured", 0.85470, "σ₁² divided by the sum of all σᵢ².")],
    3: [("Condition number before", 400, "Largest eigenvalue ÷ smallest."), ("Condition number after", 20.95, "Add 9.5 to both eigenvalues first.")],
    4: [("Fraction for 3 components", 0.975, "Divide the sum of the first three σ² by the sum of all σ².", 0.002)],
}
