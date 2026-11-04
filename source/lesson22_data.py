# Lesson 22: SQL & Data Wrangling for ML. Patches the shared per-lesson dictionaries on import.
import context, extras_ex_b, checks, running_code, running_text, challenges, reference, understanding, rai

L22 = (22, 5, "SQL & Data Wrangling for ML", "Pull training data out of databases: SELECT, GROUP BY, joins, window functions, pandas equivalents and point-in-time features.", 60)

OBJ22 = ["Write SELECT queries with WHERE, GROUP BY, HAVING and ORDER BY, and run them from Python",
         "Choose between INNER and LEFT joins and avoid the row-explosion trap",
         "Use window functions to add context features such as rank within a group",
         "Build a training table that uses only information available at prediction time"]

SRC22 = [("SQLite — SQL language reference (the database built into Python)", "https://www.sqlite.org/lang.html"),
         ("Python documentation — sqlite3 module", "https://docs.python.org/3/library/sqlite3.html"),
         ("pandas — Comparison with SQL", "https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html"),
         ("pandas — Merge, join, concatenate and compare", "https://pandas.pydata.org/docs/user_guide/merging.html"),
         ("SQLite — Window functions", "https://www.sqlite.org/windowfunctions.html"),
         ("Kaufman et al. (2012) — Leakage in Data Mining: Formulation, Detection, and Avoidance", "https://dl.acm.org/doi/10.1145/2382577.2382579")]

context.DEPS[22] = [5, 20]
context.REFRESH[22] = "Training tables are built by joining and summarising database tables, using LEFT joins and only data from before each row's prediction time."
context.FIT[22] = "Starts Part 6 by stepping back to where data really comes from. It turns the leakage rules from Lesson 5 and the pipelines of Lesson 20 into habits for pulling data out of databases."
context.USE[22] = (["Building customer, transaction and event features for churn, fraud and recommendation models",
                    "Data-science and ML-engineering interviews, which nearly always include SQL",
                    "Feature pipelines and feature stores in production systems"],
                   "Whenever your data lives in a database or arrives as several related tables.",
                   "the data already arrives as a single clean table and is small enough to handle in pandas.")
context.FAQ[22] = [
    ("SQL or pandas: which should I learn?",
     "Both. SQL is how you get data out of databases, often after the database has done most of the work on millions of rows; pandas is where you finish, explore and model. The operations map one to one."),
    ("Which database should I practise on?",
     "SQLite comes with Python and needs no setup, so it's ideal for learning. The core SQL in this lesson works almost unchanged in PostgreSQL, MySQL, BigQuery and Snowflake; they differ mainly in dates and special functions."),
    ("Why does my join have more rows than I expected?",
     "A join returns one row for every matching pair. If the right table has several rows per key, each left row is repeated. Aggregate the many side first, or check that the key is unique with COUNT(DISTINCT ...)."),
    ("What's the difference between COUNT(*) and COUNT(column)?",
     "COUNT(*) counts rows; COUNT(column) counts rows where that column isn't NULL. After a LEFT JOIN, count a column from the right table to get 0 for unmatched rows."),
]
understanding.MYTHS[22] = [
    ("Data preparation is a boring step before the real ML work.", "It decides what the model can learn. Wrong joins, dropped rows and leaked future information cause more failed projects than model choice does."),
    ("An INNER JOIN is the default and is always safe.", "It silently drops every entity without a match, which can remove exactly the unusual cases a model most needs to see."),
    ("If the feature exists in the database, the model can use it.", "Only if it was known at prediction time. A value updated after the outcome is leakage, however innocent it looks."),
]
extras_ex_b.MISTAKES[22] = [
    "Using an INNER JOIN and losing every customer who had no events.",
    "Averaging after a one-to-many join, so entities with many events count many times.",
    "Writing <code>WHERE x = NULL</code> instead of <code>WHERE x IS NULL</code>.",
    "Computing features from the whole history, including events after the prediction date.",
    "Not checking that keys are unique before joining.",
]
extras_ex_b.EX[22] = [
    ("By hand", "An orders table has 6 rows: customer A spent 20 and 30, customer B spent 50, and customer C spent 10, 15 and 5. What does <code>SELECT customer, COUNT(*), SUM(amount) FROM orders GROUP BY customer HAVING SUM(amount) &gt; 40</code> return?",
     "Totals: A = 50 (2 orders), B = 50 (1 order), C = 30 (3 orders). HAVING keeps sums above 40: A (2, 50) and B (1, 50). C is dropped."),
    ("By hand", "Customers: 10 rows. Orders: 25 rows, belonging to 6 of the customers. How many rows do <code>customers INNER JOIN orders</code> and <code>customers LEFT JOIN orders</code> return?",
     "Inner: one row per order that matches a customer, so 25. Left: the 25 matched rows plus one row for each of the 4 customers without orders, so 29."),
    ("By hand", "Prices in one area are 60, 80 and 100. What value does <code>price - AVG(price) OVER (PARTITION BY area)</code> give for each house?",
     "The area average is 80, so the values are −20, 0 and +20."),
    ("Concepts", "You're building a churn model. Each customer's prediction date is the first day of the month. Which of these features leak: (a) number of logins in the previous 30 days, (b) total refunds this year, (c) whether the customer's account was closed?",
     "(a) is fine if counted strictly before the prediction date. (b) leaks if \"this year\" includes days after the prediction date: count only up to the cut-off. (c) is essentially the outcome itself, so it's pure leakage."),
    ("Code", "In the lesson's database, write a query that returns each area with its number of houses that had at least one viewing.",
     "<code>SELECT h.area, COUNT(DISTINCT v.house_id) FROM houses h JOIN viewings v ON v.house_id = h.id GROUP BY h.area</code> gives Central 3, Outskirts 1 and Suburb 3. <code>DISTINCT</code> stops houses with several viewings from counting more than once."),
]
checks.CHECKS[(22, 0)] = [("Customers returned", 2, "Only totals above 40 survive HAVING.")]
checks.CHECKS[(22, 1)] = [("Inner join rows", 25, "Each order matches exactly one customer."), ("Left join rows", 29, "Add one row for each customer without orders.")]
checks.CHECKS[(22, 2)] = [("Values for the three houses", [-20, 0, 20], "Subtract the area average from each price.")]
checks.CHECKS[(22, 4)] = [("Central", 3, "Count distinct viewed houses in Central."), ("Outskirts", 1, "Only house 8."), ("Suburb", 3, "Houses 4, 5 and 12.")]

