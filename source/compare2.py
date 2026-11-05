# Side-by-side comparisons for Parts 6 and 7. Every chart is computed here with real models.
import warnings
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from sklearn.datasets import load_digits
from walks import T, axes
warnings.filterwarnings("ignore")

def svg(w, h, body, label):
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'

def lines(series, x0, x1, y0, y1, xt, yt, xl, yl, title, legend_y=40, legend_x=430):
    px = lambda v: 70 + (v - x0) / (x1 - x0) * 520; py = lambda v: 250 - (v - y0) / (y1 - y0) * 200
    s = axes(px, py, x0, x1, y0, y1, xt, yt, xl, yl) + T(330, 16, title, "t h", "c")
    for k, (name, xs, ys, cls) in enumerate(series):
        s += '<polyline points="' + " ".join(f"{px(a):.1f},{py(b):.1f}" for a, b in zip(xs, ys)) + f'" class="{cls}" fill="none"/>'
        s += f'<line x1="{legend_x}" y1="{legend_y + 16 * k}" x2="{legend_x + 22}" y2="{legend_y + 16 * k}" class="{cls}"/>' + T(legend_x + 28, legend_y + 4 + 16 * k, name, "t s")
    return s

FIGS, CAPS = {}, {}

# 1 ---- randomised vs observational estimates (Lesson 29)
def fig_causal():
    rng = np.random.default_rng(1); n = 5000
    loyalty = rng.normal(0, 1, n)
    t = (rng.random(n) < 1 / (1 + np.exp(-1.5 * loyalty))).astype(int)
    y = 100 + 25 * loyalty + 10 * t + rng.normal(0, 15, n)
    naive = y[t == 1].mean() - y[t == 0].mean()
    reg = LinearRegression().fit(np.c_[t, loyalty], y).coef_[0]
    ps = np.clip(LogisticRegression().fit(loyalty[:, None], t).predict_proba(loyalty[:, None])[:, 1], 0.05, 0.95)
    w1, w0 = t / ps, (1 - t) / (1 - ps)
    ipw = (w1 * y).sum() / w1.sum() - (w0 * y).sum() / w0.sum()
    r = rng.random(n) < 0.5; y2 = 100 + 25 * loyalty + 10 * r + rng.normal(0, 15, n)
    rct = y2[r].mean() - y2[~r].mean()
    vals = [("Naive comparison", naive, "wc3"), ("Regression adjustment", reg, "wc1"), ("Propensity weighting", ipw, "wc1"), ("Randomised experiment", rct, "wc0")]
    s = T(330, 16, "Estimated effect of a discount (true effect: 10)", "t h", "c")
    px = lambda v: 220 + v * 9
    s += f'<line x1="{px(0)}" y1="34" x2="{px(0)}" y2="226" class="ax"/><line x1="{px(10):.1f}" y1="30" x2="{px(10):.1f}" y2="230" class="dash"/>' + T(px(10), 246, "true effect", "t s", "c")
    for k, (name, v, cls) in enumerate(vals):
        yy = 44 + 46 * k
        s += T(210, yy + 18, name, "t s", "e") + f'<rect x="{px(0)}" y="{yy}" width="{max(1, v * 9):.1f}" height="28" class="{cls}"/>' + T(px(v) + 6, yy + 18, f"{v:.1f}", "t s")
    CAPS["observational-vs-randomised"] = (f"Simulated customers where loyalty drives both discounts and spending. The naive comparison says {naive:.1f}; adjusting for loyalty gives {reg:.1f} (regression) or "
                                          f"{ipw:.1f} (weighting), and a randomised experiment gives {rct:.1f}. Adjustment only works because loyalty was measured.")
    return svg(640, 256, s, "Bar chart: the naive comparison overstates the discount's effect; adjusted and randomised estimates are close to the truth")

