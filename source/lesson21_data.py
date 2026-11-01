# Lesson 21: Ethics & Fairness in Machine Learning. Patches the shared per-lesson dictionaries on import.
import context, extras_ex_b, checks, running_code, running_text, challenges, reference, understanding, rai

L21 = (21, 4, "Ethics & Fairness in Machine Learning", "Where bias comes from, how to measure fairness per group, why the criteria conflict, and what to do about it.", 60)

OBJ21 = ["Name the main kinds of harm and the places where bias enters an ML system",
         "Compute selection rate, TPR, FPR and precision for each group from confusion-matrix counts",
         "Explain demographic parity, equal opportunity, equalised odds and predictive parity, and the four-fifths rule",
         "Explain why the fairness criteria conflict when base rates differ, and choose mitigations"]

SRC21 = [("Barocas, Hardt & Narayanan — Fairness and Machine Learning (MIT Press, 2023, free online)", "https://fairmlbook.org/"),
         ("Hardt, Price & Srebro (2016) — Equality of Opportunity in Supervised Learning", "https://arxiv.org/abs/1610.02413"),
         ("Chouldechova (2017) — Fair prediction with disparate impact", "https://arxiv.org/abs/1703.00056"),
         ("Kleinberg, Mullainathan & Raghavan (2016) — Inherent Trade-Offs in the Fair Determination of Risk Scores", "https://arxiv.org/abs/1609.05807"),
         ("Obermeyer et al. (2019) — Dissecting racial bias in an algorithm used to manage the health of populations, Science", "https://www.science.org/doi/10.1126/science.aax2342"),
         ("Mitchell et al. (2019) — Model Cards for Model Reporting", "https://arxiv.org/abs/1810.03993"),
         ("Gebru et al. — Datasheets for Datasets", "https://arxiv.org/abs/1803.09010"),
         ("US EEOC — Uniform Guidelines on Employee Selection Procedures (the four-fifths rule), 29 CFR 1607.4(D)", "https://www.ecfr.gov/current/title-29/subtitle-B/chapter-XIV/part-1607/section-1607.4"),
         ("Fairlearn — user guide (open-source fairness toolkit)", "https://fairlearn.org/main/user_guide/index.html")]

context.DEPS[21] = [5, 8, 9]
context.REFRESH[21] = "Fairness is measured by comparing selection rate, TPR, FPR and precision across groups; when base rates differ, these criteria cannot all be equal."
context.FIT[21] = "Steps back from building models to ask who they affect. It reuses the confusion matrix from Lesson 9 and the threshold idea from Lesson 8 to measure and reduce unfairness."
context.USE[21] = (["Auditing credit, hiring, insurance and healthcare models before deployment",
                    "Model cards and impact assessments required by regulators",
                    "Monitoring deployed models for unequal error rates"],
                   "Always, whenever a model's decisions affect people.", "—")
context.FAQ[21] = [
    ("If I remove gender and ethnicity from the data, is my model fair?",
     "Not necessarily. Other features (postcode, school, first name) can act as proxies, and without the attribute you can no longer measure group differences. Keep it for auditing."),
    ("Which fairness metric is the right one?",
     "There is no universal answer. Ask which mistake hurts people most in this situation: missing qualified people (compare TPR), wrongly flagging people (compare FPR), or unequal access overall (compare selection rates). Decide with the people affected."),
    ("Isn't the model just reflecting reality?",
     "It reflects the data, which records past decisions and unequal access as well as reality. A model used to make future decisions can lock those patterns in, so 'it's in the data' is a reason to look closer, not a defence."),
    ("Are fairness rules the same everywhere?",
     "No. Laws differ by country and by domain (lending, employment, housing). The four-fifths rule is a US guideline for employment, not a universal law. Get legal advice for real deployments."),
]
understanding.MYTHS[21] = [
    ("Algorithms are objective because they are maths.", "The maths is objective about the data it's given; the data, the label, the features and the threshold all carry human choices."),
    ("A model that's accurate overall is fair.", "Overall accuracy can hide very different error rates for different groups, as the worked example shows (88% accuracy for B, yet B's qualified applicants are approved less often)."),
    ("We can satisfy every fairness definition if we try hard enough.", "When base rates differ, it is mathematically impossible (except for a perfect model). You must choose which criterion matters most."),
]
extras_ex_b.MISTAKES[21] = [
    "Reporting only overall accuracy and never splitting the metrics by group.",
    "Treating a tiny subgroup's rates as precise — with a handful of people, one person changes the rate a lot.",
    "Deleting the protected attribute and assuming the problem is solved.",
    "Choosing a fairness metric without involving the people the decisions affect.",
]
extras_ex_b.EX[21] = [
    ("By hand", "Group A: 60 of 200 applicants approved. Group B: 30 of 150 approved. Compute both selection rates and the demographic-parity ratio. Does it pass the four-fifths rule of thumb?",
     "A: $60/200 = 0.30$. B: $30/150 = 0.20$. Ratio $= 0.20/0.30 \\approx 0.667$, below 0.8, so it would be flagged for possible adverse impact."),
    ("By hand", "In group C, 40 people would repay a loan; the model approves 30 of them. Of the 60 who would not repay, it approves 6. Compute TPR, FPR and precision.",
     "TPR $= 30/40 = 0.75$. FPR $= 6/60 = 0.10$. Precision $= 30/(30+6) = 30/36 \\approx 0.833$."),
    ("By hand", "A group has base rate $p = 0.25$, precision 0.8 and TPR 0.6. Use the identity $\\text{FPR} = \\frac{p}{1-p}\\cdot\\frac{1-\\text{PPV}}{\\text{PPV}}\\cdot\\text{TPR}$ to find its FPR.",
     "$\\frac{0.25}{0.75}\\cdot\\frac{0.2}{0.8}\\cdot 0.6 = 0.3333\\times0.25\\times0.6 = 0.05$."),
    ("Concepts", "A university admissions model is trained on past admissions decisions. List two ways bias could enter, and one check you would run before using it.",
     "Historical bias: past decisions may have favoured some schools or groups, and the model copies them. Measurement bias: 'admitted' is a proxy for 'would succeed'. Representation bias: some groups have few past applicants. Check: compute selection rate and TPR (using later student success as the outcome) per group, with uncertainty for small groups."),
    ("Project", "Take the synthetic loan data from the Python section. Choose a separate threshold for group B so that its selection rate is within 0.8 of group A's. What happens to B's TPR, FPR and precision?",
     "Lowering B's threshold raises its selection rate; TPR and FPR both rise and precision falls. Equalising one rate moves the others — the trade-off from the impossibility result. The exact numbers depend on the threshold you pick."),
]
checks.CHECKS[(21, 0)] = [("selection rate A", 0.3, "Approved ÷ group size."), ("selection rate B", 0.2, "30 ÷ 150."), ("parity ratio", 0.66667, "Lower rate ÷ higher rate.")]
checks.CHECKS[(21, 1)] = [("TPR", 0.75, "Approved repayers ÷ all repayers."), ("FPR", 0.1, "Approved non-repayers ÷ all non-repayers."), ("precision", 0.83333, "Approved repayers ÷ all approved.")]
checks.CHECKS[(21, 2)] = [("FPR", 0.05, "p/(1−p) = 1/3 and (1−PPV)/PPV = 0.25.")]

