import numpy as np
import warnings
warnings.filterwarnings("ignore")          # the GP optimiser warns about its bounds on tiny data
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, ConstantKernel

# A made-up "validation score vs log10(learning rate)" curve with its peak near x = -2.3
f = lambda x: np.exp(-(x + 2.3) ** 2 / 0.3) * 0.3 + 0.65 + 0.02 * np.sin(5 * x)
grid = np.linspace(-5, 0, 501)[:, None]

def bayes_opt(n_iter, seed):
    rng = np.random.default_rng(seed)
    X = rng.uniform(-5, 0, size=(3, 1)); y = f(X[:, 0])               # 3 random starting points
    kernel = ConstantKernel(1.0, (1e-3, 1e3)) * Matern(length_scale=0.5, length_scale_bounds=(0.05, 5), nu=2.5)
    gp = GaussianProcessRegressor(kernel, alpha=1e-6, normalize_y=True, n_restarts_optimizer=3, random_state=0)
    for _ in range(n_iter - 3):
        gp.fit(X, y)
        mu, sd = gp.predict(grid, return_std=True)
        z = (mu - y.max()) / np.maximum(sd, 1e-9)
        ei = (mu - y.max()) * norm.cdf(z) + sd * norm.pdf(z)             # expected improvement
        x_next = grid[np.argmax(ei)]
        X = np.vstack([X, x_next]); y = np.append(y, f(x_next[0]))
    return y.max()

def random_search(n_iter, seed):
    return f(np.random.default_rng(seed).uniform(-5, 0, n_iter)).max()

best = f(grid[:, 0]).max()
for n in [5, 10, 15]:
    bo = np.mean([best - bayes_opt(n, s) for s in range(20)])
    rs = np.mean([best - random_search(n, s) for s in range(20)])
    print(f"{n:2d} trials: average gap to the best score, Bayesian {bo:.4f}   random {rs:.4f}")
