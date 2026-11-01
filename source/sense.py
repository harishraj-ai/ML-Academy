# "Make sense of it" boxes placed after worked examples, scenario openers for key sections,
# and interactive what-if calculators. Every number below was checked with Python.
# SENSE[(lesson, k)] = dict(s=situation, m=meaning, w=[what-if lines], ml=why it matters)  (k = k-th worked example)
# SCENE[(lesson, section_id)] = html shown right under the section heading
# WHATIF[(lesson, k)] = widget name placed after that example's sense box

SENSE = {
 (1, 0): dict(
  s="You're an estate agent testing a quick pricing rule — \"price is twice the size\" — on three homes you've already sold.",
  m="The MSE of 0.33 is the <em>average squared miss</em>. Its square root, about 0.58, is easier to feel: a typical prediction is off by roughly 0.58 price units. The rule nails the first two homes and misses the third by 1.",
  w=["<strong>One wrong price.</strong> If the third home had sold for 8 instead of 5, its error becomes 2, its square 4, and the MSE jumps from 0.33 to <strong>1.33</strong> — four times bigger from one house. The average absolute error only doubles (0.33 → 0.67).",
     "<strong>An error of 3</strong> on that house (price 9) gives MSE <strong>3.0</strong>: squaring makes an error of 3 count nine times as much as an error of 1.",
     "<strong>A better line</strong> ($w = 1.5,\\ b = 0.67$) spreads small misses across all three houses and cuts the MSE to about 0.056."],
  ml="MSE is the loss most regression models minimise. Because it squares errors, one large miss (or one bad data point) can dominate it — which is why outliers deserve a look before you train, and why some problems use the absolute error instead."),
 (2, 0): dict(
  s="A property app shows \"homes like this one\". It needs a number for how alike two homes are, and distance is that number.",
  m="A distance of 5 combines a size difference of 3 and a bedroom difference of 4 into one number, using Pythagoras. Smaller means more similar.",
  w=["<strong>Same bedrooms:</strong> if both homes had 2 bedrooms, the distance is just the size gap, <strong>3</strong>.",
     "<strong>Change the units:</strong> measure size in m² instead (500 vs 800). The difference becomes $(300, 4)$ and the distance <strong>300.03</strong> — bedrooms now barely count. Nothing about the houses changed, only the units.",
     "<strong>Shrink the size scale</strong> instead (5 → 0.5, 8 → 0.8): the distance is about <strong>4.01</strong>, almost all from bedrooms."],
  ml="kNN, k-means and SVMs all rely on distances, so the feature with the biggest numbers wins by default. That's why we standardise features first (Lessons 11 and 20)."),
 (2, 1): dict(
  s="Think of $\\mathbf{a}$ as one applicant's three feature values and $\\mathbf{b}$ as the weights a model gives those features. The dot product is the model's score.",
  m="Each pair contributes separately: $8$ from the first feature, $-3$ from the second (its weight is negative, so it pulls the score down) and $5$ from the third. The total score is 10.",
  w=["<strong>Raise the second feature</strong> from 3 to 6: the score <em>falls</em> to <strong>7</strong>, because that feature has a negative weight.",
     "<strong>Flip every weight</strong> to $(-4, 1, -5)$: the score becomes <strong>−10</strong> — the vectors now point in opposite directions.",
     "<strong>Weights $(3, -2, 0)$:</strong> the score is <strong>0</strong> — the vectors are perpendicular, and this applicant is \"neutral\" to the model."],
  ml="Every linear model, every neuron and every attention score in a Transformer is a dot product of inputs with weights. Reading it as \"sum of contributions\" lets you see which feature pushed a prediction up or down."),
 (2, 2): dict(
  s="Each row is one house: size (m²), bedrooms and age (years). The weights say each m² adds 3, each bedroom 20, and each year of age removes 5.",
  m="160, 255, 360 and 515 are the model's predicted prices for the four houses — computed in one matrix–vector product instead of four separate sums.",
  w=["<strong>House 1 gains a bedroom</strong> (1 → 2): its prediction rises by exactly the bedroom weight, 160 → <strong>180</strong>.",
     "<strong>House 1 is 10 years older</strong> (2 → 12): 10 × (−5) = −50, so the prediction drops to <strong>110</strong>.",
     "<strong>Change one weight</strong> (size 3 → 4): every prediction rises by that house's size — <strong>210, 335, 480, 665</strong>. One weight affects every row."],
  ml="Training adjusts the weights so that $X\\mathbf{w}$ matches the real prices. Because every weight touches every prediction, changing one weight is a global change — which is exactly what gradient descent does, a little at a time."),
 (2, 3): dict(
  s="A neural network applies one transformation after another. Multiplying their matrices gives a single matrix that does both steps at once.",
  m="Each entry of the result is a row of the first matrix dotted with a column of the second: $19 = 1\\cdot5 + 2\\cdot7$.",
  w=["<strong>Swap the order:</strong> $BA = \\begin{bmatrix} 23 & 34 \\\\ 31 & 46 \\end{bmatrix}$, not the same as $AB$. Doing step B then step A is a different overall transformation."],
  ml="Layers in a network are matrix multiplications applied in a fixed order. It's also why a stack of purely linear layers collapses into one matrix — and why networks need non-linear activations between them (Lesson 18)."),
 (3, 0): dict(
  s="Suppose $x$ is how far a prediction is from the truth and $f(x) = x^2$ is its squared error. The derivative tells you how fast that error changes if you nudge the prediction.",
  m="At $x = 3$ the slope is 6: move the prediction 0.01 further away and the squared error grows by about $6 \\times 0.01 = 0.06$.",
  w=["<strong>At $x = -3$</strong> the slope is <strong>−6</strong>: same steepness, opposite direction — the error falls if you increase $x$.",
     "<strong>At $x = 0$</strong> the slope is <strong>0</strong>: you're at the bottom, nothing to improve.",
     "<strong>Bigger $h$:</strong> the slope estimate is 7.0 with $h = 1$, 6.1 with $h = 0.1$ and 6.001 with $h = 0.001$ — the smaller the step, the closer to the true 6."],
  ml="The sign of the derivative tells a model which way to move a parameter, and its size tells how urgently. Far from the target (big $x$) the slope is steep; near the target it flattens — so learning naturally slows as it gets close."),
 (3, 1): dict(
  s="Picture $f$ as a cost curve. The derivative $12x^2 - 4x + 7$ gives its slope at any point, without drawing it.",
  m="Each term is differentiated on its own and the results are added. The constant $-9$ disappears because a constant doesn't change.",
  w=["<strong>At $x = 0$</strong> the slope is <strong>7</strong>; at $x = 1$ it's <strong>15</strong>; at $x = -1$ it's <strong>23</strong>.",
     "<strong>At $x = 10$</strong> it's <strong>1,167</strong>, and almost all of that comes from the $12x^2$ term. For large inputs the highest power dominates."],
  ml="Loss functions are built from sums of simple terms, so their gradients are too. This term-by-term rule is what automatic differentiation in PyTorch applies millions of times per second."),
 (3, 2): dict(
  s="A network is a chain: the input goes through one step, then another. Here the inside step multiplies by 3 and adds 1; the outside step squares.",
  m="The chain rule multiplies the slopes of the steps: the outside slope $2(3x+1)$ times the inside slope 3. At $x = 0$ that's $2 \\times 1 \\times 3 = 6$.",
  w=["<strong>Make the inside steeper</strong> ($5x + 1$): the slope at 0 becomes $2 \\times 1 \\times 5 = $ <strong>10</strong>. The inside factor is multiplied straight in.",
     "<strong>At $x = 1$</strong> the slope is $6 \\times 4 = $ <strong>24</strong>."],
  ml="Backpropagation is the chain rule through many layers, so gradients are products of many factors. If those factors are mostly below 1 the product shrinks towards zero (vanishing gradients); if above 1 it can blow up (exploding gradients) — Lesson 19."),
 (3, 3): dict(
  s="Think of $f(w, b)$ as a model's loss with two knobs, $w$ and $b$. Each partial derivative says what happens if you turn one knob and leave the other alone.",
  m="At $(1, 2)$ the loss is 11. Its slope is 8 in the $w$ direction and 7 in the $b$ direction, so the gradient is $(8, 7)$.",
  w=["<strong>Turn $w$ up by 0.1:</strong> the loss becomes 11.81 — up by about $8 \\times 0.1 = 0.8$, as predicted.",
     "<strong>Turn $b$ up by 0.1:</strong> the loss becomes 11.71 — up by about 0.7.",
     "<strong>Step against the gradient</strong> with learning rate 0.1: $(1, 2) \\to (0.2, 1.3)$ and the loss falls from 11 to <strong>2.51</strong>."],
  ml="This is one step of gradient descent in miniature. Real models have millions of knobs, but the recipe is the same: compute every partial derivative, then move each parameter a little against its own slope."),
 (4, 0): dict(
  s="A board game needs a 6 to start. How often will that happen?",
  m="A probability of 1/6 means that over many rolls, about one roll in six is a 6. Roll 600 times and you'd expect around 100 sixes — rarely exactly 100.",
  w=["<strong>Two tries:</strong> the chance of at least one 6 is $1 - (5/6)^2 \\approx$ <strong>0.31</strong>.",
     "<strong>Six tries:</strong> about <strong>0.67</strong> — not 1. Even with six rolls, one game in three still waits."],
  ml="Classifiers output probabilities. A prediction of \"70% spam\" means that among many emails given 70%, about 7 in 10 should really be spam — a property called calibration."),
 (4, 1): dict(
  s="You run a mail service. Overall, 30% of emails are spam. Should the word \"free\" make you more suspicious?",
  m="Among emails with \"free\", 75% are spam, compared with 30% overall. The word is strong evidence, because it raises the probability by a factor of 2.5.",
  w=["<strong>If only 6 of the 20 \"free\" emails were spam,</strong> $P(\\text{spam} \\mid \\text{free}) = 0.30$ — the same as the overall rate. Then the word tells you nothing.",
     "<strong>If 19 of 20 were spam,</strong> it would be <strong>0.95</strong> — almost decisive."],
  ml="A feature is useful exactly when it changes the probability of the label. Comparing $P(\\text{label} \\mid \\text{feature})$ with $P(\\text{label})$ is a quick way to find informative features."),
 (4, 2): dict(
  s="You're a doctor explaining a positive screening result to a worried patient.",
  m="15% means: among people who test positive, about 15 in 100 actually have the disease. The rest are false alarms, because healthy people vastly outnumber sick ones.",
  w=["<strong>A more common disease (10%):</strong> the chance becomes <strong>67%</strong>. The same test means something very different in a different population.",
     "<strong>A better test</strong> (false positives 1% instead of 5%): about <strong>48%</strong>.",
     "<strong>A second, independent positive test:</strong> start from 15% and apply Bayes again — about <strong>77%</strong>."],
  ml="The base rate controls what a positive prediction means. Fraud, disease and fault detectors work with rare events, so a model with high accuracy can still produce mostly false alarms — which is why precision is reported separately (Lesson 9)."),
 (4, 3): dict(
  s="A game pays you in rupees the number you roll. What's it worth on average?",
  m="3.5 is the long-run average payout per roll. No single roll pays 3.5, but over 1,000 rolls you'd collect about 3,500.",
  w=["<strong>A loaded die</strong> that shows 6 half the time (each other face 1/10): the expected value rises to <strong>4.5</strong>.",
     "<strong>Pay to play:</strong> if each roll costs 4, a fair die loses you 0.5 per roll on average."],
  ml="A model's true loss is an expected value over all possible data. We can't compute it exactly, so we estimate it with the average loss on a sample — the training or test set."),
 (4, 4): dict(
  s="A teacher has five students' test scores: 4, 6, 8, 10 and 12. She wants one number for \"how the class did\" and one for \"how spread out\" the scores are.",
  m="The mean, 8, is the balance point: the gaps below it (−4, −2) exactly cancel the gaps above it (+2, +4). The standard deviation, 2.83, says a typical student is about 3 points from that average.",
  w=["<strong>One outlier.</strong> A data-entry slip turns 12 into 52. The mean jumps from 8 to <strong>16</strong> — now higher than four of the five students — while the <strong>median stays 8</strong>. The standard deviation leaps from 2.83 to <strong>18.1</strong>.",
     "<strong>Add a sixth student who scores exactly 8:</strong> the mean stays 8, but the standard deviation <em>falls</em> to 2.58, because a score at the centre makes the class look less spread out.",
     "<strong>Give everyone 10 bonus points:</strong> the mean becomes 18; the standard deviation stays <strong>2.83</strong>. Shifting doesn't change spread.",
     "<strong>Double every score:</strong> the mean becomes 16 and the standard deviation doubles to <strong>5.66</strong>.",
     "<strong>Same mean, different class:</strong> scores 0, 0, 8, 16, 16 also average 8, but their standard deviation is 7.16. And 8, 8, 8, 8, 8 has a standard deviation of 0. The mean alone can't tell these classes apart."],
  ml="The mean is pulled by every value, so a single extreme value can move it a lot; the median ignores how extreme the values are. That's why you check for outliers before averaging, fill missing values with the median (Lesson 20), and why MSE — which is an average — is sensitive to outliers. Standardising features uses exactly this mean and standard deviation."),
 (4, 5): dict(
  s="A clothing company is planning garment sizes for adults whose average height is 170 cm and standard deviation 10 cm.",
  m="Within one standard deviation (160–180 cm) are about 68% of people; within two (150–190 cm) about 95%. 200 cm is three standard deviations up: about 1 person in 740 is taller.",
  w=["<strong>Someone 185 cm tall</strong> has $z = 1.5$: about 6.7% of people are taller.",
     "<strong>A less varied population</strong> ($\\sigma = 5$ cm): 95% now fall between 160 and 180 cm, and 200 cm is six standard deviations up — about 1 in a billion."],
  ml="z-scores put different features on a common scale and flag unusual values: a value with $|z| > 3$ is worth checking as a possible error or anomaly. Many models also assume errors are roughly normal."),
}

