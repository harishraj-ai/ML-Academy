import pandas as pd

df = pd.read_csv("houses.csv")
all3 = pd.get_dummies(df["area"], dtype=float)           # Central, Outskirts, Suburb
A = np.column_stack([np.ones(len(df)), df["size_m2"], all3])
print("columns:", A.shape[1], " independent columns (rank):", np.linalg.matrix_rank(A))

Xd = pd.get_dummies(df[["size_m2", "area"]], columns=["area"], drop_first=True, dtype=float)
m = LinearRegression().fit(Xd, df["price_lakh"])
for name, wt in zip(Xd.columns, m.coef_):
    print(f"{name:15}{wt:7.2f}")
print(f"{'bias':15}{m.intercept_:7.2f}")
