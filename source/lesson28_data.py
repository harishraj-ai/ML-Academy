# Lesson 28: Bayesian & Probabilistic ML. Patches the shared per-lesson dictionaries on import.
import context, extras_ex_b, checks, running_code, running_text, challenges, reference, understanding, rai

L28 = (28, 5, "Bayesian & Probabilistic ML", "Priors and posteriors, Bayesian A/B tests, Bayesian linear regression, Gaussian processes, MCMC, and Thompson sampling.", 55)

OBJ28 = ["Update a Beta prior with conversion data and answer decision questions such as P(B > A) and expected loss",
         "Explain Bayesian linear regression's posterior and why its prediction intervals widen away from the data",
         "Describe Gaussian processes and when their uncertainty is useful",
         "Sample a posterior with the Metropolis algorithm and use posteriors to decide with Thompson sampling"]

SRC28 = [("Gelman et al. — Bayesian Data Analysis (3rd ed.)", "http://www.stat.columbia.edu/~gelman/book/"),
         ("Rasmussen & Williams (2006) — Gaussian Processes for Machine Learning", "https://gaussianprocess.org/gpml/"),
         ("Bishop (2006) — Pattern Recognition and Machine Learning, chapter 3", "https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/"),
         ("Russo et al. (2018) — A Tutorial on Thompson Sampling", "https://arxiv.org/abs/1707.02038"),
         ("McElreath — Statistical Rethinking (2nd ed.)", "https://xcelab.net/rm/"),
         ("scikit-learn — Bayesian regressors and Gaussian processes", "https://scikit-learn.org/stable/modules/gaussian_process.html")]

context.DEPS[28] = [4, 10, 15]
context.REFRESH[28] = "Bayesian ML updates a prior with the data into a posterior, and uses the whole posterior for error bars and decisions instead of a single best guess."
context.FIT[28] = "Builds on Bayes' theorem (Lesson 4), shows that ridge (Lesson 10) is a Bayesian posterior mean, and reuses the kernels of Lesson 15 in Gaussian processes."
context.USE[28] = (["A/B tests that report the probability one version is better",
                    "Small-data science and engineering models that need honest error bars",
                    "Bandits for headlines and offers, and Bayesian optimisation of expensive experiments"],
                   "Whenever uncertainty matters to the decision, data is limited, or you have real prior knowledge to include.",
                   "you have huge data and only need point predictions: then the posterior is narrow and ordinary models are simpler and faster.")
context.FAQ[28] = [
    ("Isn't choosing a prior subjective?",
     "Somewhat, but it's explicit and can be checked: try a few reasonable priors and see whether the conclusion changes. With plenty of data the likelihood dominates and they agree."),
    ("What's the difference between a credible interval and a confidence interval?",
     "A 95% credible interval contains the parameter with 95% probability given the data and prior. A 95% confidence interval comes from a procedure that covers the true value in 95% of repeated samples; it isn't a probability statement about this interval."),
    ("Which tools do people use for Bayesian modelling?",
     "PyMC, Stan and NumPyro for general models with MCMC or variational inference; scikit-learn's BayesianRidge and GaussianProcessRegressor for the common simple cases."),
    ("Can neural networks be Bayesian?",
     "Approximately: ensembles of networks, Monte Carlo dropout and variational methods give useful uncertainty estimates, though exact Bayesian deep learning is too expensive."),
]
understanding.MYTHS[28] = [
    ("Bayesian methods need lots of computation.", "Conjugate models such as the Beta A/B test are one line of arithmetic; MCMC is only needed when there's no formula."),
    ("The prior lets you get any answer you want.", "With enough data, reasonable priors converge; a prior that changes the conclusion is a sign the data is weak, which is worth knowing."),
    ("A credible interval and a confidence interval are the same thing.", "Only a credible interval is a direct probability statement about the parameter."),
]
extras_ex_b.MISTAKES[28] = [
    "Using a strong prior without checking how much it changes the result.",
    "Reporting only the posterior mean and throwing away the uncertainty.",
    "Running MCMC without checking the acceptance rate or whether the chain has settled.",
    "Using a bandit when you need an unbiased, precise comparison of every option.",
    "Using an exact Gaussian process on hundreds of thousands of points.",
]
extras_ex_b.EX[28] = [
    ("By hand", "A Beta(1, 1) prior is updated with 30 conversions from 200 visitors. Give the posterior and its mean.",
     "Beta(1 + 30, 1 + 170) = Beta(31, 171). Mean = 31/202 ≈ 0.153."),
    ("By hand", "A Beta(20, 180) prior (centred on 10%) is updated with 5 conversions from 100 visitors. What's the posterior mean, and how does it compare with the observed 5%?",
     "Beta(25, 275), mean = 25/300 ≈ 0.083: pulled from 5% towards the prior's 10%, because the prior is worth 200 visitors and the data only 100."),
    ("By hand", "In Bayesian linear regression the noise variance is 4 and the prior variance of the weights is 2. What ridge λ is the posterior mean equivalent to?",
     "λ = σ²/τ² = 4/2 = 2."),
    ("By hand", "In a Metropolis step the current posterior density is 0.30 and the proposal's is 0.12. With what probability is the proposal accepted?",
     "min(1, 0.12/0.30) = 0.4."),
    ("Code", "In the Thompson sampling code, make the true rates closer (5%, 5.5%, 6%). How does the share of traffic for the best design change?",
     "It falls, and more traffic goes to the others for longer, because the posteriors overlap for longer and the algorithm keeps exploring. Close options are hard to separate, which is also when choosing the wrong one costs least."),
]
checks.CHECKS[(28, 0)] = [("Posterior mean", 0.1535, "31 ÷ (31 + 171).", 0.001)]
checks.CHECKS[(28, 1)] = [("Posterior mean", 0.0833, "25 ÷ 300.", 0.001)]
checks.CHECKS[(28, 2)] = [("λ", 2, "Noise variance ÷ prior variance.")]
checks.CHECKS[(28, 3)] = [("Acceptance probability", 0.4, "Ratio of new to current density, capped at 1.")]

