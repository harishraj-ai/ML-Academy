# Lesson 9 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("Using metrics to make decisions: every test score needs an error bar, two models should be compared on "
          "the same cases (with the bootstrap or McNemar's test), the best threshold comes from what each kind of "
          "mistake costs, and when positives are rare, average precision tells you more than ROC-AUC.")

QUIZ = [
    ("Two models disagree on 30 test cases: model A is right on 16 of them and model B on 14. What does McNemar's test suggest?",
     [("a", "A is clearly better"), ("b", "No real evidence of a difference"), ("c", "B is clearly better")], "b",
     "A 16–14 split is just what coin flips would give. Only the disagreements matter, and they are nearly balanced."),
    ("A false negative costs 9 and a false positive costs 1. With calibrated probabilities, flag cases with $p$ above…",
     [("a", "0.5"), ("b", "0.9"), ("c", "0.1")], "c",
     "$c_{FP}/(c_{FP} + c_{FN}) = 1/10 = 0.1$."),
    ("Positives become 10 times rarer, but the model's score distributions for each class stay the same. ROC-AUC will…",
     [("a", "Stay about the same"), ("b", "Fall sharply"), ("c", "Rise")], "a",
     "TPR and FPR are each measured within one class, so class balance doesn't change the ROC curve. Precision and average precision do fall."),
    ("On a dataset with 2% positives, a model's average precision is 0.10. Compared with random guessing, that is…",
     [("a", "Worse"), ("b", "About 5 times better"), ("c", "Exactly random")], "b",
     "A random model's AP equals the positive rate, 0.02, so 0.10 is five times that, though still low in absolute terms."),
    ("To compare two models' AUCs with the bootstrap, you should…",
     [("a", "Bootstrap each model separately and see if the intervals overlap"), ("b", "Resample the same cases for both models and bootstrap the difference"), ("c", "Average the two AUCs")], "b",
     "Pairing removes the shared variation from the test set's difficulty, so the comparison is much more sensitive."),
]

IQ = [
    (3, "Model A scores 0.851 accuracy and model B 0.846 on the same test set. Which do you ship?",
     "Picking A because the number is bigger.",
     "First check whether the difference is real: use a paired test on the same cases (McNemar, or a paired bootstrap of the difference). With a few thousand test cases, 0.5 points is often within noise. If there's no clear difference, choose on other grounds: simplicity, speed, cost of errors on the business metric, calibration, fairness across groups, or how easy each is to maintain and explain."),
    (3, "How do you choose a classification threshold?",
     "\"Use 0.5\" or \"maximise F1\" by default.",
     "Ideally from costs: with calibrated probabilities, flag when $p > c_{FP}/(c_{FP} + c_{FN})$. Without clear costs, use an operating constraint, such as recall of at least 95% or at most 100 alerts per day, and choose the threshold on validation data, then confirm on the test set. Revisit it when the base rate changes, since precision depends on it."),
    (2, "When would you report average precision (PR-AUC) instead of ROC-AUC?",
     "Saying ROC-AUC is \"wrong\" for imbalanced data.",
     "When positives are rare and what matters is the quality of the alerts. ROC-AUC is unaffected by class balance, so it can look high while most alerts are false; average precision reflects that directly. Report AP together with its baseline (the positive rate). ROC-AUC is still useful for ranking quality and for comparing across datasets with different balance."),
    (3, "Why can't you use an ordinary t-test on the 10 fold scores of 10-fold cross-validation to compare two models?",
     "Thinking the 10 scores are independent samples.",
     "The training sets of different folds overlap by about 89%, so the fold scores are correlated and their variance is underestimated. A standard t-test then claims significance far too often. Use the corrected resampled t-test (Nadeau–Bengio), the 5×2 cross-validation test, or repeated CV with a correction, or compare on a single large held-out set with a paired test."),
]

EX = [
    ("Intermediate", "Two models are compared on 500 test cases. Model A alone is right on 25 of them and model B alone on 10. Under the null hypothesis each disagreement is a coin flip. What is the expected count for each model, and the McNemar statistic $(b - c)^2/(b + c)$?",
     "There are $35$ disagreements, so each would expect $17.5$. The statistic is $(25 - 10)^2/35 = 225/35 \\approx 6.43$. Compared with a $\\chi^2$ distribution with 1 degree of freedom (critical value 3.84), it is significant at the 5% level ($p \\approx 0.011$)."),
    ("Intermediate", "A missed fraud costs ₹5,000 and checking a false alert costs ₹200. What threshold minimises expected cost for a calibrated model?",
     "$200/(200 + 5000) = 200/5200 \\approx 0.0385$. Flag any transaction with predicted fraud probability above about 3.8%."),
    ("Intermediate", "A model flags 200 cases. 50 of the 200 are truly positive, and there are 80 positives in total. Compute precision and recall.",
     "Precision $= 50/200 = 0.25$. Recall $= 50/80 = 0.625$."),
    ("Code · intermediate", "Using the bootstrap code, compute a 95% interval for the logistic model's <em>accuracy</em> alone. Compare its width with the formula $\\pm 1.96\\sqrt{p(1-p)/n}$ for $n = 171$.",
     "Bootstrap <code>np.mean(logreg.predict(Xte[i]) == yte[i])</code> instead of the AUC difference. With $p = 0.959$ and $n = 171$, the formula gives $\\pm 1.96 \\times 0.0152 = \\pm 0.030$, roughly $[0.929,\\ 0.989]$. The bootstrap interval is similar. Even a 96% accuracy is uncertain by about ±3 points on 171 cases."),
]

CHECKS = {
    0: [("Expected count each", 17.5, "Half of the 35 disagreements."), ("McNemar statistic", 6.42857, "(b − c)² / (b + c).")],
    1: [("Threshold", 0.03846, "c_FP / (c_FP + c_FN).")],
    2: [("Precision", 0.25, "True positives ÷ flagged."), ("Recall", 0.625, "True positives ÷ all positives.")],
}
