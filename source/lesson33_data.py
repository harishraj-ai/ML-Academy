# Lesson 33: Survival Analysis. Patches the shared per-lesson dictionaries on import.
import context, extras_ex_b, checks, running_code, running_text, challenges, reference, understanding, rai

L33 = (33, 6, "Survival Analysis", "Time-to-event data with censoring: Kaplan–Meier curves, median survival, the log-rank test, the Cox proportional hazards model and the concordance index.", 50)

OBJ33 = ["Explain right-censoring and why ignoring it biases time-to-event estimates",
         "Compute a Kaplan–Meier survival curve and median survival",
         "Compare groups with the log-rank test",
         "Fit and interpret a Cox proportional hazards model and evaluate it with the concordance index"]

SRC33 = [("Kaplan & Meier (1958) — Nonparametric Estimation from Incomplete Observations, JASA", "https://www.jstor.org/stable/2281868"),
         ("Cox (1972) — Regression Models and Life-Tables, JRSS B", "https://www.jstor.org/stable/2985181"),
         ("Harrell et al. (1996) — Multivariable prognostic models, Statistics in Medicine (C-index)", "https://onlinelibrary.wiley.com/doi/10.1002/(SICI)1097-0258(19960229)15:4%3C361::AID-SIM168%3E3.0.CO;2-4"),
         ("Kleinbaum & Klein — Survival Analysis: A Self-Learning Text", "https://link.springer.com/book/10.1007/978-1-4419-6646-9"),
         ("lifelines documentation", "https://lifelines.readthedocs.io/"),
         ("scikit-survival documentation", "https://scikit-survival.readthedocs.io/")]

context.DEPS[33] = [4, 8, 9]
context.REFRESH[33] = "Survival analysis models time until an event while respecting censoring: Kaplan–Meier for curves, log-rank to compare groups, Cox for hazard ratios, C-index to evaluate."
context.FIT[33] = "Applies probability (Lesson 4) and likelihood-based models like logistic regression (Lesson 8) to times, and evaluates ranking like ROC-AUC (Lesson 9)."
context.USE[33] = (["Customer churn timing and lifetime value",
                    "Predictive maintenance: time until machine failure",
                    "Clinical studies, credit default timing and employee retention"],
                   "Whenever the question is when an event happens and some subjects haven't had it yet.",
                   "you only care whether the event happens within a fixed window and everyone is followed for that whole window: then ordinary classification works.")
context.FAQ[33] = [
    ("Why not just predict churn within 6 months as a classification?",
     "You can if every customer has been observed for 6 months. Survival methods use everyone, including recent customers, and give the whole curve over time."),
    ("What if the proportional hazards assumption fails?",
     "Add time-varying coefficients, stratify by the offending variable, or use models without that assumption, such as random survival forests."),
    ("What's a hazard?",
     "The instantaneous rate of the event at a time, among those still at risk: roughly, the probability of churning in the next small interval, divided by its length."),
    ("Can machine-learning models handle censoring?",
     "Yes: random survival forests, gradient boosting with a Cox loss and survival neural networks are built for it."),
]
understanding.MYTHS[33] = [
    ("Censored customers can be dropped.", "Dropping them throws away information and biases estimates towards short times."),
    ("The mean survival time is the best summary.", "Censoring hides the long tail, so the median is usually reported."),
    ("A hazard ratio of 2 means twice as likely to churn ever.", "It means twice the rate at each moment, among those still at risk."),
]
extras_ex_b.MISTAKES[33] = [
    "Treating censored observations as events at their censoring time.",
    "Starting the clock at different kinds of moments for different people.",
    "Using features measured after time zero.",
    "Ignoring competing events, such as switching to a partner instead of cancelling.",
    "Evaluating a survival model with accuracy instead of the concordance index.",
]
extras_ex_b.EX[33] = [
    ("By hand", "Times: 3 (event), 5 (censored), 6 (event), 8 (event). Compute the Kaplan–Meier survival after time 6.",
     "At 3: 4 at risk, S = 3/4 = 0.75. At 5: censored, risk set 2. At 6: 2 at risk, S = 0.75 × 1/2 = 0.375."),
    ("By hand", "A Cox coefficient is −0.5. Compute the hazard ratio and say what it means.",
     "e^(−0.5) ≈ 0.607: at any moment, the event rate is about 39% lower for a one-unit increase."),
    ("By hand", "Of 10 comparable pairs, the model gives the earlier churner the higher risk score in 7, ties in 1. Compute the concordance index.",
     "(7 + 0.5 × 1)/10 = 0.75."),
    ("By hand", "A Kaplan–Meier curve is 0.62 at 4 months and 0.48 at 5 months. Between which months is the median survival?",
     "Between 4 and 5 months, where the curve first falls to 0.5 or below (at 5)."),
    ("Code", "In the churn simulation, double the censoring by ending the study earlier. How do the Kaplan–Meier medians change?",
     "They stay close to the truth (with wider uncertainty), because censoring is handled properly; the naive average of observed times falls even further."),
]
checks.CHECKS[(33, 0)] = [("Survival after 6", 0.375, "Multiply (1 − d/n) at each event time.")]
checks.CHECKS[(33, 1)] = [("Hazard ratio", 0.607, "e to the power of the coefficient.", 0.002)]
checks.CHECKS[(33, 2)] = [("C-index", 0.75, "Concordant plus half the ties, divided by pairs.")]
checks.CHECKS[(33, 3)] = [("Median month", 5, "The first time the curve is at or below 0.5.")]

