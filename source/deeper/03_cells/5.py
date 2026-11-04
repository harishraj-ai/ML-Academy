from scipy.optimize import minimize

# Largest rectangle with perimeter 20: maximise x·y subject to 2x + 2y = 20
res = minimize(lambda v: -v[0] * v[1], x0=[1.0, 1.0],
               constraints=[{"type": "eq", "fun": lambda v: 2 * v[0] + 2 * v[1] - 20}])
print("numerical answer (x, y):", res.x.round(4), " area:", round(-res.fun, 4))
