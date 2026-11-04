from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression

# Hinge loss and log loss give very similar linear boundaries
Xl, yl = make_moons(n_samples=400, noise=0.3, random_state=1)
svm = LinearSVC(C=1.0).fit(Xl, yl)
lr = LogisticRegression(C=1.0).fit(Xl, yl)
unit = lambda w: w / np.linalg.norm(w)
print("boundary direction, linear SVM:     ", unit(svm.coef_[0]).round(3))
print("boundary direction, logistic regr.: ", unit(lr.coef_[0]).round(3))
print("agreement on predictions:", np.mean(svm.predict(Xl) == lr.predict(Xl)))