running_code.CODE[28] = '''import pandas as pd
import numpy as np
df = pd.read_csv("houses.csv")   # download it from Lesson 1
from scipy import stats
for area, g in df.groupby("area"):
    a, b = 1 + g.sold_fast.sum(), 1 + (1 - g.sold_fast).sum()     # Beta(1, 1) prior
    lo, hi = stats.beta(a, b).ppf([0.05, 0.95])
    print(f"{area:9s} sold fast {g.sold_fast.sum()} of {len(g)}  posterior mean {a / (a + b):.2f}  90% interval [{lo:.2f}, {hi:.2f}]")'''
running_text.INTRO[28] = ("How sure can we be about which areas sell fast, with only 12 homes? Give each area's \"sold fast\" rate a Beta(1, 1) prior and update it with the area's homes. "
    "Central sold 3 of 4 fast (posterior mean 0.67) and the Suburb 3 of 5 (0.57), but their 90% credible intervals, about 0.34 to 0.92 and 0.27 to 0.85, overlap heavily. The Outskirts sold none of 3, yet the posterior still allows rates up to about 0.53. With this little data, the intervals are the honest answer.")

challenges.C[28] = [
    ("A Beta posterior", "Update a Beta(2, 2) prior with 7 successes and 3 failures, and compute the posterior mean.",
     'a, b = 2, 2\ns, f = 7, 3\n##BLANK##',
     'mean', 'mean = (a + s) / (a + s + b + f)', "The posterior is Beta(a + s, b + f); its mean is a′/(a′ + b′).",
     'mean = s / (s + f)  # ← that ignores the prior'),
    ("A Metropolis acceptance", "Compute the acceptance probability for a proposal.",
     'current, proposal = 0.25, 0.05\n##BLANK##',
     'accept', 'accept = min(1, proposal / current)', "Ratio of densities, capped at 1.",
     'accept = proposal  # ← use the ratio, capped at 1'),
]

reference.GLOSSARY += [
    ("Posterior", "The updated probability distribution over unknowns after seeing data: likelihood × prior, normalised.", 28, "recap"),
    ("Conjugate prior", "A prior whose posterior has the same family, such as Beta for a probability, so updating is simple arithmetic.", 28, "ab"),
    ("Credible interval", "An interval containing a parameter with a stated probability under the posterior.", 28, "ab"),
    ("Gaussian process", "A prior over functions defined by a kernel, giving a predictive mean and uncertainty at every input.", 28, "gp"),
    ("MCMC", "Markov chain Monte Carlo: algorithms such as Metropolis that draw samples from a posterior using only density ratios.", 28, "mcmc"),
    ("Thompson sampling", "A bandit strategy that chooses each option with the probability that it's the best, by sampling from posteriors.", 28, "decide"),
]

rai.RAI[28] = ("Priors and uncertainty in high-stakes decisions",
    "<p>A prior encodes assumptions, and in decisions about people (credit, health, policing) a prior built from biased history carries that bias into every new case. State priors openly and test how much they move conclusions. Equally, uncertainty is a responsibility: when an interval is wide, say so, and route the decision to a person rather than presenting a guess as a fact.</p>")
