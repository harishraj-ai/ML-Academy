import numpy as np
# Cliff walking: a 4×8 grid; the bottom row between start and goal is a cliff (−100, back to start).
R, C = 4, 8
start, goal = (3, 0), (3, 7)
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
def env(s, a):
    i, j = min(max(s[0] + moves[a][0], 0), R - 1), min(max(s[1] + moves[a][1], 0), C - 1)
    if i == 3 and 0 < j < 7: return start, -100
    return (i, j), -1
rng = np.random.default_rng(0)
def train(method, episodes=500, alpha=0.5, eps=0.1):
    Q = np.zeros((R, C, 4))
    pick = lambda s: rng.integers(4) if rng.random() < eps else int(Q[s].argmax())
    for _ in range(episodes):
        s = start; a = pick(s)
        for t in range(200):
            s2, r = env(s, a); a2 = pick(s2)
            nxt = 0 if s2 == goal else (Q[s2].max() if method == "Q" else Q[s2][a2])
            Q[s][a] += alpha * (r + nxt - Q[s][a]); s, a = s2, a2
            if s == goal: break
    return Q
def route(Q):
    s, path = start, [start]
    for _ in range(40):
        s, _ = env(s, int(Q[s].argmax())); path.append(s)
        if s == goal: break
    return path
for method in ["Q", "SARSA"]:
    p = route(train(method))
    edge = sum(1 for c in p if c[0] == 2)                  # steps right next to the cliff
    print(f"{method:5s}: greedy route length {len(p) - 1}, steps along the cliff edge {edge}")
