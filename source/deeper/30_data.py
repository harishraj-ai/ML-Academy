# Lesson 30 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("Why a drift test's p-value raises alarms about harmless changes once you have lots of data, while the PSI measures how big a shift really is, "
          "and how bootstrapping shows whether a new model's small improvement is real before replacing the current one.")

QUIZ = [
    ("With 50,000 live rows, a KS test gives p ≈ 0.000001 for a 0.03-standard-deviation shift. What should you conclude?",
     [("a", "The shift is real but tiny; judge it by its size, not the p-value"), ("b", "Retrain immediately"), ("c", "The test is broken")], "a",
     "Large samples make trivial differences significant."),
    ("Why is PSI more useful than a p-value for drift alerts?",
     [("a", "It measures the size of the shift"), ("b", "It's always smaller"), ("c", "It needs no data")], "a",
     "Effect sizes don't grow just because the sample does."),
    ("A challenger's AUC is 0.004 higher, with a 95% interval for the gain of −0.02 to 0.03. What should you do?",
     [("a", "Replace the champion"), ("b", "Keep the champion or gather more evidence"), ("c", "Average them")], "b",
     "The improvement isn't distinguishable from noise."),
    ("Why compare champion and challenger on the same test rows?",
     [("a", "It's a paired comparison, which removes row-to-row noise"), ("b", "It's faster"), ("c", "It makes AUC higher")], "a",
     "Both models face the same hard and easy cases."),
    ("What's the strongest evidence that a new model is better for the business?",
     [("a", "A higher offline AUC"), ("b", "A controlled online test (canary or A/B) measuring the business outcome"), ("c", "A lower training loss")], "b",
     "Offline metrics are only a proxy."),
]

IQ = [
    (3, "Your drift monitor alerts every day on several features. What's going wrong, and how do you fix it?",
     "\"Retrain every day.\"",
     "Probably it alerts on p-values from large samples, so trivial shifts are significant. Alert on effect sizes (PSI, KS statistic, standardised mean change) with thresholds tied to business impact, prioritise features by importance to the model, aggregate over sensible windows, and confirm with performance metrics when labels arrive. Tune thresholds on historical data to an acceptable false-alarm rate."),
]

EX = [
    ("Intermediate", "Bootstrapped AUC improvements have a 2.5th percentile of 0.004 and a 97.5th of 0.031. Is the challenger better?",
     "Yes: the whole 95% interval is above 0, so the improvement is unlikely to be noise (though it may still be small)."),
    ("Intermediate", "A feature's mean shifts by 0.6 units; its training standard deviation is 4. Express the shift in standard deviations.",
     "0.6/4 = 0.15 standard deviations."),
]

CHECKS = {
    1: [("Shift", 0.15, "Mean change ÷ standard deviation.")],
}
