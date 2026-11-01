# Animated walkthroughs: each is a list of SVG frames + captions, all numbers computed here in Python.
# WALKS[n] = (section_id, title, svg_w, svg_h, static_svg, [(frame_svg, caption_html), ...])
import numpy as np
from sklearn.tree import DecisionTreeClassifier

WALKS = {}

def T(x, y, s, cls="t", anchor=None):
    a = ' text-anchor="middle"' if anchor == "c" else (' text-anchor="end"' if anchor == "e" else "")
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}"{a}>{s}</text>'

def axes(px, py, x0, x1, y0, y1, xt, yt, xl, yl):
    """Axes box with ticks. px/py map data->pixels."""
    s = f'<line x1="{px(x0):.1f}" y1="{py(y0):.1f}" x2="{px(x1):.1f}" y2="{py(y0):.1f}" class="ax"/>'
    s += f'<line x1="{px(x0):.1f}" y1="{py(y0):.1f}" x2="{px(x0):.1f}" y2="{py(y1):.1f}" class="ax"/>'
    for v in xt: s += T(px(v), py(y0) + 16, f"{v:g}", "t s", "c")
    for v in yt: s += T(px(x0) - 6, py(v) + 4, f"{v:g}", "t s", "e")
    s += T((px(x0) + px(x1)) / 2, py(y0) + 32, xl, "t s", "c")
    s += T(px(x0) - 30, py(y1) - 8, yl, "t s")
    return s

def fmt(v, d=2):
    s = f"{v:.{d}f}"
    return s.replace("-", "−")