SCENE = {
 (4, "describing-data"): "<p class=\"scene\"><span class=\"scene-tag\">Picture it</span>Two coffee shops both average 5 minutes per order. At one, every order takes 4–6 minutes; at the other, some take 1 minute and some 15. The average is identical — the experience isn't. To describe data you need a centre <em>and</em> a spread, and you need to know how one strange value can move them.</p>",
 (4, "bayes"): "<p class=\"scene\"><span class=\"scene-tag\">Picture it</span>An airport scanner beeps. Is the bag dangerous? It depends on two things: how good the scanner is, and how rare dangerous bags are in the first place. Bayes' theorem combines both.</p>",
 (2, "dot-product"): "<p class=\"scene\"><span class=\"scene-tag\">Picture it</span>At a shop you buy 2 notebooks at ₹40, 3 pens at ₹10 and 1 bag at ₹500. Your bill is $2\\cdot40 + 3\\cdot10 + 1\\cdot500 = 610$: multiply matching entries and add. That's a dot product — and it's exactly how a linear model turns features and weights into a prediction.</p>",
 (3, "derivative"): "<p class=\"scene\"><span class=\"scene-tag\">Picture it</span>You're driving and glance at the speedometer: 60 km/h. That's not your average speed for the trip — it's how fast your position is changing <em>right now</em>. A derivative is the speedometer reading of any function.</p>",
}

