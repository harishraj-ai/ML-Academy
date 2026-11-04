# Lesson 22 · Going deeper — quiz, interview questions, exercises and the Simple-mode summary.

SIMPLE = ("How indexes make queries fast (and how to check with a query plan), how NULL really behaves in SQL "
          "(comparisons with it are 'unknown'), and how to build rolling time-window features such as "
          "'views in the last 7 days' with window frames, without leaking the current day.")

QUIZ = [
    ("What does an index on <code>viewings(house_id)</code> let the database do?",
     [("a", "Jump straight to a house's rows instead of scanning the whole table"), ("b", "Store the table twice"), ("c", "Remove duplicate rows")], "a",
     "A B-tree index finds matching rows in about log n steps."),
    ("A column has values 10, NULL, 0, NULL. How many rows does <code>WHERE NOT (x &gt; 5)</code> return?",
     [("a", "3"), ("b", "1"), ("c", "2")], "b",
     "Only the 0 row. For NULL rows, x &gt; 5 is unknown and so is its negation, and WHERE keeps only true conditions."),
    ("What is <code>AVG(x)</code> for the values 10, NULL, 0, NULL?",
     [("a", "2.5"), ("b", "5"), ("c", "NULL")], "b",
     "Aggregates skip NULLs: the average of 10 and 0 is 5."),
    ("A prediction for day d is made at the start of day d. Which frame avoids leakage in a 7-day sum?",
     [("a", "ROWS BETWEEN 6 PRECEDING AND CURRENT ROW"), ("b", "ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING"), ("c", "ROWS BETWEEN CURRENT ROW AND 6 FOLLOWING")], "b",
     "The window must end before the current day, whose data isn't known yet."),
    ("Why might <code>ROWS BETWEEN 6 PRECEDING AND CURRENT ROW</code> not give a 7-day window?",
     [("a", "If some days have no row, it covers more than 7 calendar days"), ("b", "ROWS always means 7 days"), ("c", "It includes future rows")], "a",
     "ROWS counts rows. Fill in missing days, or use a RANGE frame on a numeric day column."),
]

IQ = [
    (2, "A query on a large table is slow. What do you check first?",
     "Jumping straight to buying a bigger machine.",
     "Read the query plan (EXPLAIN): is it scanning the whole table? Check that filter and join columns are indexed (or, in a warehouse, that you filter on the partition column), that you select only the needed columns, and that joins aren't exploding rows. Filter early, aggregate before joining, and avoid functions on indexed columns in WHERE, which can stop the index being used."),
    (3, "Explain how NULL behaves in comparisons, NOT, COUNT and AVG.",
     "Treating NULL like zero or like false.",
     "NULL is unknown, so any comparison with it (=, &lt;, &gt;) is unknown, and NOT unknown is still unknown; WHERE keeps only true rows, so NULL rows vanish from both a condition and its negation. Use IS NULL. COUNT(*) counts rows, COUNT(col) counts non-NULLs, and AVG/SUM ignore NULLs. NULL in an IN list or a NOT IN subquery can make NOT IN return no rows at all."),
    (3, "How would you compute \"purchases in the previous 30 days\" for every customer-day without leakage?",
     "Using a window that includes the current day.",
     "Build a daily table per customer (filling days with no purchases), then use a window frame that ends before the current row, e.g. <code>SUM(purchases) OVER (PARTITION BY customer ORDER BY day ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING)</code>, or a RANGE frame on dates. Validate on a time-based split. The same logic must run identically in training and in production, which is what feature stores provide."),
]

EX = [
    ("Intermediate", "Daily views are 2, 0, 5, 1, 3 for days 1–5. Using a frame that ends at the previous row and covers 3 rows (<code>ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING</code>), what is the feature for day 5?",
     "Days 2, 3 and 4: $0 + 5 + 1 = 6$."),
    ("Intermediate", "A column holds 4, NULL, 6, NULL, 8. What are <code>COUNT(*)</code>, <code>COUNT(x)</code> and <code>AVG(x)</code>?",
     "COUNT(*) = 5, COUNT(x) = 3, AVG(x) = $(4 + 6 + 8)/3 = 6$."),
    ("Intermediate", "Roughly how many steps does a balanced B-tree lookup need on 1,000,000 rows if each node has 100 children? Compare with a full scan.",
     "About $\\log_{100} 10^6 = 3$ levels, so 3 node reads, against 1,000,000 rows for a scan."),
]

CHECKS = {
    0: [("Feature for day 5", 6, "Add the views of days 2, 3 and 4.")],
    1: [("COUNT(*), COUNT(x), AVG(x)", [5, 3, 6], "NULLs are counted by COUNT(*) only.")],
    2: [("Levels", 3, "log base 100 of a million.")],
}