# ------------------------------------------------------------------ Lesson 7: gradient descent
def walk7():
    x = np.array([1, 2, 3, 4, 5.]); y = np.array([2, 4, 5, 4, 5.])
    w = b = 0.0; lr = 0.05; hist = {0: (w, b, np.mean((w*x+b-y)**2))}
    for step in range(1, 1001):
        err = w*x + b - y
        w, b = w - lr*2*np.mean(err*x), b - lr*2*np.mean(err)
        if step in (1, 2, 3, 10, 100, 1000): hist[step] = (w, b, np.mean((w*x+b-y)**2))
    W, H = 640, 300
    px = lambda v: 50 + v*48; py = lambda v: 250 - v*28        # left panel: x 0..6, y 0..7.5
    base = axes(px, py, 0, 6, 0, 7.5, [0, 1, 2, 3, 4, 5, 6], [0, 2, 4, 6], "x", "y")
    base += "".join(f'<circle cx="{px(a):.1f}" cy="{py(c):.1f}" r="5" class="wp1"/>' for a, c in zip(x, y))
    steps = [0, 1, 2, 3, 10, 100, 1000]
    qx = lambda i: 400 + i*35; qy = lambda L: 250 - (np.log10(L) - np.log10(0.3))/(np.log10(30) - np.log10(0.3))*210
    base += f'<line x1="{qx(0)-10}" y1="250" x2="{qx(6)+12}" y2="250" class="ax"/><line x1="{qx(0)-10}" y1="250" x2="{qx(0)-10}" y2="36" class="ax"/>'
    for L in (0.5, 1, 5, 20): base += T(qx(0)-14, qy(L)+4, f"{L:g}", "t s", "e")
    for i, s in enumerate(steps): base += T(qx(i), 266, str(s), "t s", "c")
    base += T(qx(3), 284, "step (not to scale)", "t s", "c") + T(qx(0)-10, 26, "loss (MSE, log scale)", "t s")
    base += f'<line x1="{qx(0)-10}" y1="{qy(0.48):.1f}" x2="{qx(6)+12}" y2="{qy(0.48):.1f}" class="dash"/>' + T(qx(6)+12, qy(0.48)-6, "minimum 0.48", "t s", "e")
    frames = []
    H_ = {k: (round(v[0], 3), round(v[1], 3), round(v[2], 3)) for k, v in hist.items()}
    caps = {
        0: f"Start with $w = 0$, $b = 0$: the line lies flat on the x-axis and the loss is huge ({H_[0][2]:g}).",
        1: f"One step: both gradients are negative, so both parameters increase: $w = {H_[1][0]:g}$, $b = {H_[1][1]:g}$. Loss {H_[1][2]:g} — a giant improvement, but the slope is now too steep.",
        2: f"Step 2: the gradient for $w$ is now positive (we overshot), so $w$ comes back down to {H_[2][0]:g}. Loss {H_[2][2]:g}.",
        3: f"Step 3: loss {H_[3][2]:g}. The big gains are already over; from here progress is slow and steady.",
        10: f"After 10 steps the slope is close-ish ($w = {H_[10][0]:g}$) but the intercept is still far too small ($b = {H_[10][1]:g}$ vs 2.2). Loss {H_[10][2]:g}.",
        100: f"After 100 steps: $w = {H_[100][0]:g}$, $b = {H_[100][1]:g}$, loss {H_[100][2]:g}. The intercept creeps up slowly — the two parameters want very different step sizes.",
        1000: f"After 1000 steps: $w = {H_[1000][0]:.3f}$, $b = {H_[1000][1]:.3f}$, loss {H_[1000][2]:g} — exactly the least-squares answer from Lesson 6.",
    }
    for i, s in enumerate(steps):
        w_, b_, L = hist[s]
        g = f'<line x1="{px(0):.1f}" y1="{py(b_):.1f}" x2="{px(6):.1f}" y2="{py(b_+6*w_):.1f}" class="la" clip-path="url(#w7clip)"/>'
        g += "".join(f'<line x1="{px(a):.1f}" y1="{py(c):.1f}" x2="{px(a):.1f}" y2="{py(w_*a+b_):.1f}" class="dash"/>' for a, c in zip(x, y))
        g += T(px(0)+8, 44, f"step {s}:  ŷ = {fmt(w_,3)}·x + {fmt(b_,3)}", "t a")
        pts = "".join(f"{qx(k):.1f},{qy(hist[steps[k]][2]):.1f} " for k in range(i+1))
        g += f'<polyline points="{pts}" class="lw2" fill="none"/>' + "".join(f'<circle cx="{qx(k):.1f}" cy="{qy(hist[steps[k]][2]):.1f}" r="4" class="fa2"/>' for k in range(i+1))
        g += T(qx(i), qy(L)-10, fmt(L, 3), "t w", "c")
        frames.append((g, caps[s]))
    defs = f'<clipPath id="w7clip"><rect x="{px(0)}" y="{py(7.5)}" width="{px(6)-px(0)}" height="{py(0)-py(7.5)}"/></clipPath>'
    return ("worked", "Gradient descent, step by step", W, H, defs + base, frames), hist

