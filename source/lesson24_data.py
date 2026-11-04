# Lesson 24: Interpretability & Explainable ML. Patches the shared per-lesson dictionaries on import.
import context, extras_ex_b, checks, running_code, running_text, challenges, reference, understanding, rai

L24 = (24, 5, "Interpretability & Explainable ML", "Explain models globally and locally: standardised weights, permutation importance, partial dependence and ICE, SHAP values from scratch, LIME, and the traps.", 60)

OBJ24 = ["Tell global from local explanations and choose a method for each question",
         "Compute and read permutation importance and partial-dependence / ICE plots",
         "Compute Shapley values by hand for a small model and explain their fairness properties",
         "Spot misleading explanations: correlated features, unrealistic inputs and importance mistaken for causation"]

SRC24 = [("Molnar — Interpretable Machine Learning (free online book)", "https://christophm.github.io/interpretable-ml-book/"),
         ("Lundberg & Lee (2017) — A Unified Approach to Interpreting Model Predictions (SHAP)", "https://arxiv.org/abs/1705.07874"),
         ("Ribeiro, Singh & Guestrin (2016) — \"Why Should I Trust You?\": Explaining the Predictions of Any Classifier (LIME)", "https://arxiv.org/abs/1602.04938"),
         ("Breiman (2001) — Random Forests (permutation importance)", "https://link.springer.com/article/10.1023/A:1010933404324"),
         ("Goldstein et al. (2015) — Peeking Inside the Black Box: Visualizing Statistical Learning with Plots of Individual Conditional Expectation", "https://arxiv.org/abs/1309.6392"),
         ("Apley & Zhu (2020) — Visualizing the effects of predictor variables in black box supervised learning models (ALE)", "https://arxiv.org/abs/1612.08468"),
         ("Rudin (2019) — Stop explaining black box machine learning models for high stakes decisions", "https://www.nature.com/articles/s42256-019-0048-x"),
         ("scikit-learn — Inspection: permutation importance and partial dependence", "https://scikit-learn.org/stable/inspection.html")]

context.DEPS[24] = [6, 13, 14]
context.REFRESH[24] = "Permutation importance, partial dependence and SHAP explain what a model relies on; Shapley contributions add up exactly to prediction minus baseline."
context.FIT[24] = "Opens up the models of Parts 2–5. It builds on standardised weights (Lesson 6), tree importances and their flaws (Lessons 13–14) and turns them into trustworthy explanations."
context.USE[24] = (["Explaining credit, insurance and medical decisions to customers and regulators",
                    "Debugging models that learned shortcuts or leaked features",
                    "Building stakeholder trust and choosing which features to collect"],
                   "Whenever a model's predictions affect people or must be justified, and always while debugging.",
                   "you could use a simple model that is interpretable by design and nearly as accurate.")
context.FAQ[24] = [
    ("Should I use SHAP or permutation importance?",
     "Both, for different questions. Permutation importance gives a quick, honest global ranking on test data. SHAP explains individual predictions and, aggregated, also gives global views. For tree models, TreeSHAP is fast and exact."),
    ("Do I need the shap library?",
     "For real projects, yes: it implements fast approximations and plots. This lesson computes exact Shapley values from scratch so you know what the library is doing, but the exact method needs 2^p evaluations and only works for a handful of features."),
    ("Can explanations prove a model is fair?",
     "No. They show what a model uses, which helps you find proxies and shortcuts (Lesson 21), but fairness is judged by outcomes and error rates per group."),
    ("Why do different methods rank features differently?",
     "They measure different things: weights, score drops on test data, impurity on training data, average contributions. Correlated features also share credit in method-dependent ways. Report which method you used."),
]
understanding.MYTHS[24] = [
    ("A feature with high importance causes the outcome.", "It's what the model relies on. The feature may just be correlated with the true cause."),
    ("SHAP values tell you what would happen if you changed a feature.", "They split one prediction into contributions relative to a baseline. What-if questions need the model's curve (ICE) or, for the real world, causal analysis."),
    ("Deep models can't be explained, so they can't be trusted.", "Many tools work for any model. But for high-stakes decisions, an interpretable model is often almost as accurate and is easier to trust."),
]
extras_ex_b.MISTAKES[24] = [
    "Comparing raw linear weights of features measured in different units.",
    "Computing permutation importance on training data, where overfitting inflates it.",
    "Reading importance as causation.",
    "Trusting a PDP when the feature is strongly correlated with others (use ALE or ICE).",
    "Reporting a single LIME explanation without checking that it is stable.",
]
extras_ex_b.EX[24] = [
    ("By hand", "A model scores 0.90 accuracy on test data. Shuffling feature A gives 0.82, shuffling B gives 0.89 and shuffling C gives 0.90. Give the three permutation importances. Is C useless?",
     "A: 0.08, B: 0.01, C: 0. C adds no <em>unique</em> information to this model, but it may be correlated with A or B, so it isn't necessarily useless on its own."),
    ("By hand", "For $f = 3x_1 + 2x_2 + 6x_1x_2$ explained at $(1, 1)$ against the baseline $(0, 0)$, compute both Shapley values.",
     "$x_1$: own effect 3 plus half the interaction, 3, so 6. $x_2$: 2 plus 3, so 5. Check: $6 + 5 = 11 = f(1, 1) - f(0, 0)$."),
    ("By hand", "With 3 features, what weight does the Shapley formula give to a coalition $S$ of size 1 when computing $\\phi_j$? (Use $|S|!(p-|S|-1)!/p!$.)",
     "$1! \\times 1!/3! = 1/6 \\approx 0.1667$. (Size 0 and size 2 coalitions each get $2/6 = 1/3$.)"),
    ("By hand", "A model's baseline prediction is 50 lakh. For one house the SHAP values are size +12, distance −8 and age −3. What does the model predict?",
     "$50 + 12 - 8 - 3 = 51$ lakh."),
    ("Code", "In the lesson's Shapley code, explain patient 0 instead of patient 200. Check that the contributions still add up exactly to prediction minus baseline.",
     "Change <code>x = X4[200]</code> to <code>x = X4[0]</code>. The printed baseline plus the sum of contributions equals the model's prediction to the second decimal, as the efficiency property guarantees."),
]
checks.CHECKS[(24, 0)] = [("Importances A, B, C", [0.08, 0.01, 0], "Original score minus shuffled score.")]
checks.CHECKS[(24, 1)] = [("Shapley value of x₁", 6, "Own effect plus half the interaction."), ("Shapley value of x₂", 5, "2 plus half of 6.")]
checks.CHECKS[(24, 2)] = [("Weight", 0.16667, "1! × 1! / 3!.")]
checks.CHECKS[(24, 3)] = [("Prediction", 51, "Baseline plus all contributions.")]

