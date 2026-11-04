# Lesson 21 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("Why fairness metrics conflict, with the one-line identity that proves it, a perfectly calibrated model "
          "that still has very different error rates for two groups, what group-specific thresholds gain and "
          "cost, and why fairness numbers for small groups need error bars.")

QUIZ = [
    ("Two groups have different base rates. A model has equal precision and equal TPR in both. Its FPRs must be…",
     [("a", "Equal"), ("b", "Different (unless the model is perfect)"), ("c", "Zero")], "b",
     "From $\\text{FPR} = \\frac{p}{1-p}\\cdot\\frac{1-\\text{PPV}}{\\text{PPV}}\\cdot\\text{TPR}$, different $p$ forces different FPR."),
    ("A model is perfectly calibrated in both groups. Does that guarantee equal true-positive rates?",
     [("a", "Yes"), ("b", "No: with different base rates, TPR and FPR usually differ"), ("c", "Only with a 0.5 threshold")], "b",
     "In the example, calibrated scores gave TPR 0.232 vs 0.631."),
    ("Lowering one group's threshold to equalise TPR typically…",
     [("a", "Raises that group's false-positive rate"), ("b", "Changes nothing else"), ("c", "Raises its precision")], "a",
     "More people are flagged, including more true negatives: in the example FPR rose from 0.060 to 0.320."),
    ("A group's TPR is 0.23 measured on 100 positives. What should you report?",
     [("a", "Just 0.23"), ("b", "0.23 with a confidence interval, which is wide for so few cases"), ("c", "Nothing")], "b",
     "With about 100 positives the 95% interval spans roughly ±0.08."),
    ("Who should decide which fairness metric matters most?",
     [("a", "The algorithm"), ("b", "People who understand the decision and its harms, including those affected"), ("c", "Whoever has the highest accuracy")], "b",
     "The metrics encode different values; choosing between them is not a technical question."),
]

IQ = [
    (3, "Prove that equal precision, equal TPR and equal FPR can't all hold across groups with different base rates.",
     "Only citing the paper.",
     "From the confusion matrix, $\\text{FP} = \\text{TP}(1 - \\text{PPV})/\\text{PPV}$, and $\\text{FPR} = \\text{FP}/N$, $\\text{TPR} = \\text{TP}/P$. So $\\text{FPR} = \\frac{P}{N}\\cdot\\frac{1-\\text{PPV}}{\\text{PPV}}\\cdot\\text{TPR} = \\frac{p}{1-p}\\cdot\\frac{1-\\text{PPV}}{\\text{PPV}}\\cdot\\text{TPR}$. If PPV and TPR are equal in both groups, FPR is proportional to $p/(1-p)$, which differs when base rates differ. Only a perfect classifier (PPV = 1, so FPR = 0) or equal base rates escape it."),
    (3, "Your audit shows a 6-point TPR gap between two groups. Is the model unfair?",
     "Answering yes or no from the point estimate.",
     "First, is the gap real? Compute bootstrap intervals; for small groups a 6-point gap can be noise. Second, is it the gap that matters for this decision (would a missed positive or a false positive cause the harm)? Third, look at calibration within groups and at intersections. Then compare mitigations (better data, thresholds, reweighting, changing the decision) with their costs, and document the choice."),
    (2, "What are group-specific thresholds, and what are their downsides?",
     "Presenting them as a free fix.",
     "Choosing a different decision threshold per group so that a target metric (for example TPR) matches. Downsides: other metrics (precision, FPR, accuracy) move, sometimes worse for the same group; it requires knowing the protected attribute at decision time; it may be legally restricted in some domains; and it treats the symptom, while the underlying data or feature gap remains."),
]

EX = [
    ("Intermediate", "A group has base rate $p = 0.2$, precision $0.6$ and TPR $0.75$. Use the identity to find its FPR.",
     "$\\text{FPR} = \\frac{0.2}{0.8}\\cdot\\frac{0.4}{0.6}\\cdot 0.75 = 0.25 \\times 0.6667 \\times 0.75 = 0.125$."),
    ("Intermediate", "Another group has the same precision ($0.6$) and TPR ($0.75$) but base rate $p = 0.5$. What is its FPR?",
     "$\\frac{0.5}{0.5}\\cdot\\frac{0.4}{0.6}\\cdot 0.75 = 1 \\times 0.6667 \\times 0.75 = 0.5$: four times the first group's, as the identity predicts."),
    ("Intermediate", "A TPR of 0.25 is measured on 100 positives. Using the normal approximation $\\pm 1.96\\sqrt{p(1-p)/n}$, give the 95% interval.",
     "$\\sqrt{0.25 \\times 0.75/100} = 0.0433$; $\\pm 1.96 \\times 0.0433 = \\pm 0.0849$. Interval about $[0.165,\\ 0.335]$."),
]

CHECKS = {
    0: [("FPR", 0.125, "(p/(1−p)) × ((1−PPV)/PPV) × TPR.")],
    1: [("FPR", 0.5, "Same formula with p = 0.5.")],
    2: [("95% interval (low, high)", [0.165, 0.335], "0.25 ± 1.96 × √(0.25 × 0.75 / 100).", 0.002)],
}
