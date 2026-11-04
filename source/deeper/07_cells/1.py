import numpy as np

def run(update, grad, start, steps=20000, tol=1e-3):
    """Steps until w is within tol of the minimum at (0, 0)."""
    w, state = np.array(start, dtype=float), {}
    for k in range(1, steps + 1):
        w = update(w, grad(w), state, k)
        if np.linalg.norm(w) < tol: return k
    return None

def plain(lr):
    return lambda w, g, s, k: w - lr * g

def momentum(lr, beta):
    def step(w, g, s, k):
        s["v"] = beta * s.get("v", 0) + g                  # a running "velocity"
        return w - lr * s["v"]
    return step

def adam(lr, b1=0.9, b2=0.999, eps=1e-8):
    def step(w, g, s, k):
        s["m"] = b1 * s.get("m", 0) + (1 - b1) * g         # average gradient
        s["v"] = b2 * s.get("v", 0) + (1 - b2) * g**2      # average squared gradient
        m_hat, v_hat = s["m"] / (1 - b1**k), s["v"] / (1 - b2**k)   # bias correction
        return w - lr * m_hat / (np.sqrt(v_hat) + eps)
    return step

valleys = {"narrow (curvatures 2 and 20)":     (lambda w: np.array([2 * w[0], 20 * w[1]]), 20),
           "very narrow (curvatures 2 and 2000)": (lambda w: np.array([2 * w[0], 2000 * w[1]]), 2000)}
for name, (g, top) in valleys.items():
    lr = 1.8 / top                                         # just under the stability limit 2 / top
    print(name)
    print(f"  plain gradient descent: {run(plain(lr), g, [10, 1])} steps")
    print(f"  momentum (beta 0.3):    {run(momentum(lr * 1.2, 0.3), g, [10, 1])} steps")
    print(f"  Adam (lr 0.1):          {run(adam(0.1), g, [10, 1])} steps")