# 2 ---- data drift vs concept drift (Lesson 30)
def fig_drift():
    rng = np.random.default_rng(0)
    def loans(n, flip=0.0, shift=0.0):
        inc = rng.normal(50 + shift, 15, n); debt = rng.normal(20, 8, n)
        logit = (-0.08 + flip) * (inc - 50) + 0.12 * (debt - 20) - 1.5
        return np.c_[inc, debt], (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    X, y = loans(5000); m = make_pipeline(StandardScaler(), LogisticRegression()).fit(X, y)
    months = list(range(1, 13)); data_d, concept_d = [], []
    for k in months:
        Xa, ya = loans(1500, shift=-1.5 * k); data_d.append(roc_auc_score(ya, m.predict_proba(Xa)[:, 1]))
        Xb, yb = loans(1500, flip=0.0 if k < 5 else 0.02 * (k - 4)); concept_d.append(roc_auc_score(yb, m.predict_proba(Xb)[:, 1]))
    s = lines([("data drift: incomes fall", months, data_d, "la"), ("concept drift: income's effect reverses", months, concept_d, "lw")],
              1, 12, 0.3, 0.9, [1, 3, 6, 9, 12], [0.3, 0.5, 0.7, 0.9], "month after launch", "AUC", "The same model, never retrained", legend_y=200, legend_x=90)
    CAPS["data-vs-concept-drift"] = (f"A loan model in two simulated worlds. When incomes fall by 18 over the year (data drift), its AUC stays between {min(data_d):.2f} and {max(data_d):.2f}, because the "
                                    f"rule linking income to risk still holds. When the effect of income reverses (concept drift), the AUC falls to {concept_d[-1]:.2f}, worse than guessing.")
    return svg(640, 290, s, "Line chart: AUC stays high under data drift but collapses under concept drift")

# 3 ---- Q-learning vs SARSA routes (Lesson 31)
def fig_cliff():
    R, C, start, goal = 4, 8, (3, 0), (3, 7)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    def env(s, a):
        i, j = min(max(s[0] + moves[a][0], 0), R - 1), min(max(s[1] + moves[a][1], 0), C - 1)
        return (start, -100) if (i == 3 and 0 < j < 7) else ((i, j), -1)
    rng = np.random.default_rng(0)
    def train(method):
        Q = np.zeros((R, C, 4)); pick = lambda s: rng.integers(4) if rng.random() < 0.1 else int(Q[s].argmax())
        for _ in range(500):
            s = start; a = pick(s)
            for _ in range(200):
                s2, r = env(s, a); a2 = pick(s2)
                nxt = 0 if s2 == goal else (Q[s2].max() if method == "Q" else Q[s2][a2])
                Q[s][a] += 0.5 * (r + nxt - Q[s][a]); s, a = s2, a2
                if s == goal: break
        s, path = start, [start]
        for _ in range(40):
            s, _ = env(s, int(Q[s].argmax())); path.append(s)
            if s == goal: break
        return path
    cw, ox, oy = 60, 80, 40
    s = T(320, 18, "Greedy routes after learning on the cliff", "t h", "c")
    for i in range(R):
        for j in range(C):
            cliff = i == 3 and 0 < j < 7
            s += f'<rect x="{ox + j * cw}" y="{oy + i * cw}" width="{cw - 2}" height="{cw - 2}" class="{"wc3" if cliff else "ax"}" opacity="{0.5 if cliff else 1}"' + ('' if cliff else ' fill="none"') + '/>'
    s += T(ox + 4 * cw, oy + 3 * cw + 35, "cliff (−100)", "t s", "c") + T(ox + 30, oy + 4 * cw + 14, "start", "t s", "c") + T(ox + 7 * cw + 30, oy + 4 * cw + 14, "goal", "t s", "c")
    paths = {}
    for method, cls, off in [("Q", "la", -6), ("SARSA", "lv", 6)]:
        p = train(method); paths[method] = p
        s += '<polyline points="' + " ".join(f"{ox + j * cw + cw / 2 + off:.1f},{oy + i * cw + cw / 2 + off:.1f}" for i, j in p) + f'" class="{cls}" fill="none"/>'
    s += '<line x1="80" y1="306" x2="102" y2="306" class="la"/>' + T(108, 310, f"Q-learning ({len(paths['Q']) - 1} steps, along the edge)", "t s")
    s += '<line x1="350" y1="306" x2="372" y2="306" class="lv"/>' + T(378, 310, f"SARSA ({len(paths['SARSA']) - 1} steps, away from the edge)", "t s")
    CAPS["q-learning-vs-sarsa"] = (f"Both agents explore 10% of the time while learning. Q-learning learns the shortest route ({len(paths['Q']) - 1} steps) right along the cliff; "
                                  f"SARSA, which accounts for its own random steps, learns a safer {len(paths['SARSA']) - 1}-step route further away.")
    return svg(640, 320, s, "Grid with a cliff: Q-learning's route hugs the cliff edge, SARSA's route stays further away")

# 4 ---- Kaplan–Meier vs naive handling of censoring (Lesson 33)
def fig_km():
    rng = np.random.default_rng(4); n = 800
    t = rng.exponential(8, n); c = rng.uniform(2, 16, n)
    obs, ev = np.minimum(t, c), (t <= c).astype(int)
    grid = np.linspace(0, 16, 81)
    def km(tt, ee):
        out, s = [], 1.0; times = np.unique(tt[ee == 1]); vals = []
        for u in times: s *= 1 - ((tt == u) & (ee == 1)).sum() / (tt >= u).sum(); vals.append(s)
        return [vals[np.searchsorted(times, g, side="right") - 1] if g >= times[0] else 1.0 for g in grid]
    true = np.exp(-grid / 8)
    as_events = [(obs > g).mean() for g in grid]
    dropped = [(obs[ev == 1] > g).mean() for g in grid]
    s = lines([("true survival", grid, true, "dash2"), ("Kaplan–Meier", grid, km(obs, ev), "la"), ("censored counted as churned", grid, as_events, "lw"), ("censored dropped", grid, dropped, "lv")],
              0, 16, 0, 1, [0, 4, 8, 12, 16], [0, 0.25, 0.5, 0.75, 1], "months", "share still subscribed", "Survival curves from the same censored data", legend_y=40)
    CAPS["kaplan-meier-vs-naive"] = (f"800 simulated subscribers, {100 * (1 - ev.mean()):.0f}% of them censored. Kaplan–Meier follows the true curve. Counting censored customers as churners, or dropping them, "
                                    "both make customers look as if they leave much sooner.")
    return svg(640, 290, s, "Line chart: Kaplan–Meier matches the true survival curve; naive treatments of censoring fall far below it")

# 5 ---- random labelling vs active learning vs self-training (Lesson 32)
def fig_labels():
    X, y = load_digits(return_X_y=True); X = X / 16
    pool, test = np.arange(1200), np.arange(1200, len(y))
    budgets = [30, 60, 90, 120, 150, 180]
    def acc(idx): return LogisticRegression(max_iter=2000).fit(X[idx], y[idx]).score(X[test], y[test])
    rand, act = [], []
    for b in budgets:
        rand.append(np.mean([acc(np.random.default_rng(s).choice(pool, b, replace=False)) for s in range(3)]))
        res = []
        for s in range(3):
            r = np.random.default_rng(s); lab = list(r.choice(pool, 20, replace=False))
            while len(lab) < b:
                m = LogisticRegression(max_iter=2000).fit(X[lab], y[lab]); rest = np.setdiff1d(pool, lab)
                P = np.sort(m.predict_proba(X[rest]), axis=1); lab += list(rest[np.argsort(P[:, -1] - P[:, -2])[:min(10, b - len(lab))]])
            res.append(acc(lab))
        act.append(np.mean(res))
    s = lines([("random labels", budgets, rand, "lw"), ("active learning (uncertainty)", budgets, act, "la")],
              30, 180, 0.6, 1.0, [30, 60, 90, 120, 150, 180], [0.6, 0.7, 0.8, 0.9, 1.0], "labels paid for", "test accuracy", "Handwritten digits: accuracy per label", legend_y=200)
    CAPS["semi-supervised-vs-active"] = (f"With 60 labels, random labelling reaches {rand[1]:.3f} and active learning {act[1]:.3f}; with 180, {rand[-1]:.3f} against {act[-1]:.3f}. "
                                        "Active learning spends each label where the model is least sure. Semi-supervised learning instead squeezes more from the labels you already have.")
    return svg(640, 290, s, "Line chart: active learning reaches higher accuracy than random labelling for the same number of labels")

FIGS = {"observational-vs-randomised": fig_causal(), "data-vs-concept-drift": fig_drift(), "q-learning-vs-sarsa": fig_cliff(),
        "kaplan-meier-vs-naive": fig_km(), "semi-supervised-vs-active": fig_labels()}

COMPARE2 = [
 ("observational-vs-randomised", "Randomised experiment vs observational adjustment",
  "Both estimate what an action causes. A randomised experiment lets a coin decide who is treated, so the groups are alike in everything. Observational methods adjust for the differences you measured, and are only as good as that list.",
  ("Randomised experiment (A/B test)", "Observational adjustment (regression, propensity scores)"),
  [("Who decides treatment", "A random process", "People, policies or the past"),
   ("Hidden confounders", "Balanced automatically", "Bias the estimate if not measured"),
   ("Main assumption", "Randomisation done properly; no interference", "No unmeasured confounding, and overlap"),
   ("Cost and speed", "Needs time, traffic and permission to experiment", "Uses data you already have"),
   ("Strength of evidence", "The gold standard", "Weaker; support it with sensitivity analysis"),
   ("Other designs", "Bandits when you also want to earn while learning", "Difference-in-differences, regression discontinuity")],
  "you can randomise and the decision is important enough to wait for an experiment.",
  "randomising is impossible, unethical or too slow, and you can measure the main confounders.",
  [29, 4]),
 ("data-vs-concept-drift", "Data drift vs concept drift",
  "Both mean the world has changed since training. Data drift changes the inputs; concept drift changes the relationship between inputs and outcome, which is what actually breaks a model.",
  ("Data drift", "Concept drift"),
  [("What changes", "The distribution of the inputs", "How the inputs relate to the outcome"),
   ("Example", "Applicants' incomes fall in a recession", "The same income now means a different risk"),
   ("Detected by", "Comparing input distributions (PSI, KS test), right away", "Performance on new labelled outcomes, after a delay"),
   ("Does it hurt performance?", "Sometimes; only if the model extrapolates badly", "Almost always"),
   ("Typical fix", "Check performance; retrain if it dropped", "Retrain on recent data, sometimes redesign features")],
  "you want an early warning: monitor input drift continuously.",
  "you want to know if the model still works: monitor performance as outcomes arrive.",
  [30]),
 ("q-learning-vs-sarsa", "Q-learning vs SARSA",
  "Two ways to learn action values from experience. Q-learning learns about the best possible next action; SARSA learns about the action it will actually take, including its own random exploration.",
  ("Q-learning", "SARSA"),
  [("Update target", "$r + \\gamma \\max_{a'} Q(s', a')$", "$r + \\gamma Q(s', a')$, using the action actually taken"),
   ("Type", "Off-policy", "On-policy"),
   ("Learns", "The optimal policy, assuming no more exploration", "The best policy given that it keeps exploring"),
   ("Near danger", "Bold: takes the shortest route", "Cautious: keeps a safety margin"),
   ("Reward while learning", "Lower when exploration is risky", "Higher when exploration is risky"),
   ("Can learn from old data", "Yes (replay, logged data)", "Not easily")],
  "exploration will stop once learning ends, or you want to reuse logged experience.",
  "mistakes during learning are costly and the agent will keep exploring.",
  [31]),
 ("kaplan-meier-vs-naive", "Kaplan–Meier vs ignoring censoring",
  "Time-to-event data always has people whose event hasn't happened yet. Kaplan–Meier uses each person for exactly as long as they were watched; naive approaches count them as events or throw them away.",
  ("Kaplan–Meier", "Naive (drop censored, or count them as events)"),
  [("Censored people", "Count while observed, then leave the risk set", "Dropped, or wrongly counted as churned"),
   ("Bias", "None if censoring is unrelated to the event", "Survival looks much shorter than it is"),
   ("Uses all the data", "Yes", "No, or uses it wrongly"),
   ("Summary", "Median survival, survival at fixed times", "A misleading average time"),
   ("Extends to", "Log-rank test, Cox model, survival forests", "Nothing reliable")],
  "any data where some subjects haven't had the event yet — almost always.",
  "never, unless everyone has been followed until the event happened.",
  [33]),
 ("semi-supervised-vs-active", "Semi-supervised vs active learning",
  "Both help when labels are expensive. Semi-supervised learning uses the unlabelled data itself to train a better model; active learning chooses which unlabelled examples a person should label next.",
  ("Semi-supervised learning", "Active learning"),
  [("Needs a person?", "No, after the first labels", "Yes, every round"),
   ("Uses unlabelled data to", "Train, through pseudo-labels or a similarity graph", "Choose what to label"),
   ("Main risk", "Learning its own mistakes when assumptions fail", "Picking odd outliers; labelling delays"),
   ("Best when", "Nearby points really share labels", "Labels are costly but available on request"),
   ("Methods", "Self-training, label spreading", "Uncertainty sampling, query-by-committee")],
  "you can't get more labels, but the data has clear structure.",
  "you can ask an expert for labels and want each one to count.",
  [32]),
 ("collaborative-vs-content", "Collaborative filtering vs content-based recommendation",
  "Two ways to suggest items. Collaborative filtering learns from patterns of what people interacted with; content-based recommendation compares items' own features.",
  ("Collaborative filtering", "Content-based"),
  [("Uses", "The user–item interaction matrix", "Item features: text, category, price, attributes"),
   ("New items", "Can't recommend them yet (cold start)", "Can recommend them immediately"),
   ("Surprising suggestions", "Yes — finds tastes no feature describes", "Rarely — suggests similar things"),
   ("Data needed", "Many interactions", "Good item descriptions"),
   ("Main risk", "Popularity bias and feedback loops", "Narrow, repetitive suggestions"),
   ("Methods", "Item–item neighbours, matrix factorisation", "TF-IDF and cosine similarity, feature embeddings")],
  "you have lots of interaction history and want suggestions beyond the obvious.",
  "items are new or interactions are scarce. Most real systems combine both.",
  [27]),
]
SEE_ALSO2 = {27: ["collaborative-vs-content"], 29: ["observational-vs-randomised"], 30: ["data-vs-concept-drift"], 31: ["q-learning-vs-sarsa"],
             32: ["semi-supervised-vs-active"], 33: ["kaplan-meier-vs-naive"]}

if __name__ == "__main__":
    for k, v in CAPS.items(): print(k, "|", v)
