/* ML Academy — answer checking and randomised practice problems */
(function () {
  "use strict";
  // ---------- parsing & comparing answers ----------
  function parseNum(s) {
    s = String(s).trim().replace(/−/g, "-").replace(/\s+/g, "");
    if (!s) return NaN;
    var pct = /%$/.test(s); if (pct) s = s.slice(0, -1);
    s = s.replace(/,(?=\d{3}(\D|$))/g, "");            // thousands separators: 2,432
    var v;
    if (/^-?\d*\.?\d+\/-?\d*\.?\d+$/.test(s)) { var p = s.split("/"); v = parseFloat(p[0]) / parseFloat(p[1]); }
    else if (/^-?\d*\.?\d+(e-?\d+)?$/i.test(s)) v = parseFloat(s);
    else return NaN;
    return pct ? v / 100 : v;
  }
  function parseVec(s) {
    var parts = String(s).replace(/[()\[\]{}]/g, " ").replace(/−/g, "-").split(/[;,\s]+/).filter(Boolean);
    return parts.map(parseNum);
  }
  function close(got, want, tol) {
    if (isNaN(got)) return false;
    if (tol == null) tol = Number.isInteger(want) ? 1e-9 : Math.max(0.01 * Math.abs(want), 0.0006);
    return Math.abs(got - want) <= tol + 1e-12;
  }
  function judge(input, want, tol) {
    if (Array.isArray(want)) {
      var v = parseVec(input);
      if (v.length !== want.length) return { ok: false, why: "Expected " + want.length + " numbers, separated by commas." };
      return { ok: v.every(function (x, i) { return close(x, want[i], tol); }) };
    }
    var g = parseNum(input);
    if (isNaN(g)) return { ok: false, why: "Type a number, e.g. 0.75, 3/4 or 75%." };
    return { ok: close(g, want, tol) };
  }
  function store(key, ok) {
    try { var d = JSON.parse(localStorage.getItem("mla-ex") || "{}"); var r = d[key] || { tries: 0, ok: false };
      r.tries++; r.ok = r.ok || ok; r.last = ok; r.t = Date.now(); d[key] = r; localStorage.setItem("mla-ex", JSON.stringify(d)); } catch (e) { /* ignore */ }
  }
  function math(el) {
    if (typeof renderMathInElement === "function") renderMathInElement(el, { delimiters: [{ left: "$$", right: "$$", display: true }, { left: "$", right: "$", display: false }], throwOnError: false });
  }
  function wireChecker(box, key, getFields, onDone) {
    var btn = box.querySelector(".chk-btn"), hint = box.querySelector(".chk-hint");
    function run() {
      var fields = getFields(), all = true, msgs = [];
      box.querySelectorAll(".chk-row").forEach(function (row, i) {
        var f = fields[i], inp = row.querySelector("input"), res = row.querySelector(".chk-res");
        if (!inp.value.trim()) { res.textContent = ""; row.classList.remove("ok", "bad"); all = false; return; }
        var r = judge(inp.value, f.ans, f.tol);
        row.classList.toggle("ok", r.ok); row.classList.toggle("bad", !r.ok);
        res.textContent = r.ok ? "✓ Correct" : "✗ Not quite";
        if (!r.ok) { all = false; msgs.push((r.why ? r.why + " " : "") + (f.hint ? "Hint for “" + f.label + "”: " + f.hint : "")); }
      });
      var anyFilled = Array.prototype.some.call(box.querySelectorAll(".chk-row input"), function (x) { return x.value.trim(); });
      if (!anyFilled) { hint.textContent = "Type your answer(s) first."; hint.className = "chk-hint"; return; }
      if (all) { hint.textContent = "All correct — well done! Open the solution to compare your working."; hint.className = "chk-hint good"; }
      else { hint.textContent = msgs.filter(Boolean).join("  ") || "Fill in every box."; hint.className = "chk-hint warn"; }
      store(key, all);
      if (onDone) onDone(all);
    }
    btn.addEventListener("click", run);
    box.addEventListener("keydown", function (e) { if (e.key === "Enter" && e.target.tagName === "INPUT") { e.preventDefault(); run(); } });
  }

  // ---------- random helpers ----------
  function rng(seed) {
    var s = seed == null ? Math.floor(Math.random() * 2147483647) : seed;
    var next = function () { s = (s * 48271) % 2147483647; return (s - 1) / 2147483646; };
    if (seed != null) for (var k = 0; k < 3; k++) next();
    return {
      int: function (a, b) { return a + Math.floor(next() * (b - a + 1)); },
      pick: function (arr) { return arr[Math.floor(next() * arr.length)]; },
      sign: function () { return next() < 0.5 ? -1 : 1; }
    };
  }
  function r(x, d) { var f = Math.pow(10, d == null ? 3 : d); return Math.round(x * f) / f; }
  function f(x, d) { var v = r(x, d); return (v < 0 ? "-" : "") + Math.abs(v); }   // for maths
  function sum(a) { return a.reduce(function (s, x) { return s + x; }, 0); }
  function mean(a) { return sum(a) / a.length; }
  function pstd(a) { var m = mean(a); return Math.sqrt(mean(a.map(function (x) { return (x - m) * (x - m); }))); }
  function sig(z) { return 1 / (1 + Math.exp(-z)); }

  // ---------- generators: each returns {q, fields:[{label, ans, tol?, hint}], sol, params} ----------
  var G = {};
  G[0] = { title: "List positions and slices", make: function (R) {
    var a = [0, 0, 0, 0, 0, 0].map(function () { return R.int(1, 30); }), i = R.int(0, 5), k = R.int(1, 3), st = R.int(0, 3), en = R.int(st + 2, 6);
    var sl = a.slice(st, en), sm = sum(sl);
    return { params: { a: a, i: i, k: k, st: st, en: en }, q: "<code>a = [" + a.join(", ") + "]</code>. What are <code>a[" + i + "]</code>, <code>a[-" + k + "]</code> and <code>sum(a[" + st + ":" + en + "])</code>?",
      fields: [{ label: "a[" + i + "]", ans: a[i], hint: "Positions start at 0." }, { label: "a[-" + k + "]", ans: a[a.length - k], hint: "Negative positions count from the end: −1 is the last item." },
               { label: "sum(a[" + st + ":" + en + "])", ans: sm, hint: "The slice runs from position " + st + " up to, but not including, position " + en + "." }],
      sol: "<code>a[" + i + "]</code> = " + a[i] + " (item " + (i + 1) + " counting from 1). <code>a[-" + k + "]</code> = " + a[a.length - k] + ". <code>a[" + st + ":" + en + "]</code> = [" + sl.join(", ") + "], whose sum is " + sm + "." }; } };
  G[1] = { title: "Mean squared error", make: function (R) {
    var y = [R.int(2, 9), R.int(2, 9), R.int(2, 9)], e = [R.int(-3, 3), R.int(-3, 3), R.int(-3, 3)];
    if (e.every(function (x) { return x === 0; })) e[0] = 2;
    var yh = y.map(function (v, i) { return v + e[i]; }), m = mean(e.map(function (x) { return x * x; }));
    return { params: { y: y, yh: yh }, q: "True values $y = " + y.join(", ") + "$; predictions $\\hat y = " + yh.join(", ") + "$. Compute the MSE.",
      fields: [{ label: "MSE", ans: m, hint: "Errors are ŷ − y. Square each one, then average." }],
      sol: "Errors $" + e.join(",\\ ") + "$; squared $" + e.map(function (x) { return x * x; }).join(",\\ ") + "$. MSE $= " + sum(e.map(function (x) { return x * x; })) + "/3 \\approx " + f(m) + "$." }; } };
  G[2] = { title: "Dot product and length", make: function (R) {
    var a = [R.int(-4, 5), R.int(-4, 5), R.int(-4, 5)], b = [R.int(-4, 5), R.int(-4, 5), R.int(-4, 5)];
    var Q = R.pick([[1, 2, 2, 3], [2, 3, 6, 7], [1, 4, 8, 9], [4, 4, 7, 9], [2, 6, 9, 11], [2, 10, 11, 15]]);
    var v = [Q[0] * R.sign(), Q[1] * R.sign(), Q[2] * R.sign()], d = a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
    return { params: { a: a, b: b, v: v }, q: "Compute $\\mathbf a\\cdot\\mathbf b$ for $\\mathbf a = (" + a.join(", ") + ")$, $\\mathbf b = (" + b.join(", ") + ")$, and the length of $\\mathbf v = (" + v.join(", ") + ")$.",
      fields: [{ label: "a · b", ans: d, hint: "Multiply matching components, then add." }, { label: "‖v‖", ans: Q[3], hint: "Square each component, add, take the square root." }],
      sol: "$\\mathbf a\\cdot\\mathbf b = " + a.map(function (x, i) { return "(" + x + ")(" + b[i] + ")"; }).join(" + ") + " = " + d + "$. $\\ \\|\\mathbf v\\| = \\sqrt{" + v.map(function (x) { return x * x; }).join(" + ") + "} = \\sqrt{" + Q[3] * Q[3] + "} = " + Q[3] + "$." }; } };
  G[3] = { title: "Slope of a parabola", make: function (R) {
    var a = R.pick([1, 2, 3, -1, -2, 4]), b = R.int(-6, 6), c = R.int(-5, 5), x = R.int(-3, 4), s = 2 * a * x + b;
    return { params: { a: a, b: b, x: x }, q: "For $f(x) = " + (a === 1 ? "" : a === -1 ? "-" : a) + "x^2 " + (b < 0 ? "- " + (-b) : "+ " + b) + "x " + (c < 0 ? "- " + (-c) : "+ " + c) + "$, what is the slope $f'(x)$ at $x = " + x + "$?",
      fields: [{ label: "f′(" + x + ")", ans: s, hint: "The derivative of ax² + bx + c is 2ax + b." }],
      sol: "$f'(x) = " + 2 * a + "x " + (b < 0 ? "- " + (-b) : "+ " + b) + "$. At $x = " + x + "$: $" + 2 * a + "\\times(" + x + ") + (" + b + ") = " + s + "$." }; } };
  G[4] = { title: "Bayes' rule: a medical test", make: function (R) {
    var p = R.pick([0.01, 0.02, 0.05, 0.1, 0.2]), se = R.pick([0.8, 0.9, 0.95, 0.99]), fp = R.pick([0.02, 0.05, 0.1]);
    var ev = se * p + fp * (1 - p), post = se * p / ev;
    return { params: { p: p, se: se, fp: fp }, q: "A disease affects " + r(p * 100, 2) + "% of people. A test detects it " + r(se * 100, 2) + "% of the time, and gives a false positive " + r(fp * 100, 2) + "% of the time for healthy people. Someone tests positive. What is $P(\\text{disease}\\mid +)$?",
      fields: [{ label: "P(disease | positive)", ans: post, hint: "P(+) = P(+|disease)P(disease) + P(+|healthy)P(healthy). Then divide." }],
      sol: "$P(+) = " + se + "\\times" + p + " + " + fp + "\\times" + r(1 - p, 2) + " = " + f(ev, 4) + "$. $P(\\text{disease}\\mid +) = " + f(se * p, 4) + "/" + f(ev, 4) + " \\approx " + f(post) + "$." }; } };
  G[5] = { title: "Cross-validation summary", make: function (R) {
    var s = [0, 0, 0, 0, 0].map(function () { return R.int(60, 90) / 100; }), m = mean(s), sd = pstd(s);
    return { params: { s: s }, q: "5-fold accuracies: $" + s.join(",\\ ") + "$. Report the mean and the standard deviation (divide by $n$).",
      fields: [{ label: "Mean", ans: m, hint: "Add the five and divide by 5." }, { label: "Standard deviation", ans: sd, tol: 0.0006, hint: "Average the squared deviations from the mean, then take the square root. Give 3–4 decimals." }],
      sol: "Mean $= " + r(sum(s), 2) + "/5 = " + f(m, 3) + "$. Squared deviations average to $" + f(sd * sd, 5) + "$, so the standard deviation is $\\sqrt{" + f(sd * sd, 5) + "} \\approx " + f(sd, 4) + "$." }; } };
  G[6] = { title: "Least-squares line through three points", make: function (R) {
    var y = [R.int(1, 6), R.int(2, 8), R.int(3, 10)], w = (y[2] - y[0]) / 2, yb = mean(y), b = yb - 2 * w;
    return { params: { y: y }, q: "Fit $\\hat y = wx + b$ to $(1, " + y[0] + "), (2, " + y[1] + "), (3, " + y[2] + ")$.",
      fields: [{ label: "w", ans: w, hint: "x̄ = 2, so w = Σ(x − 2)(y − ȳ) / Σ(x − 2)² = (y₃ − y₁)/2 here." }, { label: "b", ans: b, hint: "b = ȳ − w·x̄." }],
      sol: "$\\bar x = 2$, $\\bar y = " + f(yb) + "$. $\\sum(x-\\bar x)(y-\\bar y) = (-1)(" + f(y[0] - yb) + ") + 0 + (1)(" + f(y[2] - yb) + ") = " + f(2 * w) + "$, $\\sum(x-\\bar x)^2 = 2$, so $w = " + f(w) + "$ and $b = " + f(yb) + " - " + f(w) + "\\times2 = " + f(b) + "$." }; } };
  G[7] = { title: "Gradient descent by hand", make: function (R) {
    var c = R.int(2, 10), eta = R.pick([0.1, 0.2, 0.25, 0.4]), w1 = 2 * eta * c, w2 = w1 - eta * 2 * (w1 - c);
    return { params: { c: c, eta: eta }, q: "Minimise $L(w) = (w - " + c + ")^2$ from $w = 0$ with $\\eta = " + eta + "$. What is $w$ after two steps?",
      fields: [{ label: "w after step 1", ans: w1, hint: "L′(w) = 2(w − " + c + "). Update w ← w − η L′(w)." }, { label: "w after step 2", ans: w2, hint: "Repeat with the new w." }],
      sol: "Step 1: $L'(0) = " + (-2 * c) + "$, $w = 0 - " + eta + "\\times(" + (-2 * c) + ") = " + f(w1) + "$. Step 2: $L'(" + f(w1) + ") = " + f(2 * (w1 - c)) + "$, $w = " + f(w1) + " - " + eta + "\\times(" + f(2 * (w1 - c)) + ") = " + f(w2) + "$." }; } };
  G[8] = { title: "Logistic regression prediction", make: function (R) {
    var a = R.pick([0.5, 1, 2]), b = -R.int(1, 6), x = R.int(0, 8), z = a * x + b, p = sig(z);
    return { params: { a: a, b: b, x: x }, q: "A model has $z = " + a + "x " + "- " + (-b) + "$. Where is its decision boundary, and what probability does it give at $x = " + x + "$?",
      fields: [{ label: "Boundary x", ans: -b / a, hint: "The boundary is where z = 0." }, { label: "p at x = " + x, ans: p, hint: "Compute z, then p = 1 / (1 + e^(−z))." }],
      sol: "Boundary: $" + a + "x = " + (-b) + "\\Rightarrow x = " + f(-b / a) + "$. At $x = " + x + "$: $z = " + f(z) + "$, $p = \\sigma(" + f(z) + ") \\approx " + f(p) + "$." }; } };
  G[9] = { title: "Precision, recall and F1", make: function (R) {
    var tp = R.int(10, 60), fp = R.int(2, 30), fn = R.int(2, 30), tn = R.int(50, 200), P = tp / (tp + fp), Rc = tp / (tp + fn), F = 2 * P * Rc / (P + Rc);
    return { params: { tp: tp, fp: fp, fn: fn, tn: tn }, q: "TP = " + tp + ", FP = " + fp + ", FN = " + fn + ", TN = " + tn + ". Compute precision, recall and F1.",
      fields: [{ label: "Precision", ans: P, hint: "TP / (TP + FP)." }, { label: "Recall", ans: Rc, hint: "TP / (TP + FN)." }, { label: "F1", ans: F, hint: "2PR / (P + R), or 2TP / (2TP + FP + FN)." }],
      sol: "Precision $= " + tp + "/" + (tp + fp) + " \\approx " + f(P) + "$. Recall $= " + tp + "/" + (tp + fn) + " \\approx " + f(Rc) + "$. F1 $= " + 2 * tp + "/" + (2 * tp + fp + fn) + " \\approx " + f(F) + "$." }; } };
  G[10] = { title: "Ridge shrinkage", make: function (R) {
    var sxy = R.int(10, 80), sxx = R.int(5, 40), l = R.pick([0, 1, 5, 10, 20, 50]), w = sxy / (sxx + l);
    return { params: { sxy: sxy, sxx: sxx, l: l }, q: "One feature, no intercept: $\\sum x_iy_i = " + sxy + "$, $\\sum x_i^2 = " + sxx + "$. What is the ridge weight for $\\lambda = " + l + "$?",
      fields: [{ label: "w", ans: w, hint: "w = Σxy / (Σx² + λ)." }],
      sol: "$w = " + sxy + "/(" + sxx + " + " + l + ") = " + sxy + "/" + (sxx + l) + " \\approx " + f(w) + "$." }; } };
  G[11] = { title: "Distances for kNN", make: function (R) {
    var p = [R.int(-3, 6), R.int(-3, 6)], q = [R.int(-3, 6), R.int(-3, 6)];
    if (p[0] === q[0] && p[1] === q[1]) q[0] += 3;
    var dx = q[0] - p[0], dy = q[1] - p[1], eu = Math.sqrt(dx * dx + dy * dy), ma = Math.abs(dx) + Math.abs(dy);
    return { params: { p: p, q: q }, q: "Distances between $(" + p.join(", ") + ")$ and $(" + q.join(", ") + ")$:",
      fields: [{ label: "Euclidean", ans: eu, hint: "√(Δx² + Δy²)." }, { label: "Manhattan", ans: ma, hint: "|Δx| + |Δy|." }],
      sol: "$\\Delta x = " + dx + "$, $\\Delta y = " + dy + "$. Euclidean $= \\sqrt{" + dx * dx + " + " + dy * dy + "} \\approx " + f(eu) + "$. Manhattan $= " + Math.abs(dx) + " + " + Math.abs(dy) + " = " + ma + "$." }; } };
  G[12] = { title: "Add-one smoothing", make: function (R) {
    var c = R.int(0, 12), N = R.int(40, 300), V = R.pick([50, 100, 200, 500]), p = (c + 1) / (N + V);
    return { params: { c: c, N: N, V: V }, q: "A word appears " + c + " times in the spam training text, which has " + N + " words in total. The vocabulary has " + V + " words. With add-one smoothing, what is $P(\\text{word}\\mid\\text{spam})$?",
      fields: [{ label: "P(word | spam)", ans: p, tol: Math.max(0.01 * p, 0.00005), hint: "(count + 1) / (total + vocabulary size). A fraction is fine." }],
      sol: "$(" + c + " + 1)/(" + N + " + " + V + ") = " + (c + 1) + "/" + (N + V) + " \\approx " + f(p, 5) + "$." }; } };
  G[13] = { title: "Gini impurity and entropy", make: function (R) {
    var a = R.int(1, 9), b = R.int(1, 9), n = a + b, pa = a / n, pb = b / n, g = 1 - pa * pa - pb * pb, H = -(pa * Math.log2(pa) + pb * Math.log2(pb));
    return { params: { a: a, b: b }, q: "A node holds " + a + " examples of class A and " + b + " of class B. Compute its Gini impurity and entropy (bits).",
      fields: [{ label: "Gini", ans: g, hint: "1 − (p_A² + p_B²)." }, { label: "Entropy", ans: H, hint: "−(p_A log₂ p_A + p_B log₂ p_B)." }],
      sol: "$p_A = " + a + "/" + n + "$, $p_B = " + b + "/" + n + "$. Gini $= 1 - (" + f(pa) + "^2 + " + f(pb) + "^2) \\approx " + f(g) + "$. Entropy $\\approx " + f(H) + "$ bits." }; } };
  G[14] = { title: "Majority vote of three models", make: function (R) {
    var p = R.pick([0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]), v = p * p * p + 3 * p * p * (1 - p);
    return { params: { p: p }, q: "Three independent classifiers are each " + r(p * 100) + "% accurate. How accurate is their majority vote?",
      fields: [{ label: "Vote accuracy", ans: v, hint: "P(all 3 right) + P(exactly 2 right) = p³ + 3p²(1 − p)." }],
      sol: "$" + p + "^3 + 3\\times" + p + "^2\\times" + r(1 - p, 2) + " = " + f(p * p * p, 4) + " + " + f(3 * p * p * (1 - p), 4) + " \\approx " + f(v) + "$." }; } };
  G[15] = { title: "SVM margin width", make: function (R) {
    var Q = R.pick([[3, 4, 5], [6, 8, 10], [5, 12, 13], [8, 15, 17], [1, 1, Math.SQRT2], [2, 1, Math.sqrt(5)]]), w = [Q[0] * R.sign(), Q[1] * R.sign()], m = 2 / Q[2];
    return { params: { w: w }, q: "A linear SVM has $\\mathbf w = (" + w.join(", ") + ")$. How wide is its margin?",
      fields: [{ label: "Margin", ans: m, hint: "Margin = 2 / ‖w‖." }],
      sol: "$\\|\\mathbf w\\| = \\sqrt{" + w[0] * w[0] + " + " + w[1] * w[1] + "} \\approx " + f(Q[2]) + "$, so the margin is $2/" + f(Q[2]) + " \\approx " + f(m) + "$." }; } };
  G[16] = { title: "One round of k-means (1D)", make: function (R) {
    var lo = [R.int(1, 3), R.int(3, 5)], hi = [R.int(8, 10), R.int(10, 12), R.int(12, 14)], pts = lo.concat(hi), c = [lo[0], hi[2]];
    var A = pts.filter(function (x) { return Math.abs(x - c[0]) <= Math.abs(x - c[1]); }), B = pts.filter(function (x) { return Math.abs(x - c[0]) > Math.abs(x - c[1]); });
    return { params: { pts: pts, c: c }, q: "Points $" + pts.join(", ") + "$, $k = 2$, starting centroids $" + c[0] + "$ and $" + c[1] + "$. After one assign + update step, where are the centroids?",
      fields: [{ label: "Centroids (smaller, larger)", ans: [mean(A), mean(B)], hint: "Give each point to its nearest centroid, then average each group." }],
      sol: "Assign: $\\{" + A.join(", ") + "\\}$ and $\\{" + B.join(", ") + "\\}$. Update: $" + f(mean(A)) + "$ and $" + f(mean(B)) + "$." }; } };
  G[17] = { title: "Explained variance", make: function (R) {
    var ev = [R.int(6, 12), R.int(3, 6), R.int(1, 3), 1, 1].sort(function (x, y) { return y - x; }), T = sum(ev), cum = 0, k = 0;
    while (cum < 0.9 * T) { cum += ev[k]; k++; }
    return { params: { ev: ev }, q: "PCA eigenvalues: $" + ev.join(", ") + "$. What share of the variance do the first two components explain, and how many are needed for at least 90%?",
      fields: [{ label: "Share of the first two", ans: (ev[0] + ev[1]) / T, hint: "(λ₁ + λ₂) / Σλ." }, { label: "Components for ≥ 90%", ans: k, hint: "Add eigenvalues from the largest until the total reaches 90% of " + T + "." }],
      sol: "Total $= " + T + "$. First two: $" + (ev[0] + ev[1]) + "/" + T + " \\approx " + f((ev[0] + ev[1]) / T) + "$. Running totals: $" + ev.map(function (_, i) { return sum(ev.slice(0, i + 1)); }).join(", ") + "$; 90% of " + T + " is " + f(0.9 * T, 2) + ", reached with " + k + " components." }; } };
  G[18] = { title: "Counting network parameters", make: function (R) {
    var a = R.pick([4, 8, 10, 20, 64]), h1 = R.pick([8, 16, 32, 64]), h2 = R.pick([4, 8, 16]), o = R.pick([1, 2, 3, 10]), n = (a * h1 + h1) + (h1 * h2 + h2) + (h2 * o + o);
    return { params: { a: a, h1: h1, h2: h2, o: o }, q: "How many parameters (weights + biases) has a network with " + a + " inputs, hidden layers of " + h1 + " and " + h2 + " neurons, and " + o + " output" + (o > 1 ? "s" : "") + "?",
      fields: [{ label: "Parameters", ans: n, hint: "Each layer: inputs × outputs + outputs." }],
      sol: "$(" + a + "\\cdot" + h1 + " + " + h1 + ") + (" + h1 + "\\cdot" + h2 + " + " + h2 + ") + (" + h2 + "\\cdot" + o + " + " + o + ") = " + (a * h1 + h1) + " + " + (h1 * h2 + h2) + " + " + (h2 * o + o) + " = " + n + "$." }; } };
  G[19] = { title: "Convolution output size", make: function (R) {
    var k = R.pick([3, 5, 7]), p = R.pick([0, 1, 2]), s = R.pick([1, 2]), out = R.int(6, 30), n = (out - 1) * s + k - 2 * p;
    return { params: { n: n, k: k, p: p, s: s }, q: "Input width " + n + ", kernel " + k + ", padding " + p + ", stride " + s + ". What is the output width?",
      fields: [{ label: "Output width", ans: out, hint: "(n − k + 2p) / s + 1." }],
      sol: "$(" + n + " - " + k + " + 2\\times" + p + ")/" + s + " + 1 = " + (n - k + 2 * p) + "/" + s + " + 1 = " + out + "$." }; } };
  G[20] = { title: "Standardising a new value", make: function (R) {
    var t = [R.int(1, 10) * 10, R.int(1, 10) * 10, R.int(1, 10) * 10]; if (t[0] === t[1] && t[1] === t[2]) t[2] += 20;
    var x = R.int(0, 12) * 10, m = mean(t), sd = pstd(t), z = (x - m) / sd;
    return { params: { t: t, x: x }, q: "Training values of a feature: $" + t.join(", ") + "$. Standardise the new value $" + x + "$ (standard deviation dividing by $n$).",
      fields: [{ label: "z", ans: z, hint: "Use the mean and standard deviation of the training values only: z = (x − mean)/sd." }],
      sol: "Mean $= " + f(m) + "$, standard deviation $= " + f(sd) + "$. $z = (" + x + " - " + f(m) + ")/" + f(sd) + " \\approx " + f(z) + "$." }; } };
  G[21] = { title: "Group rates and the parity ratio", make: function (R) {
    var nA = R.pick([100, 120, 150, 200, 250]), nB = R.pick([80, 100, 120, 150, 200]), aA = Math.round(nA * R.int(30, 60) / 100), aB = Math.round(nB * R.int(10, 45) / 100);
    var sA = aA / nA, sB = aB / nB, ratio = Math.min(sA, sB) / Math.max(sA, sB);
    return { params: { nA: nA, nB: nB, aA: aA, aB: aB }, q: "Group A: " + aA + " of " + nA + " applicants approved. Group B: " + aB + " of " + nB + " approved. Find both selection rates and the demographic-parity ratio (lower ÷ higher).",
      fields: [{ label: "selection rate A", ans: sA, hint: "Approved ÷ group size." }, { label: "selection rate B", ans: sB, hint: "Approved ÷ group size." }, { label: "parity ratio", ans: ratio, hint: "Divide the lower rate by the higher one." }],
      sol: "A: $" + aA + "/" + nA + " \\approx " + f(sA) + "$. B: $" + aB + "/" + nB + " \\approx " + f(sB) + "$. Ratio $\\approx " + f(ratio) + "$ — " + (ratio >= 0.8 ? "at least 0.8, so it passes the four-fifths rule of thumb." : "below 0.8, so it would be flagged for possible adverse impact.") }; } };
  window.MLA_GEN = G; window.MLA_RNG = rng; window.MLA_JUDGE = judge;

  function fieldRows(fields) {
    return fields.map(function (fl, i) { return '<div class="chk-row"><label><span>' + fl.label + '</span><input type="text" inputmode="decimal" autocomplete="off" spellcheck="false" aria-label="' + fl.label + '"></label><span class="chk-res" aria-live="polite"></span></div>'; }).join("");
  }

  document.addEventListener("DOMContentLoaded", function () {
    // static exercises
    document.querySelectorAll(".chk[data-key]").forEach(function (box) {
      var fields = JSON.parse(box.getAttribute("data-fields"));
      wireChecker(box, box.getAttribute("data-key"), function () { return fields; });
    });
    // randomised problems
    document.querySelectorAll(".gen[data-gen]").forEach(function (box) {
      var g = G[box.getAttribute("data-gen")]; if (!g) return;
      var cur, count = 0, solved = 0, stats = box.querySelector(".gen-stats");
      function fresh() {
        cur = g.make(rng());
        box.querySelector(".gen-title").textContent = g.title;
        box.querySelector(".gen-q").innerHTML = cur.q;
        box.querySelector(".gen-fields").innerHTML = fieldRows(cur.fields);
        var sol = box.querySelector(".gen-sol"); sol.innerHTML = cur.sol; sol.hidden = true;
        box.querySelector(".gen-show").textContent = "Show worked solution";
        var h = box.querySelector(".chk-hint"); h.textContent = ""; h.className = "chk-hint";
        count++; math(box); stats.textContent = "Problem " + count + " · solved " + solved;
        box._counted = false;
      }
      wireChecker(box, "gen-" + box.getAttribute("data-gen"), function () { return cur.fields; }, function (ok) {
        if (ok && !box._counted) { solved++; box._counted = true; stats.textContent = "Problem " + count + " · solved " + solved; }
      });
      box.querySelector(".gen-new").addEventListener("click", fresh);
      box.querySelector(".gen-show").addEventListener("click", function () {
        var s = box.querySelector(".gen-sol"); s.hidden = !s.hidden; this.textContent = s.hidden ? "Show worked solution" : "Hide worked solution";
      });
      fresh();
    });
  });
})();
/* Notebook downloads that also work when the course is opened straight from disk (file://),
   where browsers ignore the download attribute. Each notebook has a companion <name>.ipynb.js
   that holds its text; we load it on click and save it through a Blob. */
(function () {
  "use strict";
  window.MLA_NB = window.MLA_NB || {};
  function save(name, text) {
    var url = URL.createObjectURL(new Blob([text], { type: "application/x-ipynb+json" }));
    var a = document.createElement("a"); a.href = url; a.download = name; document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(url); a.remove(); }, 1000);
  }
  document.addEventListener("click", function (e) {
    var link = e.target.closest && e.target.closest('a[href$=".ipynb"]'); if (!link) return;
    var href = link.getAttribute("href"), name = href.split("/").pop();
    e.preventDefault();
    if (window.MLA_NB[href]) { save(name, window.MLA_NB[href]); return; }
    var s = document.createElement("script"); s.src = href + ".js";
    s.onload = function () { if (window.MLA_NB[href]) save(name, window.MLA_NB[href]); else s.onerror(); };
    s.onerror = function () { window.alert("Couldn't prepare the download. The notebook is already in your course folder: " + href); };
    document.head.appendChild(s);
  });
})();
