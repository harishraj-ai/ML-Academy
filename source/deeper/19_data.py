# Lesson 19 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("The two ideas behind modern architectures, built from scratch: attention (each token takes a weighted "
          "average of the others, with weights from matching queries and keys) and residual connections (a "
          "shortcut that lets gradients reach the early layers). Also: why attention divides by the square root "
          "of the dimension, positional encodings, and ways to adapt pretrained models (fine-tuning, LoRA).")

QUIZ = [
    ("In attention, what does each row of $\\operatorname{softmax}(QK^\\top/\\sqrt{d})$ add up to?",
     [("a", "0"), ("b", "1"), ("c", "$d$")], "b",
     "Each row is a softmax: a set of weights for averaging the value vectors."),
    ("Without the $\\sqrt{d}$ scaling, large $d$ makes the attention weights…",
     [("a", "Almost one-hot, with tiny gradients"), ("b", "Exactly uniform"), ("c", "Negative")], "a",
     "Dot-product spread grows like $\\sqrt{d}$, pushing the softmax towards a single winner."),
    ("Why do residual connections help gradients flow?",
     [("a", "The derivative of $\\mathbf{h} + f(\\mathbf{h})$ includes an identity term"), ("b", "They remove non-linearities"), ("c", "They make the network shallower")], "a",
     "Even if $f$'s Jacobian is tiny, the identity path carries the gradient back."),
    ("Without positional encodings, a transformer would treat a sentence as…",
     [("a", "A sequence"), ("b", "An unordered set of tokens"), ("c", "A single token")], "b",
     "Self-attention is permutation-equivariant: it has no built-in notion of order."),
    ("LoRA fine-tunes a large model by…",
     [("a", "Retraining every weight"), ("b", "Learning small low-rank matrices added to frozen weights"), ("c", "Deleting layers")], "b",
     "$\\Delta W = BA$ with a small rank, which is far fewer numbers to train and store."),
]

IQ = [
    (3, "Walk me through what a single self-attention head computes.",
     "Describing attention as \"focusing\" without the computation.",
     "Project each token's vector into a query, key and value with learned matrices. Compute scores $QK^\\top$, scale by $1/\\sqrt{d_k}$, apply a mask if needed (causal masking for language models), and softmax each row into weights. Each output is the weighted sum of the value vectors. Cost is quadratic in sequence length, which is why long contexts are expensive and why efficient-attention variants exist."),
    (3, "Why are residual connections so important in deep networks?",
     "\"They add information from earlier layers.\"",
     "They make each block learn a correction $f(\\mathbf{h})$ to an identity mapping. In backprop the Jacobian becomes $I + J_f$, so gradients always have a direct path to early layers, avoiding vanishing gradients through many layers. They also make very deep networks easy to optimise, since a block can default to doing almost nothing. Both ResNets and transformers depend on them."),
    (2, "What's LoRA, and why is it popular for fine-tuning LLMs?",
     "Calling it a type of quantization.",
     "Low-Rank Adaptation freezes the pretrained weights and learns, for chosen layers, a low-rank update $\\Delta W = BA$ (rank 4–64). That trains and stores a tiny fraction of the parameters, needs much less GPU memory, and lets you keep many task-specific adapters for one base model. Quality is often close to full fine-tuning. QLoRA combines it with a quantized base model to save more memory."),
]

EX = [
    ("Intermediate", "Two tokens have attention scores $(2, 0)$ after scaling. What are the softmax weights? If their value vectors are $(1, 0)$ and $(0, 1)$, what is the output?",
     "Weights: $e^2/(e^2 + 1) \\approx 0.881$ and $1/(e^2 + 1) \\approx 0.119$. Output: $0.881(1, 0) + 0.119(0, 1) = (0.881, 0.119)$."),
    ("Intermediate", "Queries and keys have $d_k = 64$ with entries of variance 1. What is the standard deviation of a raw dot product, and after dividing by $\\sqrt{d_k}$?",
     "Variance $64$, so standard deviation $8$. After scaling: $8/8 = 1$."),
    ("Intermediate", "A $1024 \\times 1024$ weight matrix gets a LoRA update of rank 16. How many trainable numbers does LoRA add, and what fraction is that of the full matrix?",
     "$B$ is $1024 \\times 16$ and $A$ is $16 \\times 1024$: $2 \\times 16{,}384 = 32{,}768$. The full matrix has $1{,}048{,}576$, so the fraction is $0.03125$ (3.1%)."),
]

CHECKS = {
    0: [("Softmax weights", [0.8808, 0.1192], "e² / (e² + 1) and 1 / (e² + 1).")],
    1: [("Std of raw dot product", 8, "√64."), ("Std after scaling", 1, "Divide by √64.")],
    2: [("LoRA numbers", 32768, "1024 × 16 + 16 × 1024."), ("Fraction of the full matrix", 0.03125, "Divide by 1024².")],
}
