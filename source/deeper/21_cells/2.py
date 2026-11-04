# Equalise true-positive rates with group-specific thresholds, and see what it costs
def rates(score, y, t):
    flag = score >= t
    return flag[y == 1].mean(), flag[y == 0].mean(), (flag == y).mean()

sA, yA = groups["group A"]; sB, yB = groups["group B"]
target_tpr = rates(sB, yB, 0.5)[0]
ts = np.linspace(0.05, 0.95, 181)
tA = ts[np.argmin([abs(rates(sA, yA, t)[0] - target_tpr) for t in ts])]
for name, t_A in [("one threshold 0.5 for both", 0.5), (f"threshold {tA:.3f} for group A", tA)]:
    tprA, fprA, accA = rates(sA, yA, t_A); tprB, fprB, accB = rates(sB, yB, 0.5)
    print(f"{name:28}: TPR A {tprA:.3f} / B {tprB:.3f}   FPR A {fprA:.3f} / B {fprB:.3f}   accuracy A {accA:.3f}")
