def run_returns(method, episodes=500, eps=0.1):
    Q, total = np.zeros((R, C, 4)), []
    for _ in range(episodes):
        s, G = start, 0
        a = rng.integers(4) if rng.random() < eps else int(Q[s].argmax())
        for t in range(200):
            s2, r = env(s, a); G += r
            a2 = rng.integers(4) if rng.random() < eps else int(Q[s2].argmax())
            nxt = 0 if s2 == goal else (Q[s2].max() if method == "Q" else Q[s2][a2])
            Q[s][a] += 0.5 * (r + nxt - Q[s][a]); s, a = s2, a2
            if s == goal: break
        total.append(G)
    return np.mean(total[-200:])
q_ret = np.mean([run_returns("Q") for _ in range(5)]); s_ret = np.mean([run_returns("SARSA") for _ in range(5)])
print("average return while still exploring: Q-learning", round(q_ret, 1), "  SARSA", round(s_ret, 1))