# ------------------------------------------------------------------ Lesson 11: kNN vote
def walk11():
    A = [(2, 6), (3, 8), (4, 5.6), (1.5, 3.5), (3.2, 3), (5.4, 6.8), (2.5, 4.6)]   # class 0 (green)
    B = [(5.6, 4.5), (7, 3), (8, 6), (8.5, 2.5), (6.5, 7.5), (7.5, 5.2), (5.8, 2.2)]  # class 1 (violet)
    P = [(p, 0) for p in A] + [(p, 1) for p in B]
    q = (4.8, 5.0); k = 5
    d = sorted(((np.hypot(p[0]-q[0], p[1]-q[1]), p, c) for p, c in P), key=lambda t: t[0])
    W, H = 640, 324
    px = lambda v: 40 + v*36; py = lambda v: 284 - v*30
    base = axes(px, py, 0, 9.5, 0, 8.5, [0, 2, 4, 6, 8], [0, 2, 4, 6, 8], "feature 1", "feature 2")
    base += "".join(f'<circle cx="{px(p[0]):.1f}" cy="{py(p[1]):.1f}" r="6" class="wp{c}"/>' for p, c in P)
    lx = 410
    frames = []
    def panel(rows, vote=None):
        s = T(lx, 40, "Nearest neighbours (sorted)", "t h")
        for i, (dist, p, c) in enumerate(rows):
            s += f'<circle cx="{lx+8}" cy="{62+i*24}" r="6" class="wp{c}"/>' + T(lx+22, 66+i*24, f"#{i+1}  at ({p[0]:g}, {p[1]:g})  distance {dist:.2f}", "t")
        if vote: s += T(lx, 66+len(rows)*24+16, vote, "t h")
        return s
    qpt = f'<circle cx="{px(q[0]):.1f}" cy="{py(q[1]):.1f}" r="8" class="wq"/>' + T(px(q[0])+12, py(q[1])-10, "?", "t h")
    frames.append(("", "Training data: two classes (green and violet). kNN does no training at all — it simply stores these points."))
    frames.append((qpt, f"A new point arrives at $({q[0]:g}, {q[1]:g})$. Which class is it? kNN measures its distance to <em>every</em> stored point."))
    for j in range(1, k+1):
        r = d[j-1][0]
        g = qpt + f'<circle cx="{px(q[0]):.1f}" cy="{py(q[1]):.1f}" r="{r*36:.1f}" class="ring2"/>'
        g += "".join(f'<line x1="{px(q[0]):.1f}" y1="{py(q[1]):.1f}" x2="{px(p[0]):.1f}" y2="{py(p[1]):.1f}" class="lw2"/>' for _, p, _c in d[:j])
        g += panel(d[:j])
        nm = ["green", "violet"][d[j-1][2]]
        cap = f"Neighbour {j} is {nm}, at distance {r:.2f}." + (" With $k = 1$ we would stop here and predict <strong>violet</strong>." if j == 1 and d[0][2] == 1 else "")
        frames.append((g, cap))
    votes = [sum(1 for t in d[:k] if t[2] == c) for c in (0, 1)]
    win = int(np.argmax(votes))
    g = qpt.replace('class="wq"', f'class="wp{win}"') + f'<circle cx="{px(q[0]):.1f}" cy="{py(q[1]):.1f}" r="{d[k-1][0]*36:.1f}" class="ring2"/>'
    g += panel(d[:k], f"Vote: {votes[0]} green vs {votes[1]} violet → {['green', 'violet'][win]}")
    frames.append((g, f"With $k = {k}$ the vote is {votes[0]} green to {votes[1]} violet, so the prediction is <strong>{['green', 'violet'][win]}</strong>. The choice of $k$ changed the answer — that's why $k$ is tuned with cross-validation."))
    return ("algorithm", "kNN classifies a new point", W, H, base, frames), (d, votes)

