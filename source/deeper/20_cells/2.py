from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge

# One pipeline for mixed data: numbers, a category and free text (Chennai Homes)
df = pd.read_csv("houses.csv")
df.loc[2, "age_yrs"] = np.nan                              # pretend one value is missing
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), ["size_m2", "bedrooms", "dist_km", "age_yrs"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["area"]),
    ("txt", TfidfVectorizer(), "description"),
])
model = make_pipeline(prep, Ridge(alpha=1.0))
scores = cross_val_score(model, df, df["price_lakh"], cv=KFold(4, shuffle=True, random_state=0), scoring="neg_mean_absolute_error")
print("columns after preprocessing:", prep.fit_transform(df).shape[1])
print("4-fold mean absolute error:", round(-scores.mean(), 1), "lakh")
