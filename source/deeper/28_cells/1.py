from scipy import stats
for visitors, conv in [(50, 3), (500, 30), (5000, 300)]:
    row = []
    for name, a, b in [("flat", 1, 1), ("sceptical", 10, 190), ("optimistic", 30, 170)]:
        post = stats.beta(a + conv, b + visitors - conv)
        row.append(f"{name} {post.mean():.3f}")
    print(f"{visitors:5d} visitors (6% converted):", "   ".join(row))
