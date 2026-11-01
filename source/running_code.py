# Code for the running example ("Chennai Homes"), one snippet per lesson.
# Every snippet starts by loading the CSV so it runs on its own.
LOAD = 'import pandas as pd\nimport numpy as np\ndf = pd.read_csv("houses.csv")   # download it from Lesson 1\n'

CODE = {
 1: LOAD + '''print(df.shape)                       # rows = houses, columns = facts about each house
print(df[["area", "size_m2", "dist_km", "price_lakh", "sold_fast"]].head(3))
print("average price:", round(df["price_lakh"].mean(), 1), "lakh")''',
 2: LOAD + '''X = df[["size_m2", "bedrooms", "dist_km", "age_yrs"]].to_numpy()
print(X.shape)                                   # 12 houses x 4 features
a, b = X[0], X[1]                                # house 1 and house 2 as vectors
print(a, b, round(np.linalg.norm(a - b), 2))     # their Euclidean distance
w = np.array([0.6, 2.0, -1.2, -0.5])             # some made-up weights
print((X @ w)[:3].round(1))                      # predictions for the first 3 houses''',
 3: LOAD + '''x, y = df["size_m2"].to_numpy(), df["price_lakh"].to_numpy()
def loss(w):            # MSE for the model price = w * size
    return np.mean((w * x - y) ** 2)
def grad(w):            # dL/dw = (2/n) * sum((w*x - y) * x)
    return 2 * np.mean((w * x - y) * x)
for w in [0.4, 0.65, 0.9]:
    print(w, round(loss(w), 1), round(grad(w), 1))''',
 4: LOAD + '''p = df["price_lakh"]
print("mean", round(p.mean(), 2), "std", round(p.std(ddof=0), 2))
print("z-score of house 12:", round((96 - p.mean()) / p.std(ddof=0), 2))
print("P(sold fast) =", df["sold_fast"].mean())
central = df[df["area"] == "Central"]
print("P(sold fast | Central) =", central["sold_fast"].mean())
print("P(Central | sold fast) =", round((df[df["sold_fast"] == 1]["area"] == "Central").mean(), 3))''',
 5: LOAD + '''from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
X, y = df[["size_m2"]], df["price_lakh"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
print(len(X_train), "train /", len(X_test), "test houses")
scores = cross_val_score(LinearRegression(), X, y, cv=4, scoring="neg_mean_absolute_error")
print("MAE per fold:", (-scores).round(1), " mean:", round(-scores.mean(), 1))''',
 6: LOAD + '''from sklearn.linear_model import LinearRegression
m1 = LinearRegression().fit(df[["size_m2"]], df["price_lakh"])
print("price = %.3f * size + %.2f" % (m1.coef_[0], m1.intercept_), " R2 =", round(m1.score(df[["size_m2"]], df["price_lakh"]), 3))
cols = ["size_m2", "dist_km", "age_yrs"]
m3 = LinearRegression().fit(df[cols], df["price_lakh"])
print({c: round(float(v), 3) for c, v in zip(cols, m3.coef_)}, round(m3.intercept_, 2), " R2 =", round(m3.score(df[cols], df["price_lakh"]), 3))''',
 7: LOAD + '''x = df["size_m2"].to_numpy(); y = df["price_lakh"].to_numpy()
xs = (x - x.mean()) / x.std()            # standardise so one learning rate suits both parameters
w, b, lr = 0.0, 0.0, 0.1
for step in range(200):
    err = w * xs + b - y
    w -= lr * 2 * np.mean(err * xs)
    b -= lr * 2 * np.mean(err)
print("in standardised units: w =", round(w, 3), " b =", round(b, 3))
print("back in m2: slope =", round(w / x.std(), 3), " intercept =", round(b - w * x.mean() / x.std(), 2))''',
 8: LOAD + '''from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
cols = ["dist_km", "age_yrs"]
clf = make_pipeline(StandardScaler(), LogisticRegression()).fit(df[cols], df["sold_fast"])
print({c: round(float(v), 2) for c, v in zip(cols, clf[-1].coef_[0])})
new = pd.DataFrame({"dist_km": [3, 20], "age_yrs": [5, 25]})
print(clf.predict_proba(new)[:, 1].round(2))      # P(sells fast) for two new houses''',
 9: LOAD + '''from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix, precision_score, recall_score
clf = make_pipeline(StandardScaler(), LogisticRegression())
pred = cross_val_predict(clf, df[["dist_km", "age_yrs"]], df["sold_fast"], cv=4)   # honest predictions
tn, fp, fn, tp = confusion_matrix(df["sold_fast"], pred).ravel()
print("TP", tp, "FP", fp, "FN", fn, "TN", tn)
print("precision", round(precision_score(df["sold_fast"], pred), 2), "recall", round(recall_score(df["sold_fast"], pred), 2))''',
 10: LOAD + '''from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
cols = ["size_m2", "bedrooms", "dist_km", "age_yrs"]
for name, reg in [("OLS", LinearRegression()), ("Ridge a=1", Ridge(alpha=1)), ("Ridge a=10", Ridge(alpha=10))]:
    m = make_pipeline(StandardScaler(), reg).fit(df[cols], df["price_lakh"])
    print(f"{name:11s}", m[-1].coef_.round(2))''',
 11: LOAD + '''from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
cols = ["size_m2", "dist_km", "age_yrs"]
knn = make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=3)).fit(df[cols], df["price_lakh"])
new = pd.DataFrame({"size_m2": [100], "dist_km": [6], "age_yrs": [5]})
dist, idx = knn[-1].kneighbors(knn[0].transform(new))
print("nearest houses:", (df["id"].iloc[idx[0]]).tolist(), "prices:", df["price_lakh"].iloc[idx[0]].tolist())
print("predicted price:", round(knn.predict(new)[0], 1), "lakh")''',
 12: LOAD + '''from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
vec = CountVectorizer()
Xw = vec.fit_transform(df["description"])
nb = MultinomialNB(alpha=1.0).fit(Xw, df["sold_fast"])
for text in ["new flat near metro", "old villa needs renovation", "quiet flat with garden"]:
    print(f"{text:28s} P(sells fast) = {nb.predict_proba(vec.transform([text]))[0, 1]:.2f}")''',
 13: LOAD + '''from sklearn.tree import DecisionTreeClassifier, export_text
cols = ["size_m2", "dist_km", "age_yrs"]
tree = DecisionTreeClassifier(max_depth=2, random_state=0).fit(df[cols], df["sold_fast"])
print(export_text(tree, feature_names=cols))
print("training accuracy:", tree.score(df[cols], df["sold_fast"]))''',
 14: LOAD + '''from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, LeaveOneOut
cols = ["size_m2", "bedrooms", "dist_km", "age_yrs"]
for name, m in [("single tree", DecisionTreeClassifier(random_state=0)),
                ("random forest", RandomForestClassifier(n_estimators=300, random_state=0))]:
    acc = cross_val_score(m, df[cols], df["sold_fast"], cv=LeaveOneOut()).mean()
    print(f"{name:14s} leave-one-out accuracy {acc:.2f}")
rf = RandomForestClassifier(n_estimators=300, random_state=0).fit(df[cols], df["sold_fast"])
print({c: round(float(v), 2) for c, v in zip(cols, rf.feature_importances_)})''',
 15: LOAD + '''from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
cols = ["dist_km", "age_yrs"]
svm = make_pipeline(StandardScaler(), SVC(kernel="linear", C=1.0)).fit(df[cols], df["sold_fast"])
w = svm[-1].coef_[0]
print("margin width (standardised units):", round(2 / np.linalg.norm(w), 2))
print("support vectors: houses", (df["id"].iloc[svm[-1].support_]).tolist())''',
 16: LOAD + '''from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
cols = ["size_m2", "dist_km", "price_lakh"]
Z = StandardScaler().fit_transform(df[cols])
km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(Z)
df["cluster"] = km.labels_
print(df.groupby("cluster")[cols].mean().round(1))
print(pd.crosstab(df["cluster"], df["area"]))''',
 17: LOAD + '''from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
cols = ["size_m2", "bedrooms", "dist_km", "age_yrs"]
pca = PCA().fit(StandardScaler().fit_transform(df[cols]))
print("explained variance ratio:", pca.explained_variance_ratio_.round(3))
print("PC1 weights:", {c: round(float(v), 2) for c, v in zip(cols, pca.components_[0])})''',
 18: LOAD + '''from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, LeaveOneOut
cols = ["size_m2", "dist_km", "age_yrs"]
mlp = make_pipeline(StandardScaler(), MLPClassifier(hidden_layer_sizes=(4,), max_iter=5000, random_state=0))
print("training accuracy:", mlp.fit(df[cols], df["sold_fast"]).score(df[cols], df["sold_fast"]))
print("leave-one-out accuracy:", round(cross_val_score(mlp, df[cols], df["sold_fast"], cv=LeaveOneOut()).mean(), 2))''',
 19: LOAD + '''# A Transformer would read the listing text word by word; here we just look at what it would see.
for d in df["description"].head(3):
    tokens = d.split()
    print(len(tokens), "tokens:", tokens)
print("vocabulary size:", len({w for d in df["description"] for w in d.split()}))''',
 20: LOAD + '''from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score
df.loc[3, "age_yrs"] = np.nan                     # pretend one value is missing
num = ["size_m2", "bedrooms", "dist_km", "age_yrs"]
numeric = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
with_area = ColumnTransformer([("num", numeric, num), ("cat", OneHotEncoder(handle_unknown="ignore"), ["area"])])
numbers_only = ColumnTransformer([("num", numeric, num)])
for name, prep in [("numbers only", numbers_only), ("numbers + area", with_area)]:
    model = Pipeline([("prep", prep), ("ridge", Ridge(alpha=1.0))])
    mae = -cross_val_score(model, df, df["price_lakh"], cv=4, scoring="neg_mean_absolute_error").mean()
    print(f"{name:15s} cross-validated MAE: {mae:.1f} lakh")''',
}
