# Five more animated walkthroughs (Lessons 8, 9, 14, 15, 17). Same format as walks.py; all numbers computed here.
import numpy as np
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeRegressor
from walks import T, axes

def pts(px, py, X, y, r=6):
    return "".join(f'<circle cx="{px(a):.1f}" cy="{py(b):.1f}" r="{r}" class="wp{int(c)}"/>' for (a, b), c in zip(X, y))

def poly(px, py, xs, ys, cls="ln3"):
    return f'<polyline points="{" ".join(f"{px(a):.1f},{py(b):.1f}" for a, b in zip(xs, ys))}" class="{cls}" fill="none"/>'

# ------------------------------------------------------------------ Lesson 8: logistic regression learns its S-curve
def walk8():
    x = np.array([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])      # the lesson's study-hours data
    y = np.array([0, 0, 0, 1, 0, 1, 0, 1, 1, 1.])
    sg = lambda z: 1 / (1 + np.exp(-z))
    w = b = 0.0; lr = 0.5; hist = {}
    for step in range(0, 3001):
        p = sg(w * x + b)
        if step in (0, 1, 10, 100, 500, 3000): hist[step] = (w, b, -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))
        w, b = w - lr * np.mean((p - y) * x), b - lr * np.mean(p - y)
    W, H = 640, 300
    px = lambda v: 50 + v * 54; py = lambda v: 250 - v * 200
    base = axes(px, py, 0, 5.5, 0, 1, [0, 1, 2, 3, 4, 5], [0, 0.5, 1], "hours studied", "P(pass)")
    base += f'<line x1="{px(0):.1f}" y1="{py(.5):.1f}" x2="{px(5.5):.1f}" y2="{py(.5):.1f}" class="dash"/>'
    base += "".join(f'<circle cx="{px(a):.1f}" cy="{py(c):.1f}" r="5" class="wp{int(c)}"/>' for a, c in zip(x, y))
    xs = np.linspace(0, 5.5, 120); frames = []
    caps = {0: "Start with $w = 0$, $b = 0$: every student gets probability 0.5, a flat line. Log loss {L}.",
            1: "One gradient step: passers sit at larger hours, so $w$ grows and the curve starts to tilt. $w = {w}$, $b = {b}$, log loss {L}.",
            10: "After 10 steps the line has become an S-curve, but a shallow one. $w = {w}$, $b = {b}$, log loss {L}.",
            100: "After 100 steps the S is steeper and shifts right, towards the hours where passes start. Log loss {L}.",
            500: "After 500 steps: $w = {w}$, $b = {b}$, log loss {L}. Progress is now slow: the overlapping students (a pass at 2 hours, fails at 2.5 and 3.5) stop the curve becoming a cliff.",
            3000: "After 3000 steps the curve has settled: $w = {w}$, $b = {b}$, within 0.001 of the lesson's answer. The decision boundary is where it crosses 0.5: $x = -b/w = {bd}$ hours. Left of it we predict fail, right of it pass."}
    for k, (w_, b_, L) in hist.items():
        g = poly(px, py, xs, sg(w_ * xs + b_))
        g += T(380, 40, f"step {k}", "t h") + T(380, 62, f"w = {w_:.3f}   b = {b_:.3f}", "t s") + T(380, 82, f"log loss {L:.3f}", "t a")
        bd = -b_ / w_ if w_ else float("nan")
        if k == 3000:
            g += f'<line x1="{px(bd):.1f}" y1="{py(0):.1f}" x2="{px(bd):.1f}" y2="{py(1):.1f}" class="lw"/>' + T(px(bd) + 6, py(1) + 14, f"boundary {bd:.2f} h", "t s")
        frames.append((g, caps[k].format(w=f"{w_:.3f}", b=f"{b_:.3f}", L=f"{L:.3f}", bd=f"{bd:.2f}")))
    return ("boundary", "Logistic regression learns its S-curve", W, H, base, frames), dict(hist=hist)

