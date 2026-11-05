# Lesson 29: Causal Inference. Patches the shared per-lesson dictionaries on import.
import context, extras_ex_b, checks, running_code, running_text, challenges, reference, understanding, rai

L29 = (29, 6, "Causal Inference", "Prediction versus causation: confounding, randomised experiments, regression adjustment, propensity scores, difference-in-differences and uplift modelling.", 60)

OBJ29 = ["Explain potential outcomes, the average treatment effect and why confounding biases naive comparisons",
         "Estimate effects with randomised experiments, regression adjustment and inverse propensity weighting",
         "Apply difference-in-differences and check its parallel-trends assumption",
         "Build a T-learner uplift model to target an action at the people it helps"]

SRC29 = [("Hernán & Robins — Causal Inference: What If", "https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/"),
         ("Cunningham — Causal Inference: The Mixtape", "https://mixtape.scunning.com/"),
         ("Pearl, Glymour & Jewell (2016) — Causal Inference in Statistics: A Primer", "https://bayes.cs.ucla.edu/PRIMER/"),
         ("Künzel et al. (2019) — Metalearners for estimating heterogeneous treatment effects, PNAS", "https://www.pnas.org/doi/10.1073/pnas.1804597116"),
         ("Kohavi, Tang & Xu (2020) — Trustworthy Online Controlled Experiments", "https://experimentguide.com/"),
         ("DoWhy — causal inference library documentation", "https://www.pywhy.org/dowhy/")]

context.DEPS[29] = [4, 6, 8]
context.REFRESH[29] = "Causal questions ask what happens if we act: randomise when you can, otherwise adjust for every confounder, and check the assumptions each method needs."
context.FIT[29] = "Builds on the A/B tests of Lesson 4's \"Going deeper\" and Lesson 28, and uses regression (Lesson 6) and logistic regression (Lesson 8) as tools for adjustment and propensity scores."
context.USE[29] = (["Measuring the effect of a price change, campaign or product feature",
                    "Evaluating policies and programmes from observational data",
                    "Targeting offers, treatments and interventions at the people they help"],
                   "Whenever a decision depends on what an action will cause, not just on what will happen.",
                   "you only need a prediction and won't act on it: then ordinary supervised learning is enough.")
context.FAQ[29] = [
    ("Can't I just add the treatment as a feature in a predictive model?",
     "Only if every confounder is also in the model and you don't include things the treatment itself causes. Even then, flexible models with regularisation can shrink or distort the treatment's effect. Use methods built for estimating effects, and check them against an experiment when possible."),
    ("How do I know I've measured all the confounders?",
     "You can't prove it from data. Use domain knowledge and a causal diagram, run sensitivity analyses (how strong would a hidden confounder have to be to change the conclusion?), and prefer randomised or natural experiments."),
    ("What's a natural experiment?",
     "A situation where something close to random decides who is treated: a lottery, a policy that starts on a certain date, a threshold rule. Difference-in-differences and regression discontinuity exploit these."),
    ("Is correlation ever enough?",
     "For prediction, yes. For decisions about interventions, only when the correlation comes from a randomised comparison or a credible design."),
]
understanding.MYTHS[29] = [
    ("A model with high accuracy tells you what causes the outcome.", "Prediction exploits any correlation, including confounded ones; it doesn't separate cause from association."),
    ("Adjusting for more variables is always safer.", "Adjusting for variables the treatment causes (mediators) or for common effects (colliders) creates bias."),
    ("Observational data can never give causal answers.", "With good designs (DiD, regression discontinuity) and credible assumptions, it often can, though less securely than experiments."),
]
extras_ex_b.MISTAKES[29] = [
    "Reading a model's feature importance or coefficient as a causal effect.",
    "Comparing treated and untreated groups without asking who chose treatment and why.",
    "Adjusting for something the treatment itself causes.",
    "Using inverse propensity weights near 0 or 1 without trimming or checking overlap.",
    "Targeting an offer by predicted purchase instead of predicted uplift.",
]
extras_ex_b.EX[29] = [
    ("By hand", "Treated customers spent an average of 140, untreated 110. Among treated customers, loyal ones are 70%; among untreated, 30%. Can you conclude the treatment's effect is 30? Why or why not?",
     "No. Loyalty differs sharply between the groups, and loyal customers probably spend more anyway, so part (possibly all) of the 30 is confounding. Compare within loyalty levels, adjust, or randomise."),
    ("By hand", "An untreated customer has a propensity score of 0.75. Compute their inverse propensity weight.",
     "The weight is 1/(1 − 0.75) = 4."),
    ("By hand", "City B's sales rose from 200 to 260 after a campaign; city A, without it, rose from 180 to 220 over the same months. Compute the difference-in-differences estimate.",
     "(260 − 200) − (220 − 180) = 60 − 40 = 20."),
    ("By hand", "A T-learner predicts a 0.30 purchase probability with a coupon and 0.22 without for one customer. What is the predicted uplift?",
     "0.30 − 0.22 = 0.08, an 8-percentage-point increase."),
    ("Code", "In the confounding code, add a second hidden confounder that affects both discount and spend, but don't include it in the adjustment. What happens to the regression and weighting estimates?",
     "Both become biased again, in the direction of the hidden confounder's effect, while the randomised estimate is unaffected. No adjustment method can fix a confounder that isn't measured."),
]
checks.CHECKS[(29, 1)] = [("Weight", 4, "1 ÷ (1 − propensity).")]
checks.CHECKS[(29, 2)] = [("DiD estimate", 20, "Treated change minus control change.")]
checks.CHECKS[(29, 3)] = [("Uplift", 0.08, "Treated prediction minus untreated prediction.")]

