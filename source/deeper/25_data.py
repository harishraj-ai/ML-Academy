# Lesson 25 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("How to turn a class-weighted model's inflated probabilities back into real risks with one formula, and "
          "why Isolation Forest works: a far-away point is cut off by random splits in about 2 steps, while a "
          "typical point needs about 15.")

QUIZ = [
    ("A model trained with balanced weights gives $p = 0.5$. The real positive rate is 2%. What is the corrected probability?",
     [("a", "0.5"), ("b", "About 0.02"), ("c", "About 0.25")], "b",
     "Odds $1 \\times 0.02/0.98 = 0.0204$, so $p \\approx 0.020$."),
    ("Why do class weights inflate predicted probabilities?",
     [("a", "The model learns as if positives were much more common than they are"), ("b", "They add noise"), ("c", "They change the features")], "a",
     "Weighting positives up is equivalent to changing the prior class balance."),
    ("In Isolation Forest, a short average path length means…",
     [("a", "The point is typical"), ("b", "The point is easy to isolate, so it's likely an anomaly"), ("c", "The tree is too deep")], "b",
     "Few, different points get separated after few random splits."),
    ("Why can Isolation Forest use small subsamples (such as 256 points) per tree?",
     [("a", "Anomalies stand out even in small samples, and smaller samples reduce masking by dense clusters"), ("b", "It can't handle more data"), ("c", "To save labels")], "a",
     "Subsampling keeps it fast and often improves detection."),
    ("After oversampling to 50/50, the simplest fix for probabilities is…",
     [("a", "Ignore it"), ("b", "Apply the prior-odds correction or recalibrate on held-out data"), ("c", "Retrain with more trees")], "b",
     "Either restores realistic risk estimates."),
]

IQ = [
    (3, "You trained on a 50/50 resampled dataset, but the real positive rate is 1%. How do you get calibrated probabilities?",
     "Using the raw scores as risks.",
     "Apply the prior correction: multiply the model's odds by $\\pi/(1-\\pi)$ divided by the training odds (1 for 50/50), then convert back to a probability. Equivalently, add $\\log\\frac{\\pi}{1-\\pi} - \\log\\frac{\\pi_{train}}{1-\\pi_{train}}$ to the logit. Or recalibrate on a held-out set with the real class balance (Platt scaling or isotonic regression). Verify with a reliability table and the Brier score."),
]

EX = [
    ("Intermediate", "A balanced-weight model outputs $p = 0.8$. The true positive rate is 5%. Compute the corrected probability.",
     "Model odds $= 0.8/0.2 = 4$. Prior odds $= 0.05/0.95 = 0.05263$. Corrected odds $= 0.2105$, so $p = 0.2105/1.2105 \\approx 0.174$."),
    ("Intermediate", "An Isolation Forest uses subsamples of 256 points. Roughly what average path length is expected for a typical point, using $2\\ln n$?",
     "$2\\ln 256 = 2 \\times 5.545 \\approx 11.1$ splits (the exact normalising constant is a little smaller, about 10.2)."),
]

CHECKS = {
    0: [("Corrected probability", 0.1739, "Multiply the odds by 0.05/0.95, then p = odds/(1 + odds).")],
    1: [("2 ln 256", 11.09, "Natural log of 256, doubled.", 0.05)],
}
