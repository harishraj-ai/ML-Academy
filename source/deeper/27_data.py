# Lesson 27 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("How alternating least squares trains matrix factorisation by solving one small ridge regression per user and per item in turn, "
          "and how catalogue coverage and average popularity reveal a recommender that only pushes what's already popular.")

QUIZ = [
    ("In ALS, with the item factors fixed, each user's vector is found by…",
     [("a", "A small ridge regression on the items that user rated"), ("b", "Gradient boosting"), ("c", "Random search")], "a",
     "That's the closed-form step."),
    ("Why does ALS parallelise well?",
     [("a", "Each user's (and each item's) update is independent of the others in that step"), ("b", "It uses no matrices"), ("c", "It needs only one sweep")], "a",
     "All users can be solved at once, then all items."),
    ("A recommender's catalogue coverage is 0.1. What does that mean?",
     [("a", "Only 10% of items are ever recommended to anyone"), ("b", "Precision is 0.1"), ("c", "10% of users get recommendations")], "a",
     "Coverage is the share of distinct items recommended."),
    ("Why do accuracy metrics tend to favour popular items?",
     [("a", "Popular items are most likely to be in any user's held-out interactions"), ("b", "They have better ratings"), ("c", "They're cheaper")], "a",
     "Recommending them is a safe bet for the metric."),
    ("What's the ALS update for a user vector?",
     [("a", "$(Q_u^\\top Q_u + \\lambda I)^{-1} Q_u^\\top \\mathbf{r}_u$"), ("b", "$Q_u^\\top \\mathbf{r}_u$"), ("c", "$\\mathbf{r}_u / \\lambda$")], "a",
     "The ridge regression solution."),
]

IQ = [
    (3, "SGD or ALS for matrix factorisation: how do you choose?",
     "Saying one is always better.",
     "SGD is simple, handles explicit ratings and extra terms (biases, side features) easily and is cheap per step, but needs a tuned learning rate. ALS has closed-form steps, needs no learning rate, parallelises across users and items, and handles implicit feedback with all unobserved pairs efficiently, which is why it's common on Spark. Both need regularisation tuned on validation data."),
]

EX = [
    ("Intermediate", "A user rated two items whose factor vectors (1 factor) are 2 and 1, with ratings 4 and 3. With λ = 1, find the user's factor from the ALS formula.",
     "$Q^\\top Q = 4 + 1 = 5$, plus λ gives 6. $Q^\\top r = 8 + 3 = 11$. So $p = 11/6 \\approx 1.833$."),
    ("Intermediate", "A catalogue has 500 items. Across all users' top-10 lists, 120 distinct items appear. What's the catalogue coverage?",
     "120/500 = 0.24."),
]

CHECKS = {
    0: [("User factor", 1.833, "(Σ q·r) ÷ (Σ q² + λ).", 0.002)],
    1: [("Coverage", 0.24, "Distinct items ÷ catalogue size.")],
}