# ------------------------------------------------------------------ Lesson 13: a tree grows
def walk13():
    X = np.array([[1, 1], [1.5, 3], [2, 6.5], [2.5, 2], [3, 7.5], [1, 8], [3.5, 4], [4.5, 1.5], [5, 8.5], [5.5, 3], [6, 6], [6.5, 1],
                  [7, 4.5], [7.5, 8], [8, 2.5], [8.5, 6.5], [9, 1], [9, 4], [2, 4.5], [4, 6], [7.4, 2.0], [8.2, 1.4], [3.8, 2.6], [1.2, 5.6]])
    y = np.array([0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0])
    t = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X, y).tree_
    W, H = 640, 324
    px = lambda v: 40 + v*32; py = lambda v: 286 - v*28
    names = ["x₁", "x₂"]
    def gini(idx):
        if len(idx) == 0: return 0
        p = y[idx].mean(); return 1 - p*p - (1-p)*(1-p)
    # BFS over internal nodes
    order, queue = [], [(0, (0, 10, 0, 9.3), np.arange(len(y)))]
    while queue:
        node, box_, idx = queue.pop(0)
        if t.children_left[node] == -1: continue
        f, th = t.feature[node], t.threshold[node]
        L = idx[X[idx, f] <= th]; R = idx[X[idx, f] > th]
        x0, x1, y0, y1 = box_
        bl = (x0, th, y0, y1) if f == 0 else (x0, x1, y0, th)
        br = (th, x1, y0, y1) if f == 0 else (x0, x1, th, y1)
        order.append((node, f, th, box_, idx, L, R, bl, br))
        queue.append((t.children_left[node], bl, L)); queue.append((t.children_right[node], br, R))
    base = axes(px, py, 0, 10, 0, 9.3, [0, 2, 4, 6, 8, 10], [0, 2, 4, 6, 8], "x₁", "x₂")
    pts = "".join(f'<circle cx="{px(a):.1f}" cy="{py(b):.1f}" r="6" class="wp{c}"/>' for (a, b), c in zip(X, y))
    def region(bx, idx):
        cls = int(round(y[idx].mean())) if len(idx) else 0
        pure = len(idx) and (y[idx].min() == y[idx].max())
        return f'<rect x="{px(bx[0]):.1f}" y="{py(bx[3]):.1f}" width="{px(bx[1])-px(bx[0]):.1f}" height="{py(bx[2])-py(bx[3]):.1f}" class="wr{cls}{"" if pure else " mixed"}"/>'
    frames = []
    root_idx = np.arange(len(y))
    frames.append((region((0, 10, 0, 9.3), root_idx) + pts,
                   f"Start: one region holding all {len(y)} points ({(y==0).sum()} green, {(y==1).sum()} violet). Gini impurity {gini(root_idx):.3f}. The tree tries every possible threshold on every feature and keeps the one that lowers impurity the most."))
    leaves = {0: ((0, 10, 0, 9.3), root_idx)}
    lines = ""
    for k, (node, f, th, bx, idx, L, R, bl, br) in enumerate(order):
        del leaves[node]
        leaves[t.children_left[node]] = (bl, L); leaves[t.children_right[node]] = (br, R)
        if f == 0: ln = f'<line x1="{px(th):.1f}" y1="{py(bx[3]):.1f}" x2="{px(th):.1f}" y2="{py(bx[2]):.1f}" class="ln3"/>'
        else: ln = f'<line x1="{px(bx[0]):.1f}" y1="{py(th):.1f}" x2="{px(bx[1]):.1f}" y2="{py(th):.1f}" class="ln3"/>'
        lines += ln
        regs = "".join(region(b_, i_) for b_, i_ in leaves.values())
        hot = ln.replace('class="ln3"', 'class="lw"')
        wg = (len(L)*gini(L) + len(R)*gini(R)) / len(idx)
        panel = T(400, 40, f"Split {k+1}:  {names[f]} ≤ {th:g} ?", "t h")
        panel += T(400, 64, f"region before: {len(idx)} points, Gini {gini(idx):.3f}", "t s")
        panel += T(400, 84, f"yes side: {len(L)} points, Gini {gini(L):.3f}", "t s")
        panel += T(400, 104, f"no side: {len(R)} points, Gini {gini(R):.3f}", "t s")
        panel += T(400, 124, f"weighted Gini after: {wg:.3f}", "t a")
        cap = (f"Split {k+1}: the best question for this region is \"{names[f]} ≤ {th:g}?\". It divides {len(idx)} points into {len(L)} and {len(R)}, "
               f"lowering the weighted Gini from {gini(idx):.3f} to {wg:.3f}.")
        frames.append((regs + lines + hot + pts + panel, cap))
    acc = (DecisionTreeClassifier(max_depth=3, random_state=0).fit(X, y).predict(X) == y).mean()
    regs = "".join(region(b_, i_) for b_, i_ in leaves.values())
    frames.append((regs + lines + pts + T(400, 40, f"Depth 3 reached: {len(leaves)} leaves", "t h") + T(400, 64, f"training accuracy {acc:.0%}", "t a"),
                   f"The maximum depth (3) is reached. Each of the {len(leaves)} rectangles is a leaf; a new point gets the majority class of the rectangle it falls in. Training accuracy: {acc:.0%}. Shaded rectangles still containing both colours are impure."))
    return ("algorithm", "A decision tree grows, split by split", W, H, base, frames), (order, acc)

