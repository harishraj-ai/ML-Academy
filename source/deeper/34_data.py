# Lesson 34 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("PageRank is the eigenvector of the random surfer's matrix with eigenvalue 1, which repeated multiplication finds in a few dozen steps, "
          "and the second eigenvector of the graph Laplacian splits a graph into its two communities.")

QUIZ = [
    ("PageRank is an eigenvector of the surfer's matrix with eigenvalue…",
     [("a", "1"), ("b", "0"), ("c", "d")], "a",
     "r G = r."),
    ("Why does power iteration converge for PageRank?",
     [("a", "All entries of G are positive, so eigenvalue 1 is the largest and its eigenvector unique"), ("b", "Graphs are small"), ("c", "Because of the learning rate")], "a",
     "Perron–Frobenius guarantees it."),
    ("On a directed graph, PageRank mostly depends on…",
     [("a", "Incoming links"), ("b", "Outgoing links"), ("c", "Node names")], "a",
     "Links to a node pass importance to it."),
    ("What's the smallest eigenvalue of a graph Laplacian?",
     [("a", "0"), ("b", "1"), ("c", "The largest degree")], "a",
     "A constant vector gives L f = 0."),
    ("What does the sign of the Fiedler vector do?",
     [("a", "Splits the graph along a weak cut, often into communities"), ("b", "Ranks nodes by degree"), ("c", "Finds shortest paths")], "a",
     "It's the basis of spectral clustering."),
]

IQ = [
    (3, "How does spectral clustering work on a graph?",
     "Calling it \"k-means on the adjacency matrix\".",
     "Build the Laplacian L = D − A (or its normalised form), compute the eigenvectors for its k smallest eigenvalues, use them as new coordinates for each node, and run k-means there. Small eigenvalues correspond to smooth vectors that vary little across edges, so nodes in the same dense community get similar coordinates. The number of near-zero eigenvalues hints at the number of well-separated communities."),
]

EX = [
    ("Intermediate", "A graph has edges A–B and B–C. Write the diagonal of its degree matrix D (A, B, C).",
     "Degrees are 1, 2, 1."),
    ("Intermediate", "Power iteration's error shrinks by about the damping factor 0.85 each step. Roughly how many steps reduce an error of 1 to below 0.001?",
     "Solve 0.85^k < 0.001: k > ln(0.001)/ln(0.85) ≈ 42.5, so about 43 steps."),
]

CHECKS = {
    0: [("Degrees", [1, 2, 1], "Count each node's edges.")],
    1: [("Steps", 43, "ln(0.001) ÷ ln(0.85), rounded up.")],
}
