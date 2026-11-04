# Salaries whose spread grows with experience (simulated, in lakh per year)
rng = np.random.default_rng(2)
years = rng.uniform(0, 30, size=300)
salary = 4 * np.exp(0.06 * years) * rng.lognormal(0, 0.25, size=300)

def spread(x, target):
    """Fit a line, then compare residual spread for the lowest and highest third of x."""
    m = LinearRegression().fit(x[:, None], target)
    r = target - m.predict(x[:, None])
    low, high = x < np.quantile(x, 1/3), x > np.quantile(x, 2/3)
    return m, r[low].std(), r[high].std()

_, a, b = spread(years, salary)
print(f"raw salary: spread {a:.2f} (junior) vs {b:.2f} (senior)")
m_log, a, b = spread(years, np.log(salary))
print(f"log salary: spread {a:.3f} (junior) vs {b:.3f} (senior)")
k = m_log.coef_[0]
print(f"weight {k:.4f} -> each extra year multiplies salary by {np.exp(k):.3f}")