# ------------------------------------------------------------------ Lesson 16: k-means iterations
def walk16():
    rng = np.random.default_rng(3)
    C = np.array([[2.2, 2.5], [7.5, 3], [4.8, 7.2]])
    X = np.vstack([c + rng.normal(0, 0.9, (10, 2)) for c in C]).clip(0.2, 9.6)
    mu = X[[0, 1, 12]].copy()   # deliberately poor start: two centroids in the same blob
    W, H = 640, 324
    px = lambda v: 40 + v*34; py = lambda v: 286 - v*27
    base = axes(px, py, 0, 10, 0, 9.5, [0, 2, 4, 6, 8, 10], [0, 2, 4, 6, 8], "feature 1", "feature 2")
    def cent(m, cls="cen"):
        return "".join(f'<g class="{cls} cen{j}"><path d="M{px(a)-9:.1f},{py(b)-9:.1f} L{px(a)+9:.1f},{py(b)+9:.1f} M{px(a)+9:.1f},{py(b)-9:.1f} L{px(a)-9:.1f},{py(b)+9:.1f}"/></g>' for j, (a, b) in enumerate(m))
    def ptsf(lab=None):
        return "".join(f'<circle cx="{px(a):.1f}" cy="{py(b):.1f}" r="5.5" class="{"wn" if lab is None else "wc" + str(lab[i])}"/>' for i, (a, b) in enumerate(X))
    inertia = lambda lab, m: float(((X - m[lab])**2).sum())
    frames = [(ptsf() + cent(mu), "30 unlabelled points and $k = 3$ starting centroids (✕), picked at random from the data. Two of them landed in the same group — a poor start, on purpose.")]
    it, lab_old, info = 0, None, []
    while True:
        it += 1
        lab = np.argmin(((X[:, None, :] - mu[None]) ** 2).sum(-1), axis=1)
        if lab_old is not None and (lab == lab_old).all():
            frames.append((ptsf(lab) + cent(mu), f"Iteration {it}: assigning again changes nothing — the algorithm has <strong>converged</strong> after {it-1} updates. Final inertia {inertia(lab, mu):.1f}."))
            info.append(("converged", it-1, inertia(lab, mu)))
            break
        changed = len(X) if lab_old is None else int((lab != lab_old).sum())
        I1 = inertia(lab, mu)
        frames.append((ptsf(lab) + cent(mu), f"Iteration {it} — <strong>assign</strong>: each point joins its nearest centroid" + ("" if lab_old is None else f" ({changed} point{'' if changed == 1 else 's'} switched cluster)") + f". Inertia {I1:.1f}."))
        new = np.array([X[lab == j].mean(0) for j in range(3)])
        trail = "".join(f'<line x1="{px(mu[j,0]):.1f}" y1="{py(mu[j,1]):.1f}" x2="{px(new[j,0]):.1f}" y2="{py(new[j,1]):.1f}" class="dash2" marker-end="url(#ah)"/>' for j in range(3))
        I2 = inertia(lab, new)
        frames.append((ptsf(lab) + cent(mu, "cen ghost") + trail + cent(new), f"Iteration {it} — <strong>update</strong>: each centroid moves to the mean of its points. Inertia falls to {I2:.1f}."))
        info.append((it, changed, I1, I2))
        mu, lab_old = new, lab
    return ("kmeans", "k-means, iteration by iteration", W, H, base, frames), info

