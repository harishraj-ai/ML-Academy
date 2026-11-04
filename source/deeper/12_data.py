# Lesson 12 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("Why naive Bayes adds a small count to every word (it's a Bayesian prior), how to read which words push "
          "towards each class, how real text classifiers are built (word pairs, TF-IDF, complement naive Bayes), and "
          "the difference between generative models (how each class creates data) and discriminative ones (the "
          "boundary only).")

QUIZ = [
    ("Laplace smoothing in naive Bayes is the same as…",
     [("a", "A Bayesian prior that adds α imaginary counts of every word"), ("b", "Removing rare words"), ("c", "Scaling the features")], "a",
     "It's the posterior mean under a symmetric Dirichlet prior."),
    ("What does TF-IDF do to a word that appears in almost every document?",
     [("a", "Gives it a large weight"), ("b", "Gives it a small weight"), ("c", "Removes the document")], "b",
     "The inverse-document-frequency factor $\\log(N/\\text{df})$ is near 0 for very common words."),
    ("Multinomial naive Bayes's decision rule is…",
     [("a", "Linear in the word counts"), ("b", "Quadratic in the word counts"), ("c", "A decision tree")], "a",
     "The log-odds is a constant plus a sum of (log-ratio × count) over words."),
    ("Which model is generative?",
     [("a", "Logistic regression"), ("b", "Gaussian naive Bayes"), ("c", "A linear SVM")], "b",
     "It models $P(\\mathbf{x}\\mid y)$ for each class, then applies Bayes' theorem."),
    ("With only 30 labelled examples and 1,000 word features, a quick strong baseline is…",
     [("a", "A deep neural network"), ("b", "Naive Bayes"), ("c", "kNN with Euclidean distance")], "b",
     "Generative models like naive Bayes typically reach their best accuracy with far fewer examples."),
]

IQ = [
    (3, "Naive Bayes vs logistic regression for text: how do you choose?",
     "Saying one is always better.",
     "Naive Bayes trains by counting, needs very little data to reach its best accuracy, and handles huge vocabularies cheaply, but its independence assumption double-counts correlated words, so its probabilities are over-confident and its final accuracy is often lower. Logistic regression (or a linear SVM) on the same TF-IDF features usually wins with enough data and gives better-calibrated probabilities. Try both: they're cheap. NB is great as a baseline, for tiny datasets, or for streaming updates."),
    (2, "What is TF-IDF and why use it instead of raw counts?",
     "Only giving the acronym.",
     "Term frequency × inverse document frequency: a word's count in a document, multiplied by $\\log(N/\\text{df})$, where df is the number of documents containing it (implementations add smoothing). Very common words get weights near 0; distinctive words get more. Vectors are usually normalised to unit length, so long documents don't dominate. It gives linear models and kNN a much better representation than raw counts."),
    (3, "Why is the smoothing parameter α a regularization hyperparameter?",
     "Thinking it only avoids division by zero.",
     "It pulls every class's word distribution towards uniform, like a prior. A large α means estimates trust the prior more, giving simpler, less confident models (more bias, less variance); a tiny α trusts sparse counts, giving extreme, overfit probabilities. So it's tuned by cross-validation like any regularization strength."),
]

EX = [
    ("Intermediate", "A word appears 3 times in spam emails, which contain 200 words in total. The vocabulary has 1,000 words. With $\\alpha = 1$, what is $P(\\text{word}\\mid\\text{spam})$? What would it be for a word never seen in spam?",
     "$(3 + 1)/(200 + 1000) = 4/1200 \\approx 0.00333$. An unseen word: $1/1200 \\approx 0.000833$, small but not zero."),
    ("Intermediate", "A word appears in 10 of 1,000 documents. Using $\\text{idf} = \\ln(N/\\text{df})$, compute its IDF. A word in all 1,000 documents gets what IDF?",
     "$\\ln(1000/10) = \\ln 100 \\approx 4.605$. In every document: $\\ln 1 = 0$."),
    ("Intermediate", "The spam log-odds starts at the log prior ratio $\\ln(0.4/0.6)$. A message contains one word with log-ratio $+1.5$ and two copies of a word with log-ratio $-0.3$. What are the final log-odds and $P(\\text{spam})$?",
     "$\\ln(0.4/0.6) = -0.405$. Total: $-0.405 + 1.5 - 0.6 = 0.495$. $P(\\text{spam}) = 1/(1 + e^{-0.495}) \\approx 0.621$."),
]

CHECKS = {
    0: [("P(word | spam)", 0.00333, "(count + α) / (total + α·V)."), ("Unseen word", 0.00083, "(0 + 1) / 1200.")],
    1: [("IDF for df = 10", 4.60517, "ln(1000 / 10)."), ("IDF for df = 1000", 0, "ln(1).")],
    2: [("Log-odds", 0.49453, "Add the prior term and each word's log-ratio (twice for the repeated word)."), ("P(spam)", 0.62117, "Apply the sigmoid.")],
}
