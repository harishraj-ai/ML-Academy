import numpy as np

# Scaled dot-product attention from scratch, for a "sentence" of 4 tokens with 8-number vectors
rng = np.random.default_rng(0)
X = rng.normal(size=(4, 8))                                    # one row per token
Wq, Wk, Wv = (rng.normal(0, 1 / np.sqrt(8), size=(8, 8)) for _ in range(3))
Q, K, V = X @ Wq, X @ Wk, X @ Wv

def softmax(s):
    e = np.exp(s - s.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)

A = softmax(Q @ K.T / np.sqrt(8))                              # attention weights, one row per token
out = A @ V                                                    # each output mixes the value vectors
print("attention weights (row i: how much token i looks at each token):")
print(A.round(2))
print("each row sums to:", A.sum(axis=1).round(3), "  output shape:", out.shape)
