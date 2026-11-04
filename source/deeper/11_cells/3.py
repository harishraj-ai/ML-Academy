import time
from sklearn.neighbors import NearestNeighbors

data = rng.normal(size=(200000, 3)); queries = rng.normal(size=(2000, 3))
found, times = {}, {}
for algo in ["brute", "kd_tree"]:
    nn = NearestNeighbors(n_neighbors=5, algorithm=algo).fit(data)
    t = time.perf_counter(); found[algo] = nn.kneighbors(queries)[1]; times[algo] = time.perf_counter() - t
print("same neighbours found by both:", np.array_equal(np.sort(found["brute"]), np.sort(found["kd_tree"])))
print("k-d tree faster:", times["kd_tree"] < times["brute"])   # exact timings vary from computer to computer