running_code.CODE[33] = '''import pandas as pd
import numpy as np
df = pd.read_csv("houses.csv")   # download it from Lesson 1
# Simulated days on the market: fast sellers go quickly; one listing is still unsold (censored at 90 days).
df["days"] = np.where(df.sold_fast == 1, 10 + 4 * df.id, 40 + 5 * df.id).clip(max=90)
df["sold"] = (df.days < 90).astype(int)
def km(t, e):
    s, out = 1.0, []
    for u in np.unique(t[e == 1]):
        s *= 1 - ((t == u) & (e == 1)).sum() / (t >= u).sum(); out.append((int(u), round(float(s), 3)))
    return out
print("days:", df.days.tolist(), " sold:", df.sold.tolist())
print("Kaplan–Meier (day, share unsold):", km(df.days.to_numpy(), df.sold.to_numpy()))'''
running_text.INTRO[33] = ("How long do homes stay on the market? The houses file has no dates, so this example simulates days on the market: fast sellers go in about 2 to 8 weeks, others take longer, and one listing is still unsold when the data is collected, so it's censored at 90 days. "
    "The Kaplan–Meier curve falls with each sale, and reaches 0.5 at day 55: half the homes sell within about 8 weeks. The unsold home keeps the curve above 0 at the end, rather than being wrongly counted as a sale at day 90.")

challenges.C[33] = [
    ("A Kaplan–Meier step", "Multiply the survival by the share that survives this event time.",
     's, at_risk, events = 0.8, 10, 2\n##BLANK##',
     's_new', 's_new = s * (1 - events / at_risk)', "Multiply by 1 − d/n.",
     's_new = s - events  # ← multiply by the surviving share instead'),
    ("A hazard ratio", "Convert a Cox coefficient to a hazard ratio, rounded to 2 decimals.",
     'import math\nbeta = 0.7\n##BLANK##',
     'hr', 'hr = round(math.exp(beta), 2)', "The hazard ratio is e to the power of beta.",
     'hr = beta  # ← exponentiate'),
]

reference.GLOSSARY += [
    ("Censoring", "When an event hasn't been observed by the end of follow-up, so only a lower bound on its time is known.", 33, "censoring"),
    ("Kaplan–Meier estimator", "A survival-curve estimate multiplying the share surviving each event time among those at risk.", 33, "km"),
    ("Hazard", "The instantaneous event rate at a time among those still at risk.", 33, "cox"),
    ("Cox proportional hazards model", "A survival regression where features multiply a baseline hazard by e^(βx).", 33, "cox"),
    ("Concordance index", "The share of comparable pairs a survival model orders correctly; 0.5 is random.", 33, "evaluate"),
]

rai.RAI[33] = ("Time-to-event models in sensitive decisions",
    "<p>Survival models are used to predict how long patients live, when employees will leave and when borrowers will default. Errors and biases translate into who gets treatment, promotion or credit. Check that censoring isn't related to the group (people who leave the data for reasons linked to the outcome bias every estimate), validate by group, and present predicted times as uncertain ranges, not fixed dates.</p>")