WHATIF = {(1, 0): "mse", (2, 0): "distance", (3, 0): "derivative", (4, 4): "mean-median", (4, 5): "zscore"}

SENSE.update({
 (5, 0): dict(
  s="You're choosing between models for a client and want a score you can trust, not one that depends on a lucky split.",
  m="0.83 is the model's average accuracy across five different validation folds. The ± 0.02 says the score moves by about two points depending on which data it's tested on.",
  w=["<strong>One bad fold.</strong> If the third fold scored 0.70 instead of 0.80, the mean drops to <strong>0.81</strong> and the standard deviation more than triples to <strong>0.056</strong>. A big spread is a warning that the model is unstable or one fold is unusual.",
     "<strong>A rival model</strong> scores 0.84, 0.86, 0.82, 0.85, 0.83: mean <strong>0.84 ± 0.014</strong>. It's ahead by 0.01, less than the spread of either model — not convincing evidence that it's better."],
  ml="Every score you compute is an estimate from a sample. Reporting the spread stops you from \"improving\" a model by chasing noise, and a high spread across folds is a clue to overfitting or data problems."),
 (6, 0): dict(
  s="Five students: hours of revision $x$ and test score $y$ out of 10. A teacher wants a simple rule for how much each hour helps.",
  m="Slope 0.6: on average each extra hour goes with 0.6 more marks. Intercept 2.2: the line's prediction for zero hours. MSE 0.48 means a typical miss of about $\\sqrt{0.48} \\approx 0.69$ marks.",
  w=["<strong>One outlier.</strong> If the last student had scored 15 instead of 5 (a typo), the slope jumps from 0.6 to <strong>2.6</strong> and the intercept to <strong>−1.8</strong>. Change the <em>first</em> student from 2 to 12 instead, and the slope flips to <strong>−1.4</strong>: \"more revision, lower score\". One point at the edge can tilt the whole line.",
     "<strong>Everyone gets 10 more marks:</strong> the intercept becomes 12.2; the slope stays 0.6.",
     "<strong>Measure time in tenths of an hour</strong> ($x \\times 10$): the slope becomes 0.06 — the same relationship, in different units. A weight's size depends on its feature's units.",
     "<strong>Add a sixth point exactly on the line</strong> (6, 5.8): the line doesn't move at all, and the MSE falls to 0.40."],
  ml="Least squares squares the residuals, so points far from the line — especially at the ends of the $x$ range — pull hard on it. Plot your data and look for outliers before trusting a fitted slope."),
 (6, 1): dict(
  s="Your manager asks: \"How much of the difference in scores does revision time actually explain?\"",
  m="$R^2 = 0.6$: the line removes 60% of the squared variation around the average score. The other 40% comes from things the model doesn't know about — sleep, ability, luck.",
  w=["<strong>Points exactly on a line</strong> ($y = x$): $R^2 = 1$.",
     "<strong>Predict the average score for everyone:</strong> $R^2 = 0$ — no better than knowing nothing.",
     "<strong>A model worse than the average</strong> has a <em>negative</em> $R^2$ (Lesson 9 has an example with −1.53)."],
  ml="$R^2$ compares your model with the simplest possible baseline, the mean. It's unitless, so it's easy to communicate — but always report an error in real units (RMSE, MAE) too."),
 (6, 2): dict(
  s="The same calculation as the worked example, but written so it works unchanged for 2 features or 2,000.",
  m="Solving $X^\\top X\\,\\mathbf{w} = X^\\top\\mathbf{y}$ gives bias 2.2 and slope 0.6 — the same answer as the formula, which is a good check.",
  w=["<strong>All students revised 3 hours:</strong> $X^\\top X = \\begin{bmatrix}5 & 15\\\\15 & 45\\end{bmatrix}$ and $ad - bc = 225 - 225 = 0$. No inverse, no unique line — you can't learn the effect of revision if it never varies.",
     "<strong>Two identical feature columns</strong> (say, hours and hours again) cause the same problem: the model can't tell how to split the credit between them."],
  ml="When features are perfectly or nearly duplicates (<em>multicollinearity</em>), the solution becomes unstable or impossible. Regularisation (Lesson 10) fixes this by adding $\\lambda$ to the diagonal so the matrix always has an inverse."),
 (7, 0): dict(
  s="Same five students as Lesson 6, but now the computer finds the line by trial and improvement instead of by formula.",
  m="Each step moves $w$ and $b$ a little in the direction that lowers the loss. After 1,000 steps it lands on $w = 0.6,\\ b = 2.2$ — the exact least-squares answer.",
  w=["<strong>Smaller learning rate</strong> ($\\eta = 0.01$): after 1,000 steps it's still at $w \\approx 0.618,\\ b \\approx 2.136$; it needs about 10,000 steps. Safe but slow.",
     "<strong>Larger learning rate</strong> ($\\eta = 0.1$): it <em>diverges</em> — after 10 steps the loss is over 8,000 and still growing. On this data any $\\eta$ above about 0.085 blows up.",
     "<strong>Unscaled features</strong> ($x \\times 10$) with the original $\\eta = 0.05$: the loss explodes within 5 steps. Bigger feature values mean steeper slopes, so the same step size overshoots."],
  ml="The learning rate is the most important setting in training. Too small wastes time; too big never converges. Scaling features (Lesson 20) makes one learning rate work for every weight."),
 (7, 1): dict(
  s="A ball rolling into a valley. Each step you move it by the learning rate times the slope.",
  m="With $\\eta = 0.1$ you keep 80% of the distance each step; with $\\eta = 0.9$ you jump past the bottom but still get closer; with $\\eta = 1.1$ each jump is bigger than the last.",
  w=["<strong>A steeper valley</strong> $L = 5w^2$ (gradient $10w$, update factor $1 - 10\\eta$): now the limit is $\\eta &lt; 0.2$. With $\\eta = 0.15$ the values go $-0.5, 0.25, -0.125$ (bouncing but shrinking); with $\\eta = 0.25$ they go $-1.5, 2.25, -3.375$ (diverging).",
     "<strong>The lucky case</strong> $\\eta = 0.1$ on $5w^2$ gives factor 0: it lands on the minimum in one step."],
  ml="Real loss surfaces are steep in some directions and flat in others. A learning rate small enough for the steep direction crawls in the flat one — which is why adaptive optimisers like Adam use a different step size for each weight."),
 (8, 0): dict(
  s="A tutor uses past results to tell each student their chance of passing from how many hours they studied.",
  m="27% and 84% are probabilities, not grades: among many students who study 2 hours, about 27 in 100 pass.",
  w=["<strong>No study at all:</strong> $p = \\sigma(-3.723) \\approx$ <strong>2%</strong>.",
     "<strong>The 50% point</strong> is where $z = 0$: $x = 3.723/1.354 \\approx$ <strong>2.75 hours</strong>. That's the decision boundary at a 0.5 threshold.",
     "<strong>6 and 8 hours:</strong> about <strong>99%</strong> and <strong>99.9%</strong>. The curve flattens — extra hours add less and less probability."],
  ml="The sigmoid turns any score into a probability between 0 and 1. The threshold that turns it into a yes/no decision is a separate choice, set by the cost of each kind of mistake (Lesson 9)."),
 (8, 1): dict(
  s="Odds are how bookmakers talk: 3 to 1 means three times as likely to happen as not.",
  m="A weight of 1.354 means each extra hour multiplies the odds of passing by $e^{1.354} \\approx 3.87$. The <em>probability</em> doesn't go up by a fixed amount, but the odds do go up by a fixed factor.",
  w=["<strong>From 2 to 3 hours:</strong> odds go from 0.36 (p = 0.27) to $0.36 \\times 3.87 \\approx 1.40$ (p = 0.58).",
     "<strong>A weight of 0</strong> gives a factor of $e^0 = 1$: the feature doesn't change the odds at all.",
     "<strong>A weight of −0.5</strong> gives a factor of 0.61: each unit <em>reduces</em> the odds by about 39%."],
  ml="This is how logistic-regression results are reported in medicine and credit scoring: \"each extra year of age multiplies the odds of default by 1.05\". Remember it's an association in the data, not proof of cause."),
 (8, 2): dict(
  s="A weather app says \"1% chance of rain\" and it pours. How embarrassed should it be? Log loss puts a number on it.",
  m="The loss is small when the model gives high probability to what actually happened, and grows without limit as that probability approaches zero.",
  w=["<strong>p = 0.001 on something that happens:</strong> loss <strong>6.91</strong>.",
     "<strong>One disaster among many successes:</strong> 99 predictions at 0.9 (loss 0.105 each) plus one at 0.001 average to <strong>0.173</strong> — that single confident miss raises the average loss by about 65%."],
  ml="Log loss rewards honest probabilities, not just correct labels. Training with it pushes models away from overconfidence — and it's the same cross-entropy loss used to train neural networks and language models."),
 (8, 3): dict(
  s="The model sees one student who studied 2 hours and passed, and adjusts itself.",
  m="Its prediction was 0.5 (no idea). The error $p - y = -0.5$ says \"too low\", so both $w$ and $b$ move up and the new prediction is 0.777.",
  w=["<strong>A second step</strong> on the same student: $p$ rises to about <strong>0.859</strong> and the loss falls to 0.152. Each step helps a little less, because the error $p - y$ is shrinking.",
     "<strong>If the student had failed</strong> ($y = 0$): the error is $+0.5$, the weights move <em>down</em> to $w = -0.5,\\ b = -0.25$, and $p$ falls to 0.223."],
  ml="The gradient for logistic regression is just (prediction − truth) × input. Big mistakes cause big updates; correct, confident predictions barely change anything."),
 (8, 4): dict(
  s="An image model scores a photo as cat 2, dog 1, rabbit 0 and has to turn the scores into probabilities.",
  m="Softmax gives 66.5% cat, 24.5% dog, 9% rabbit. The probabilities always add to 1 and keep the order of the scores.",
  w=["<strong>Bigger gaps</strong> (4, 2, 0): <strong>86.7%</strong>, 11.7%, 1.6% — more confident.",
     "<strong>Add 10 to every score</strong> (12, 11, 10): exactly the same probabilities. Only differences between scores matter.",
     "<strong>Equal scores</strong> (2, 2, 2): one-third each."],
  ml="Softmax is the last layer of nearly every classifier and of every language model, where the \"classes\" are possible next words. Making scores more spread out (or using a lower \"temperature\") makes the model more decisive."),
 (9, 0): dict(
  s="A hospital vendor boasts that its screening model is \"99% accurate\".",
  m="On a disease affecting 1 in 100 people, a model that never finds anyone sick is also 99% accurate. Accuracy is dominated by the large healthy group.",
  w=["<strong>A model that flags everyone</strong> finds every sick person but is only <strong>1%</strong> accurate.",
     "<strong>If half the population were sick,</strong> \"always healthy\" would be just <strong>50%</strong> accurate. How good an accuracy is depends on the base rate."],
  ml="Always compare a model with the trivial baseline that predicts the most common class, and use recall, precision or AUC when one class is rare."),
 (9, 1): dict(
  s="A clinic screens 100 patients; 10 are really sick. The model flags 18 for a follow-up test.",
  m="It catches 8 of the 10 sick patients (recall 0.8), but only 8 of the 18 it flags are really sick (precision 0.44). Overall accuracy is 0.88.",
  w=["<strong>Flag more people (30)</strong> and catch all 10: recall <strong>1.0</strong>, but precision falls to <strong>0.33</strong> and accuracy to 0.80. More follow-up tests, no missed patients.",
     "<strong>Flag fewer (5)</strong>, of whom 4 are sick: precision <strong>0.80</strong>, recall only <strong>0.40</strong> — yet accuracy <em>rises</em> to 0.93, because missing sick people barely dents accuracy.",
     "<strong>Flag everyone:</strong> recall 1.0, precision 0.10, accuracy 0.10."],
  ml="Precision and recall pull against each other as you move the threshold. Which matters more depends on costs: missing a cancer (low recall) is worse than an extra test (low precision); for spam filters it's the other way round."),
 (9, 2): dict(
  s="A fraud team only has time to check the riskiest transactions first. What matters is whether the model <em>ranks</em> fraud above normal transactions.",
  m="AUC 0.78: pick one fraud and one normal transaction at random, and 78% of the time the model gives the fraud the higher score.",
  w=["<strong>The weakest positive improves</strong> (0.4 → 0.85): it now beats the 0.8 negative too, and AUC rises to <strong>8/9 ≈ 0.89</strong>.",
     "<strong>A negative scores 0.95</strong> (instead of 0.2): AUC falls to <strong>4/9 ≈ 0.44</strong> — worse than guessing.",
     "<strong>Add 0.05 to every score,</strong> or square them all: AUC doesn't change, because the order is the same."],
  ml="AUC measures ranking quality across all thresholds, so it's good for comparing models before you've chosen a threshold. It says nothing about whether the scores are well-calibrated probabilities."),
 (9, 3): dict(
  s="A delivery app predicts arrival times in minutes for four orders.",
  m="MAE 0.875: on average the estimate is off by under a minute. RMSE 1.15 is larger because the one 2-minute miss counts extra.",
  w=["<strong>One bad miss</strong> (predict 8 for the order that took 2): MAE becomes 1.875, RMSE <strong>3.05</strong>, and $R^2$ drops to <strong>−1.53</strong> — worse than predicting the average for every order.",
     "<strong>Predict the average (4.25) for everyone:</strong> $R^2 = 0$, MAE 1.75."],
  ml="MAE treats every minute of error the same; RMSE punishes big misses. A large gap between them tells you a few predictions are badly wrong — worth investigating."),
 (10, 0): dict(
  s="With only three data points, a model can chase noise. Ridge adds a cost for large weights, a bit like telling the model \"be cautious unless the data insists\".",
  m="Without a penalty the weight is 2.214. As $\\lambda$ grows, the weight shrinks — to 1.292 at $\\lambda = 10$ and 0.272 at $\\lambda = 100$.",
  w=["<strong>Ten times more data</strong> (each point repeated 10 times): at $\\lambda = 10$ the weight is <strong>2.067</strong> instead of 1.292. With more evidence, the same penalty matters less.",
     "<strong>Measure $x$ in units ten times larger</strong> ($x = 0.1, 0.2, 0.3$): the unpenalised weight becomes 22.1 and $\\sum x^2$ only 0.14, so $\\lambda = 1$ now shrinks the weight to <strong>2.72</strong> — just 12% of its value, compared with 93% before. The penalty's strength depends on feature scale — standardise first."],
  ml="Regularisation trades a little bias for less variance. Choose $\\lambda$ by cross-validation, and always scale features first so the penalty treats them fairly."),
})

