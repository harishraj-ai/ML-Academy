# Lesson 25: Imbalanced Data & Anomaly Detection. Patches the shared per-lesson dictionaries on import.
import context, extras_ex_b, checks, running_code, running_text, challenges, reference, understanding, rai

L25 = (25, 5, "Imbalanced Data & Anomaly Detection", "Rare events: the right metrics, thresholds vs class weights vs resampling, SMOTE, and finding anomalies without labels with z-scores, Isolation Forest and LOF.", 55)

OBJ25 = ["Explain why accuracy fails on rare classes and choose recall, precision, average precision or cost instead",
         "Compare threshold moving, class weights, oversampling and SMOTE, and apply them without leakage",
         "Detect anomalies without labels using z-scores, the IQR rule, Isolation Forest and Local Outlier Factor",
         "Evaluate a detector with precision in the top k and plan how it runs in practice"]

SRC25 = [("He & Garcia (2009) — Learning from Imbalanced Data, IEEE TKDE", "https://ieeexplore.ieee.org/document/5128907"),
         ("Chawla et al. (2002) — SMOTE: Synthetic Minority Over-sampling Technique, JAIR", "https://www.jair.org/index.php/jair/article/view/10302"),
         ("Liu, Ting & Zhou (2008) — Isolation Forest", "https://ieeexplore.ieee.org/document/4781136"),
         ("Breunig et al. (2000) — LOF: Identifying Density-Based Local Outliers", "https://dl.acm.org/doi/10.1145/342009.335388"),
         ("Saito & Rehmsmeier (2015) — The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets", "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118432"),
         ("scikit-learn — Novelty and outlier detection", "https://scikit-learn.org/stable/modules/outlier_detection.html"),
         ("van den Goorbergh et al. (2022) — The harm of class imbalance corrections for risk prediction models, JAMIA", "https://academic.oup.com/jamia/article/29/9/1525/6605096")]

context.DEPS[25] = [8, 9, 16]
context.REFRESH[25] = "With rare classes, judge by precision, recall or average precision; a tuned threshold often beats reweighting, and anomalies can be found without labels by modelling normal data."
context.FIT[25] = "Applies the metrics of Lesson 9 and the calibration and imbalance ideas of Lesson 8 to rare events, and uses the density ideas of clustering (Lesson 16) to find anomalies without labels."
context.USE[25] = (["Fraud and money-laundering detection",
                    "Predictive maintenance and quality control (rare failures and defects)",
                    "Rare-disease screening, intrusion detection and monitoring data pipelines for bad records"],
                   "Whenever the class you care about is rare, or when you need to find unusual cases nobody has labelled.",
                   "the classes are roughly balanced: then ordinary methods and metrics work.")
context.FAQ[25] = [
    ("How rare is \"imbalanced\"?",
     "There's no hard line, but below about 10% positives accuracy starts to mislead, and below 1% the choice of metric and threshold dominates everything else."),
    ("Should I always use SMOTE?",
     "No. It sometimes helps flexible models, but often a calibrated model with a tuned threshold does as well or better, and class-imbalance corrections can distort risk estimates. Compare on average precision or cost with untouched validation data."),
    ("Isolation Forest or LOF?",
     "Isolation Forest is fast, scales to large data and works well in many dimensions. LOF judges each point against its local neighbourhood, so it's better when normal data has clusters of different densities, but it's slower on large datasets."),
    ("What's the difference between outlier detection and novelty detection?",
     "Outlier detection finds unusual points inside a dataset that may contain them. Novelty detection trains on clean, normal data and flags new points that don't fit, as a one-class model would."),
]
understanding.MYTHS[25] = [
    ("You must balance the classes before training.", "Many models train fine on imbalanced data; what must change is the metric and the threshold. Rebalancing is optional and can hurt calibration and ranking."),
    ("A high ROC-AUC means the alerts will be useful.", "With very rare positives, even a small false-positive rate floods analysts with false alarms. Check precision and average precision (Lesson 9's \"Going deeper\")."),
    ("Anomalies are just points far from the average.", "With several clusters, unusual points can sit near the overall average. Judge points against their local neighbourhood."),
]
extras_ex_b.MISTAKES[25] = [
    "Reporting accuracy on a dataset with 1% positives.",
    "Oversampling or applying SMOTE before splitting, so copies leak into the test set.",
    "Using a class-weighted model's probabilities as if they were real risks.",
    "Tuning the threshold on the test set.",
    "Assuming unflagged cases are normal, without ever checking a sample of them.",
]
extras_ex_b.EX[25] = [
    ("By hand", "1,000 transactions include 10 frauds. A model flags 25, of which 8 are fraud. Compute accuracy, recall and precision.",
     "Correct: 8 true positives + (990 − 17) true negatives = 981, so accuracy is 0.981. Recall = 8/10 = 0.8. Precision = 8/25 = 0.32."),
    ("By hand", "A training set has 19,600 negatives and 400 positives. What balanced class weights does scikit-learn give each class, using $n/(k\\,n_c)$?",
     "$n = 20{,}000$, $k = 2$. Negatives: $20{,}000/39{,}200 \\approx 0.510$. Positives: $20{,}000/800 = 25$."),
    ("By hand", "SMOTE picks a positive at $(2, 4)$ and its neighbour $(6, 2)$, with random gap 0.25. Where is the new point?",
     "$(2, 4) + 0.25\\,(4, -2) = (3, 3.5)$."),
    ("By hand", "Values: 10, 12, 11, 13, 12, 40. Using the quartiles $Q_1 = 11$ and $Q_3 = 13$, which values does the IQR rule (beyond $1.5 \\times$ IQR) flag?",
     "IQR $= 2$; the fences are $11 - 3 = 8$ and $13 + 3 = 16$. Only 40 is flagged."),
    ("Code", "In the anomaly code, change LocalOutlierFactor's <code>n_neighbors</code> to 5 and to 50. How does its precision in the top 20 change?",
     "Very small neighbourhoods make LOF noisy (a few close anomalies can look like a dense cluster); very large ones blur local structure towards a global view. Try both and compare with 20; the best value depends on cluster sizes and is worth tuning on labelled examples."),
]
checks.CHECKS[(25, 0)] = [("Accuracy", 0.981, "(true positives + true negatives) ÷ 1000."), ("Recall", 0.8, "8 ÷ 10."), ("Precision", 0.32, "8 ÷ 25.")]
checks.CHECKS[(25, 1)] = [("Negative weight", 0.5102, "20,000 ÷ (2 × 19,600)."), ("Positive weight", 25, "20,000 ÷ (2 × 400).")]
checks.CHECKS[(25, 2)] = [("New point", [3, 3.5], "point + gap × (neighbour − point).")]
checks.CHECKS[(25, 3)] = [("Flagged value", 40, "Fences at Q1 − 1.5·IQR and Q3 + 1.5·IQR.")]

