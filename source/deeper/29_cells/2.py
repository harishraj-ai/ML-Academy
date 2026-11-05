# Regression discontinuity: customers with a score of 600 or more get a credit limit increase.
score = rng.uniform(450, 750, n)
treated = (score >= 600).astype(int)
spend2 = 20 + 0.1 * score + 15 * treated + rng.normal(0, 10, n)   # true jump: 15
naive2 = spend2[treated == 1].mean() - spend2[treated == 0].mean()
band = np.abs(score - 600) < 25                                     # only customers near the threshold
Xb = np.c_[treated[band], score[band] - 600, treated[band] * (score[band] - 600)]
rdd = LinearRegression().fit(Xb, spend2[band]).coef_[0]
print("naive difference:", round(naive2, 1), "  regression discontinuity (±25 points):", round(rdd, 1))
