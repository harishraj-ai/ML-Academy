# Supporting content for Lesson 0 (Python, NumPy & pandas for beginners).
LESSON0 = (0, 0, "Python, NumPy & pandas for Beginners", "Never coded? Learn just enough Python, NumPy and pandas to read and run every example in the course.", 60)
OBJ0 = ["Run Python code in a Jupyter notebook and read its output and error messages",
        "Use variables, numbers, strings, lists and dictionaries, counting positions from 0",
        "Write if-statements, for-loops and simple functions",
        "Do arithmetic on whole NumPy arrays and use shape, axis and boolean filtering",
        "Load, select, filter and summarise a table with pandas"]
SRC0 = [("The Python Tutorial (python.org)", "https://docs.python.org/3/tutorial/index.html"),
        ("NumPy: the absolute basics for beginners", "https://numpy.org/doc/stable/user/absolute_beginners.html"),
        ("pandas: 10 minutes to pandas", "https://pandas.pydata.org/docs/user_guide/10min.html"),
        ("Matplotlib: quick start guide", "https://matplotlib.org/stable/users/explain/quick_start.html"),
        ("Project Jupyter: JupyterLab documentation", "https://jupyterlab.readthedocs.io/en/stable/")]
FIT0 = "This optional lesson comes before everything else. If you can already read basic Python, NumPy and pandas, skip straight to Lesson 1."
FAQ0 = [("Do I have to finish this before Lesson 1?", "No. Lesson 1 has very little code. Many people read Lessons 1–5 first and come back here when the code in later lessons starts to matter."),
        ("Which version of Python?", "Any Python 3 from the last few years (3.9 or newer). Python 2 is obsolete; you won't meet it."),
        ("Can I break my computer by running code?", "Not with anything in this course. The worst that happens is an error message — then you fix the cell and run it again."),
        ("Why do positions start at 0?", "It's a convention most programming languages share: the position is \"how many steps from the start\". You'll stop noticing it within a day or two."),
        ("NumPy or pandas — when do I use which?", "pandas for loading and exploring tables with named columns; NumPy for maths on arrays of numbers. Models in scikit-learn accept either, and <code>df.to_numpy()</code> converts a table into an array.")]
MIST0 = ["Forgetting that positions start at 0, so <code>a[3]</code> is the fourth item and a slice <code>a[1:3]</code> has two items.",
         "Mixing tabs and spaces, or forgetting to indent the lines under <code>if</code>, <code>for</code> or <code>def</code>.",
         "Running notebook cells out of order, so a variable doesn't exist yet (NameError). Restart and run all cells from the top.",
         "Using a plain list where you need a NumPy array: <code>[1, 2] * 2</code> repeats the list, <code>np.array([1, 2]) * 2</code> doubles the numbers.",
         "Writing <code>df[\"price\"] > 80</code> and expecting the rows; you need <code>df[df[\"price\"] > 80]</code>."]
EX0 = [("By hand", "For <code>a = [3, 6, 9, 12, 15]</code>, what are (a) <code>a[-2]</code> and (b) <code>a[1:4]</code>?",
        "(a) <code>a[-2]</code> counts from the end: the second-to-last item, <strong>12</strong>. (b) Positions 1, 2 and 3 (the stop position 4 is excluded): <strong>[6, 9, 12]</strong>."),
       ("By hand", "<code>X = np.array([[1, 2, 3], [4, 5, 6]])</code>. Give <code>X.shape</code>, <code>X.sum(axis=0)</code> and <code>X[:, 1]</code>.",
        "Two rows and three columns: shape <strong>(2, 3)</strong>. <code>axis=0</code> adds down the rows, one total per column: <strong>[5, 7, 9]</strong>. <code>X[:, 1]</code> is every row, column 1 (the second column): <strong>[2, 5]</strong>."),
       ("Code", "Load <code>houses.csv</code> with pandas. How many houses cost more than 80 lakh, and what is the average price of the houses that sold fast (<code>sold_fast == 1</code>)?",
        "<pre><code>df = pd.read_csv(\"houses.csv\")\nprint((df[\"price_lakh\"] &gt; 80).sum())                    # 5\nprint(df[df[\"sold_fast\"] == 1][\"price_lakh\"].mean())    # 75.1666...</code></pre>Summing a True/False column counts the Trues. <strong>5</strong> houses, and the fast sellers average about <strong>75.17</strong> lakh."),
       ("Code", "Write a function <code>celsius_to_f(c)</code> that returns <code>c × 9/5 + 32</code>. What does <code>celsius_to_f(37)</code> return?",
        "<pre><code>def celsius_to_f(c):\n    return c * 9 / 5 + 32\n\nprint(celsius_to_f(37))   # 98.6</code></pre>Body temperature, <strong>98.6</strong> °F.")]
CHECKS0 = {(0, 0): [("(a) a[-2]", 12, "Negative positions count from the end: −1 is the last item."), ("(b) a[1:4]", [6, 9, 12], "From position 1 up to, but not including, position 4.")],
           (0, 1): [("X.shape", [2, 3], "Rows first, then columns. Type it as 2, 3."), ("X.sum(axis=0)", [5, 7, 9], "Add down each column."), ("X[:, 1]", [2, 5], "Every row, column 1 — the second column.")],
           (0, 2): [("Houses over 80 lakh", 5, "Filter with df[\"price_lakh\"] > 80, then count."), ("Average price of fast sellers", 75.1667, "df[df[\"sold_fast\"] == 1][\"price_lakh\"].mean().")],
           (0, 3): [("celsius_to_f(37)", 98.6, "37 × 9 / 5 + 32.")]}
CHAL0 = [("Average with a loop", "Use a for-loop to add up the prices, then divide by how many there are.",
          "prices = [58, 82, 55, 88, 96]\ntotal = 0\nfor p in prices:\n    total = total + p\n##BLANK##", "average", "average = total / len(prices)", "Divide the total by len(prices)."),
         ("Filter a table", "Keep only the Central houses from the Chennai Homes data.",
          "import pandas as pd\ndf = pd.read_csv(\"../data/houses.csv\")\n##BLANK##\nn_central = len(central)", "n_central", "central = df[df[\"area\"] == \"Central\"]", "Put the condition df[\"area\"] == \"Central\" inside df[...].",
          "central = df  # ← replace: keep only rows where area is Central")]
