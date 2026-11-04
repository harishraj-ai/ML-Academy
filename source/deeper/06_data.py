# Lesson 6 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("For trusting and explaining a model rather than just building one. You'll learn the four assumptions behind "
          "linear regression (LINE), how to tell which weights are real (standard errors, p-values, intervals), why "
          "overlapping features make weights unreliable (VIF), how to spot single points that bend the line, how to "
          "read a model of log(price), and how to use categories without falling into the dummy-variable trap.")

# (question, [(option id, text)], correct id, explanation)
QUIZ = [
    ("A feature has $\\text{VIF} = 10$. Compared with a feature unrelated to the others, its standard error is multiplied by about…",
     [("a", "$\\sqrt{10} \\approx 3.2$"), ("b", "10"), ("c", "100")], "a",
     "The VIF multiplies the <em>variance</em> of the weight; the standard error is its square root, so it grows by $\\sqrt{10}$."),
    ("Which of these is <strong>not</strong> an assumption of linear regression?",
     [("a", "The errors have about equal spread"), ("b", "The features are normally distributed"), ("c", "The errors are independent")], "b",
     "Only the <em>errors</em> matter (LINE). Features can have any distribution: a 0/1 dummy is fine as a feature."),
    ("A model predicts $\\log(\\text{price})$, and the weight on bedrooms is $0.10$. One extra bedroom is linked to a price that is…",
     [("a", "₹0.10 lakh higher"), ("b", "about 10.5% higher"), ("c", "10 times higher")], "b",
     "Adding 1 to the feature multiplies the price by $e^{0.10} = 1.105$, about 10.5% more."),
    ("A point has very high leverage but lies exactly on the line through the other points. Its Cook's distance is…",
     [("a", "Large: high leverage is always dangerous"), ("b", "Close to zero: its residual is tiny"), ("c", "Undefined")], "b",
     "Cook's distance multiplies the squared residual by a leverage factor. A point on the line has residual ≈ 0, so deleting it hardly changes anything. It's unusual, but not influential."),
    ("A category has 4 values and the model has a bias term. How many dummy columns should ordinary least squares get?",
     [("a", "4"), ("b", "3"), ("c", "1")], "b",
     "Leave one out as the baseline. All 4 would always add up to the bias column (the dummy-variable trap)."),
]

# (level, question, trap, answer) — level 3 = "Deep-dive" on the interview page
IQ = [
    (2, "What are the assumptions of linear regression, and which of them do you need just to get good predictions?",
     "Reciting the list without saying what each one is for.",
     "Linearity, independent errors, normally distributed errors and equal error spread (LINE). For predictions checked on a test set, none is strictly required, although a badly wrong linearity assumption will show up as poor test error. The assumptions matter for <em>inference</em>: trusting standard errors, p-values and confidence intervals. Independence and equal spread affect the SEs most; normality matters only in small samples."),
    (3, "A feature's p-value is 0.4. Should you remove it from the model?",
     "\"Yes — it isn't significant.\"",
     "Not automatically. A large p-value means the data can't pin the effect down, not that the effect is zero. It may overlap with another feature (check its VIF), the sample may be small, or domain knowledge may say it belongs. For prediction, decide with cross-validation; for explanation, report its confidence interval honestly instead of deleting it quietly."),
    (3, "Two features are 95% correlated. What happens to the model's predictions, and to its weights?",
     "Saying the model becomes inaccurate.",
     "Predictions are usually fine: the model only needs the shared information, and either feature carries it. The individual weights become unstable, with huge standard errors (high VIF), and can even flip sign between samples, so you can't interpret them. Fixes: drop or merge one feature, or use ridge regression, which splits the credit smoothly."),
    (3, "Why do we minimise squared error rather than, say, absolute error?",
     "\"Because squares are easier to differentiate.\"",
     "That's part of it (it gives a closed-form solution), but the deeper reasons are statistical. If the noise is normal, least squares is the maximum-likelihood estimate. By the Gauss–Markov theorem, it is also the best linear unbiased estimator whenever the errors are uncorrelated with equal spread. Absolute error is the maximum-likelihood choice for heavier-tailed (Laplace) noise and is more robust to outliers; Huber loss is a compromise."),
    (3, "What's the difference between an outlier, a high-leverage point and an influential point?",
     "Using the three words as if they meant the same thing.",
     "An outlier has an unusual $y$ (large residual). A high-leverage point has unusual $x$ values (large diagonal entry of the hat matrix), so the line is forced to pass near it. An influential point actually changes the fit a lot when removed. That usually takes both: high leverage <em>and</em> off the line. Cook's distance measures influence directly."),
    (2, "You one-hot encode a 3-level category, keep all 3 columns, and fit ordinary least squares with an intercept. What goes wrong?",
     "Expecting an error message every time.",
     "The 3 dummies always sum to the intercept column, so $X^\\top X$ is singular: the dummy-variable trap. The weights have no unique solution. Some solvers (including scikit-learn's) still return an answer, but the individual weights mean nothing. Drop one level (it becomes the baseline), or use regularization, which makes the solution unique."),
]

