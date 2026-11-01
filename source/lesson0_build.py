"""Builds lessons/00.html (Lesson 0: Python, NumPy & pandas) by running every code cell and inserting its real output."""
import os, io, sys, html, contextlib, traceback, shutil, tempfile, base64
import matplotlib
matplotlib.use("Agg")
HERE = os.path.dirname(os.path.abspath(__file__))
e = html.escape

# ("h2", id, title) | ("p", html) | ("code", src) | ("box", kind, title, html) | ("error", src) | ("plot", src, caption)
S = [
 ("h2", "why", "Why Python — and how to use this lesson"),
 ("p", "Every lesson in this course has Python code. If you've never programmed, this lesson gives you exactly enough to read and run it: about an hour, no prior experience needed. You will learn the core of the language, then the two libraries that machine learning in Python is built on: <strong>NumPy</strong> for numbers in bulk and <strong>pandas</strong> for tables."),
 ("p", "Python is popular for machine learning because it reads almost like English, and because the best ML libraries (scikit-learn, PyTorch, TensorFlow) use it. You don't need to memorise anything here — come back whenever a later lesson's code looks unfamiliar."),
 ("box", "tip", "Learn by running", "Each code box below is followed by the <strong>output</strong> Python actually printed. The best way to learn is to type the code yourself in the Lesson 0 notebook, run it, then change something and run it again."),
 ("h2", "run", "Running Python code"),
 ("p", "Follow the <a href=\"index.html#setup\">Setup</a> instructions once: they install Python and <strong>JupyterLab</strong>, a notebook that runs in your browser. A notebook is a list of <em>cells</em>. Type code in a cell and press <strong>Shift+Enter</strong>: the code runs and its output appears underneath. Download this lesson's notebook with the button at the top of the page."),
 ("p", "The simplest program prints a message:"),
 ("code", 'print("Hello, machine learning!")'),
 ("p", "<code>print</code> is a <em>function</em>: you give it something in brackets and it shows it. Text goes inside quotes. Anything after a <code>#</code> is a <em>comment</em> — a note for humans that Python ignores."),
 ("h2", "values", "Values, variables and arithmetic"),
 ("p", "A <strong>variable</strong> is a name for a value. The <code>=</code> sign means \"store this value under this name\" (it is not the maths equals)."),
 ("code", "price = 72.5        # a decimal number (a float)\nbedrooms = 3        # a whole number (an int)\ncity = \"Chennai\"     # text (a string)\nprint(price, bedrooms, city)"),
 ("p", "Arithmetic works like a calculator. <code>**</code> means \"to the power of\", <code>/</code> always gives a decimal, and <code>//</code> divides and drops the remainder."),
 ("code", "print(7 + 2, 7 - 2, 7 * 2, 7 / 2)\nprint(7 // 2, 7 % 2, 2 ** 10)\narea = 12.5 * 8     # a variable can hold the result of a calculation\nprint(area)"),
 ("p", "You can change a variable at any time; the new value replaces the old one:"),
 ("code", "count = 1\ncount = count + 1   # take the old value, add 1, store it back\ncount += 1          # a shorter way to write the same thing\nprint(count)"),
 ("h2", "text", "Text and printing"),
 ("p", "Text values are called <strong>strings</strong>. An <em>f-string</em> (a string with <code>f</code> before the quote) lets you drop variables into text with curly brackets, and <code>:.2f</code> rounds a number to 2 decimal places:"),
 ("code", "name = \"house 7\"\nprice = 84.1234\nprint(f\"{name} costs {price:.2f} lakh\")\nprint(name.upper(), len(name))   # a method, and the length of the string"),
 ("h2", "lists", "Lists and indexing"),
 ("p", "A <strong>list</strong> holds several values in order, inside square brackets. Positions are counted from <strong>0</strong>, not 1 — the first item is <code>[0]</code>. Negative positions count from the end."),
 ("code", "prices = [58, 82, 55, 88, 96]\nprint(prices[0], prices[1], prices[-1])   # first, second, last\nprint(len(prices))                          # how many items"),
 ("p", "A <strong>slice</strong> <code>[start:stop]</code> takes items from <code>start</code> up to <em>but not including</em> <code>stop</code>:"),
 ("code", "print(prices[1:3])     # items at positions 1 and 2\nprint(prices[:2])      # the first two\nprint(prices[2:])      # from position 2 to the end\nprices.append(61)      # add an item at the end\nprint(prices)"),
 ("box", "warn", "The off-by-one trap", "<code>prices[1:3]</code> has <em>two</em> items (positions 1 and 2), and the last item of a 5-item list is <code>prices[4]</code> — <code>prices[5]</code> is an error. Almost every beginner trips on this; it soon becomes natural."),
 ("h2", "dicts", "Dictionaries"),
 ("p", "A <strong>dictionary</strong> stores values under names (<em>keys</em>) instead of positions — like a row of a table:"),
 ("code", "house = {\"area\": \"Central\", \"size_m2\": 120, \"price_lakh\": 88}\nprint(house[\"size_m2\"])\nhouse[\"sold_fast\"] = True     # add a new key\nprint(house)"),
 ("h2", "control", "Making decisions and repeating: if and for"),
 ("p", "<code>if</code> runs code only when a condition is true. The indented lines (4 spaces) belong to it — in Python, <strong>indentation is part of the syntax</strong>."),
 ("code", "price = 96\nif price > 90:\n    print(\"expensive\")\nelif price > 60:\n    print(\"mid-range\")\nelse:\n    print(\"affordable\")"),
 ("p", "A <code>for</code> loop repeats its indented block once for each item:"),
 ("code", "prices = [58, 82, 55, 88]\ntotal = 0\nfor p in prices:\n    total = total + p\nprint(\"total:\", total, \" average:\", total / len(prices))"),
 ("p", "<code>range(n)</code> gives the numbers 0 to n−1, handy for repeating something n times. A <strong>list comprehension</strong> builds a new list from an old one in one line:"),
 ("code", "for step in range(3):\n    print(\"step\", step)\nsquares = [x ** 2 for x in [1, 2, 3, 4]]\nprint(squares)"),
 ("h2", "functions", "Functions"),
 ("p", "A <strong>function</strong> packages code under a name so you can reuse it. <code>def</code> defines it, the brackets list its inputs, and <code>return</code> sends back the result. This one is the mean squared error from Lesson 1:"),
 ("code", "def mse(y_true, y_pred):\n    total = 0\n    for t, p in zip(y_true, y_pred):   # zip walks through both lists together\n        total += (p - t) ** 2\n    return total / len(y_true)\n\nprint(mse([3, 5, 7], [2.5, 5, 8]))"),
 ("h2", "imports", "Libraries and import"),
 ("p", "Python's real power is its libraries. <code>import</code> loads one; <code>as</code> gives it a short nickname. These three lines start almost every notebook in this course:"),
 ("code", "import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\nprint(\"NumPy\", np.__version__, \"and pandas\", pd.__version__, \"loaded\")"),
 ("h2", "numpy", "NumPy: numbers in bulk"),
 ("p", "A NumPy <strong>array</strong> is like a list of numbers, but arithmetic applies to <em>every element at once</em> — no loop needed. This is called <strong>vectorisation</strong>, and it's both shorter and much faster."),
 ("code", "x = np.array([1.0, 2.0, 3.0, 4.0])\nprint(x * 2)          # every element doubled\nprint(x + 10)\nprint(x ** 2)\nprint(x.mean(), x.sum(), x.max())"),
 ("p", "Arrays can have two dimensions — rows and columns, like a table of examples × features. <code>.shape</code> tells you the size, and <code>axis=0</code> means \"down the rows\" (one result per column):"),
 ("code", "X = np.array([[120, 3, 4.0],\n              [ 95, 2, 6.5],\n              [150, 4, 12.0]])   # 3 houses × 3 features\nprint(X.shape)\nprint(X[0])           # the first row (house 1)\nprint(X[:, 0])        # the first column (sizes)\nprint(X.mean(axis=0)) # the average of each column"),
 ("p", "Comparisons give arrays of True/False, which you can use to <strong>filter</strong>. And <code>@</code> multiplies a matrix by a vector — the dot product of each row with the weights (Lesson 2):"),
 ("code", "sizes = X[:, 0]\nprint(sizes > 100)\nprint(sizes[sizes > 100])\nw = np.array([0.5, 2.0, -1.0])\nprint(X @ w)          # one prediction per house"),
 ("h2", "pandas", "pandas: tables of data"),
 ("p", "pandas works with <strong>DataFrames</strong> — tables with named columns, like a spreadsheet. Let's load the course's running example, 12 houses in Chennai (<code>houses.csv</code>, in the <code>data</code> folder):"),
 ("code", "df = pd.read_csv(\"houses.csv\")\nprint(df.shape)                # (rows, columns)\nprint(df.columns.tolist())"),
 ("code", "print(df[[\"area\", \"size_m2\", \"price_lakh\"]].head(4))   # the first 4 rows of three columns"),
 ("p", "Select one column with <code>df[\"name\"]</code> (it behaves like a NumPy array) and filter rows with a condition in square brackets:"),
 ("code", "print(df[\"price_lakh\"].mean())\nbig = df[df[\"size_m2\"] > 120]\nprint(len(big), \"houses over 120 m²\")\nprint(big[[\"id\", \"size_m2\", \"price_lakh\"]])"),
 ("p", "<code>groupby</code> summarises by category, and you can create new columns from old ones:"),
 ("code", "print(df.groupby(\"area\")[\"price_lakh\"].mean().round(1))\ndf[\"price_per_m2\"] = df[\"price_lakh\"] / df[\"size_m2\"]\nprint(df.sort_values(\"price_per_m2\", ascending=False)[[\"id\", \"area\", \"price_per_m2\"]].head(3).round(3))"),
 ("h2", "plotting", "A first plot"),
 ("p", "matplotlib draws charts. A scatter plot of price against size is the first thing you'd look at before fitting a model (Lesson 6):"),
 ("plot", "plt.figure(figsize=(5, 3.2))\nplt.scatter(df[\"size_m2\"], df[\"price_lakh\"])\nplt.xlabel(\"size (m²)\")\nplt.ylabel(\"price (lakh)\")\nplt.title(\"Chennai Homes\")\nplt.show()", "The plot this code draws: bigger houses tend to cost more, but with plenty of scatter — distance and age matter too."),
 ("h2", "errors", "Reading error messages"),
 ("p", "Errors are normal — professionals see them all day. Python stops and prints a <em>traceback</em>; the <strong>last line</strong> says what went wrong. Here are the ones you'll meet most, with the real messages:"),
 ("error", "print(prise)"),
 ("p", "<strong>NameError</strong>: a typo, or a variable used before the cell that creates it was run. In notebooks, run cells from the top."),
 ("error", "\"Price: \" + 72"),
 ("p", "<strong>TypeError</strong>: mixing types that don't go together. Fix: <code>\"Price: \" + str(72)</code>, or an f-string."),
 ("error", "prices = [58, 82, 55]\nprices[3]"),
 ("p", "<strong>IndexError</strong>: counting from 1 instead of 0 — the last of 3 items is <code>prices[2]</code>."),
 ("error", "np.array([1, 2, 3]) + np.array([1, 2])"),
 ("p", "<strong>ValueError</strong> (a shape mismatch): element-by-element arithmetic needs arrays of the same size. Print <code>.shape</code> to check — the single most useful debugging habit in machine learning."),
 ("box", "tip", "When you're stuck", "Read the last line of the error, then the line of your code it points to. Check spelling, brackets, quotes and indentation. Restart the notebook and run all cells from the top. Searching the exact error message online almost always finds an answer."),
 ("h2", "summary", "Key takeaways"),
 ("p", "<ul><li>Variables name values: numbers, strings, lists (positions from 0) and dictionaries (named keys).</li><li><code>if</code> decides, <code>for</code> repeats, <code>def</code> packages code into functions — and indentation marks which lines belong together.</li><li>NumPy arrays do arithmetic on every element at once; <code>.shape</code>, <code>axis=</code>, boolean filtering and <code>@</code> are the tools you'll use most.</li><li>pandas DataFrames are tables: <code>read_csv</code>, <code>df[\"col\"]</code>, <code>df[condition]</code>, <code>groupby</code> and new columns cover most everyday work.</li><li>Errors are information: read the last line first.</li></ul>"),
 ("quiz", None),
]

