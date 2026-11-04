# Residual connections: gradient reaching the first of 50 layers, with and without a shortcut h + f(h)
def first_layer_grad(residual, depth=50, width=64):
    W = [rng.normal(0, 0.5 / np.sqrt(width), size=(width, width)) for _ in range(depth)]   # small weights
    h = rng.normal(size=(32, width)); zs = []
    for Wl in W:
        z = h @ Wl; zs.append(z)
        h = h + np.tanh(z) if residual else np.tanh(z)
    g = np.ones_like(h)
    for Wl, z in zip(reversed(W), reversed(zs)):
        local = (g * (1 - np.tanh(z) ** 2)) @ Wl.T              # gradient through the layer itself
        g = g + local if residual else local                    # the shortcut adds an identity path
    return np.linalg.norm(g)

print("plain 50-layer network, gradient at layer 1:   ", f"{first_layer_grad(False):.2e}")
print("residual 50-layer network, gradient at layer 1:", f"{first_layer_grad(True):.2e}")
