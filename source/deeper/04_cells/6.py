# A/B test: did the new checkout page raise the conversion rate?
conv = np.array([120, 156]); n = np.array([2400, 2400])
p1, p2 = conv / n
p_pool = conv.sum() / n.sum()
se = np.sqrt(p_pool * (1 - p_pool) * (1 / n[0] + 1 / n[1]))
z = (p2 - p1) / se
print(f"conversion: A {p1:.3f}, B {p2:.3f}   z {z:.2f}   two-sided p-value {2 * stats.norm.sf(abs(z)):.4f}")
