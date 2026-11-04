def hessian_numeric(g, v, h=1e-4):
    d = len(v); H = np.zeros((d, d))
    for i in range(d):
        for j in range(d):
            ei, ej = np.eye(d)[i] * h, np.eye(d)[j] * h
            H[i, j] = (g(v + ei + ej) - g(v + ei - ej) - g(v - ei + ej) + g(v - ei - ej)) / (4 * h * h)
    return H

bowl = lambda w: w[0]**2 + 10 * w[1]**2          # a long, narrow valley
saddle = lambda w: w[0]**2 - w[1]**2             # up in one direction, down in the other
for name, g in [("bowl", bowl), ("saddle", saddle)]:
    H = hessian_numeric(g, np.array([0.0, 0.0]))
    print(name, "Hessian eigenvalues:", np.linalg.eigvalsh(H).round(3))
