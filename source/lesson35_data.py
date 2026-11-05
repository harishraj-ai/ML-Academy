# Lesson 35: Probabilistic Graphical Models & HMMs. Patches the shared per-lesson dictionaries on import.
import context, extras_ex_b, checks, running_code, running_text, challenges, reference, understanding, rai

L35 = (35, 6, "Graphical Models & Hidden Markov Models", "Bayesian networks and explaining away, hidden Markov models, the forward and Viterbi algorithms, learning parameters, and stationary distributions.", 55)

OBJ35 = ["Factorise a joint distribution with a Bayesian network and answer queries by enumeration",
         "Explain explaining away and other effects of conditioning on evidence",
         "Define a hidden Markov model and compute sequence likelihoods with the forward algorithm",
         "Decode hidden states with the Viterbi algorithm and learn HMM parameters"]

SRC35 = [("Koller & Friedman (2009) — Probabilistic Graphical Models", "https://mitpress.mit.edu/9780262013192/probabilistic-graphical-models/"),
         ("Rabiner (1989) — A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition", "https://ieeexplore.ieee.org/document/18626"),
         ("Pearl (1988) — Probabilistic Reasoning in Intelligent Systems", "https://www.sciencedirect.com/book/9780080514895/probabilistic-reasoning-in-intelligent-systems"),
         ("Jurafsky & Martin — Speech and Language Processing, appendix on HMMs", "https://web.stanford.edu/~jurafsky/slp3/"),
         ("Murphy (2022) — Probabilistic Machine Learning: An Introduction", "https://probml.github.io/pml-book/book1.html"),
         ("pgmpy documentation", "https://pgmpy.org/")]

context.DEPS[35] = [4, 12, 28]
context.REFRESH[35] = "Graphical models break a joint distribution into local pieces; Bayesian networks reason about causes and evidence, and HMMs decode hidden states from noisy sequences."
context.FIT[35] = "Generalises Bayes' theorem (Lesson 4) and naive Bayes (Lesson 12), and connects to MCMC (Lesson 28) and causal diagrams (Lesson 29)."
context.USE[35] = (["Medical and fault diagnosis from symptoms and test results",
                    "Speech, part-of-speech tagging and gene finding",
                    "Activity recognition, regime detection and machine health monitoring"],
                   "Whenever several uncertain variables influence each other, or a hidden state drives noisy observations over time.",
                   "you only need a prediction from many features and don't care about the structure: then a discriminative model is usually more accurate.")
context.FAQ[35] = [
    ("Is a Bayesian network the same as a causal diagram?",
     "Not necessarily. A Bayesian network encodes probabilistic dependencies; it's causal only if the arrows also mean causation, which needs domain knowledge or experiments."),
    ("How is an HMM different from a Markov chain?",
     "In a Markov chain you observe the states directly. In an HMM the states are hidden and you see only observations that depend on them."),
    ("Have neural networks replaced HMMs?",
     "For speech and text, mostly yes. HMMs remain useful where data is small, interpretability matters, or the structure is known, such as sensor monitoring and genomics."),
    ("What's a conditional random field?",
     "A discriminative cousin of the HMM: it models the labels given the observations directly, and can use rich, overlapping features."),
]
understanding.MYTHS[35] = [
    ("Two independent causes stay independent whatever you observe.", "Observing a shared effect makes them dependent: explaining away."),
    ("Viterbi gives each day's most likely state.", "It gives the most likely whole sequence; per-day probabilities come from the forward–backward algorithm."),
    ("Bigger graphical models are always more accurate.", "Every extra arrow needs more parameters and data, and exact inference gets harder."),
]
extras_ex_b.MISTAKES[35] = [
    "Writing a full joint table instead of factorising.",
    "Multiplying many small probabilities without logarithms, so they underflow to 0.",
    "Confusing transition and emission matrices.",
    "Reading Bayesian-network arrows as causes without justification.",
    "Running Baum–Welch once and trusting a possibly local optimum.",
]
extras_ex_b.EX[35] = [
    ("By hand", "Network: Burglary (0.01) → Alarm; P(alarm | burglary) = 0.9, P(alarm | no burglary) = 0.05. Compute P(burglary | alarm).",
     "Numerator 0.01 × 0.9 = 0.009. Denominator 0.009 + 0.99 × 0.05 = 0.009 + 0.0495 = 0.0585. Answer 0.009/0.0585 ≈ 0.154."),
    ("By hand", "An HMM has T = [[0.9, 0.1], [0.5, 0.5]]. Today is state 1 for sure. What's the probability of state 2 in two days?",
     "Tomorrow: (0.9, 0.1). In two days: state 2 = 0.9 × 0.1 + 0.1 × 0.5 = 0.09 + 0.05 = 0.14."),
    ("By hand", "Find the stationary distribution of T = [[0.8, 0.2], [0.4, 0.6]].",
     "Solve π₁ × 0.2 = π₂ × 0.4 with π₁ + π₂ = 1: π₁ = 2/3 ≈ 0.667, π₂ = 1/3."),
    ("By hand", "A full joint table over 10 binary variables needs how many probabilities (minus one for the sum)? A chain-shaped network where each has one parent needs how many?",
     "2¹⁰ − 1 = 1,023. Chain: 1 for the first variable plus 2 for each of the other 9 = 19."),
    ("Code", "In the weather HMM, make the weather less sticky (0.6 instead of 0.8 for staying sunny). How does Viterbi's advantage over day-by-day guessing change?",
     "It shrinks, because yesterday tells you less about today; with no stickiness at all, the sequence adds nothing beyond the prior."),
]
checks.CHECKS[(35, 0)] = [("P(burglary | alarm)", 0.154, "Bayes' theorem: P(B) P(A|B) ÷ P(A).", 0.002)]
checks.CHECKS[(35, 1)] = [("P(state 2 in two days)", 0.14, "Multiply the starting vector by T twice.")]
checks.CHECKS[(35, 2)] = [("π₁", 0.667, "Balance the flows between the two states.", 0.002)]
checks.CHECKS[(35, 3)] = [("Full table", 1023, "2 to the 10th, minus 1."), ("Chain", 19, "1 + 2 × 9.")]