running_code.CODE[29] = '''import pandas as pd
import numpy as np
df = pd.read_csv("houses.csv")   # download it from Lesson 1
from sklearn.linear_model import LinearRegression
df["metro"] = df.description.str.contains("metro").astype(int)
naive = df[df.metro == 1].sold_fast.mean() - df[df.metro == 0].sold_fast.mean()
X = pd.get_dummies(df[["metro", "area"]], columns=["area"], drop_first=True, dtype=float)
adjusted = LinearRegression().fit(X, df.sold_fast).coef_[0]
print("homes near a metro:", df.metro.sum(), "of", len(df))
print("naive difference in sold-fast rate:", round(naive, 2), "  adjusted for area:", round(adjusted, 2))'''
running_text.INTRO[29] = ("Do homes near a metro sell faster? Three of the 12 homes mention a metro, and all three sold fast, against about a third of the others: a naive difference of 0.67. "
    "Adjusting for area gives 1.0, but that number shouldn't be trusted: all three metro homes are Central, so there are no non-Central metro homes to compare with. This is the overlap problem in miniature: with no comparable untreated cases, no method can separate the metro effect from the area effect.")

challenges.C[29] = [
    ("Difference-in-differences", "Compute the DiD estimate from the four group averages.",
     'treated_before, treated_after = 50.0, 70.0\ncontrol_before, control_after = 48.0, 58.0\n##BLANK##',
     'did', 'did = (treated_after - treated_before) - (control_after - control_before)', "Subtract the control group's change from the treated group's change.",
     'did = treated_after - treated_before  # ← subtract the control group\'s change'),
    ("Inverse propensity weights", "Compute the weight for each person: 1/p if treated, 1/(1 − p) if not.",
     'import numpy as np\nt = np.array([1, 0, 1, 0])\np = np.array([0.8, 0.8, 0.25, 0.5])\n##BLANK##\nresult = w.tolist()',
     'result', 'w = np.where(t == 1, 1 / p, 1 / (1 - p))', "Use np.where on the treatment flag.",
     'w = 1 / p  # ← untreated people need 1 / (1 - p)'),
]

reference.GLOSSARY += [
    ("Confounder", "A variable that affects both the treatment and the outcome, biasing naive comparisons.", 29, "potential"),
    ("Average treatment effect (ATE)", "The average over a population of the difference between outcomes with and without treatment.", 29, "potential"),
    ("Propensity score", "The probability of receiving treatment given a person's characteristics.", 29, "adjust"),
    ("Difference-in-differences", "An effect estimate: the treated group's change over time minus a comparable control group's change.", 29, "did"),
    ("Uplift modelling", "Estimating each individual's treatment effect, to target an action at those it changes.", 29, "uplift"),
]

rai.RAI[29] = ("Causal claims carry weight",
    "<p>\"This programme reduces reoffending\" or \"this drug causes side effects\" changes lives and policies, so causal claims need stronger evidence than predictions. State the assumptions behind every estimate, report how sensitive it is to hidden confounders, and be careful with uplift targeting: deciding who receives help, a discount or extra scrutiny based on predicted effects can quietly exclude groups, so check outcomes across groups.</p>")
