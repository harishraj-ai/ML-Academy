# Practice exercises + common mistakes, lessons 1-10. All numeric answers verified with Python.
EX = {}
MISTAKES = {}

EX[1] = [
 ("Concepts", "Classify each task as <strong>regression</strong>, <strong>classification</strong> or <strong>clustering</strong>: (a) predicting a delivery time in minutes; (b) deciding whether a photo contains a cat; (c) grouping news articles by topic when no topics are given; (d) predicting tomorrow's rainfall in mm.",
  "(a) regression — a number. (b) classification — yes/no. (c) clustering — no labels, discover groups. (d) regression — a number."),
 ("By hand", "True values are $y = 4, 7, 10$ and predictions are $\\hat{y} = 5, 6, 10$. Compute the MSE.",
  "Errors $\\hat{y} - y$: $1, -1, 0$. Squared: $1, 1, 0$. MSE $= 2/3 \\approx 0.667$."),
 ("By hand", "Points $(1, 3), (2, 4), (3, 8)$. Which line has the lower MSE: $\\hat{y} = 2x + 1$ or $\\hat{y} = 2x + 0.5$?",
  "Line 1 predicts $3, 5, 7$; errors $0, 1, -1$; MSE $= 2/3 \\approx 0.667$.<br>Line 2 predicts $2.5, 4.5, 6.5$; errors $-0.5, 0.5, -1.5$; squared $0.25, 0.25, 2.25$; MSE $= 2.75/3 \\approx 0.917$.<br><strong>$\\hat{y} = 2x + 1$ is better.</strong>"),
 ("Code", "Change the Lesson 1 code so it predicts the price of a 350 m² house (that's $x = 3.5$). What does it print?",
  "Replace the last line with <code>print(model.predict([[3.5]]))</code>. It prints about <code>[7.015]</code> — roughly 701,500 USD, since the learned line is about $1.99x + 0.05$."),
]
MISTAKES[1] = [
 "Thinking a model that scores perfectly on its training data must be good — it may simply have memorised it (overfitting).",
 "Confusing the label (what you predict) with the features (what you know).",
 "Calling every yes/no problem \"regression\" because the algorithm is named logistic <em>regression</em>.",
]

EX[2] = [
 ("By hand", "For $\\mathbf{a} = (3, -1, 2)$ and $\\mathbf{b} = (1, 4, 0)$ compute $\\mathbf{a} + \\mathbf{b}$, $2\\mathbf{a} - \\mathbf{b}$ and $\\mathbf{a}\\cdot\\mathbf{b}$.",
  "$\\mathbf{a} + \\mathbf{b} = (4, 3, 2)$. $\\ 2\\mathbf{a} - \\mathbf{b} = (6-1, -2-4, 4-0) = (5, -6, 4)$. $\\ \\mathbf{a}\\cdot\\mathbf{b} = 3 - 4 + 0 = -1$ (slightly opposite directions)."),
 ("By hand", "Find the length of $(2, -3, 6)$ and the cosine similarity between $(1, 0)$ and $(1, 1)$.",
  "$\\sqrt{4 + 9 + 36} = \\sqrt{49} = 7$.<br>$\\cos\\theta = \\frac{1\\cdot1 + 0\\cdot1}{1\\cdot\\sqrt2} = \\frac{1}{\\sqrt2} \\approx 0.707$ (an angle of 45°)."),
 ("By hand", "$X = \\begin{bmatrix}1&2\\\\3&4\\\\5&6\\end{bmatrix}$ and $\\mathbf{w} = (2, -1)$. Compute $X\\mathbf{w}$. What shape is $AB$ if $A$ is $2\\times3$ and $B$ is $3\\times4$?",
  "Row by row: $2 - 2 = 0$, $6 - 4 = 2$, $10 - 6 = 4$, so $X\\mathbf{w} = (0, 2, 4)$.<br>$AB$ is $2\\times4$ (inner sizes 3 match; outer sizes remain)."),
 ("Code", "Check all three answers above with NumPy.",
  "<code>import numpy as np</code><br><code>a, b = np.array([3, -1, 2]), np.array([1, 4, 0])</code><br><code>print(a + b, 2*a - b, a @ b)</code> → <code>[4 3 2] [ 5 -6  4] -1</code><br><code>print(np.linalg.norm([2, -3, 6]))</code> → <code>7.0</code><br><code>print(np.array([[1,2],[3,4],[5,6]]) @ np.array([2,-1]))</code> → <code>[0 2 4]</code>"),
]
MISTAKES[2] = [
 "Multiplying matrices whose inner sizes don't match — check shapes first: $(m\\times n)(n\\times p)$.",
 "Assuming $AB = BA$. Matrix multiplication order matters.",
 "Mixing up NumPy's <code>*</code> (element-wise) with <code>@</code> (matrix multiplication / dot product).",
]