running_code.CODE[24] = '''import pandas as pd
import numpy as np
df = pd.read_csv("houses.csv")   # download it from Lesson 1
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
cols = ["size_m2", "dist_km", "age_yrs"]
Xs = StandardScaler().fit_transform(df[cols])
lr = LinearRegression().fit(Xs, df["price_lakh"])
base = lr.intercept_                                  # average price (features are centred)
contrib = Xs * lr.coef_                               # for a linear model, SHAP = weight × centred value
h = 4                                                 # house id 5
print("baseline", round(base, 1), "| contributions:", {c: float(v) for c, v in zip(cols, contrib[h].round(1))})
print("prediction", round(base + contrib[h].sum(), 1), "| actual", df.price_lakh[h])'''
running_text.INTRO[24] = ("For a linear model with standardised features, each feature's SHAP value is simply its weight times its centred value, so explanations are exact and cheap. "
    "House 5 (a new Suburb villa) starts from the average price, then gains for its size, loses a little for its distance, and gains for being new; the contributions add up exactly to the model's prediction.")

challenges.C[24] = [
    ("Permutation importance by hand", "Shuffle one column and measure how much the score drops.",
     'import numpy as np\nrng = np.random.default_rng(0)\nX = rng.normal(size=(500, 2)); y = 3 * X[:, 0] + 0.1 * rng.normal(size=500)\nw = np.array([3.0, 0.0])\nscore = lambda X: -np.mean((X @ w - y) ** 2)\nXp = X.copy(); Xp[:, 0] = rng.permutation(Xp[:, 0])\n##BLANK##\nresult = round(float(drop), 1)',
     'result', 'drop = score(X) - score(Xp)', "Original score minus the score with feature 0 shuffled.",
     'drop = score(X)  # ← replace: subtract the shuffled score'),
    ("Shapley values for two features", "For f(a, b) = 2a + 4ab at (1, 1) with baseline (0, 0), compute a's Shapley value as the average of its two marginal contributions.",
     'f = lambda a, b: 2 * a + 4 * a * b\n##BLANK##',
     'phi_a', 'phi_a = ((f(1, 0) - f(0, 0)) + (f(1, 1) - f(0, 1))) / 2', "a joins first (adds f(1,0) − f(0,0)) or second (adds f(1,1) − f(0,1)); average the two.",
     'phi_a = f(1, 1)  # ← replace with the average marginal contribution'),
]

reference.GLOSSARY += [
    ("Permutation importance", "The drop in a model's held-out score when one feature's values are randomly shuffled.", 24, "permutation"),
    ("Partial dependence plot (PDP)", "A curve of the average prediction as one feature is set to each value in turn for every row.", 24, "pdp"),
    ("ICE plot", "Individual conditional expectation: one partial-dependence curve per row, revealing differences between rows.", 24, "pdp"),
    ("Shapley value", "A feature's fair share of a prediction minus the baseline: its average marginal contribution over all orders in which features could be added.", 24, "shap"),
    ("SHAP", "SHapley Additive exPlanations: methods and a library that compute Shapley values for model predictions efficiently.", 24, "shap"),
    ("LIME", "Local Interpretable Model-agnostic Explanations: fits a simple weighted model around one prediction to explain it.", 24, "lime"),
]

rai.RAI[24] = ("Explanations people can act on",
    "<p>Laws such as the EU's GDPR and AI Act, and lending rules in many countries, expect meaningful reasons for automated decisions. A useful explanation is one the affected person can understand and act on (\"your debt-to-income ratio was the main factor\"), not a list of 40 numbers. Check that explanations are faithful to the model, stable, and don't reveal other people's data.</p>")