SCENE.update({
 (5, "cross-validation"): "<p class=\"scene\"><span class=\"scene-tag\">Picture it</span>Judging a restaurant by one meal is risky: maybe the chef was off that night. Eat there five times and you know it far better. Cross-validation tests a model five times on five different slices of data for the same reason.</p>",
 (7, "learning-rate"): "<p class=\"scene\"><span class=\"scene-tag\">Picture it</span>Walking down a dark hill, you can take tiny shuffles (safe, slow) or giant leaps (fast, but you might jump straight over the bottom onto the opposite slope). The learning rate is your stride length.</p>",
 (9, "metrics"): "<p class=\"scene\"><span class=\"scene-tag\">Picture it</span>An airport security scanner can be tuned to beep at everything (it never misses a threat, but delays thousands of travellers) or almost nothing (smooth queues, real danger). Precision and recall put numbers on that trade-off.</p>",
 (10, "bias-variance"): "<p class=\"scene\"><span class=\"scene-tag\">Picture it</span>Two students prepare for an exam. One memorises last year's paper word for word (high variance: lost if the questions change). The other learns only one rule of thumb for everything (high bias: wrong in a predictable way). Good learning sits between them.</p>",
})

WHATIF.update({(5, 0): "cv", (6, 0): "lsfit", (7, 0): "gd", (8, 1): "sigmoid", (9, 1): "confusion", (10, 0): "ridge"})

