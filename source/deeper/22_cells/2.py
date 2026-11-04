# NULL is "unknown": comparisons with it are neither true nor false
t = pd.DataFrame({"id": [1, 2, 3, 4], "discount": [10, None, 0, None]})
t.to_sql("t", con, index=False)
conds = {"discount > 5": "discount > 5", "NOT (discount > 5)": "NOT (discount > 5)",
         "discount equals NULL": "discount = NULL", "discount IS NULL": "discount IS NULL"}
for label, cond in conds.items():
    print(f"{label:21} -> rows {[r[0] for r in con.execute(f'SELECT id FROM t WHERE {cond}')]}")
print("COUNT(*), COUNT(discount), AVG(discount):", con.execute("SELECT COUNT(*), COUNT(discount), AVG(discount) FROM t").fetchone())
