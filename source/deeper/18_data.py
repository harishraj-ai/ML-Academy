# Lesson 18 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("Why very deep networks are hard to train, with measurements: signals shrink or explode through the layers "
          "and gradients vanish on the way back. The standard fixes are careful starting weights (Xavier and He), "
          "ReLU, batch normalisation and dropout, plus a sensible default recipe for training a new network.")

QUIZ = [
    ("He initialisation uses weight variance $2/n$ rather than $1/n$ because…",
     [("a", "ReLU zeroes about half its inputs, halving the variance passed on"), ("b", "It trains faster on GPUs"), ("c", "Tanh needs it")], "a",
     "Doubling the variance compensates for the half of the signal ReLU throws away."),
    ("A deep sigmoid network's first layers barely learn. The most likely reason is…",
     [("a", "Vanishing gradients: each sigmoid layer multiplies the gradient by at most 0.25"), ("b", "Too much data"), ("c", "The learning rate is too small for the last layer")], "a",
     "Over 20 layers the product of slopes can be around $10^{-12}$."),
    ("At prediction time, batch normalisation uses…",
     [("a", "The statistics of the current batch"), ("b", "Running averages of the mean and variance saved during training"), ("c", "No normalisation")], "b",
     "So a single example gets the same output whatever else is in the batch."),
    ("With inverted dropout and $p = 0.2$, surviving units during training are multiplied by…",
     [("a", "0.8"), ("b", "1.25"), ("c", "5")], "b",
     "$1/(1 - p) = 1/0.8 = 1.25$, so the expected activation is unchanged."),
    ("Weights drawn with standard deviation 1 in a 256-wide tanh network mostly cause…",
     [("a", "Saturation: units stuck near ±1 with almost zero slope"), ("b", "Activations that shrink to zero"), ("c", "Perfect training")], "a",
     "The pre-activations are huge (variance about 256), so tanh is flat almost everywhere it's evaluated."),
]

IQ = [
    (3, "Explain vanishing and exploding gradients and three ways to fix them.",
     "Naming the problem without the mechanism.",
     "Backprop multiplies, layer by layer, by each layer's weights and activation slopes. If those factors are typically below 1 the gradient shrinks exponentially with depth (vanishing); if above 1 it grows (exploding). Fixes: ReLU-family activations (slope 1 when active); variance-preserving initialisation (Xavier for tanh, He for ReLU); normalisation layers (batch or layer norm); residual connections that give gradients a shortcut; gradient clipping for explosions; and, for sequences, gated units (LSTM, GRU) or attention."),
    (2, "How does batch normalisation behave differently in training and inference, and what goes wrong if you forget?",
     "Not knowing there's a difference.",
     "In training it standardises with the current mini-batch's mean and variance and updates running averages. In inference it uses those running averages, so predictions don't depend on the batch. Forgetting to switch to evaluation mode (<code>model.eval()</code> in PyTorch) makes predictions depend on batch composition and size, often badly for batch size 1. Very small training batches also make batch statistics noisy, which is one reason layer or group norm are used instead."),
    (3, "Why does dropout reduce overfitting, and why scale by $1/(1-p)$?",
     "\"It removes neurons.\"",
     "Randomly dropping units prevents co-adaptation (units relying on specific partners) and acts like training an exponential ensemble of thinned subnetworks that share weights; prediction with the full network approximates averaging them. Scaling survivors by $1/(1-p)$ during training keeps each unit's expected input the same as at test time, when nothing is dropped, so no adjustment is needed at prediction."),
]

EX = [
    ("Intermediate", "A layer has 512 inputs. What weight standard deviation does Xavier ($\\text{var} = 1/n$) give, and what does He ($\\text{var} = 2/n$) give?",
     "Xavier: $\\sqrt{1/512} \\approx 0.0442$. He: $\\sqrt{2/512} = 0.0625$."),
    ("Intermediate", "Each layer of a 10-layer network multiplies the gradient by about 0.25. By what factor has it shrunk at the first layer? And if each factor is 1.3?",
     "$0.25^{10} \\approx 9.5\\times 10^{-7}$ (vanishing). $1.3^{10} \\approx 13.79$ (exploding, and much worse with more layers)."),
    ("Intermediate", "Batch norm receives values $(2, 4, 6, 8)$ for one unit, with $\\gamma = 2$, $\\beta = 1$ and $\\epsilon \\approx 0$. What are the outputs? (Use the population variance.)",
     "Mean $5$; variance $(9 + 1 + 1 + 9)/4 = 5$; std $\\approx 2.236$. Standardised: $(-1.342, -0.447, 0.447, 1.342)$. Output $= 2\\hat{z} + 1$: $(-1.683, 0.106, 1.894, 3.683)$."),
]

CHECKS = {
    0: [("Xavier std", 0.04419, "√(1/512)."), ("He std", 0.0625, "√(2/512).")],
    1: [("Factor with 0.25", 9.5367e-7, "0.25 to the power 10.", 2e-8), ("Factor with 1.3", 13.786, "1.3 to the power 10.")],
    2: [("Outputs", [-1.683, 0.106, 1.894, 3.683], "Standardise, then γ·ẑ + β.", 0.005)],
}