QUIZ = [
 ("What does <code>[10, 20, 30, 40][1]</code> give?", ["10", "20", "30"], 1, "Positions start at 0, so position 1 is the second item, 20."),
 ("What does <code>[10, 20, 30, 40][1:3]</code> give?", ["[20, 30]", "[10, 20, 30]", "[20, 30, 40]"], 0, "A slice runs from the start position up to, but not including, the stop position: positions 1 and 2."),
 ("<code>x = np.array([1, 2, 3])</code>. What is <code>x * 2</code>?", ["[1, 2, 3, 1, 2, 3]", "[2, 4, 6]", "An error"], 1, "NumPy applies arithmetic to every element. (With a plain Python list, <code>* 2</code> would repeat the list instead.)"),
 ("A NumPy array has shape <code>(100, 5)</code>. What does <code>X.mean(axis=0)</code> return?", ["One number", "100 numbers (one per row)", "5 numbers (one per column)"], 2, "<code>axis=0</code> averages down the rows, giving one result per column — here, the average of each of the 5 features."),
 ("Which line keeps only the rows of a DataFrame where the price is above 80?", ["<code>df[\"price\"] > 80</code>", "<code>df[df[\"price\"] > 80]</code>", "<code>df.price(80)</code>"], 1, "The comparison makes a True/False column; putting it inside <code>df[...]</code> keeps the True rows. The first option only gives the True/False values."),
]

