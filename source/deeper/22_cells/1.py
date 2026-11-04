import sqlite3
import numpy as np
import pandas as pd

# A bigger events table: 200,000 viewings of 5,000 houses
rng = np.random.default_rng(0)
con = sqlite3.connect(":memory:")
pd.DataFrame({"house_id": rng.integers(1, 5001, 200000), "day": rng.integers(1, 366, 200000)}).to_sql("viewings", con, index=False)
q = "SELECT COUNT(*) FROM viewings WHERE house_id = 42"
print("plan without an index:", con.execute("EXPLAIN QUERY PLAN " + q).fetchall()[0][-1])
con.execute("CREATE INDEX idx_house ON viewings(house_id)")
print("plan with an index:   ", con.execute("EXPLAIN QUERY PLAN " + q).fetchall()[0][-1])
print("viewings of house 42:", con.execute(q).fetchone()[0])