running_code.CODE[21] = '''import pandas as pd
import numpy as np
df = pd.read_csv("houses.csv")   # download it from Lesson 1
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_predict
cols = ["dist_km", "age_yrs"]                 # the model never sees "area"
clf = make_pipeline(StandardScaler(), LogisticRegression())
df["pred"] = cross_val_predict(clf, df[cols], df["sold_fast"], cv=4)   # honest out-of-fold predictions
df["group"] = np.where(df["area"] == "Central", "Central", "Not central")
for g, s in df.groupby("group"):
    tp = ((s.pred == 1) & (s.sold_fast == 1)).sum(); fp = ((s.pred == 1) & (s.sold_fast == 0)).sum()
    pos, neg = (s.sold_fast == 1).sum(), (s.sold_fast == 0).sum()
    print(f"{g:12s} n={len(s):2d}  base rate {s.sold_fast.mean():.3f}  flagged {s.pred.mean():.3f}  "
          f"TPR {tp / pos:.2f}  FPR {fp / neg if neg else float('nan'):.2f}")'''
running_text.INTRO[21] = ("Does the Lesson 8 model treat areas differently? It only sees distance and age, never the area name — yet distance is a near-perfect <strong>proxy</strong> for area. "
    "Every Central house is flagged as a fast seller (4 of 4), including the one that didn't sell fast (FPR 1.00); elsewhere only 3 of 8 are flagged and none wrongly. "
    "With 4 and 8 houses these rates are extremely noisy — one house moves a rate by 25 points — which is itself a fairness lesson: small groups need far more data before you trust their numbers.")

challenges.C[21] = [
    ("Selection rate per group", "Compute the share of applicants approved in each group.",
     'import pandas as pd\ndf = pd.DataFrame({"group": ["A", "A", "A", "A", "B", "B", "B", "B"], "approved": [1, 1, 0, 1, 0, 1, 0, 0]})\n##BLANK##\nratio = round(rates.min() / rates.max(), 3)',
     'ratio', 'rates = df.groupby("group")["approved"].mean()', "Group by the group column and take the mean of the 0/1 approval column.",
     'rates = df["approved"]  # ← replace with the per-group mean'),
    ("True-positive rate for one group", "Compute the TPR: approved repayers divided by all repayers.",
     'import numpy as np\nrepay = np.array([1, 1, 1, 1, 0, 0, 0, 0, 0, 0])\napprove = np.array([1, 1, 1, 0, 1, 0, 0, 0, 0, 0])\n##BLANK##',
     'tpr', 'tpr = (approve[repay == 1] == 1).mean()', "Look only at people with repay == 1 and take the share approved.",
     'tpr = approve.mean()  # ← replace: only count people who would repay'),
]

reference.GLOSSARY += [
    ("Demographic parity", "Fairness criterion: every group is selected (approved, flagged) at the same rate. Summarised by the ratio of the lower to the higher selection rate.", 21, "metrics"),
    ("Equal opportunity", "Fairness criterion: the true-positive rate is the same in every group, so qualified people are approved equally often.", 21, "metrics"),
    ("Equalised odds", "Fairness criterion: both the true-positive rate and the false-positive rate are equal across groups.", 21, "metrics"),
    ("Proxy feature", "A feature that stands in for another, often sensitive, attribute because it is correlated with it — e.g. a postcode standing in for ethnicity.", 21, "sources"),
    ("Model card", "A short document that records a model's intended use, how it was evaluated (including per group) and its known limitations.", 21, "beyond"),
]

rai.RAI[21] = ("Fairness is a process, not a number",
    "<p>No single metric certifies a model as fair. Fairness work means involving the people affected, documenting choices and their reasons, and keeping the ability to question, override and switch off the system. Metrics are evidence for that conversation, not a replacement for it.</p>")
