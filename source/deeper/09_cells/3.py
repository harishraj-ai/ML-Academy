# Choosing the threshold from costs: a missed cancer (false negative) costs 20, a false alarm costs 1
y_bad = 1 - yte                            # in this dataset 0 = malignant, so flip: 1 = malignant
p_bad = 1 - p_lr
for t in [0.5, 0.2, 0.1, 0.05]:
    flag = p_bad >= t
    fn, fp = np.sum(~flag & (y_bad == 1)), np.sum(flag & (y_bad == 0))
    print(f"threshold {t:4.2f}: missed {fn:2d}, false alarms {fp:2d}, total cost {20 * fn + fp}")
print("theory: flag when p is above cost_FP / (cost_FP + cost_FN), which is", round(1 / 21, 3))