def run_all():
    ns = {"__name__": "__main__"}
    out_html = []
    plot_png = None
    cwd = os.getcwd()
    tmp = tempfile.mkdtemp()
    shutil.copy(os.path.join(HERE, "data", "houses.csv"), os.path.join(tmp, "houses.csv"))
    os.chdir(tmp)
    try:
        for item in S:
            k = item[0]
            if k == "h2": out_html.append(f'<h2 id="{item[1]}">{e(item[2])}</h2>')
            elif k == "p": out_html.append(item[1] if item[1].startswith("<ul") else f"<p>{item[1]}</p>")
            elif k == "box": out_html.append(f'<div class="box {item[1]}"><div class="box-title">{item[2]}</div><p>{item[3]}</p></div>')
            elif k in ("code", "plot"):
                buf = io.StringIO()
                src = item[1]
                with contextlib.redirect_stdout(buf):
                    exec(src.replace("plt.show()", "") if k == "plot" else src, ns)
                out_html.append(f"<pre><code>{e(src)}</code></pre>")
                if k == "plot":
                    import matplotlib.pyplot as plt
                    b = io.BytesIO(); plt.savefig(b, format="png", dpi=110, bbox_inches="tight"); plt.close("all")
                    plot_png = base64.b64encode(b.getvalue()).decode()
                    out_html.append(f'<figure class="fig"><img src="data:image/png;base64,{plot_png}" alt="Scatter plot of price in lakh against size in square metres for the 12 Chennai houses" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#fff;border-radius:8px"><figcaption>{e(item[2])}</figcaption></figure>')
                elif buf.getvalue().strip():
                    out_html.append(f'<p class="run-out-label">Output:</p><pre class="output"><code>{e(buf.getvalue().rstrip())}</code></pre>')
            elif k == "error":
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        exec(item[1], ns)
                    raise SystemExit("expected an error: " + item[1])
                except Exception as ex:
                    msg = f"{type(ex).__name__}: {ex}"
                out_html.append(f"<pre class=\"errcode\"><code>{e(item[1])}</code></pre><p class=\"run-out-label\">Error:</p><pre class=\"output err\"><code>{e(msg)}</code></pre>")
            elif k == "quiz":
                q = '<h2 id="quiz">Check your understanding</h2>\n<div class="quiz">\n'
                for i, (qt, opts, c, ex) in enumerate(QUIZ):
                    q += f'<div class="q" data-correct="{"abc"[c]}"><p class="q-text">{i+1}. {qt}</p>\n' + "".join(f'<button data-opt="{"abc"[j]}">{o}</button>' for j, o in enumerate(opts)) + f'\n<div class="q-explain">{ex}</div></div>\n'
                out_html.append(q + "</div>")
    finally:
        os.chdir(cwd); shutil.rmtree(tmp)
    return "\n".join(out_html), ns

if __name__ == "__main__":
    body, ns = run_all()
    open(os.path.join(HERE, "lessons", "00.html"), "w").write(body + "\n")
    import pandas as pd
    df = pd.read_csv(os.path.join(HERE, "data", "houses.csv"))
    print("written", len(body), "chars; houses >80 lakh:", int((df.price_lakh > 80).sum()), "; >120 m2:", int((df.size_m2 > 120).sum()))
