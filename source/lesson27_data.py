# Lesson 27: Recommender Systems. Patches the shared per-lesson dictionaries on import.
import context, extras_ex_b, checks, running_code, running_text, challenges, reference, understanding, rai

L27 = (27, 5, "Recommender Systems", "Explicit and implicit feedback, bias baselines, neighbour-based collaborative filtering, matrix factorisation, ranking metrics, and cold start.", 55)

OBJ27 = ["Represent explicit and implicit feedback as a sparse user–item matrix and build bias baselines",
         "Compute item–item collaborative filtering with cosine similarity",
         "Train a matrix factorisation model with stochastic gradient descent and explain its latent factors",
         "Evaluate recommendations with ranking metrics such as precision@k, and handle cold start with content features"]

SRC27 = [("Koren, Bell & Volinsky (2009) — Matrix Factorization Techniques for Recommender Systems, IEEE Computer", "https://ieeexplore.ieee.org/document/5197422"),
         ("Sarwar et al. (2001) — Item-based Collaborative Filtering Recommendation Algorithms", "https://dl.acm.org/doi/10.1145/371920.372071"),
         ("Hu, Koren & Volinsky (2008) — Collaborative Filtering for Implicit Feedback Datasets", "https://ieeexplore.ieee.org/document/4781121"),
         ("Covington, Adams & Sargin (2016) — Deep Neural Networks for YouTube Recommendations", "https://dl.acm.org/doi/10.1145/2959100.2959190"),
         ("Chaney, Stewart & Engelhardt (2018) — How Algorithmic Confounding in Recommendation Systems Increases Homogeneity and Decreases Utility", "https://dl.acm.org/doi/10.1145/3240323.3240370"),
         ("Ricci, Rokach & Shapira (eds.) — Recommender Systems Handbook", "https://link.springer.com/book/10.1007/978-1-0716-2197-4")]

context.DEPS[27] = [7, 11, 17]
context.REFRESH[27] = "Recommenders fill in a sparse user–item matrix: start from bias baselines, use similar items or learned latent factors, and judge them by ranking metrics on held-out interactions."
context.FIT[27] = "Uses the similarity and nearest-neighbour ideas of Lesson 11, the gradient descent of Lesson 7 and the low-rank thinking of PCA (Lesson 17) on the user–item matrix."
context.USE[27] = (["Products, films, music and news recommendations",
                    "Job, property and course matching",
                    "Ranking search results and choosing which content to show next"],
                   "Whenever many users interact with many items and you need to choose a few items for each user.",
                   "there are few items or no interaction history: then simple rules, popularity or content similarity are enough.")
context.FAQ[27] = [
    ("What if I only have clicks or purchases, not ratings?",
     "That's implicit feedback: treat interactions as positive signals and unobserved pairs as weak negatives, use methods built for it (weighted matrix factorisation, ranking losses) and evaluate with ranking metrics."),
    ("How many latent factors should I use?",
     "Tune it on validation data: typically 10 to 200. More factors fit more detail but overfit sparse data, so tune regularisation at the same time."),
    ("How are recommenders built at very large scale?",
     "Usually in two stages: a fast candidate generator (approximate nearest neighbours on embeddings) picks hundreds of items, then a ranking model with many features orders them."),
    ("How do I recommend to a brand-new user?",
     "Use popularity, simple questions at sign-up, context (location, device) or content features, then switch to collaborative filtering as interactions arrive."),
]
understanding.MYTHS[27] = [
    ("Lower rating error means better recommendations.", "Users see a ranked top few; a model can have good RMSE but rank poorly. Evaluate rankings."),
    ("Missing ratings mean the user dislikes the item.", "Mostly they haven't seen it. Treating every missing value as a zero biases the model."),
    ("More recommendations of what someone liked is always better.", "Narrow feedback loops reduce diversity and discovery; good systems mix in exploration."),
]
extras_ex_b.MISTAKES[27] = [
    "Evaluating on a random split that lets the model see a user's future interactions.",
    "Treating unobserved user–item pairs as negative ratings.",
    "Reporting RMSE only, when users experience a ranked list.",
    "Forgetting to exclude items the user already has from their recommendations.",
    "Comparing only with random recommendations instead of a popularity baseline.",
]
extras_ex_b.EX[27] = [
    ("By hand", "The global mean rating is 3.5. An item's average is 4.1 and a user's average is 3.0. Using simple deviations, predict this user's rating of the item.",
     "Item bias +0.6, user bias −0.5, so the prediction is 3.5 + 0.6 − 0.5 = 3.6."),
    ("By hand", "Two items have rating vectors (over the same three users) (5, 3, 0) and (4, 0, 2). Compute their cosine similarity.",
     "Dot product 20. Lengths √34 ≈ 5.831 and √20 ≈ 4.472. Cosine = 20/26.08 ≈ 0.767."),
    ("By hand", "A user's latent vector is (1.2, −0.5) and an item's is (0.8, 0.4). The global mean is 3.5 and both biases are 0. Predict the rating.",
     "Dot product 0.96 − 0.20 = 0.76, so the prediction is 3.5 + 0.76 = 4.26."),
    ("By hand", "Of 10 recommended items, 4 are in the user's held-out set of 8 liked items. Compute precision@10 and recall@10.",
     "Precision@10 = 4/10 = 0.4. Recall@10 = 4/8 = 0.5."),
    ("Code", "In the matrix factorisation code, change the number of factors from 5 to 1 and to 20. How does the test RMSE change?",
     "With 1 factor the model underfits (RMSE rises towards the bias baseline); with 20, the training error keeps falling but the test RMSE gets worse unless you raise the regularisation. It's the usual bias–variance trade-off."),
]
checks.CHECKS[(27, 0)] = [("Prediction", 3.6, "Global mean + item bias + user bias.")]
checks.CHECKS[(27, 1)] = [("Cosine similarity", 0.767, "Dot product ÷ (product of lengths).", 0.002)]
checks.CHECKS[(27, 2)] = [("Prediction", 4.26, "Global mean + dot product of the two vectors.")]
checks.CHECKS[(27, 3)] = [("Precision@10", 0.4, "Hits ÷ 10."), ("Recall@10", 0.5, "Hits ÷ liked items.")]

