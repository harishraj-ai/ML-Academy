# Why divide by sqrt(d)? Dot products of random vectors grow with d, making softmax nearly one-hot
for d in [8, 64, 512]:
    q, k = rng.normal(size=(1000, d)), rng.normal(size=(1000, 10, d))
    raw = np.einsum("nd,nkd->nk", q, k)
    top_raw = softmax(raw).max(axis=1).mean()
    top_scaled = softmax(raw / np.sqrt(d)).max(axis=1).mean()
    print(f"d {d:3d}: spread of dot products {raw.std():6.1f}   average top weight, unscaled {top_raw:.2f}, scaled {top_scaled:.2f}")
