# Lesson 23 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("Bayesian optimisation built from scratch: a Gaussian process predicts the validation score and how unsure "
          "it is for every setting, and expected improvement picks the next trial by balancing a high predicted "
          "score against high uncertainty. On a narrow peak it beats random search once it has about 10 trials.")

QUIZ = [
    ("What does a Gaussian process surrogate predict at an untried setting?",
     [("a", "Only the score"), ("b", "A mean score and a standard deviation (its uncertainty)"), ("c", "The best learning rate")], "b",
     "The uncertainty is what lets Bayesian optimisation explore sensibly."),
    ("In expected improvement, the term $\\sigma\\,\\phi(z)$ rewards…",
     [("a", "Exploitation of high predicted scores"), ("b", "Exploration of uncertain regions"), ("c", "Fast training")], "b",
     "It grows with the uncertainty $\\sigma$, so unexplored regions get tried."),
    ("When does Bayesian optimisation help most compared with random search?",
     [("a", "Cheap trials, hundreds of hyperparameters"), ("b", "Expensive trials, a few hyperparameters, a small budget"), ("c", "Never")], "b",
     "Each trial's information matters most when trials are scarce."),
    ("Why is basic Bayesian optimisation hard to run in parallel?",
     [("a", "Each choice depends on the results of the previous trials"), ("b", "GPs can't use more than one CPU"), ("c", "It needs a GPU")], "a",
     "Random search's trials are independent; Bayesian optimisation is sequential by design."),
    ("If the best so far is $f^* = 0.90$ and a candidate has $\\mu = 0.90$, $\\sigma = 0.02$, its expected improvement is about…",
     [("a", "0"), ("b", "0.008"), ("c", "0.02")], "b",
     "With $z = 0$: EI $= 0 + 0.02 \\times \\phi(0) = 0.02 \\times 0.399 \\approx 0.008$."),
]

IQ = [
    (3, "Explain expected improvement and the exploration–exploitation trade-off it encodes.",
     "Describing it only as \"pick the best predicted point\".",
     "Given the surrogate's normal prediction $(\\mu, \\sigma)$ and the best score $f^*$, EI is the expected amount by which a trial beats $f^*$: $(\\mu - f^*)\\Phi(z) + \\sigma\\phi(z)$ with $z = (\\mu - f^*)/\\sigma$. The first term favours points predicted to be good (exploitation); the second favours uncertain points (exploration). Points with a low mean but high uncertainty can still be chosen, which prevents getting stuck near an early lucky result."),
    (2, "When would you choose Optuna's TPE over a Gaussian-process optimiser?",
     "\"TPE is always better.\"",
     "When there are many hyperparameters, categorical or conditional ones (a choice of model with its own settings), or many trials: TPE scales to these, while GP cost grows cubically with the number of trials and GPs struggle beyond about 20 dimensions. A GP can be more sample-efficient for a few continuous hyperparameters and very expensive trials."),
]

EX = [
    ("Intermediate", "The best score so far is 0.80. A candidate has $\\mu = 0.82$ and $\\sigma = 0.02$. Compute $z$ and the expected improvement, using $\\Phi(1) = 0.8413$ and $\\phi(1) = 0.2420$.",
     "$z = 0.02/0.02 = 1$. EI $= 0.02 \\times 0.8413 + 0.02 \\times 0.2420 = 0.01683 + 0.00484 = 0.02167$."),
    ("Intermediate", "Two candidates: A has $\\mu = 0.85$, $\\sigma = 0.001$; B has $\\mu = 0.83$, $\\sigma = 0.05$. The best so far is 0.85. Which has the higher expected improvement? (Use $\\phi(0) = 0.399$, $\\Phi(-0.4) = 0.345$, $\\phi(-0.4) = 0.368$.)",
     "A: $z = 0$, EI $= 0 + 0.001 \\times 0.399 = 0.0004$. B: $z = -0.02/0.05 = -0.4$, EI $= -0.02 \\times 0.345 + 0.05 \\times 0.368 = -0.0069 + 0.0184 = 0.0115$. B wins: its uncertainty makes it worth exploring."),
]

CHECKS = {
    0: [("z", 1, "(μ − f*) / σ."), ("Expected improvement", 0.02167, "(μ − f*)Φ(z) + σφ(z).")],
    1: [("EI for A", 0.0004, "z = 0.", 0.0001), ("EI for B", 0.0115, "z = −0.4.", 0.0003)],
}
