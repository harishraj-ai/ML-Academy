# Lesson 11 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("Why kNN struggles with many features (all distances become nearly equal), which distance and weighting "
          "to choose, how k-d trees and approximate search find neighbours among millions of points quickly (the "
          "same technology behind vector databases and LLM retrieval), and how good kNN can get with lots of data.")

QUIZ = [
    ("In 1,000 dimensions, the farthest of 1,000 random points is only about 1.1 times farther than the nearest. What does that mean for kNN?",
     [("a", "Neighbours are very informative"), ("b", "\"Nearest\" carries little information, so kNN struggles"), ("c", "kNN becomes faster")], "b",
     "When all distances are similar, the nearest neighbours are hardly more similar than random points."),
    ("Which distance ignores vector length and compares only direction?",
     [("a", "Euclidean"), ("b", "Manhattan"), ("c", "Cosine distance")], "c",
     "Cosine distance is $1 - \\cos\\theta$, which is why it's standard for text and embeddings."),
    ("What does <code>weights=\"distance\"</code> do in kNN?",
     [("a", "Closer neighbours get bigger votes"), ("b", "It scales the features"), ("c", "It picks k automatically")], "a",
     "Each neighbour's vote is weighted by $1/d$."),
    ("When do k-d trees stop helping much?",
     [("a", "With more than about 20 dimensions"), ("b", "With more than 1,000 points"), ("c", "With categorical labels")], "a",
     "In high dimensions, distance concentration means the search can rarely skip regions."),
    ("Approximate nearest-neighbour methods such as HNSW trade…",
     [("a", "A little accuracy for a huge speed-up"), ("b", "Speed for perfect accuracy"), ("c", "Memory for nothing")], "a",
     "They usually find most true neighbours, far faster, which is what vector databases need."),
]

IQ = [
    (3, "How would you serve nearest-neighbour search over 100 million embeddings with low latency?",
     "Proposing brute force or a k-d tree.",
     "Use an approximate nearest-neighbour index: graph-based (HNSW) or inverted-file with product quantization (IVF-PQ, as in FAISS), often in a vector database. Normalise the embeddings if using cosine similarity. Tune the index (graph degree, number of probed clusters) for the recall/latency trade-off, measure recall against brute force on a sample, and shard across machines when the index doesn't fit in memory."),
    (3, "Why do distances concentrate in high dimensions, and why does kNN still work on images and text?",
     "Saying kNN never works in high dimensions.",
     "Each dimension adds an independent random difference, so squared distances are sums of many terms, whose relative spread shrinks like $1/\\sqrt{d}$. Nearest and farthest become similar. Real data, though, lies near a much lower-dimensional manifold, so its intrinsic dimension is small. Good representations (PCA, learned embeddings) expose that structure, and kNN works in that space."),
    (2, "When would you choose cosine distance over Euclidean?",
     "\"Cosine is always better for text.\" without saying why.",
     "When the length of a vector reflects something irrelevant, such as document length or overall activity, and only the pattern matters. TF-IDF vectors, word and sentence embeddings, and user-preference vectors are typical. On unit-length vectors, cosine and Euclidean rank neighbours identically, because $\\lVert\\mathbf{a}-\\mathbf{b}\\rVert^2 = 2 - 2\\cos\\theta$."),
    (3, "What's the theoretical guarantee for 1-nearest-neighbour as data grows?",
     "Claiming it reaches perfect accuracy.",
     "Cover and Hart (1967): as $n \\to \\infty$, the 1-NN error is at most twice the Bayes error (the best achievable). With $k \\to \\infty$ and $k/n \\to 0$, kNN's error approaches the Bayes error itself. The data needed to get close grows exponentially with dimension, which is the practical catch."),
]

EX = [
    ("Intermediate", "Show that for unit-length vectors, $\\lVert\\mathbf{a}-\\mathbf{b}\\rVert^2 = 2 - 2\\cos\\theta$. If the cosine similarity is 0.8, what is the Euclidean distance?",
     "$\\lVert\\mathbf{a}-\\mathbf{b}\\rVert^2 = \\lVert\\mathbf{a}\\rVert^2 + \\lVert\\mathbf{b}\\rVert^2 - 2\\,\\mathbf{a}\\cdot\\mathbf{b} = 1 + 1 - 2\\cos\\theta$. With $\\cos\\theta = 0.8$: $\\sqrt{2 - 1.6} = \\sqrt{0.4} \\approx 0.632$."),
    ("Intermediate", "A query has 3 neighbours at distances 1, 2 and 4, with classes A, B and B. Which class wins with uniform votes, and which with distance weights $1/d$?",
     "Uniform: B wins 2 to 1. Distance-weighted: A gets $1/1 = 1$; B gets $1/2 + 1/4 = 0.75$, so A wins."),
    ("Intermediate", "Brute-force kNN on $n = 10^6$ points with $d = 100$ features: roughly how many multiply-adds does one query need?",
     "About $n \\times d = 10^6 \\times 100 = 10^8$ multiply-adds per query. At $10^9$ per second that's about 0.1 seconds per query: too slow for live serving, which is why indexes exist."),
    ("Code · intermediate", "Change the concentration code to use 1,000 points from a normal distribution (<code>rng.normal</code>) instead of the cube. Does the farthest/nearest ratio still shrink towards 1 as dimension grows?",
     "Yes. The ratio falls in the same way (large in 2 dimensions, close to 1 in 1,000), because concentration comes from adding many independent differences, not from the cube's shape."),
]

CHECKS = {
    0: [("Euclidean distance", 0.63246, "√(2 − 2 × 0.8).")],
    2: [("Multiply-adds per query", 100000000, "n × d.")],
}