EX[3] = [
 ("By hand", "Differentiate $f(x) = 3x^2 - 5x + 2$ and evaluate the slope at $x = 2$.",
  "$f'(x) = 6x - 5$. At $x = 2$: $12 - 5 = 7$ (going up, fairly steeply)."),
 ("By hand", "Use the chain rule on $f(x) = (2x + 1)^3$. What is $f'(0)$?",
  "Outer: $3u^2$; inner $u = 2x + 1$ with derivative 2. So $f'(x) = 3(2x+1)^2\\cdot2 = 6(2x+1)^2$, and $f'(0) = 6$."),
 ("By hand", "For $f(w, b) = w^2b + 3b$, find both partial derivatives and the gradient at $(w, b) = (2, 1)$.",
  "$\\frac{\\partial f}{\\partial w} = 2wb$, $\\ \\frac{\\partial f}{\\partial b} = w^2 + 3$. At $(2, 1)$: $\\nabla f = (4, 7)$."),
 ("By hand", "Run 3 steps of gradient descent on $L(w) = (w - 4)^2$ from $w = 0$ with $\\eta = 0.25$.",
  "$L'(w) = 2(w - 4)$, so $w \\leftarrow w - 0.5(w - 4)$.<br>Step 1: $0 + 2 = 2$. Step 2: $2 + 1 = 3$. Step 3: $3 + 0.5 = 3.5$.<br>Each step halves the distance to the minimum at $w = 4$."),
]
MISTAKES[3] = [
 "Forgetting the inner derivative in the chain rule: $\\frac{d}{dx}(3x+1)^2 \\ne 2(3x+1)$; it's $6(3x+1)$.",
 "Moving <em>with</em> the gradient instead of against it — that climbs uphill and increases the loss.",
 "Treating the other variables as zero (instead of as constants) when taking a partial derivative.",
]

EX[4] = [
 ("By hand", "Two fair dice are rolled. What is the probability their sum is 7?",
  "36 equally likely outcomes; 6 give 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1). Probability $6/36 = 1/6$."),
 ("By hand", "For the data $2, 4, 4, 4, 5, 5, 7, 9$, compute the mean, the variance (divide by $n$) and the standard deviation.",
  "Mean $= 40/8 = 5$. Squared deviations: $9, 1, 1, 1, 0, 0, 4, 16$ → sum 32. Variance $= 32/8 = 4$. Standard deviation $= 2$."),
 ("By hand", "20% of emails are spam. The word \"winner\" appears in 50% of spam and 5% of normal emails. An email contains \"winner\". What is $P(\\text{spam} \\mid \\text{winner})$?",
  "$P(\\text{winner}) = 0.5\\times0.2 + 0.05\\times0.8 = 0.10 + 0.04 = 0.14$.<br>$P(\\text{spam} \\mid \\text{winner}) = 0.10/0.14 \\approx 0.714$ — about 71%."),
 ("By hand", "Test scores are normal with $\\mu = 70$, $\\sigma = 10$. What is the z-score of 85? Between which two scores do about 95% of students fall?",
  "$z = (85 - 70)/10 = 1.5$. About 95% lie within $2\\sigma$: between $70 - 20 = 50$ and $70 + 20 = 90$."),
]
MISTAKES[4] = [
 "Confusing $P(A \\mid B)$ with $P(B \\mid A)$ — the base-rate trap in the medical test example.",
 "Multiplying probabilities of events that are <em>not</em> independent.",
 "Using the mean to describe skewed data such as incomes, where the median is far more representative.",
]

EX[5] = [
 ("Concepts", "Diagnose each model: (a) training error 0.02, test error 0.40; (b) training 0.35, test 0.37; (c) training 0.10, test 0.12.",
  "(a) Overfitting — a big gap. (b) Underfitting — both high. (c) A good fit — both low and close."),
 ("By hand", "5-fold cross-validation accuracies: $0.70, 0.74, 0.72, 0.76, 0.73$. Report mean ± standard deviation.",
  "Mean $= 3.65/5 = 0.73$. Deviations $-0.03, 0.01, -0.01, 0.03, 0$; squared sum $0.002$; variance $0.0004$; std $0.02$. Report $0.73 \\pm 0.02$."),
 ("Concepts", "Spot the leakage: a team (a) removes outliers using the whole dataset before splitting; (b) predicts loan default using the column \"collections_agency_contacted\"; (c) shuffles stock prices randomly before splitting.",
  "(a) Leakage — decisions were made using test data. Split first. (b) Leakage — that column is only known <em>after</em> a default. (c) Leakage — the model trains on the future. Split by time instead."),
 ("By hand", "You have 10,000 examples. How many go to training, validation and test with a 70/15/15 split?",
  "7,000 training, 1,500 validation, 1,500 test."),
]
MISTAKES[5] = [
 "Tuning on the test set — then its score is no longer an honest estimate.",
 "Preprocessing (scaling, imputing, selecting features) before splitting the data.",
 "Splitting time-ordered data randomly, so the model trains on the future.",
]