SENSE.update({
 (11, 0): dict(
  s="A new customer, $\\mathbf{q} = (2, 2)$, arrives. The two red points are customers who left; the three blue ones stayed. Will this one leave?",
  m="kNN copies its nearest neighbours. With $k = 1$ or $3$ the closest customers are mostly red, so it predicts red. With $k = 5$ it asks everyone, and the majority (blue) wins wherever $\\mathbf{q}$ is.",
  w=["<strong>Move the customer to (3.5, 3):</strong> the three nearest are all blue, so every $k$ from 1 to 5 says <strong>blue</strong>.",
     "<strong>Move to (3, 2):</strong> the nearest red and the nearest blue are both exactly 1.414 away — a tie that the order of the data has to break.",
     "<strong>Weight votes by 1/distance</strong> with $k = 5$: red scores $1/1 + 1/1.414 = 1.71$, blue scores 1.28, so close neighbours win and the answer is <strong>red</strong> again."],
  ml="$k$ controls how local the model is: small $k$ follows every quirk of the data (overfitting); large $k$ smooths everything towards the majority (underfitting). Pick it by cross-validation."),
 (11, 1): dict(
  s="A dating app matches people by age and income. P is 30 earning 50,000; Q is 60 earning 51,000; R is 31 earning 70,000. Who is P's closest match?",
  m="On raw numbers Q looks 20 times closer than R, purely because income is measured in thousands and age in tens. The 30-year age gap barely registers.",
  w=["<strong>Standardise both features</strong> (using these three people): P–Q becomes <strong>2.16</strong> and P–R <strong>2.17</strong>. Now the age gap and the income gap count about equally — a very different picture.",
     "<strong>Income in thousands</strong> (50, 51, 70): P–Q $= \\sqrt{30^2 + 1^2} \\approx 30.0$ and P–R $= \\sqrt{1 + 20^2} \\approx 20.0$, so R becomes the closer one. The \"nearest\" person depends entirely on the units."],
  ml="Every distance-based method (kNN, k-means, SVMs with RBF kernels) is sensitive to scale. Standardising is not optional for them."),
 (11, 2): dict(
  s="You want the 10% of houses most like yours. With one feature (size) that's a narrow band. Add more features and see what happens to \"nearby\".",
  m="In 10 dimensions, a box holding 10% of the data must stretch 79% of the way along every feature. Your \"neighbours\" differ from you on almost everything.",
  w=["<strong>Ask for only 1% of the data</strong> as neighbours: the side length is still <strong>0.63</strong> in 10 dimensions and <strong>0.955</strong> in 100.",
     "<strong>To keep a side of 0.1</strong> (truly local) in 10 dimensions, the box holds only $0.1^{10}$ — one ten-billionth of the data. You'd need billions of examples to find a single neighbour."],
  ml="This is the curse of dimensionality: with many features, data becomes sparse and distances lose their meaning. Remove irrelevant features or reduce dimensions (Lesson 17) before using kNN."),
 (12, 0): dict(
  s="A real spam filter multiplies hundreds of small probabilities. Computers can't store numbers that tiny, so they add logarithms instead.",
  m="The log scores −8.32 (spam) and −11.49 (ham) differ by 3.17, so spam is $e^{3.17} \\approx 24$ times more likely: a 96% chance.",
  w=["<strong>The email also says \"meeting\"</strong> (3 times in ham, never in spam): the chance of spam falls to <strong>88%</strong>. One ham-like word pulls it back.",
     "<strong>\"free\" appears twice:</strong> its evidence counts twice, and the chance rises to <strong>99.2%</strong>.",
     "<strong>Spam is rarer</strong> (prior 0.1 instead of 0.4): the same words now give <strong>80%</strong>. The prior matters.",
     "<strong>No smoothing:</strong> \"free\" has probability 0 in ham, the ham score is 0, and the email is 100% spam whatever else it says."],
  ml="Each word adds its own log-evidence for or against a class, so the model is easy to explain: you can list the words that pushed the decision. The \"naive\" independence assumption makes repeated or correlated words over-count."),
 (12, 1): dict(
  s="A fruit-sorting machine on a conveyor belt weighs each fruit and must decide: apple or orange?",
  m="170 g is 1 standard deviation above the apple average but 1.2 below the orange average, so it's a bit more apple-like: 61%.",
  w=["<strong>160 g:</strong> 80% apple. <strong>175 g:</strong> 49% — almost a coin toss. <strong>185 g:</strong> 25%. <strong>200 g:</strong> 5%.",
     "<strong>80% of the fruit are apples</strong> (prior 0.8): a 170 g fruit becomes 86% apple, and even 185 g is 56% apple. A strong prior shifts the boundary."],
  ml="Gaussian Naive Bayes turns each feature into a likelihood using its mean and standard deviation, then multiplies. It trains instantly and gives probabilities — a good first baseline."),
 (13, 0): dict(
  s="A bank sorts loan applicants into groups. A group where everyone repaid is easy to act on; a 50/50 group isn't. Impurity measures that mix.",
  m="Gini 0.48 means: pick two people at random from this node and there's a 48% chance they have different labels. Entropy 0.971 bits says you'd need almost one yes/no question to learn the label.",
  w=["<strong>5 yes, 5 no:</strong> Gini <strong>0.5</strong>, entropy <strong>1 bit</strong> — the worst possible mix for two classes.",
     "<strong>9 yes, 1 no:</strong> Gini 0.18, entropy 0.47 — nearly pure.",
     "<strong>Three classes, equally mixed:</strong> Gini 0.667, entropy 1.585 bits — more classes, more uncertainty."],
  ml="A tree's whole job is to make its leaves pure. Impurity is the score it uses to choose every question it asks."),
 (13, 1): dict(
  s="The tree has to pick its first question. Each candidate split divides the 10 applicants differently.",
  m="Split A creates one perfectly pure group and cuts impurity from 0.48 to 0.267 — a gain of 0.213. Split B leaves both groups as mixed as before, so it's worthless.",
  w=["<strong>A perfect split</strong> (6 yes on one side, 4 no on the other): both children are pure and the gain is the full <strong>0.48</strong>.",
     "<strong>Peeling off one example</strong> (1 yes alone, 5 yes + 4 no together): a pure leaf, but the gain is only <strong>0.036</strong>. Tiny pure leaves look tempting and help little — that's how deep trees overfit."],
  ml="Trees choose splits greedily, one at a time, by the biggest gain. Limiting depth or requiring a minimum number of samples per leaf stops them chasing tiny pure leaves."),
 (14, 0): dict(
  s="A random forest trains each tree on a \"bootstrap\" sample: draw examples at random, with replacement, as many times as there are examples.",
  m="Each tree sees about 63% of the distinct examples, some of them more than once. The other 37% are \"out-of-bag\" for that tree.",
  w=["<strong>Small data:</strong> with 10 examples, 65% are picked; with 3, 70%. It settles at 63.2% as $n$ grows.",
     "<strong>The left-out 37%</strong> can test each tree for free — the out-of-bag score, a built-in validation estimate."],
  ml="Different samples make the trees different, so their mistakes partly cancel when they vote. That's how bagging reduces variance without needing more data."),
 (14, 1): dict(
  s="A teacher sets the next practice test using the questions the class got wrong last time. AdaBoost does the same with its training examples.",
  m="The stump is 70% right, so it gets a vote of 0.424. Then the 3 mistakes are up-weighted until they hold exactly half of the total weight.",
  w=["<strong>A better stump</strong> ($\\varepsilon = 0.1$): its vote is <strong>1.10</strong>, and again its mistakes end up with exactly 50% of the weight. This always happens: after each round, the last stump is no better than a coin toss on the new weights.",
     "<strong>A coin-flip stump</strong> ($\\varepsilon = 0.5$): its vote is <strong>0</strong> — it's ignored.",
     "<strong>Worse than chance</strong> ($\\varepsilon = 0.6$): its vote is <strong>negative</strong> (−0.20), so its predictions are flipped."],
  ml="Boosting focuses each new model on what the ensemble still gets wrong. That's powerful, but it also means noisy or mislabelled examples get more and more weight — boosting is sensitive to label noise."),
 (14, 2): dict(
  s="Predicting delivery times. The first guess is the average; each new small tree corrects part of what's still wrong.",
  m="After one round the MSE falls from 4.22 to 1.56. Each tree predicts the <em>residuals</em> — the leftover errors — and only half its correction is applied.",
  w=["<strong>A third round</strong> (η = 0.5): MSE <strong>0.20</strong>.",
     "<strong>η = 1</strong> (full corrections): MSE 0.67 after one round and 0.17 after two — faster, but with real noisy data this memorises the training set.",
     "<strong>η = 0.1</strong>: after 10 rounds the MSE is still 0.85. Small steps need many trees, but generalise better."],
  ml="The learning rate and the number of trees work together: smaller steps plus more trees usually give the best test accuracy. Libraries like XGBoost and LightGBM use early stopping on a validation set to choose when to stop."),
 (15, 0): dict(
  s="Picture a road between two neighbourhoods. The SVM wants the widest road that keeps every red house on one side and every blue house on the other.",
  m="The road is 1.41 units wide. A point with score exactly ±1, like (1, 1), sits on the edge of the road: a support vector.",
  w=["<strong>Double the weights</strong> to $\\mathbf{w} = (2, 2),\\ b = -6$: the boundary line is the same, but the road narrows to <strong>0.71</strong>. The margin is set by $\\|\\mathbf{w}\\|$, which is why SVMs minimise it.",
     "<strong>Halve them</strong> to $(0.5, 0.5),\\ b = -1.5$: road width <strong>2.83</strong> — but now points like (1, 1) are inside the road."],
  ml="A wider margin usually means the boundary is less sensitive to small changes in the data, so it generalises better."),
 (15, 1): dict(
  s="A strict but fair examiner: full marks with no comment if you're clearly right, a small penalty if you're right but only just, a bigger one if you're wrong.",
  m="Hinge loss is zero once a point is past the edge of the road (score ≥ 1), and grows in a straight line as the point moves into or across the road.",
  w=["<strong>Score exactly 1:</strong> loss 0 — on the edge, no penalty.",
     "<strong>Score 0</strong> (on the boundary): loss 1.",
     "<strong>A negative point</strong> ($y = -1$) with score −1.5: loss $\\max(0, 1 - (-1)(-1.5)) = 0$ — correctly classified and outside the road."],
  ml="Because confident, correct points have zero loss, they have no influence on the solution. Only points near or across the road shape the boundary — which makes SVMs robust to far-away points but sensitive to the ones near the boundary."),
 (15, 2): dict(
  s="Normal blood pressure is in the middle; both very low and very high are dangerous. No single threshold separates healthy from unhealthy.",
  m="Adding $x^2$ as a feature turns \"far from 0 in either direction\" into \"large $x^2$\", which one threshold can separate.",
  w=["<strong>Bring the outer points in</strong> to ±2: their $x^2 = 4$ is still above the inner points' 1, so a threshold between 1 and 4 still works.",
     "<strong>Put a −1 point at ±3 too:</strong> then no threshold on $x^2$ works, and you'd need yet another feature."],
  ml="Many non-linear problems become linear with the right extra features. Kernels add them implicitly; neural networks learn them."),
 (15, 3): dict(
  s="Comparing two documents by every pair of words they contain would mean building enormous vectors. The kernel gets the same similarity from the short vectors.",
  m="Both ways give 25: the kernel $(\\mathbf{x}\\cdot\\mathbf{z})^2$ equals a dot product in the 3-D feature space, without building it.",
  w=["<strong>Perpendicular inputs</strong> $\\mathbf{x} = (1, 2),\\ \\mathbf{z} = (2, -1)$: $\\mathbf{x}\\cdot\\mathbf{z} = 0$, so $K = 0$.",
     "<strong>100 features, degree 3:</strong> the explicit feature space has <strong>171,700</strong> dimensions; the kernel needs one 100-term dot product and a cube."],
  ml="The kernel trick lets SVMs use huge (even infinite, for the RBF kernel) feature spaces cheaply. The cost moves elsewhere: kernel SVMs compare every pair of training points, so they slow down badly beyond tens of thousands of examples."),
})

