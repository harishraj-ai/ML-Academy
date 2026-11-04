# Lesson 7 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("The improvements to gradient descent that real projects use: momentum (build up speed along a valley), "
          "Adam (a separate step size for every weight, which copes with badly scaled problems), learning-rate "
          "schedules (big steps first, small steps later), and gradient clipping (stop one huge gradient from "
          "wrecking training).")

QUIZ = [
    ("Why does momentum help in a long, narrow valley?",
     [("a", "Zig-zag gradients across the valley cancel, while gradients along it add up"), ("b", "It computes the Hessian"), ("c", "It uses a bigger learning rate for every weight")], "a",
     "The velocity averages past gradients: the side-to-side parts cancel and the downhill part accumulates."),
    ("What does Adam divide each weight's step by?",
     [("a", "The number of steps so far"), ("b", "The square root of a running average of that weight's squared gradients"), ("c", "The loss")], "b",
     "That per-weight scaling is the RMSProp part; the running average of gradients is the momentum part."),
    ("Why does SGD with a constant learning rate keep wobbling near the minimum?",
     [("a", "Mini-batch gradients are noisy, so each step adds noise that never shrinks"), ("b", "The loss isn't convex"), ("c", "Floating-point errors")], "a",
     "Decaying the learning rate shrinks the noisy steps so the weights can settle."),
    ("What does gradient clipping by norm do to a gradient longer than the threshold?",
     [("a", "Sets it to zero"), ("b", "Rescales it to the threshold length, keeping its direction"), ("c", "Clips each entry separately to ±threshold")], "b",
     "Clipping by norm keeps the direction. (Clipping each value separately is a different method, which can change the direction.)"),
    ("What is learning-rate warm-up?",
     [("a", "Starting with a small learning rate and increasing it over the first steps"), ("b", "Training a smaller model first"), ("c", "Running a few epochs without updates")], "a",
     "It protects fragile early training, especially for Adam-trained transformers, before the usual decay."),
]

IQ = [
    (2, "Explain Adam in two sentences. Why is it so popular?",
     "Saying \"it adapts the learning rate\" without saying how.",
     "Adam keeps two running averages per weight: of the gradient (momentum) and of the squared gradient. It steps along the first divided by the square root of the second, with a bias correction for the early steps. Because each weight's step is scaled by its own gradient size, it copes with badly scaled problems and needs little tuning, which suits deep networks with millions of very different weights."),
    (3, "If Adam is so good, why do people still train some models with SGD and momentum?",
     "\"SGD is just older.\"",
     "On many image tasks, well-tuned SGD with momentum and a decaying schedule reaches slightly better test accuracy than Adam (a generalisation gap that is still debated). SGD also uses less memory (Adam stores two extra numbers per weight) and has fewer moving parts. Adam's strengths are speed, robustness to scaling and less tuning, which is why it dominates for transformers, usually as AdamW."),
    (3, "What's the difference between L2 regularization and weight decay, and why does it matter for Adam?",
     "\"They're the same thing.\"",
     "For plain SGD they are mathematically equivalent. For Adam they aren't: an L2 term in the loss gets divided by Adam's per-weight scaling, so weights with large gradients are barely regularized. Decoupled weight decay (AdamW) shrinks the weights directly, $\\mathbf{w} \\leftarrow \\mathbf{w} - \\eta\\lambda\\mathbf{w}$, separately from the adaptive step, which restores the intended effect and usually generalises better."),
    (2, "Why use a learning-rate schedule instead of one well-chosen constant rate?",
     "\"To train faster.\"",
     "Early on, large steps make fast progress and the noise helps explore; near the end, mini-batch noise keeps the weights bouncing around the minimum unless the step size shrinks. Decaying the rate gets both. Warm-up at the very start avoids instability while optimiser statistics and early layers settle. Theory agrees: SGD needs decaying rates to converge."),
]

EX = [
    ("Intermediate", "A loss has curvatures 4 and 400 in its two main directions. What is the largest stable learning rate for plain gradient descent, and roughly by what factor is the error in the gentle direction reduced per step at that rate?",
     "Stability needs $\\eta &lt; 2/400 = 0.005$. In the gentle direction each step multiplies the error by $1 - \\eta\\cdot 4 = 1 - 0.02 = 0.98$. Only a 2% reduction per step, so hundreds of steps are needed."),
    ("Intermediate", "Run one step of momentum by hand: $\\beta = 0.9$, $\\eta = 0.1$, starting from $\\mathbf{v} = (1, 0)$, $\\mathbf{w} = (2, 3)$, with gradient $\\mathbf{g} = (0.5, -1)$. Give the new $\\mathbf{w}$.",
     "$\\mathbf{v} = 0.9(1, 0) + (0.5, -1) = (1.4, -1)$. $\\mathbf{w} = (2, 3) - 0.1(1.4, -1) = (1.86, 3.1)$."),
    ("Intermediate", "Adam's first step ($k = 1$), with $\\mathbf{m}$ and $\\mathbf{s}$ starting at 0, $\\beta_1 = 0.9$, $\\beta_2 = 0.999$, $\\epsilon \\approx 0$ and a single weight with gradient $g = 4$. What is $\\hat{m}/\\sqrt{\\hat{s}}$, and how big is the step with $\\eta = 0.001$?",
     "$m = 0.1 \\times 4 = 0.4$, $\\hat{m} = 0.4/0.1 = 4$. $s = 0.001 \\times 16 = 0.016$, $\\hat{s} = 0.016/0.001 = 16$. Ratio $= 4/\\sqrt{16} = 1$, so the step is $0.001$. Adam's first step has size $\\eta$ whatever the gradient's scale."),
    ("Intermediate", "Clip the gradient $(6, 8)$ to maximum norm 2.",
     "Its length is $\\sqrt{36 + 64} = 10$, above 2, so multiply by $2/10 = 0.2$: $(1.2, 1.6)$."),
]

CHECKS = {
    0: [("Largest stable learning rate", 0.005, "2 ÷ the largest curvature."), ("Error factor per step (gentle direction)", 0.98, "1 − η × 4.")],
    1: [("New w (two numbers)", [1.86, 3.1], "First update v, then w ← w − η·v.")],
    2: [("m̂ / √ŝ", 1, "Apply the bias corrections: divide m by 1 − 0.9 and s by 1 − 0.999."), ("Step size", 0.001, "η × that ratio.")],
    3: [("Clipped gradient", [1.2, 1.6], "Scale by 2 ÷ the length.")],
}