running_code.CODE[27] = '''import pandas as pd
import numpy as np
df = pd.read_csv("houses.csv")   # download it from Lesson 1
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
cols = ["size_m2", "bedrooms", "dist_km", "age_yrs", "price_lakh"]
Z = StandardScaler().fit_transform(df[cols])
sim = cosine_similarity(Z)
np.fill_diagonal(sim, -1)
for viewed in [2, 11]:
    row = df.index[df.id == viewed][0]
    top = np.argsort(sim[row])[::-1][:3]
    print("viewed", viewed, "→ similar:", df.id.iloc[top].tolist(), " similarity", np.round(sim[row, top], 2).tolist())'''
running_text.INTRO[27] = ("A buyer looks at a house; which others should the site show? Standardise size, bedrooms, distance, age and price, and recommend the homes with the highest cosine similarity. "
    "For the Central flat with id 2, the top matches are ids 11 and 1 (similarity 0.69 and 0.68), both nearby flats; for id 11 they are 1, 4 and 2. This is content-based recommendation: it works with no interaction history at all, which is how the cold-start problem is usually handled.")

challenges.C[27] = [
    ("A bias baseline", "Predict a rating as the global mean plus the item's and the user's deviations.",
     'mu, item_avg, user_avg = 3.5, 4.2, 3.1\n##BLANK##',
     'pred', 'pred = mu + (item_avg - mu) + (user_avg - mu)', "Add each deviation from the global mean.",
     'pred = mu  # ← add the item and user deviations'),
    ("Precision at k", "Compute precision@5 for these recommendations.",
     'recommended = [4, 9, 1, 7, 3]\nliked = {1, 2, 3, 8}\n##BLANK##',
     'result', 'result = len(set(recommended) & liked) / 5', "Count recommended items that are in liked, divided by k.",
     'result = len(liked) / 5  # ← count only the hits'),
]

reference.GLOSSARY += [
    ("Collaborative filtering", "Recommending from the interactions of many users: similar users like similar items.", 27, "cf"),
    ("Matrix factorisation", "Approximating the user–item matrix as a product of user and item latent-factor matrices.", 27, "mf"),
    ("Implicit feedback", "Interactions such as clicks, views or purchases, used as signals of preference instead of explicit ratings.", 27, "data"),
    ("Cold start", "The problem of recommending for new users or items with no interaction history.", 27, "practice"),
    ("Precision@k", "The share of the top k recommendations that are relevant to the user.", 27, "evaluation"),
]

rai.RAI[27] = ("Feedback loops and filter bubbles",
    "<p>A recommender learns from what it showed, so popular items get more popular and niche ones disappear, and users can be pushed towards ever more extreme content if that maximises clicks. Measure diversity, coverage and exposure for item creators, not just clicks; add exploration; and give users controls to see why something was shown and to change it.</p>")