EX[6] = [
 ("By hand", "Fit a least-squares line to $x = 1, 2, 3$ and $y = 2, 3, 5$. Predict $y$ at $x = 4$.",
  "$\\bar{x} = 2$, $\\bar{y} = 10/3 \\approx 3.333$. $\\sum(x-\\bar{x})(y-\\bar{y}) = (-1)(-1.333) + 0 + (1)(1.667) = 3$; $\\sum(x-\\bar{x})^2 = 2$.<br>$w = 3/2 = 1.5$, $b = 3.333 - 1.5\\times2 = 0.333$. At $x = 4$: $\\hat{y} = 6.333$."),
 ("By hand", "For the line from exercise 1, compute $R^2$.",
  "Predictions $1.833, 3.333, 4.833$; residuals $0.167, -0.333, 0.167$; $\\text{SS}_{\\text{res}} \\approx 0.167$. $\\text{SS}_{\\text{tot}} = 1.778 + 0.111 + 2.778 = 4.667$.<br>$R^2 = 1 - 0.167/4.667 \\approx 0.964$."),
 ("Concepts", "A model predicts salary (in thousands) as $12 + 3.5\\times\\text{years of experience}$. Interpret both numbers. Is it safe to say \"experience causes salary\"?",
  "The intercept 12 is the predicted salary at 0 years; each extra year adds about 3.5k on average. It's an association in this data — other factors (role, education) may drive both, so causation isn't established."),
 ("Code", "Solve exercise 1 with the normal equation in NumPy.",
  "<code>X = np.column_stack([np.ones(3), [1, 2, 3]])</code><br><code>y = np.array([2, 3, 5])</code><br><code>print(np.linalg.solve(X.T @ X, X.T @ y))</code> → <code>[0.333... 1.5]</code> (bias, slope)."),
]
MISTAKES[6] = [
 "Comparing raw weights across features measured in different units.",
 "Extrapolating far outside the range of the training data.",
 "Ignoring outliers, which can pull a least-squares line a long way.",
]

EX[7] = [
 ("By hand", "Model $\\hat{y} = wx$, data $(1, 2)$ and $(2, 4)$, MSE loss, $w = 0$, $\\eta = 0.1$. Do two steps of gradient descent.",
  "Gradient $= \\frac{2}{n}\\sum(\\hat{y} - y)x$.<br>Step 1: errors $-2, -4$; gradient $= (-2\\cdot1 - 4\\cdot2) = -10$; $w = 0 + 1 = 1$.<br>Step 2: errors $-1, -2$; gradient $= -1 - 4 = -5$; $w = 1 + 0.5 = 1.5$. (It's heading for $w = 2$.)"),
 ("By hand", "On $L(w) = w^2$, start at $w = 1$ with $\\eta = 1.5$. What happens over three steps, and why?",
  "Update $w \\leftarrow w - 1.5\\cdot2w = -2w$: $1 \\to -2 \\to 4 \\to -8$. The steps overshoot more each time — <strong>divergence</strong>; for this function you need $\\eta &lt; 1$."),
 ("By hand", "10,000 training examples, mini-batch size 100. How many parameter updates happen in 5 epochs?",
  "100 updates per epoch × 5 epochs = <strong>500 updates</strong>."),
 ("Code", "In the Lesson 7 from-scratch code, change <code>lr = 0.05</code> to <code>lr = 0.1</code> and run 20 steps. What happens?",
  "The loss explodes: after 20 steps $w \\approx -575$ and the MSE is in the millions. 0.1 is above this problem's stable limit (about 0.085, as the Lesson 7 demo shows). Standardising $x$ would allow larger rates."),
]
MISTAKES[7] = [
 "Forgetting to scale features, which forces a tiny learning rate and slow zigzagging.",
 "Concluding a model can't learn when the learning rate is simply too small or too large — plot the loss curve.",
 "Assuming gradient descent always finds the global minimum; that's only guaranteed for convex losses.",
]

