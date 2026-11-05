popularity = train.sum(axis=0)                         # how many users interacted with each item
scores_pop = np.tile(popularity, (n_users, 1)).astype(float)
scores_mf = P @ Q.T
for name, S in [("popular", scores_pop), ("matrix factorisation", scores_mf)]:
    S = np.where(train, -np.inf, S)                    # don't recommend items already seen
    top = np.argsort(-S, axis=1)[:, :5]
    coverage = len(np.unique(top)) / n_items
    avg_pop = popularity[top].mean()
    print(f"{name:21s} catalogue coverage {coverage:.2f}   average popularity of recommended items {avg_pop:.1f}")
print("average popularity across all items:", round(popularity.mean(), 1))