SCENE.update({
 (11, "idea"): "<p class=\"scene\"><span class=\"scene-tag\">Picture it</span>New to a city and wondering whether a restaurant is any good? Ask the three people who live closest to it. That's k-nearest neighbours: no formula, just \"you're probably like the examples you're near\".</p>",
 (13, "impurity"): "<p class=\"scene\"><span class=\"scene-tag\">Picture it</span>Sorting laundry: a pile of only white shirts is \"pure\" — you know exactly what to do with it. A pile of mixed colours is \"impure\". A decision tree keeps asking questions until its piles are as pure as possible.</p>",
 (14, "why-it-works"): "<p class=\"scene\"><span class=\"scene-tag\">Picture it</span>At a village fair, nobody guesses the ox's weight exactly, but the average of hundreds of guesses is remarkably close. Many imperfect models whose errors differ can be better together than any one of them.</p>",
 (15, "margin"): "<p class=\"scene\"><span class=\"scene-tag\">Picture it</span>Parking between two cars, you aim for the middle of the gap, not just anywhere that fits — leaving the most room for error on both sides. An SVM chooses its boundary the same way.</p>",
})

WHATIF.update({(11, 0): "knn", (12, 1): "fruit", (13, 1): "split", (14, 1): "adaboost", (15, 1): "hinge"})

