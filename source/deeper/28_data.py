# Lesson 28 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("How three different priors give very different answers with 50 visitors but almost the same with 5,000, "
          "and how running several MCMC chains and comparing them with R-hat shows whether the sampler really reached the posterior.")

QUIZ = [
    ("A Beta(30, 170) prior is worth roughly how many earlier visitors?",
     [("a", "30"), ("b", "200"), ("c", "170")], "b",
     "$a + b$ acts as a prior sample size."),
    ("Three reasonable priors give clearly different posteriors. What should you conclude?",
     [("a", "The data isn't yet strong enough to settle the question"), ("b", "Pick the prior you like"), ("c", "Bayesian methods don't work")], "a",
     "Collect more data, or report the range."),
    ("What does $\\hat{R}$ compare?",
     [("a", "The spread between chains with the spread within chains"), ("b", "Prior and posterior means"), ("c", "Training and test error")], "a",
     "Chains that agree have $\\hat{R}$ near 1."),
    ("Why is one smooth-looking chain not enough?",
     [("a", "A stuck chain can look smooth while exploring only a tiny region"), ("b", "Chains are always wrong"), ("c", "It's too slow")], "a",
     "Multiple starting points reveal it."),
    ("$\\hat{R}$ is 1.3. What do you do?",
     [("a", "Run longer or improve the sampler before using the samples"), ("b", "Report the results"), ("c", "Lower the prior variance")], "a",
     "Values above about 1.01 mean the chains haven't converged."),
]

IQ = [
    (3, "How do you check that an MCMC run is trustworthy?",
     "\"Look at the trace and it looks fine.\"",
     "Run several chains from dispersed starting points; check that $\\hat{R}$ is close to 1 (below about 1.01) and that the effective sample size is large enough for the quantities you report; inspect trace plots and, for HMC, divergent transitions. Then do posterior predictive checks: simulate data from the fitted model and compare with the real data."),
]

EX = [
    ("Intermediate", "A Beta(10, 190) prior sees 30 conversions from 500 visitors. Compute the posterior mean.",
     "Beta(40, 660): mean = 40/700 ≈ 0.0571."),
    ("Intermediate", "Two chains have within-chain variances 1.0 and 1.2, so W = 1.1, with n = 1000 samples each, and B/n = 0.05. Compute $\\hat{R} = \\sqrt{((n-1)/n \\cdot W + B/n)/W}$.",
     "$(0.999 \\times 1.1 + 0.05)/1.1 = (1.0989 + 0.05)/1.1 = 1.0445$; square root ≈ 1.022: slightly too high."),
]

CHECKS = {
    0: [("Posterior mean", 0.0571, "40 ÷ 700.", 0.0005)],
    1: [("R-hat", 1.022, "Follow the formula step by step.", 0.002)],
}
