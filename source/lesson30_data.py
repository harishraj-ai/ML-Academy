# Lesson 30: MLOps for Classical Models. Patches the shared per-lesson dictionaries on import.
import context, extras_ex_b, checks, running_code, running_text, challenges, reference, understanding, rai

L30 = (30, 6, "MLOps: Deploying & Monitoring Models", "Packaging and versioning, input validation, drift detection with PSI and KS tests, concept drift and retraining, behavioural tests, serving and rollout.", 55)

OBJ30 = ["Package a fitted pipeline with versioned metadata and verify it reloads identically",
         "Validate incoming data against a schema before predicting",
         "Detect data drift with PSI and the KS test, and concept drift by monitoring performance",
         "Write minimum-quality, directional and invariance tests, and choose a serving and rollout pattern"]

SRC30 = [("Sculley et al. (2015) — Hidden Technical Debt in Machine Learning Systems, NeurIPS", "https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html"),
         ("Breck et al. (2017) — The ML Test Score: A Rubric for ML Production Readiness", "https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/"),
         ("Ribeiro et al. (2020) — Beyond Accuracy: Behavioral Testing of NLP Models with CheckList", "https://aclanthology.org/2020.acl-main.442/"),
         ("Huyen (2022) — Designing Machine Learning Systems", "https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/"),
         ("Mitchell et al. (2019) — Model Cards for Model Reporting", "https://arxiv.org/abs/1810.03993"),
         ("MLflow documentation — Model Registry", "https://mlflow.org/docs/latest/model-registry.html")]

context.DEPS[30] = [5, 9, 20]
context.REFRESH[30] = "Ship the whole pipeline with metadata, validate inputs, watch for data and concept drift, retrain on a plan, and test model behaviour like code."
context.FIT[30] = "Extends Lesson 20's pipelines and deployment into the full life cycle, using the metrics of Lesson 9 and the distribution-shift ideas of Lesson 5."
context.USE[30] = (["Credit, fraud and churn models that run every day",
                    "Demand forecasts feeding stock and staffing systems",
                    "Any model whose predictions reach customers or automated decisions"],
                   "Whenever a model will run repeatedly on new data, outside a one-off analysis.",
                   "the analysis is a one-off report: then reproducibility matters, but monitoring and serving don't.")
context.FAQ[30] = [
    ("How often should I retrain?",
     "It depends on how fast the world changes. Start with a schedule that matches the pace (weekly for fraud, monthly or quarterly for slow-moving risk), then add triggers based on drift and performance. Always compare a new model with the current one before switching."),
    ("Do I need special MLOps tools?",
     "Not to start. Version code with git, pin library versions, save pipelines with metadata, log predictions, and schedule jobs. Tools such as MLflow, feature stores and monitoring platforms help as the number of models grows."),
    ("What's the difference between data drift and concept drift?",
     "Data drift: the inputs' distribution changes. Concept drift: the relationship between inputs and outcome changes. Data drift can be seen immediately; concept drift needs outcomes."),
    ("What should a model card contain?",
     "What the model is for and not for, the training data, metrics overall and by group, known limitations, the version, and who to contact."),
]
understanding.MYTHS[30] = [
    ("Once a model is deployed, the work is done.", "Models decay as the world changes; monitoring and retraining are ongoing work."),
    ("If input drift is detected, the model must be retrained.", "Drift is a warning; check whether performance has actually dropped before acting."),
    ("A high test score means the model is ready for production.", "It also needs input validation, behavioural tests, monitoring, logging and a rollback plan."),
]
extras_ex_b.MISTAKES[30] = [
    "Saving the model without its preprocessing, then re-implementing the preprocessing in production.",
    "Not recording library versions, so the model can't be reloaded later.",
    "Predicting on invalid inputs instead of rejecting or flagging them.",
    "Monitoring only inputs, never actual performance once outcomes arrive.",
    "Replacing a model without comparing it with the current one on recent data.",
]
extras_ex_b.EX[30] = [
    ("By hand", "A feature's training shares in two bins are 0.5 and 0.5; live shares are 0.7 and 0.3. Compute the PSI.",
     "Bin 1: (0.7 − 0.5) ln(0.7/0.5) = 0.2 × 0.3365 = 0.0673. Bin 2: (0.3 − 0.5) ln(0.3/0.5) = −0.2 × −0.5108 = 0.1022. PSI ≈ 0.170: moderate drift, worth investigating."),
    ("By hand", "A model's monthly AUC is 0.84, 0.83, 0.79, 0.74. Your retraining rule is \"retrain if AUC falls more than 0.05 below the launch value of 0.84\". In which month does it trigger?",
     "Month 4: 0.74 is 0.10 below 0.84 (month 3's 0.79 is exactly 0.05 below, which doesn't exceed it)."),
    ("By hand", "Name one directional test and one invariance test for a house-price model.",
     "Directional: increasing size (all else equal) shouldn't lower the price. Invariance: changing the listing ID or the seller's name shouldn't change the price."),
    ("By hand", "A canary rollout sends 5% of 40,000 daily requests to a new model. How many requests does it handle per day?",
     "0.05 × 40,000 = 2,000."),
    ("Code", "In the drift code, also shift the debt feature by +10 in the live data. How do its PSI and KS statistic change?",
     "Both rise sharply (PSI well above 0.25), flagging a major shift in debt too. Whether to retrain depends on whether performance drops, which needs outcomes."),
]
checks.CHECKS[(30, 0)] = [("PSI", 0.170, "Sum of (live − training) × ln(live ÷ training) over bins.", 0.002)]
checks.CHECKS[(30, 1)] = [("Month", 4, "Find the first month more than 0.05 below 0.84.")]
checks.CHECKS[(30, 3)] = [("Requests", 2000, "5% of 40,000.")]