# ------------------------------------------------------------------ Lesson 9: sweeping the threshold traces the ROC curve
def walk9():
    pos = np.array([0.95, 0.9, 0.85, 0.8, 0.7, 0.65, 0.55, 0.45, 0.35, 0.2])
    neg = np.array([0.75, 0.6, 0.5, 0.4, 0.3, 0.25, 0.15, 0.12, 0.08, 0.05])
    W, H = 640, 320
    sx = lambda v: 40 + v * 300                                   # score strip
    rx = lambda v: 420 + v * 190; ry = lambda v: 270 - v * 190    # ROC panel
    base = f'<line x1="{sx(0)}" y1="120" x2="{sx(1)}" y2="120" class="ax"/>'
    for v in (0, .25, .5, .75, 1): base += T(sx(v), 136, f"{v:g}", "t s", "c")
    base += T(sx(.5), 156, "model score", "t s", "c") + T(40, 40, "positives (violet) above, negatives (green) below", "t s")
    base += "".join(f'<circle cx="{sx(s):.1f}" cy="90" r="6" class="wp1"/>' for s in pos) + "".join(f'<circle cx="{sx(s):.1f}" cy="104" r="6" class="wp0"/>' for s in neg)
    base += f'<line x1="{rx(0)}" y1="{ry(0)}" x2="{rx(1)}" y2="{ry(0)}" class="ax"/><line x1="{rx(0)}" y1="{ry(0)}" x2="{rx(0)}" y2="{ry(1)}" class="ax"/>'
    base += f'<line x1="{rx(0)}" y1="{ry(0)}" x2="{rx(1)}" y2="{ry(1)}" class="dash"/>'
    for v in (0, .5, 1): base += T(rx(v), ry(0) + 16, f"{v:g}", "t s", "c") + T(rx(0) - 6, ry(v) + 4, f"{v:g}", "t s", "e")
    base += T(rx(.5), ry(0) + 32, "false-positive rate", "t s", "c") + T(rx(0) - 20, ry(1) - 10, "true-positive rate", "t s")
    ths = [1.01, 0.82, 0.62, 0.42, 0.22, 0.0]
    cur = []; frames = []
    order = sorted(set(np.r_[pos, neg]), reverse=True)
    full = [(0.0, 0.0)] + [((neg >= t).mean(), (pos >= t).mean()) for t in order]
    auc = np.mean([(p > n) + 0.5 * (p == n) for p in pos for n in neg])
    for t in ths:
        tpr, fpr = (pos >= t).mean(), (neg >= t).mean()
        path = [(f, r) for f, r in full if (f, r) == (0, 0) or True]
        upto = [(0.0, 0.0)] + [((neg >= s).mean(), (pos >= s).mean()) for s in order if s >= t]
        g = f'<line x1="{sx(min(t, 1)):.1f}" y1="70" x2="{sx(min(t, 1)):.1f}" y2="120" class="lw"/>' + T(sx(min(t, 1)), 64, f"threshold {min(t, 1):.2f}", "t s", "c")
        g += poly(rx, ry, [a for a, _ in upto], [b for _, b in upto], "la") + f'<circle cx="{rx(fpr):.1f}" cy="{ry(tpr):.1f}" r="6" class="fa2"/>'
        g += T(40, 200, f"caught {int(tpr * 10)} of 10 positives: TPR {tpr:.1f}", "t s") + T(40, 220, f"false alarms {int(round(fpr * 10))} of 10 negatives: FPR {fpr:.1f}", "t s")
        if t == ths[0]: cap = "Threshold above every score: nothing is flagged. TPR = 0 and FPR = 0, the bottom-left corner of the ROC plot."
        elif t == 0.0: cap = f"Threshold 0: everything is flagged, TPR = FPR = 1 (top-right). The finished curve's area is the AUC = {auc:.2f}: the chance a random positive scores above a random negative. The dashed diagonal (AUC 0.5) is guessing."
        else: cap = f"Lower the threshold to {t:.2f}: everything to its right is flagged. {int(tpr * 10)} positives are caught (TPR {tpr:.1f}) at the cost of {int(round(fpr * 10))} false alarms (FPR {fpr:.1f}). Each threshold is one point on the curve."
        if t == 0.0: g += T(rx(.55), ry(.25), f"AUC = {auc:.2f}", "t h")
        frames.append((g, cap))
    return ("roc", "Sweeping the threshold traces the ROC curve", W, H, base, frames), dict(auc=auc)

