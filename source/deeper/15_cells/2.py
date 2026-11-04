from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

X, y = make_moons(n_samples=400, noise=0.3, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.5, random_state=0)
print("    C   gamma   support vectors   train   test")
for C in [0.1, 1, 100]:
    for gamma in [0.1, 1, 30]:
        m = SVC(C=C, gamma=gamma).fit(Xtr, ytr)
        print(f"{C:5} {gamma:7}   {m.n_support_.sum():15d}   {m.score(Xtr, ytr):5.3f}   {m.score(Xte, yte):5.3f}")
