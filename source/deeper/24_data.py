# Lesson 24 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("When two features carry the same information, explanation methods disagree: permutation importance shows "
          "what the model uses, drop-column importance shows what is replaceable, and SHAP splits credit "
          "arbitrarily between near-copies. For linear models, a feature's SHAP value is simply its weight times "
          "how far the value is from average.")

QUIZ = [
    ("Two near-identical features both have drop-column importance close to 0. The best conclusion is…",
     [("a", "Both are useless"), ("b", "Each one is replaceable by the other; together they may matter a lot"), ("c", "The model is broken")], "b",
     "Dropping one lets the model use the other. Drop or shuffle them as a group to see their joint importance."),
    ("For a linear model with weight 2 on feature $x$, mean of $x$ 5 and a row with $x = 8$, the SHAP value of $x$ is…",
     [("a", "16"), ("b", "6"), ("c", "2")], "b",
     "$w(x - \\bar{x}) = 2 \\times 3 = 6$."),
    ("What does drop-column importance require that permutation importance doesn't?",
     [("a", "Retraining the model once per feature"), ("b", "Labels"), ("c", "A linear model")], "a",
     "That's why it's expensive, but it measures how replaceable each feature's information is."),
    ("Global SHAP importance is usually computed as…",
     [("a", "The sum of SHAP values"), ("b", "The mean of absolute SHAP values over many rows"), ("c", "The largest weight")], "b",
     "Absolute values stop positive and negative contributions cancelling out."),
    ("Interventional SHAP treats features as…",
     [("a", "Independent when filling in absent features"), ("b", "Causal"), ("c", "Always correlated")], "a",
     "It explains the model's behaviour; conditional SHAP respects correlations in the data instead."),
]

IQ = [
    (3, "Permutation importance, drop-column importance and SHAP rank your features differently. How do you explain that to a stakeholder?",
     "Picking whichever ranking looks most sensible.",
     "They answer different questions. Permutation importance: how much does this trained model rely on the feature's information? Drop-column: how much would we lose if the feature didn't exist and we retrained (low for features with substitutes)? SHAP: how much does each feature move individual predictions from the baseline? Correlated features cause most of the disagreement, so report correlated groups together and say which question each number answers."),
    (2, "What's the closed-form SHAP value for a linear model, and what assumption does it rely on?",
     "Saying the SHAP value equals the weight.",
     "$\\phi_j = w_j(x_j - E[x_j])$: the weight times the row's deviation from the feature's mean. It assumes features are independent (interventional SHAP), so with correlated features it explains the model's arithmetic rather than how the features move together in reality."),
]

EX = [
    ("Intermediate", "A linear model is $f = 10 + 2x_1 - 3x_2$, with feature means $\\bar{x}_1 = 4$, $\\bar{x}_2 = 1$. For the row $(6, 2)$, compute both SHAP values and check that baseline + contributions = prediction.",
     "$\\phi_1 = 2(6 - 4) = 4$; $\\phi_2 = -3(2 - 1) = -3$. Baseline $f(\\bar{\\mathbf{x}}) = 10 + 8 - 3 = 15$. $15 + 4 - 3 = 16$, and $f(6, 2) = 10 + 12 - 6 = 16$ ✓."),
    ("Intermediate", "A model scores $R^2 = 0.80$. Retrained without feature A it scores 0.79; without feature B, 0.60. What are the drop-column importances?",
     "A: $0.01$ (largely replaceable). B: $0.20$ (unique, important information)."),
]

CHECKS = {
    0: [("SHAP values (x₁, x₂)", [4, -3], "w(x − mean) for each."), ("Baseline", 15, "The prediction at the feature means.")],
    1: [("Drop-column importances (A, B)", [0.01, 0.2], "Full score minus the score without each feature.")],
}
