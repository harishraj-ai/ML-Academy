rng = np.random.default_rng(0)
z = [0]
for _ in range(2999): z.append(rng.choice(2, p=T[z[-1]]))
o = np.array([rng.choice(3, p=E[s]) for s in z])
# Baum–Welch from the observations only, starting from a rough guess
Th, Eh, ph = np.array([[0.6, 0.4], [0.4, 0.6]]), np.array([[0.4, 0.3, 0.3], [0.2, 0.3, 0.5]]), np.array([0.5, 0.5])
for it in range(50):
    n = len(o); a = np.zeros((n, 2)); b = np.ones((n, 2)); c = np.zeros(n)
    a[0] = ph * Eh[:, o[0]]; c[0] = a[0].sum(); a[0] /= c[0]
    for t in range(1, n): a[t] = (a[t - 1] @ Th) * Eh[:, o[t]]; c[t] = a[t].sum(); a[t] /= c[t]
    for t in range(n - 2, -1, -1): b[t] = Th @ (Eh[:, o[t + 1]] * b[t + 1]) / c[t + 1]
    gam = a * b
    xi = np.einsum("ti,ij,tj->ij", a[:-1], Th, Eh[:, o[1:]].T * b[1:] / c[1:, None])
    Th = xi / xi.sum(axis=1, keepdims=True)
    Eh = np.array([[gam[o == k, i].sum() for k in range(3)] for i in range(2)]) / gam.sum(axis=0)[:, None]
    ph = gam[0]
print("log-likelihood after 50 iterations:", round(float(np.log(c).sum()), 1))
print("learned transitions:", np.round(Th, 2).tolist())
print("learned emissions:  ", np.round(Eh, 2).tolist())