# Practice exercises, tagged as intermediate. (tag, question, solution)
EX = [
    ("Intermediate", "A model with $d = 4$ features is fitted to $n = 50$ points and has training $R^2 = 0.80$. Compute the adjusted $R^2$.",
     "$R^2_{\\text{adj}} = 1 - (1 - 0.80)\\cdot\\frac{50 - 1}{50 - 4 - 1} = 1 - 0.20 \\times \\frac{49}{45} = 1 - 0.2178 = 0.782$."),
    ("Intermediate", "Feature $j$ can be predicted from the other features with $R_j^2 = 0.9$. What is its VIF, and by what factor is its standard error inflated?",
     "$\\text{VIF} = 1/(1 - 0.9) = 10$. The variance is multiplied by 10, so the standard error is multiplied by $\\sqrt{10} \\approx 3.162$."),
    ("Intermediate", "A weight is $\\hat{w} = 4.0$ with standard error $1.5$, from $n = 200$ points and $d = 3$ features. Compute its t-statistic and its 95% confidence interval, using $t^{*} = 1.97$.",
     "$t = 4.0/1.5 = 2.667$. Interval: $4.0 \\pm 1.97 \\times 1.5 = 4.0 \\pm 2.955$, so $[1.045,\\ 6.955]$. It doesn't include 0, so the effect is positive at the 5% level ($p \\approx 0.008$)."),
    ("Intermediate", "A model predicts $\\log(\\text{price})$ and the weight on <em>number of bathrooms</em> is $0.05$. By what factor does one extra bathroom multiply the predicted price, and what percentage increase is that?",
     "Factor $e^{0.05} = 1.0513$, an increase of about $5.13\\%$. (The shortcut $100 \\times 0.05 = 5\\%$ is close because $w$ is small.)"),
    ("Code · intermediate", "Using the diabetes model from the \"Going deeper\" code, compute Cook's distance for all 442 patients. What is the largest value, and how many patients are above the sensitive threshold $4/n$?",
     "Build <code>A</code> with a column of ones, compute <code>lev = np.diag(A @ np.linalg.inv(A.T @ A) @ A.T)</code>, the residuals <code>e</code>, <code>s2 = e @ e / (n - 11)</code> and <code>D = e**2 / (11 * s2) * lev / (1 - lev)**2</code>. The largest is $D \\approx 0.0245$ (patient at index 382), and 22 patients exceed $4/442 \\approx 0.009$. None is anywhere near 1: no single patient controls this model."),
]

# Answer boxes: exercise index (0-based within EX) -> [(label, answer, hint[, tolerance])]
CHECKS = {
    0: [("Adjusted R²", 0.78222, "Use 1 − (1 − R²)(n − 1)/(n − d − 1) with n = 50 and d = 4.")],
    1: [("VIF", 10, "VIF = 1 / (1 − R²ⱼ)."), ("Standard-error factor", 3.16228, "The SE grows by the square root of the VIF.")],
    2: [("t-statistic", 2.66667, "t = weight / SE."), ("95% interval (low, high)", [1.045, 6.955], "weight ± 1.97 × SE.")],
    3: [("Price multiplier", 1.05127, "Compute e to the power of the weight."), ("Percentage increase (type it with %)", 0.05127, "(multiplier − 1) × 100, then add the % sign.")],
    4: [("Largest Cook's distance", 0.0245, "D = e²/((d+1)s²) · h/(1 − h)² with d + 1 = 11.", 0.0005), ("Patients above 4/n", 22, "Count D > 4/442.")],
}
