import numpy as np
pi = np.array([0.6, 0.4]); T = np.array([[0.8, 0.2], [0.3, 0.7]]); E = np.array([[0.6, 0.3, 0.1], [0.1, 0.4, 0.5]])
obs = [0, 1, 1, 2, 1, 0]                                   # Walk Shop Shop Clean Shop Walk
def forward_backward(o):
    n = len(o); a = np.zeros((n, 2)); b = np.ones((n, 2))
    a[0] = pi * E[:, o[0]]
    for t in range(1, n): a[t] = (a[t - 1] @ T) * E[:, o[t]]
    for t in range(n - 2, -1, -1): b[t] = T @ (E[:, o[t + 1]] * b[t + 1])
    post = a * b
    return post / post.sum(axis=1, keepdims=True)
print("P(rainy) each day:", np.round(forward_backward(obs)[:, 1], 3).tolist())
