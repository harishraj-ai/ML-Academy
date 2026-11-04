# Lesson 4 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("How to learn from data and judge how sure you can be: which distribution fits which kind of data, how to "
          "fit parameters (maximum likelihood), how to combine data with prior beliefs (Bayesian estimation, and why "
          "that equals regularization), why averages are so predictable (the central limit theorem), error bars for "
          "anything (the bootstrap), A/B tests, and why testing many things at once produces false discoveries.")

QUIZ = [
    ("A coin shows 12 heads in 20 flips. What is the maximum-likelihood estimate of $p$?",
     [("a", "0.5"), ("b", "0.6"), ("c", "0.12")], "b",
     "For yes/no data the MLE is the observed fraction: $12/20 = 0.6$."),
    ("You start with a Beta(1, 1) prior and see 3 heads and 1 tail. What is the posterior?",
     [("a", "Beta(4, 2)"), ("b", "Beta(3, 1)"), ("c", "Beta(2, 4)")], "a",
     "Add the heads to $a$ and the tails to $b$: Beta($1+3$, $1+1$)."),
    ("To halve the standard error of an average, you need…",
     [("a", "Twice as much data"), ("b", "Four times as much data"), ("c", "Half as much data")], "b",
     "SE $= \\sigma/\\sqrt{n}$, so halving it needs $\\sqrt{n}$ to double, which means $n$ times 4."),
    ("MAP estimation of linear-regression weights with a normal (Gaussian) prior is the same as…",
     [("a", "Lasso"), ("b", "Ridge regression"), ("c", "Ordinary least squares")], "b",
     "The log of a normal prior is $-\\lambda\\lVert\\mathbf{w}\\rVert^2$, the ridge penalty. A Laplace prior gives lasso."),
    ("You test 10 independent features with no real effect, each at $\\alpha = 0.05$. The chance of at least one false positive is about…",
     [("a", "5%"), ("b", "40%"), ("c", "50%")], "b",
     "$1 - 0.95^{10} \\approx 0.401$."),
]

IQ = [
    (2, "What's the difference between maximum likelihood (MLE) and maximum a posteriori (MAP) estimation?",
     "Saying they always give the same answer.",
     "MLE chooses the parameters that make the observed data most probable. MAP maximises likelihood × prior, so it also uses a belief about the parameters held before seeing the data. They agree with a flat prior or when there's lots of data. With little data, MAP is pulled towards the prior. MAP with a Gaussian prior is ridge regression, and with a Laplace prior it is lasso."),
    (3, "What does the central limit theorem actually say, and what doesn't it say?",
     "\"With enough data, everything becomes normally distributed.\"",
     "It's about <em>averages</em> (and sums) of many independent values with finite variance: their distribution approaches a normal with standard deviation $\\sigma/\\sqrt{n}$. It does <em>not</em> make the data itself normal: 10,000 incomes are still skewed. It also needs independence and finite variance, and convergence is slow for very skewed or heavy-tailed data. It's why error bars on averages, test accuracy and A/B results work."),
    (2, "How does the bootstrap work, and when would you use it?",
     "Describing it as \"making more data\".",
     "Resample your dataset with replacement to the same size, recompute the statistic, and repeat thousands of times. The spread of the results estimates the statistic's sampling variability. The middle 95% gives a confidence interval. Use it when no simple formula exists: medians, percentiles, ratios, AUC or F1 on a test set. It doesn't create information. With a tiny or unrepresentative sample, the intervals are unreliable too."),
    (3, "Your A/B test reaches $p &lt; 0.05$ on day 3 of a planned 14-day test. Can you stop and ship?",
     "\"Yes, it's significant.\"",
     "No. Checking repeatedly and stopping at the first significant result (peeking) inflates the false-positive rate far above 5%, because random fluctuations cross the threshold at some point quite often. Run for the planned sample size, which should come from a power calculation, or use a method designed for continuous monitoring (sequential tests or Bayesian approaches). Also watch for weekday/weekend effects, which a 3-day window can't average out."),
    (3, "You tried 50 model variants and the best one beats the baseline with $p = 0.03$. How much do you trust it?",
     "Trusting the p-value as if it were a single planned test.",
     "Not much. With 50 tries, a few will look significant at the 5% level by chance alone (expected about 2.5). Correct for the number of comparisons (Bonferroni: $0.05/50 = 0.001$), or better, confirm on a fresh test set that wasn't used for choosing. Choosing a model on a validation set and reporting that same score is the ML version of this mistake."),
]