running_code.CODE[25] = '''import pandas as pd
import numpy as np
df = pd.read_csv("houses.csv")   # download it from Lesson 1
from sklearn.ensemble import IsolationForest
cols = ["size_m2", "price_lakh", "dist_km", "age_yrs"]
iso = IsolationForest(n_estimators=500, random_state=0).fit(df[cols])
df["oddness"] = -iso.score_samples(df[cols])            # higher = more unusual
print(df.sort_values("oddness", ascending=False)[["id", "area", "description", "oddness"]].head(3).round(3).to_string(index=False))'''
running_text.INTRO[25] = ("Which Chennai homes look least like the others? An Isolation Forest on size, price, distance and age ranks every house by how easily it can be isolated. "
    "The three Outskirts homes come out on top (scores 0.578, 0.558 and 0.546): they are the only houses more than 20 km from the centre. With 12 houses the scores are rough, but a ranked list like this is where an analyst starts checking for data errors or genuinely unusual properties.")

challenges.C[25] = [
    ("Recall and precision from counts", "A detector flags 30 cases, 12 of which are real anomalies, out of 20 anomalies in total. Compute recall.",
     'flagged, true_in_flagged, total_anomalies = 30, 12, 20\n##BLANK##',
     'recall', 'recall = true_in_flagged / total_anomalies', "Recall is caught anomalies divided by all anomalies.",
     'recall = true_in_flagged / flagged  # ← that is precision; compute recall'),
    ("A z-score detector", "Flag the values whose z-score is above 2 in absolute value.",
     'import numpy as np\nx = np.array([10, 11, 9, 10, 12, 30, 10, 11])\nz = (x - x.mean()) / x.std()\n##BLANK##\nresult = x[flags].tolist()',
     'result', 'flags = np.abs(z) > 2', "Compare the absolute z-score with 2.",
     'flags = z > 100  # ← replace with the right condition'),
]

reference.GLOSSARY += [
    ("Class imbalance", "When one class is far rarer than the others, so accuracy becomes misleading.", 25, "why"),
    ("SMOTE", "Synthetic Minority Over-sampling Technique: creates new minority examples on lines between a minority point and its minority neighbours.", 25, "smote"),
    ("Isolation Forest", "An anomaly detector that isolates points with random splits; anomalies need fewer splits.", 25, "anomaly"),
    ("Local Outlier Factor (LOF)", "An anomaly score comparing a point's local density with its neighbours' densities.", 25, "anomaly"),
    ("Precision at k", "The share of real positives among the k highest-scored cases, used when people review a ranked list.", 25, "anomaly"),
]

rai.RAI[25] = ("Who pays for a false alarm?",
    "<p>In fraud and safety systems, false alarms are not free: a blocked card, a frozen account or an unnecessary investigation lands on a real person, and often unevenly across groups. Measure false-positive rates per group (Lesson 21), give people a fast way to contest a flag, and budget alerts so humans can review them properly rather than rubber-stamping.</p>")
