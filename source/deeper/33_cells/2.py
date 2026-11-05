def km_curve(tt, ee):
    times, s, at, out = np.sort(np.unique(tt[ee == 1])), 1.0, None, []
    for u in times:
        s *= 1 - ((tt == u) & (ee == 1)).sum() / (tt >= u).sum(); out.append((u, s))
    return out
def rmst(curve, horizon):
    area, prev_t, prev_s = 0.0, 0.0, 1.0
    for u, s in curve:
        if u > horizon: break
        area += prev_s * (u - prev_t); prev_t, prev_s = u, s
    return area + prev_s * (horizon - prev_t)
for grp in [0, 1]:
    print(f"group {grp}: restricted mean survival over 12 months {rmst(km_curve(t[g == grp], e[g == grp]), 12):.2f} months")