SENSE.update({
 (16, 0): dict(
  s="A delivery company has customers along one road at kilometres 1, 2, 3, 8, 9 and 10, and wants two depots. Where should they go?",
  m="k-means puts the depots at 2 and 9 — the middle of each group of customers. The inertia, 4, is the total squared distance from every customer to their depot.",
  w=["<strong>A sensible start</strong> (depots at 1 and 10): it reaches the same answer in one round instead of two.",
     "<strong>Three depots, started at 2, 8 and 10:</strong> groups {1, 2, 3}, {8, 9}, {10}, and the inertia falls to <strong>2.5</strong>. More clusters always lower the inertia — six depots would make it 0 — so inertia alone can't choose $k$.",
     "<strong>Three depots, started at 1, 5 and 10:</strong> the middle depot attracts no customers and stays empty, and the inertia stays at 4. A bad start can waste a cluster — which is why k-means++ and several restarts are used.",
     "<strong>A far-away customer at 50</strong> with two depots: one depot moves out to serve that single customer, the other has to cover 1–10 from 5.5, and the inertia leaps to <strong>77.5</strong>. Outliers can grab a whole cluster."],
  ml="k-means minimises squared distances, so like the mean it is pulled by outliers, depends on its starting points and on feature scale, and always returns exactly $k$ groups whether or not they really exist."),
 (16, 1): dict(
  s="Checking whether each customer really belongs with their depot or would be better served by the next one.",
  m="0.75 means the point is much closer to its own cluster than to the next one. A negative value means it's closer to another cluster — probably in the wrong one.",
  w=["<strong>a = 0.5, b = 4:</strong> $s = 0.875$ — even better placed.",
     "<strong>a = b:</strong> $s = 0$ — right on the border between two clusters."],
  ml="The average silhouette over all points is a common way to compare different values of $k$: higher is better. Look at the individual values too — a cluster full of near-zero scores may not be a real group."),
 (17, 0): dict(
  s="Two exam scores per student — maths and physics — that rise and fall together. Could one number describe each student almost as well?",
  m="PC1 is the diagonal direction \"good at both\". It holds 95% of the variation, so a single score per student keeps nearly all the information. PC2, \"better at one than the other\", holds only 5%.",
  w=["<strong>Points exactly on a line</strong> (1, 1), (2, 2), …: the second eigenvalue is 0 and PC1 keeps <strong>100%</strong>. One number loses nothing.",
     "<strong>Weakly related scores</strong> (1, 4), (2, 2), (3, 6), (4, 4), (5, 4): PC1 keeps only <strong>62%</strong>. Dropping PC2 would throw away a lot.",
     "<strong>Measure the second score in different units</strong> (×10): PC1 now keeps <strong>99.8%</strong> and points almost entirely along that feature (0.996). Nothing about the students changed — PCA simply chases the feature with the biggest numbers."],
  ml="PCA finds the directions of greatest variance, so it works best when features are correlated — and it must be run on standardised features, or the units decide the answer. Check the explained-variance ratio before deciding how many components to keep."),
})

SCENE.update({
 (16, "idea"): "<p class=\"scene\"><span class=\"scene-tag\">Picture it</span>A shop owner looks at what people buy and notices groups: families buying in bulk, students buying snacks, office workers buying lunch. Nobody labelled them — the groups emerged from the data. That's clustering.</p>",
 (17, "why"): "<p class=\"scene\"><span class=\"scene-tag\">Picture it</span>A photo of a teapot from its best angle tells you almost everything about its shape; a photo straight down the spout tells you very little. PCA finds the \"best angles\" to look at your data from, so that a few of them show nearly everything.</p>",
})

WHATIF.update({(16, 0): "kmeans1d", (17, 0): "pca2"})