running_code.CODE[22] = '''import sqlite3
import pandas as pd
df = pd.read_csv("houses.csv")   # download it from Lesson 1
con = sqlite3.connect(":memory:")
df.to_sql("houses", con, index=False)
q = """SELECT area, COUNT(*) AS homes, SUM(sold_fast) AS sold_fast,
              ROUND(AVG(sold_fast), 2) AS fast_rate, ROUND(AVG(price_lakh), 1) AS avg_price
       FROM houses GROUP BY area ORDER BY fast_rate DESC"""
print(pd.read_sql(q, con))'''
running_text.INTRO[22] = ("The Chennai Homes table becomes a database table. One GROUP BY gives the fast-sale rate per area: "
    "3 of 4 Central homes sold fast (0.75), 3 of 5 Suburb homes (0.60) and none of the 3 Outskirts homes. "
    "A per-group rate like this is a useful feature, but compute it from training folds only, or it leaks the target (Lesson 20's \"Going deeper\").")

challenges.C[22] = [
    ("Average price per area with SQL", "Complete the query so it returns the average price of each area.",
     'import sqlite3\nimport pandas as pd\ncon = sqlite3.connect(":memory:")\npd.DataFrame({"area": ["A", "A", "B", "B", "B"], "price": [10, 20, 30, 40, 50]}).to_sql("t", con, index=False)\n##BLANK##\nresult = pd.read_sql(q, con)["avg_price"].round(2).tolist()',
     'result', 'q = "SELECT area, AVG(price) AS avg_price FROM t GROUP BY area ORDER BY area"', "SELECT the area and AVG(price) AS avg_price, then GROUP BY area (and ORDER BY area).",
     'q = "SELECT area, price AS avg_price FROM t"  # ← replace with a GROUP BY query'),
    ("A left join in pandas", "Merge the counts onto every customer, keeping customers with no orders, and fill their count with 0.",
     'import pandas as pd\ncustomers = pd.DataFrame({"id": [1, 2, 3, 4]})\norders = pd.DataFrame({"customer_id": [1, 1, 3]})\ncounts = orders.groupby("customer_id").size().rename("n").reset_index()\n##BLANK##\nresult = merged["n"].tolist()',
     'result', 'merged = customers.merge(counts, left_on="id", right_on="customer_id", how="left").fillna({"n": 0})', "Use how=\"left\" and fill missing counts with 0.",
     'merged = customers.merge(counts, left_on="id", right_on="customer_id")  # ← keep every customer'),
]

reference.GLOSSARY += [
    ("Primary key", "A column (or set of columns) whose value uniquely identifies each row of a table.", 22, "tables"),
    ("Foreign key", "A column that refers to the primary key of another table, linking the two.", 22, "tables"),
    ("LEFT JOIN", "A join that keeps every row of the left table and fills the right table's columns with NULL where there is no match.", 22, "joins"),
    ("Window function", "A SQL function computed over related rows (a window) without collapsing them, written with OVER (PARTITION BY … ORDER BY …).", 22, "window"),
    ("Point-in-time correctness", "Building every feature only from data that existed before the moment each prediction would have been made, to avoid leakage.", 22, "pit"),
]

rai.RAI[22] = ("Data minimisation",
    "<p>Pulling data is the moment to ask whether you need each column at all. Join and keep only what the model needs, avoid copying personal data into notebooks and spreadsheets, and respect the purpose it was collected for. Data-protection laws such as the GDPR and India's DPDP Act make purpose limitation and minimisation legal duties, not just good practice.</p>")