# ------------------------------------------------------------------ Lesson 18: forward & backward pass
def walk18():
    sg = lambda z: 1/(1+np.exp(-z))
    x = np.array([1., 0.]); yv = 1
    Wh = np.array([[0.5, 0.3], [-0.5, 0.8]]); v = np.array([1., -1.]); c = 0.0
    z = Wh @ x; h = sg(z); zo = v @ h + c; p = sg(zo); L = -np.log(p)
    do = p - yv; gv = do*h; dh = do*v*h*(1-h); gW = np.outer(dh, x)
    Wn = Wh - gW; vn = v - gv; cn = c - do
    p2 = sg(vn @ sg(Wn @ x) + cn); L2 = -np.log(p2)
    W, H = 640, 300
    N = {"x1": (70, 90), "x2": (70, 210), "h1": (280, 90), "h2": (280, 210), "o": (480, 150)}
    E = [("x1", "h1"), ("x2", "h1"), ("x1", "h2"), ("x2", "h2"), ("h1", "o"), ("h2", "o")]
    def edge(a, b, cls="ln"):
        (x1, y1), (x2, y2) = N[a], N[b]
        return f'<line x1="{x1+24}" y1="{y1}" x2="{x2-24}" y2="{y2}" class="{cls}"/>'
    def node(k, lab, cls="b"):
        a, b = N[k]; return f'<circle cx="{a}" cy="{b}" r="24" class="{cls}"/>' + T(a, b+5, lab, "t c")
    def mid(a, b, off=-8):
        (x1, y1), (x2, y2) = N[a], N[b]; return ((x1+x2)/2, (y1+y2)/2 + off)
    base = "".join(edge(a, b) for a, b in E)
    base += node("x1", "x₁") + node("x2", "x₂") + node("h1", "h₁") + node("h2", "h₂") + node("o", "p")
    base += f'<line x1="504" y1="150" x2="560" y2="150" class="ln"/>' + T(590, 155, "L", "t h c")
    base += T(70, 40, "input", "t s c") + T(280, 40, "hidden (sigmoid)", "t s c") + T(480, 40, "output (sigmoid)", "t s c")
    wl = {("x1", "h1"): Wh[0, 0], ("x2", "h1"): Wh[0, 1], ("x1", "h2"): Wh[1, 0], ("x2", "h2"): Wh[1, 1], ("h1", "o"): v[0], ("h2", "o"): v[1]}
    offs = {("x1", "h1"): (-10, -10), ("x2", "h1"): (-40, -18), ("x1", "h2"): (-40, 26), ("x2", "h2"): (-10, 22), ("h1", "o"): (0, -12), ("h2", "o"): (0, 24)}
    def wlabels(vals, cls="t s"):
        s = ""
        for e_, val in vals.items():
            m = mid(*e_, off=0); o = offs[e_]
            s += T(m[0]+o[0], m[1]+o[1], fmt(val, 4 if abs(val - round(val, 1)) > 1e-9 else 1), cls, "c")
        return s
    W0 = wlabels(wl)
    inp = T(70, 130, "1", "t a c") + T(70, 250, "0", "t a c") + T(590, 185, "y = 1", "t s c")
    hidv = T(280, 130, f"z={fmt(z[0],2)} h={fmt(h[0],4)}", "t a c") + T(280, 250, f"z={fmt(z[1],2)} h={fmt(h[1],4)}", "t a c")
    outv = T(480, 192, f"z={fmt(zo,4)}", "t a c") + T(480, 210, f"p={fmt(p,4)}", "t a c")
    lossv = T(590, 128, f"{fmt(L,3)}", "t w c")
    hot = lambda ks: "".join(node(k, {"x1": "x₁", "x2": "x₂", "h1": "h₁", "h2": "h₂", "o": "p"}[k], "b2") for k in ks)
    hotr = lambda ks: "".join(node(k, {"x1": "x₁", "x2": "x₂", "h1": "h₁", "h2": "h₂", "o": "p"}[k], "b3") for k in ks)
    fr = []
    fr.append((W0 + inp, "The 2-2-1 network from the worked example, with its starting weights on the edges. Input $\\mathbf{x} = (1, 0)$, true label $y = 1$, all biases 0."))
    fr.append((W0 + inp + "".join(edge(a, b, "la") for a, b in E[:4]) + hot(["h1", "h2"]) + hidv,
               f"<strong>Forward 1:</strong> each hidden neuron computes $z = \\mathbf{{w}}\\cdot\\mathbf{{x}}$ and squashes it: $h_1 = \\sigma(0.5) = {h[0]:.4f}$, $h_2 = \\sigma(-0.5) = {h[1]:.4f}$."))
    fr.append((W0 + inp + hidv + "".join(edge(a, b, "la") for a, b in E[4:]) + hot(["o"]) + outv,
               f"<strong>Forward 2:</strong> the output neuron combines them: $z = 1\\cdot{h[0]:.4f} - 1\\cdot{h[1]:.4f} = {zo:.4f}$, so $p = \\sigma(z) = {p:.4f}$."))
    fr.append((W0 + inp + hidv + outv + lossv + '<line x1="504" y1="150" x2="560" y2="150" class="la"/>',
               f"<strong>Loss:</strong> $L = -\\ln p = {L:.3f}$. The network gives only a {p:.0%} chance to the right answer. Now the backward pass works out who to blame."))
    dov = T(480, 100, f"δ={fmt(do,4)}", "t r c")
    fr.append((W0 + inp + hidv + outv + lossv + hotr(["o"]) + dov + '<line x1="504" y1="150" x2="560" y2="150" class="lr"/>',
               f"<strong>Backward 1:</strong> the error signal at the output is $\\delta_{{out}} = p - y = {do:.4f}$ (negative: $p$ should go <em>up</em>)."))
    gvl = T(380, 98, f"∂L/∂v₁={fmt(gv[0],4)}", "t r c") + T(380, 214, f"∂L/∂v₂={fmt(gv[1],4)}", "t r c")
    fr.append((inp + hidv + outv + lossv + dov + hotr(["o"]) + "".join(edge(a, b, "lr") for a, b in E[4:]) + gvl + wlabels({k: wl[k] for k in E[:4]}),
               f"<strong>Backward 2:</strong> each output weight's gradient is (error arriving) × (input it carried): $\\partial L/\\partial v_1 = {do:.4f}\\times{h[0]:.4f} = {gv[0]:.4f}$, $\\partial L/\\partial v_2 = {gv[1]:.4f}$."))
    dhl = T(280, 50 + 6, f"δ₁={fmt(dh[0],4)}", "t r c") + T(280, 276, f"δ₂={fmt(dh[1],4)}", "t r c")
    fr.append((inp + outv + lossv + dov + hotr(["o", "h1", "h2"]) + "".join(edge(a, b, "lr") for a, b in E[4:]) + dhl + wlabels(wl),
               f"<strong>Backward 3:</strong> the error flows back through each output weight and the sigmoid's slope $h(1-h) = {h[0]*(1-h[0]):.4f}$: $\\delta_1 = {do:.4f}\\times 1\\times{h[0]*(1-h[0]):.4f} = {dh[0]:.4f}$, $\\delta_2 = {dh[1]:.4f}$."))
    gWl = wlabels({("x1", "h1"): gW[0, 0], ("x2", "h1"): gW[0, 1], ("x1", "h2"): gW[1, 0], ("x2", "h2"): gW[1, 1]}, "t r")
    fr.append((inp + outv + lossv + hotr(["h1", "h2"]) + "".join(edge(a, b, "lr") for a, b in E[:4]) + dhl + gWl + wlabels({k: wl[k] for k in E[4:]}),
               f"<strong>Backward 4:</strong> hidden-weight gradients are $\\delta_j \\times x_k$. Because $x_2 = 0$, the weights leaving $x_2$ get zero gradient — that input contributed nothing."))
    wn = {("x1", "h1"): Wn[0, 0], ("x2", "h1"): Wn[0, 1], ("x1", "h2"): Wn[1, 0], ("x2", "h2"): Wn[1, 1], ("h1", "o"): vn[0], ("h2", "o"): vn[1]}
    fr.append((inp + wlabels(wn, "t w") + T(480, 210, f"bias c={fmt(cn,4)}", "t w c"),
               f"<strong>Update</strong> ($\\eta = 1$): every weight moves against its gradient. $v = ({vn[0]:.4f}, {vn[1]:.4f})$, $c = {cn:.4f}$, $w_{{11}} = {Wn[0,0]:.4f}$, $w_{{21}} = {Wn[1,0]:.4f}$."))
    fr.append((inp + wlabels(wn) + "".join(edge(a, b, "la") for a, b in E) + hot(["o"]) + T(480, 210, f"p={fmt(p2,4)}", "t a c") + T(590, 128, f"{fmt(L2,3)}", "t w c"),
               f"<strong>Forward again</strong> with the new weights: $p = {p2:.4f}$ and the loss drops from {L:.3f} to {L2:.3f}. Training repeats this loop thousands of times."))
    return ("backprop", "Forward pass, backward pass, update", W, H, base, fr), dict(h=h, zo=zo, p=p, L=L, do=do, gv=gv, dh=dh, vn=vn, cn=cn, Wn=Wn, p2=p2, L2=L2)