EX = [
    ("Intermediate", "Calls to a help desk follow a Poisson distribution with an average of 2 per hour. What is the probability of exactly 4 calls in an hour? (Use $P(k) = e^{-\\lambda}\\lambda^k/k!$.)",
     "$P(4) = e^{-2}\\,2^4/4! = 0.1353 \\times 16/24 = 0.0902$."),
    ("Intermediate", "With a Beta(2, 2) prior, you observe 3 successes and 7 failures. Give the posterior's parameters, its mean, and the MAP estimate.",
     "Posterior Beta($2+3$, $2+7$) = Beta(5, 9). Mean $= 5/14 \\approx 0.357$. MAP $= (5-1)/(5+9-2) = 4/12 \\approx 0.333$. (The MLE would be $3/10 = 0.3$; the prior pulls both towards 0.5.)"),
    ("Intermediate", "A model is right on 850 of 1,000 test examples. Using the CLT, give its accuracy's standard error and an approximate 95% confidence interval.",
     "$\\hat{p} = 0.85$, $\\text{SE} = \\sqrt{0.85 \\times 0.15/1000} = 0.0113$. Interval: $0.85 \\pm 1.96 \\times 0.0113 = 0.85 \\pm 0.0221$, so about $[0.828,\\ 0.872]$."),
    ("Intermediate", "An A/B test has 200 conversions out of 4,000 for A and 250 out of 4,000 for B. Compute the pooled rate and the z-statistic.",
     "$\\hat{p}_A = 0.05$, $\\hat{p}_B = 0.0625$, pooled $\\hat{p} = 450/8000 = 0.05625$. SE $= \\sqrt{0.05625 \\times 0.94375 \\times (2/4000)} = 0.005152$. $z = 0.0125/0.005152 \\approx 2.43$, so $p \\approx 0.015$."),
    ("Code · intermediate", "Change the bootstrap code to estimate a 95% interval for the <em>mean</em> of the 60 prices instead of the median, keeping the same random seed. Compare it with $\\bar{x} \\pm 1.96\\,s/\\sqrt{n}$.",
     "Replace <code>np.median</code> with <code>np.mean</code> in the resampling loop. The bootstrap gives about $[68.6,\\ 88.3]$ and the formula about $[68.2,\\ 88.4]$: very similar, because the CLT already applies at $n = 60$. The bootstrap's advantage shows for statistics like the median, where no simple formula exists."),
]

CHECKS = {
    0: [("P(4 calls)", 0.09022, "e^(−2) × 2⁴ / 4!")],
    1: [("Posterior (a, b)", [5, 9], "Add successes to a and failures to b."), ("Posterior mean", 0.35714, "a / (a + b)."), ("MAP", 0.33333, "(a − 1) / (a + b − 2).")],
    2: [("Standard error", 0.01129, "√(p(1 − p)/n)."), ("95% interval (low, high)", [0.828, 0.872], "0.85 ± 1.96 × SE.", 0.002)],
    4: [("Bootstrap interval for the mean (low, high)", [68.6, 88.3], "Use np.mean instead of np.median, same seed.", 0.3)],
    3: [("Pooled rate", 0.05625, "Total conversions ÷ total visitors."), ("z", 2.426, "Difference in rates ÷ SE.", 0.02)],
}