# ------------------------------------------------------------------ Lesson 14: gradient boosting, tree by tree
def walk14():
    rng = np.random.default_rng(14)
    x = np.linspace(0.3, 9.7, 24); y = 2 + 3 * np.sin(x / 1.6) + rng.normal(0, 0.5, x.size)
    W, H = 640, 320
    px = lambda v: 40 + v * 32; py = lambda v: 270 - (v + 2) * 24
    base = axes(px, py, 0, 10, -2, 7, [0, 2, 4, 6, 8, 10], [0, 2, 4, 6], "x", "y")
    base += "".join(f'<circle cx="{px(a):.1f}" cy="{py(b):.1f}" r="5" class="wp1"/>' for a, b in zip(x, y))
    lr = 0.5; F = np.full_like(y, y.mean()); xs = np.linspace(0, 10, 400); Fs = np.full_like(xs, y.mean()); frames = []
    mse = lambda: np.mean((y - F) ** 2)
    def curve(): return poly(px, py, xs, Fs, "la")
    def res_lines(): return "".join(f'<line x1="{px(a):.1f}" y1="{py(b):.1f}" x2="{px(a):.1f}" y2="{py(f):.1f}" class="lr"/>' for a, b, f in zip(x, y, F))
    frames.append((curve() + res_lines() + T(390, 40, "model 0: the mean", "t h") + T(390, 62, f"MSE {mse():.2f}", "t a"),
                   f"Start with the simplest model: predict the mean ({y.mean():.2f}) everywhere. The red lines are the residuals, the errors still to explain. MSE {mse():.2f}."))
    for k in range(1, 7):
        r = y - F; t = DecisionTreeRegressor(max_depth=1).fit(x[:, None], r)
        F = F + lr * t.predict(x[:, None]); Fs = Fs + lr * t.predict(xs[:, None])
        th = t.tree_.threshold[0]
        if k <= 3 or k == 6:
            g = curve() + res_lines() + f'<line x1="{px(th):.1f}" y1="{py(-2):.1f}" x2="{px(th):.1f}" y2="{py(7):.1f}" class="dash2"/>'
            g += T(390, 40, f"after tree {k}", "t h") + T(390, 62, f"tree {k} splits at x = {th:.2f}", "t s") + T(390, 82, f"MSE {mse():.2f}", "t a")
            cap = (f"Tree {k} is a one-split stump fitted to the current residuals (split at x = {th:.2f}). Half of its prediction (learning rate {lr}) is added to the model. MSE falls to {mse():.2f}."
                   if k < 6 else f"After 6 small trees the steps add up to a wiggly curve that follows the data. MSE {mse():.2f}. Each tree is weak on its own; boosting adds them one by one, each fixing what the previous ones got wrong.")
            frames.append((g, cap))
    return ("gradient-boosting", "Gradient boosting, tree by tree", W, H, base, frames), dict(mse=float(mse()))

# ------------------------------------------------------------------ Lesson 15: finding the widest margin
def walk15():
    A = np.array([[1.5, 6], [2, 8], [3, 7.2], [1, 4], [2.6, 5.2], [3.8, 8.6], [1.8, 2.8]])
    B = np.array([[6, 2], [7, 4], [8, 1.5], [6.6, 6], [8.5, 5.5], [5.4, 0.8], [7.8, 7.6]])
    X = np.vstack([A, B]); y = np.r_[np.zeros(len(A)), np.ones(len(B))]; ys = 2 * y - 1
    W, H = 640, 324
    px = lambda v: 40 + v * 30; py = lambda v: 290 - v * 30    # same scale on both axes, so right angles look right
    base = axes(px, py, 0, 10, 0, 9, [0, 2, 4, 6, 8, 10], [0, 2, 4, 6, 8], "x₁", "x₂") + pts(px, py, X, y)
    def line(w, b, cls, off=0.0):  # w·x + b = off
        xa, xb = 0.0, 10.0
        if abs(w[1]) > 1e-9: ya, yb = (off - b - w[0] * xa) / w[1], (off - b - w[0] * xb) / w[1]
        else: return ""
        return f'<line x1="{px(xa):.1f}" y1="{py(ya):.1f}" x2="{px(xb):.1f}" y2="{py(yb):.1f}" class="{cls}" clip-path="url(#svmclip)"/>'
    def margin(w, b): return np.min(ys * (X @ w + b)) / np.linalg.norm(w)
    clip = f'<clipPath id="svmclip"><rect x="{px(0)}" y="{py(9)}" width="{px(10) - px(0)}" height="{py(0) - py(9)}"/></clipPath>'
    frames = []
    for w, b, txt in [(np.array([1.0, 0.25]), -5.4, "This line separates the classes, but it passes very close to a green point."),
                      (np.array([1.0, -0.6]), -2.0, "Another separating line, tilted the other way: it nearly touches a violet point.")]:
        m = margin(w, b)
        frames.append((line(w, b, "lw") + T(390, 40, f"margin {m:.2f}", "t a"), f"{txt} Its margin (distance to the nearest point) is only {m:.2f}. Infinitely many lines separate the data; which is best?"))
    svm = SVC(kernel="linear", C=1e6).fit(X, y); w, b = svm.coef_[0], svm.intercept_[0]; m = 1 / np.linalg.norm(w)
    sv = svm.support_vectors_
    g = line(w, b, "ln3") + line(w, b, "dash", 1) + line(w, b, "dash", -1)
    frames.append((g + T(390, 40, f"margin {m:.2f}", "t a"), f"The SVM picks the line with the widest margin: {m:.2f} on each side (dashed lines). This leaves the most room for new points that land a little off."))
    g2 = g + "".join(f'<circle cx="{px(a):.1f}" cy="{py(c):.1f}" r="11" class="ring2"/>' for a, c in sv)
    frames.append((g2 + T(390, 40, f"{len(sv)} support vectors", "t h"),
                   f"Only the {len(sv)} circled points touch the margin: the <strong>support vectors</strong>. Move or delete any other point and the line stays exactly where it is."))
    return ("margin", "Finding the widest margin", W, H, clip + base, frames), dict(m=m, nsv=len(sv))

