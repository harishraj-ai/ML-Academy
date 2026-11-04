grad = lambda w: np.array([2 * w[0], 20 * w[1]])
H = np.array([[2.0, 0.0], [0.0, 20.0]])

for lr in [0.01, 0.05, 0.09, 0.11]:
    w = np.array([10.0, 1.0])
    for step in range(1, 10001):
        w = w - lr * grad(w)
        if np.linalg.norm(w) < 1e-6 or np.linalg.norm(w) > 1e6: break
    status = "diverged" if np.linalg.norm(w) > 1e6 else f"{step} steps"
    print(f"gradient descent, learning rate {lr}: {status}")

w = np.array([10.0, 1.0])
w = w - np.linalg.solve(H, grad(w))              # one Newton step
print("Newton's method: 1 step, lands at", w)