CHECK = {}
for n, fn in [(7, walk7), (11, walk11), (13, walk13), (16, walk16), (18, walk18)]:
    WALKS[n], CHECK[n] = fn()

def walk_html(title, W, H, static, frames, n):
    gs = "".join(f'<g class="wf{" on" if i == 0 else ""}" data-i="{i}">{g}</g>' for i, (g, _) in enumerate(frames))
    caps = "".join(f'<p class="walk-cap{" on" if i == 0 else ""}" data-i="{i}">{c}</p>' for i, (_, c) in enumerate(frames))
    defs = '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="fa"/></marker></defs>'
    if static.startswith("<clipPath"):
        cp_end = static.index("</clipPath>") + 11
        defs = defs.replace("</defs>", static[:cp_end] + "</defs>"); static = static[cp_end:]
    svg = f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{title}" xmlns="http://www.w3.org/2000/svg">{defs}{static}{gs}</svg>'
    svg = svg.replace('id="ah"', f'id="wah{n}"').replace('url(#ah)', f'url(#wah{n})')
    ctr = ('<div class="walk-ctl"><button type="button" class="wk-prev" aria-label="Previous step">‹ Back</button>'
           '<button type="button" class="wk-play" aria-label="Play">▶ Play</button>'
           '<button type="button" class="wk-next" aria-label="Next step">Next ›</button>'
           f'<span class="wk-count" aria-live="polite">Step 1 / {len(frames)}</span>'
           '<button type="button" class="wk-reset">↺ Restart</button></div>')
    return (f'<figure class="fig walk" data-walk="{n}"><div class="walk-head"><span class="walk-tag">Animated walkthrough</span>'
            f'<span class="walk-title">{title}</span></div>{svg}<div class="walk-caps">{caps}</div>{ctr}</figure>')

if __name__ == "__main__":
    import json
    print(CHECK[7])
    d, votes = CHECK[11]; print([(round(a, 2), p, c) for a, p, c in d[:6]], votes)
    order, acc = CHECK[13]; print([(f, th, len(L), len(R)) for _, f, th, _, _, L, R, _, _ in order], acc)
    print(CHECK[16])
    print({k: np.round(v, 4) for k, v in CHECK[18].items()})
    for n, w in WALKS.items(): print(n, w[0], len(w[5]), "frames")