running_code.CODE[30] = '''import pandas as pd
import numpy as np
df = pd.read_csv("houses.csv")   # download it from Lesson 1
import joblib
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
cols = ["size_m2", "bedrooms", "dist_km", "age_yrs"]
pipe = make_pipeline(StandardScaler(), Ridge(1.0)).fit(df[cols], df.price_lakh)
joblib.dump({"model": pipe, "features": cols, "version": "1.0.0"}, "price_model.joblib")
bundle = joblib.load("price_model.joblib")
new = pd.DataFrame({"size_m2": [95], "bedrooms": [2], "dist_km": [5], "age_yrs": [3]})
print("model", bundle["version"], "predicts", round(float(bundle["model"].predict(new[bundle["features"]])[0]), 1), "lakh")
ranges = {c: (df[c].min(), df[c].max()) for c in cols}
print("inside the training range:", {c: bool(ranges[c][0] <= new[c].iloc[0] <= ranges[c][1]) for c in cols})'''
running_text.INTRO[30] = ("Package the house-price pipeline as a versioned bundle: the fitted pipeline, its feature list and a version number, saved with joblib and loaded back as a service would. "
    "The reloaded model predicts 78.9 lakh for a 95 m², 2-bedroom home 5 km out and 3 years old, and a simple range check confirms every input lies within the training data. With only 12 training homes, inputs outside those ranges deserve a warning rather than a confident answer.")

challenges.C[30] = [
    ("Population stability index", "Compute the PSI between expected and actual bin shares.",
     'import numpy as np\ne = np.array([0.25, 0.25, 0.25, 0.25])\na = np.array([0.10, 0.20, 0.30, 0.40])\n##BLANK##\nresult = round(float(psi), 4)',
     'result', 'psi = np.sum((a - e) * np.log(a / e))', "Sum (a − e) × ln(a ÷ e) over the bins.",
     'psi = np.sum(a - e)  # ← multiply by the log ratio'),
    ("Validate a row", "Count the fields that are missing or not numbers.",
     'row = {"income": 50.0, "debt": None, "age": "40"}\nfields = ["income", "debt", "age"]\n##BLANK##',
     'bad', 'bad = sum(1 for f in fields if not isinstance(row.get(f), (int, float)))', "Check each field's type with isinstance and count the failures.",
     'bad = 0  # ← count the fields that fail the check'),
]

reference.GLOSSARY += [
    ("MLOps", "Practices for deploying, monitoring, retraining and maintaining ML models in production.", 30, "lifecycle"),
    ("Data drift", "A change in the distribution of a model's inputs compared with its training data.", 30, "drift"),
    ("Concept drift", "A change in the relationship between inputs and the outcome, which lowers performance.", 30, "monitor"),
    ("Population stability index (PSI)", "A drift measure: the sum over bins of (live share − training share) × ln(live ÷ training).", 30, "drift"),
    ("Canary deployment", "Sending a small share of traffic to a new model and increasing it if it performs well.", 30, "serving"),
]

rai.RAI[30] = ("Accountability after launch",
    "<p>Harm from models often appears after deployment: inputs shift for one region, a data pipeline breaks for one group, a model slowly drifts. Monitor metrics by group as well as overall, keep prediction logs so individual decisions can be explained and challenged, publish a model card with intended uses and limits, and make sure someone is responsible for acting when monitoring raises an alarm.</p>")
