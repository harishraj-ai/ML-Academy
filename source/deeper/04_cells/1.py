import numpy as np
from scipy import stats

print("Binomial: P(8 or more of 10 visitors click | p 0.5):", round(stats.binom.sf(7, 10, 0.5), 4))
print("Poisson:  P(no support calls in an hour | 3 per hour):", round(stats.poisson.pmf(0, 3), 4))
print("Exponential: P(wait over 30 min | mean wait 20 min):", round(stats.expon.sf(30, scale=20), 4))
