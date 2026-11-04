import numpy as np

# Push a batch through 20 layers of width 256 and watch the activations' spread
rng = np.random.default_rng(0)
x0 = rng.normal(size=(500, 256))
relu = lambda z: np.maximum(z, 0)
setups = {"tanh, weights std 1":           (np.tanh, 1.0),
          "tanh, weights std 0.01":        (np.tanh, 0.01),
          "tanh, Xavier std 1/sqrt(n)":    (np.tanh, 1 / np.sqrt(256)),
          "ReLU, Xavier std 1/sqrt(n)":    (relu, 1 / np.sqrt(256)),
          "ReLU, He std sqrt(2/n)":        (relu, np.sqrt(2 / 256))}
for name, (act, std) in setups.items():
    h = x0; spreads = []
    for layer in range(20):
        h = act(h @ rng.normal(0, std, size=(256, 256)))
        spreads.append(h.std())
    print(f"{name:27}: activation std after layers 1, 10, 20: {spreads[0]:.3f}, {spreads[9]:.3g}, {spreads[19]:.3g}")

# With weights of std 1, tanh is saturated: almost every unit sits near −1 or +1, where its slope is ~0
h = x0
for _ in range(20): h = np.tanh(h @ rng.normal(0, 1.0, size=(256, 256)))
print("tanh with std 1: share of units with |activation| > 0.99:", round(np.mean(np.abs(h) > 0.99), 3))