# ------------------------------------------------------------------ Lesson 17: PCA finds the direction of most variance
def walk17():
    rng = np.random.default_rng(17)
    z = rng.normal(0, 1, (30, 2)) * [2.0, 0.6]; th = np.deg2rad(30); R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    X = z @ R.T + [5, 4.5]; mu = X.mean(0); Xc = X - mu
    W, H = 640, 324
    px = lambda v: 40 + v * 30; py = lambda v: 290 - v * 30    # same scale on both axes, so right angles look right
    base = axes(px, py, 0, 10, 0, 9, [0, 2, 4, 6, 8, 10], [0, 2, 4, 6, 8], "x₁", "x₂") + pts(px, py, X, np.ones(len(X)), 5)
    var = lambda a: np.var(Xc @ np.array([np.cos(a), np.sin(a)]), ddof=1)
    def dirline(a, cls):
        d = np.array([np.cos(a), np.sin(a)]) * 5
        return f'<line x1="{px(mu[0] - d[0]):.1f}" y1="{py(mu[1] - d[1]):.1f}" x2="{px(mu[0] + d[0]):.1f}" y2="{py(mu[1] + d[1]):.1f}" class="{cls}"/>'
    def proj(a):
        u = np.array([np.cos(a), np.sin(a)]); P = mu + np.outer(Xc @ u, u)
        return "".join(f'<line x1="{px(p[0]):.1f}" y1="{py(p[1]):.1f}" x2="{px(q[0]):.1f}" y2="{py(q[1]):.1f}" class="dash"/>' for p, q in zip(X, P)) + \
               "".join(f'<circle cx="{px(q[0]):.1f}" cy="{py(q[1]):.1f}" r="3" class="fa2"/>' for q in P)
    ev, evec = np.linalg.eigh(np.cov(Xc.T)); a1 = np.arctan2(evec[1, 1], evec[0, 1]); a2 = a1 + np.pi / 2
    frames = [(f'<circle cx="{px(mu[0]):.1f}" cy="{py(mu[1]):.1f}" r="7" class="wq"/>', f"30 points with two correlated features. Step 1: find the centre (mean) at ({mu[0]:.2f}, {mu[1]:.2f}); PCA works with the data centred there.")]
    for a, nm in ((np.deg2rad(100), "a steep direction"), (np.deg2rad(-20), "a shallow direction")):
        frames.append((dirline(a, "lw") + proj(a) + T(390, 40, f"variance along it {var(a):.2f}", "t a"),
                       f"Try {nm}: drop each point onto the line (orange dots). The spread of the dots along the line is the variance it keeps: {var(a):.2f}. Too little; information is lost."))
    frames.append((dirline(a1, "la") + proj(a1) + T(390, 40, f"PC1 variance {ev[1]:.2f}", "t a"),
                   f"The first principal component is the direction where the projected dots spread out most: variance {ev[1]:.2f}, {ev[1] / ev.sum():.0%} of the total. It is the top eigenvector of the covariance matrix."))
    frames.append((dirline(a1, "la") + dirline(a2, "lw") + T(390, 40, f"PC2 variance {ev[0]:.2f}", "t a"),
                   f"PC2 is at right angles to PC1 and keeps the remaining {ev[0]:.2f} ({ev[0] / ev.sum():.0%}). Keeping only PC1 turns each 2-D point into one number while keeping {ev[1] / ev.sum():.0%} of the variance."))
    return ("variance-idea", "PCA finds the direction of most variance", W, H, base, frames), dict(ev=ev)

NEW = [(8, walk8), (9, walk9), (14, walk14), (15, walk15), (17, walk17)]
