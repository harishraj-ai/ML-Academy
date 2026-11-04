# Backpropagate through 20 sigmoid layers vs 20 ReLU layers: how big is the gradient at the first layer?
def grad_norms(act, dact, std):
    h, cache, Ws = x0[:100], [], []
    for _ in range(20):
        W = rng.normal(0, std, size=(256, 256)); z = h @ W
        cache.append(z); Ws.append(W); h = act(z)
    g = np.ones_like(h)                                  # pretend dLoss/dOutput is all ones
    norms = []
    for z, W in zip(reversed(cache), reversed(Ws)):
        g = (g * dact(z)) @ W.T                          # chain rule, one layer back
        norms.append(np.linalg.norm(g))
    return norms[0], norms[-1]

sig = lambda z: 1 / (1 + np.exp(-z))
for name, act, dact, std in [("sigmoid", sig, lambda z: sig(z) * (1 - sig(z)), 1 / np.sqrt(256)),
                             ("ReLU", relu, lambda z: (z > 0).astype(float), np.sqrt(2 / 256))]:
    last, first = grad_norms(act, dact, std)
    print(f"{name:7}: gradient size at the last layer {last:.3g}, at the first layer {first:.3g}")