running_code.CODE[35] = '''import pandas as pd
import numpy as np
df = pd.read_csv("houses.csv")   # download it from Lesson 1
df["metro"] = df.description.str.contains("metro").astype(int)
# A tiny Bayesian network learned by counting: Area → Metro, Area → SoldFast
p_area = df.area.value_counts(normalize=True)
p_metro = df.groupby("area").metro.mean(); p_fast = df.groupby("area").sold_fast.mean()
num = sum(p_area[a] * p_metro[a] * p_fast[a] for a in p_area.index)
den = sum(p_area[a] * p_metro[a] for a in p_area.index)
print("P(sold fast):", round(df.sold_fast.mean(), 3), "  P(sold fast | near metro), via area:", round(num / den, 3))
print("P(area | near metro):", {a: round(float(p_area[a] * p_metro[a] / den), 2) for a in p_area.index})'''
running_text.INTRO[35] = ("Build a tiny Bayesian network from the 12 homes by counting: Area → near a metro, and Area → sold fast. Then ask how a metro mention changes the chance of a fast sale. "
    "Overall, half the homes sold fast; given a metro mention, the network says 0.75, because every metro home is Central and Central homes mostly sell fast. The network makes the reasoning explicit: the metro mention is evidence about the area, which is what drives the prediction here.")

challenges.C[35] = [
    ("Bayes in a two-node network", "Compute P(cause | effect).",
     'p_cause = 0.02\np_eff_given_cause, p_eff_given_not = 0.8, 0.1\n##BLANK##',
     'post', 'post = p_cause * p_eff_given_cause / (p_cause * p_eff_given_cause + (1 - p_cause) * p_eff_given_not)', "Prior × likelihood, divided by the total probability of the effect.",
     'post = p_eff_given_cause  # ← apply Bayes\' theorem'),
    ("One step of a Markov chain", "Compute tomorrow's state probabilities.",
     'import numpy as np\ntoday = np.array([0.5, 0.5])\nT = np.array([[0.9, 0.1], [0.2, 0.8]])\n##BLANK##\nresult = np.round(tomorrow, 2).tolist()',
     'result', 'tomorrow = today @ T', "Multiply the row vector by the transition matrix.",
     'tomorrow = T @ today  # ← the row vector goes on the left'),
]

reference.GLOSSARY += [
    ("Bayesian network", "A directed acyclic graph with a conditional probability table for each node given its parents.", 35, "bn"),
    ("Explaining away", "When observing a shared effect makes two independent causes dependent.", 35, "bn"),
    ("Hidden Markov model (HMM)", "A model of hidden states following a Markov chain, each emitting an observation.", 35, "hmm"),
    ("Viterbi algorithm", "Dynamic programming that finds the most likely sequence of hidden states in an HMM.", 35, "viterbi"),
    ("Stationary distribution", "The long-run share of time a Markov chain spends in each state.", 35, "evaluate"),
]

rai.RAI[35] = ("Making assumptions visible",
    "<p>A graphical model's arrows are assumptions about how the world works, and they shape every answer it gives. That's a strength: experts can inspect and challenge them. Use it. Document why each arrow is there, test conclusions under alternative structures, and remember that a model learned from historical data encodes historical patterns, including unfair ones, in its tables.</p>")