SENSE.update({
 (18, 0): dict(
  s="A tiny network decides whether to approve something from two yes/no signals. Each hidden neuron is a small feature detector; the output neuron weighs their opinions.",
  m="Neuron 1 likes input 1 (output 0.62); neuron 2 dislikes it (0.38). The output adds them with weights +1 and −1, giving 0.56 — barely leaning towards \"yes\".",
  w=["<strong>Other input</strong> $\\mathbf{x} = (0, 1)$: the hidden outputs become 0.57 and 0.69, and $p$ drops to <strong>0.47</strong> — the network now leans \"no\" (loss 0.75 if the truth is 1).",
     "<strong>ReLU hidden neurons</strong> instead of sigmoid: $h = (0.5, 0)$ and $p = 0.62$ — neuron 2 is switched off entirely for this input.",
     "<strong>All weights 0:</strong> both hidden neurons output exactly 0.5 and $p = 0.5$. Worse, both neurons get identical gradients forever, so they never become different — which is why weights start random."],
  ml="A forward pass is just repeated dot products (Lesson 2) followed by a non-linear function. Stacking layers lets the network build complex features out of simple ones."),
 (18, 1): dict(
  s="The network gave 56% to the right answer. Backpropagation works out how much each weight was to blame, and nudges each one.",
  m="The output error −0.44 says \"too low\". It flows back through each weight: weights that pushed the wrong way get the biggest corrections. After one step the network gives 72%.",
  w=["<strong>Learning rate 0.1:</strong> $p$ rises only to <strong>0.579</strong> (loss 0.547) — a small, safe step.",
     "<strong>Learning rate 5:</strong> $p$ jumps to <strong>0.98</strong> in one step — great on this one example, but steps this big usually make training on many examples unstable.",
     "<strong>If the truth were 0:</strong> every gradient flips sign; one step ($\\eta = 1$) lowers $p$ to 0.34 and the loss from 0.82 to 0.41."],
  ml="Every deep-learning framework does exactly this, automatically, for millions of weights: forward pass, loss, backward pass (the chain rule, Lesson 3), update (gradient descent, Lesson 7)."),
 (19, 0): dict(
  s="A phone camera app needs to find the edge of a document in a photo. A 3×3 kernel slides across the image looking for a jump from dark to bright.",
  m="The feature map is 27 where the window straddles the edge and 0 in flat areas. Big value = \"edge here\".",
  w=["<strong>Bright on the left, dark on the right:</strong> the map becomes <strong>−27</strong>. The sign tells you the direction of the edge.",
     "<strong>A faint edge</strong> (0 to 1 instead of 0 to 9): the response is only <strong>3</strong>. The size tells you the strength.",
     "<strong>A horizontal edge</strong> (dark top, bright bottom): this vertical-edge kernel gives <strong>0</strong> everywhere. You need a different kernel — so CNNs learn many."],
  ml="The same small kernel is reused at every position, so a CNN needs few weights and finds a pattern wherever it appears. Early layers learn edges like this; later layers combine them into shapes and objects."),
 (19, 1): dict(
  s="After finding edges, the network only needs to know <em>roughly</em> where each one is, not to the exact pixel.",
  m="Each 2×2 window keeps only its strongest response, so the map shrinks to a quarter of its size while keeping the important signals.",
  w=["<strong>Move the 6 one pixel</strong> within its window: the output is still 6. Small shifts don't change the result.",
     "<strong>Average pooling</strong> instead: 3.5, 1, 1, 4.25 — smoother, but weak signals dilute strong ones."],
  ml="Pooling makes CNNs cheaper and more tolerant of small shifts in position. Many modern networks use strided convolutions instead, but the idea is the same."),
 (19, 2): dict(
  s="In \"The animal didn't cross the street because it was tired\", the word \"it\" must find which earlier word it refers to. Attention lets each word ask the others \"are you relevant to me?\"",
  m="Token 1's query matches keys 1 and 3 equally, so it takes 40% from each and 20% from token 2. Its new vector (0.60, 0.40) is a blend weighted by relevance.",
  w=["<strong>Without dividing by $\\sqrt{d_k}$:</strong> weights (0.42, 0.16, 0.42) — sharper. With 512-dimensional vectors, unscaled scores get huge and softmax becomes almost all-or-nothing, which makes training unstable; that's why the scaling is there.",
     "<strong>A stronger query</strong> (10, 0): weights (0.5, 0.0, 0.5) — it ignores token 2 completely.",
     "<strong>Token 3's query</strong> (1, 1) matches itself most: weights (0.25, 0.25, 0.50)."],
  ml="Attention is dot products (similarity), softmax (turn scores into weights) and a weighted average. That's the core of every Transformer, including large language models."),
 (20, 0): dict(
  s="A telecom company's churn model uses tenure (months with the company). It must be put on a standard scale before training.",
  m="The z-scores say how many standard deviations each customer is from the average: −1.16 is short tenure, +1.28 is long.",
  w=["<strong>A new customer with 60 months:</strong> $z = (60 - 13)/8.60 = 5.46$ — far outside anything seen in training. Worth flagging: the model is extrapolating.",
     "<strong>One long-standing customer (120 months) in the training data:</strong> the mean becomes 39.75 and the standard deviation 46.9, so the original three get z-scores −0.78, −0.59 and −0.34. One outlier squashes everyone else together — robust scaling (median and IQR) avoids this."],
  ml="Compute the mean and standard deviation on the training data only and reuse them — otherwise information from the test set leaks into training and your scores are over-optimistic."),
 (20, 1): dict(
  s="City is a category, not a number. Coding Chennai = 1, Delhi = 2, Mumbai = 3 would tell a linear model that Mumbai is \"three times\" Chennai.",
  m="One-hot encoding gives each city its own 0/1 column, so no city is \"bigger\" or \"between\" others.",
  w=["<strong>A new city</strong> (Kolkata) appears after deployment: with handle_unknown=\"ignore\" it becomes all zeros — the model treats it as \"none of the known cities\".",
     "<strong>1,000 different cities:</strong> 1,000 new columns, most almost always 0. Group rare categories into \"other\", or use target or frequency encoding."],
  ml="Tree models can cope with simple integer codes; linear models, kNN and neural networks need one-hot (or learned embeddings, Lesson 19)."),
 (21, 0): dict(
  s="A bank's compliance officer audits the loan model before it goes live, comparing two groups of applicants.",
  m="Group B is approved far less often (16% vs 45%), and qualified B applicants are approved less often (60% vs 80%) — yet B's accuracy is higher. Each metric answers a different fairness question.",
  w=["<strong>Lower group B's threshold</strong> so it approves 32 people (16 who would repay, 16 who wouldn't): selection 0.32 (ratio <strong>0.71</strong>), TPR <strong>0.80</strong> (now equal to A), but FPR doubles to 0.20 and precision falls to 0.50.",
     "<strong>A smaller audit:</strong> if group B had only 10 people, one applicant would move B's selection rate by 10 points. Small groups need confidence intervals before conclusions."],
  ml="Fairness metrics are the confusion matrix (Lesson 9) computed per group. Changing a threshold for one group moves all its metrics at once — the trade-offs are unavoidable, so decide which matters most with the people affected."),
 (21, 1): dict(
  s="A regulator asks: \"Can't you just make every error rate equal for both groups?\"",
  m="The identity links FPR, precision, TPR and the base rate. Because the groups' base rates differ (50% vs 20%), fixing two of the rates forces the third apart.",
  w=["<strong>Insist B's FPR equals A's 0.10</strong> while keeping TPR 0.8: B's precision must drop to <strong>0.67</strong> (vs A's 0.89).",
     "<strong>If both groups had the same base rate,</strong> the factor $\\frac{p}{1-p}$ would be the same and all three rates could match."],
  ml="This is why fairness is a choice, not a setting. The impossibility comes from the data's base rates, not from a bad algorithm."),
})

SCENE.update({
 (18, "neuron"): "<p class=\"scene\"><span class=\"scene-tag\">Picture it</span>Deciding whether to go for a run, you weigh the weather, how tired you are and whether a friend is coming, then decide yes or no. A neuron does the same: weigh the inputs, add them up, and squash the total into a decision.</p>",
 (19, "transformers"): "<p class=\"scene\"><span class=\"scene-tag\">Picture it</span>At a busy party you hear your name across the room and instantly tune in to that conversation. Attention lets each word in a sentence tune in to the other words that matter for it, and mostly ignore the rest.</p>",
 (20, "categorical"): "<p class=\"scene\"><span class=\"scene-tag\">Picture it</span>Giving cities numbers like house numbers on a street would imply Delhi lives \"between\" Chennai and Mumbai. One-hot encoding gives each city its own light switch instead: on or off.</p>",
})

WHATIF.update({(18, 0): "neuron", (19, 2): "softmax", (20, 0): "standardise", (21, 0): "fairmetrics"})