EX[8] = [
 ("By hand", "Compute $\\sigma(1.5)$ and $\\sigma(-3)$.",
  "$\\sigma(1.5) = 1/(1 + e^{-1.5}) \\approx 0.818$. $\\ \\sigma(-3) = 1/(1 + e^{3}) \\approx 0.047$."),
 ("By hand", "A model has $z = 0.8x - 4$. Where is the decision boundary? What probability does it give at $x = 7$?",
  "Boundary where $z = 0$: $x = 5$. At $x = 7$: $z = 1.6$, $p = \\sigma(1.6) \\approx 0.832$."),
 ("By hand", "Compute the log loss for $p = 0.2$ when the true label is $y = 0$, and when it is $y = 1$.",
  "$y = 0$: $-\\ln(1 - 0.2) = -\\ln 0.8 \\approx 0.223$ (good prediction, small loss).<br>$y = 1$: $-\\ln 0.2 \\approx 1.609$ (confident and wrong, big loss)."),
 ("Concepts", "A feature's weight is $0.405$. By what factor do the odds change per unit increase? If the probability was 0.5, what does it become?",
  "$e^{0.405} \\approx 1.5$, so the odds are multiplied by 1.5. Odds 1 (probability 0.5) become 1.5, which is probability $1.5/2.5 = 0.6$."),
]
MISTAKES[8] = [
 "Using MSE instead of log loss for classification.",
 "Reading the weight as a change in probability — it changes the log-odds.",
 "Assuming 0.5 is always the right threshold; the costs of each mistake should decide it.",
]

EX[9] = [
 ("By hand", "TP = 40, FP = 10, FN = 20, TN = 130. Compute accuracy, precision, recall, F1 and specificity.",
  "Accuracy $= 170/200 = 0.85$. Precision $= 40/50 = 0.80$. Recall $= 40/60 \\approx 0.667$. F1 $= 80/(80 + 10 + 20) \\approx 0.727$. Specificity $= 130/140 \\approx 0.929$."),
 ("Concepts", "Which metric matters most? (a) An airport scanner for dangerous items; (b) a system that automatically blocks bank accounts; (c) comparing models on a balanced dataset.",
  "(a) Recall — missing a dangerous item is unacceptable. (b) Precision — wrongly blocking accounts is very costly. (c) Accuracy or ROC-AUC is fine."),
 ("By hand", "Positive scores $0.8, 0.6$; negative scores $0.7, 0.2$. Compute the AUC by counting pairs.",
  "4 pairs. $0.8$ beats $0.7$ and $0.2$ (2); $0.6$ beats $0.2$ only (1). AUC $= 3/4 = 0.75$."),
 ("By hand", "Compare MAE and RMSE for errors $2, -2, 2, -2$ and for errors $0, 0, 0, 8$.",
  "First: MAE $= 2$, RMSE $= 2$. Second: MAE $= 2$, RMSE $= \\sqrt{64/4} = 4$. Same MAE, but RMSE flags the single big miss."),
]
MISTAKES[9] = [
 "Reporting only accuracy on imbalanced data.",
 "Choosing the threshold on the test set — that's tuning, so use validation data.",
 "Forgetting that scikit-learn's error scorers are negated (e.g. <code>neg_mean_squared_error</code>).",
]

EX[10] = [
 ("Concepts", "Your model has training $R^2 = 0.98$ and test $R^2 = 0.55$. Name the problem and three things to try.",
  "High variance (overfitting). Try: stronger regularization (larger $\\lambda$/alpha), a simpler model or fewer features, more training data (also early stopping for iterative models)."),
 ("By hand", "One feature, no intercept: $\\sum x_iy_i = 50$, $\\sum x_i^2 = 20$. Compute the ridge weight for $\\lambda = 0, 5, 30$.",
  "$w = 50/(20 + \\lambda)$: $\\lambda = 0 \\to 2.5$; $\\lambda = 5 \\to 2.0$; $\\lambda = 30 \\to 1.0$."),
 ("Concepts", "Lasso or ridge? (a) Genetic data with 20,000 features where only a few genes matter; (b) house prices with 15 features that all plausibly matter.",
  "(a) Lasso — it sets most weights to exactly zero. (b) Ridge — it keeps every feature but shrinks them."),
 ("By hand", "<code>LogisticRegression(C=0.01)</code>: what is $\\lambda$, and is regularization strong or weak?",
  "$\\lambda = 1/C = 100$ — strong regularization."),
]
MISTAKES[10] = [
 "Regularizing without scaling the features first.",
 "Penalising the bias term.",
 "Choosing $\\lambda$ by looking at test-set results instead of cross-validation.",
]
