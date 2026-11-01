/* ML Academy — "What if?" calculators: change the numbers in a worked example and see what happens. */
(function () {
  "use strict";
  function pn(v) { return v < 0 ? "(" + f(v) + ")" : f(v); }
  function f(v, d) { if (!isFinite(v)) return "—"; d = d === undefined ? 3 : d; return (+v.toFixed(d)).toString(); }
  function num(id, label, val, step) { return '<label class="wi-in"><span>' + label + '</span><input type="number" inputmode="decimal" data-k="' + id + '" value="' + val + '" step="' + (step || "any") + '"></label>'; }
  function shell(el, title, inputs, extra) {
    el.innerHTML = '<div class="wi-head"><span class="wi-tag">What if?</span><span class="wi-title">' + title + '</span></div>' +
      '<div class="wi-inputs">' + inputs + '</div>' + (extra || "") + '<div class="wi-out" aria-live="polite"></div>';
    return el.querySelector(".wi-out");
  }
  function val(el, k) { var i = el.querySelector('[data-k="' + k + '"]'); var v = parseFloat(i.value); return isFinite(v) ? v : NaN; }
  function wire(el, fn) { el.addEventListener("input", fn); el.addEventListener("change", fn); fn(); }
  function btn(text, act) { return '<button type="button" class="wi-btn" data-act="' + act + '">' + text + '</button>'; }
  function setVals(el, o) { Object.keys(o).forEach(function (k) { el.querySelector('[data-k="' + k + '"]').value = o[k]; }); el.dispatchEvent(new Event("input")); }
  function erf(x) { var s = x < 0 ? -1 : 1; x = Math.abs(x); var t = 1 / (1 + 0.3275911 * x); var y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x); return s * y; }
  function Phi(z) { return 0.5 * (1 + erf(z / Math.SQRT2)); }

  var W = {};

  W["mse"] = function (el) {
    var out = shell(el, "change the prices or the line and watch the loss",
      num("y1", "price of house 1 (size 1)", 2) + num("y2", "price of house 2 (size 2)", 4) + num("y3", "price of house 3 (size 3)", 5) + num("w", "slope w", 2) + num("b", "bias b", 0),
      '<div class="wi-acts">' + btn("Make house 3 an outlier (price 8)", "out") + btn("Use the better line", "better") + btn("Reset", "reset") + '</div>');
    el.addEventListener("click", function (e) { var a = e.target.getAttribute && e.target.getAttribute("data-act");
      if (a === "out") setVals(el, { y3: 8 }); if (a === "better") setVals(el, { w: 1.5, b: 0.67 }); if (a === "reset") setVals(el, { y1: 2, y2: 4, y3: 5, w: 2, b: 0 }); });
    wire(el, function () {
      var w = val(el, "w"), b = val(el, "b"), y = [val(el, "y1"), val(el, "y2"), val(el, "y3")], rows = "", se = 0, ae = 0, sq = [];
      y.forEach(function (yi, i) { var p = w * (i + 1) + b, e = p - yi; sq.push(e * e); se += e * e; ae += Math.abs(e);
        rows += "<tr><td>" + (i + 1) + "</td><td>" + f(yi) + "</td><td>" + f(p) + "</td><td>" + f(e) + "</td><td>" + f(e * e) + "</td></tr>"; });
      var mse = se / 3, big = sq.indexOf(Math.max.apply(null, sq));
      out.innerHTML = '<div class="table-scroll"><table class="tbl"><thead><tr><th>house</th><th>price y</th><th>prediction ŷ</th><th>error</th><th>squared</th></tr></thead><tbody>' + rows + '</tbody></table></div>' +
        '<p><b>MSE ' + f(mse) + '</b> · RMSE (typical miss) ' + f(Math.sqrt(mse)) + ' · mean absolute error ' + f(ae / 3) + '</p>' +
        (se > 0 && sq.filter(function (q) { return q > 1e-12; }).length === 1 ? '<p class="wi-note">Only house ' + (big + 1) + ' is missed, so all of the loss comes from it. Try the outlier button to see how fast that loss grows.</p>' : se > 0 ? '<p class="wi-note">House ' + (big + 1) + ' contributes ' + f(100 * sq[big] / se, 0) + '% of the total squared error.' + (sq[big] / se > 0.7 ? ' One house dominates the loss — that is how a single outlier can steer a whole model.' : '') + '</p>' : '<p class="wi-note">A perfect fit: every error is zero.</p>');
    });
  };

  W["distance"] = function (el) {
    var out = shell(el, "how alike are two homes? — try changing the units",
      num("s1", "size of home A", 5) + num("s2", "size of home B", 8) + num("r1", "bedrooms in A", 2) + num("r2", "bedrooms in B", 6),
      '<div class="wi-acts">' + btn("Size in m² (×100)", "m2") + btn("Size in 100 m²", "h") + '</div>');
    el.addEventListener("click", function (e) { var a = e.target.getAttribute && e.target.getAttribute("data-act");
      if (a === "m2") setVals(el, { s1: 500, s2: 800 }); if (a === "h") setVals(el, { s1: 5, s2: 8 }); });
    wire(el, function () {
      var ds = val(el, "s2") - val(el, "s1"), dr = val(el, "r2") - val(el, "r1"), d = Math.hypot(ds, dr), tot = ds * ds + dr * dr;
      out.innerHTML = '<p>Differences: size ' + f(ds) + ', bedrooms ' + f(dr) + ' → <b>distance ' + f(d) + '</b></p>' +
        (tot > 0 ? '<div class="wi-bar" role="img" aria-label="Share of the squared distance: size ' + f(100 * ds * ds / tot, 0) + ' percent, bedrooms ' + f(100 * dr * dr / tot, 0) + ' percent"><span class="wi-b1" style="width:' + (100 * ds * ds / tot) + '%"></span><span class="wi-b2" style="width:' + (100 * dr * dr / tot) + '%"></span></div>' +
        '<p class="wi-note">Share of the distance² from size: <b>' + f(100 * ds * ds / tot, 2) + '%</b>, from bedrooms: <b>' + f(100 * dr * dr / tot, 2) + '%</b>.' + (ds * ds / tot > 0.99 ? ' Size completely dominates — bedrooms are ignored. Standardising the features would fix this.' : '') + '</p>' : '<p class="wi-note">Identical homes: distance 0.</p>');
    });
  };

  W["derivative"] = function (el) {
    var out = shell(el, "estimate the slope of f(x) = x² with a small step h", num("x", "point x", 3) + num("h", "step h", 0.001));
    wire(el, function () {
      var x = val(el, "x"), h = val(el, "h"), est = ((x + h) * (x + h) - x * x) / h;
      out.innerHTML = '<p>Estimate (f(x+h) − f(x)) / h = <b>' + f(est, 5) + '</b> · true slope 2x = <b>' + f(2 * x, 5) + '</b> · gap ' + f(est - 2 * x, 5) + '</p>' +
        '<p class="wi-note">' + (h === 0 ? "h can't be 0 — you'd divide by zero. That's why the derivative is defined as a limit." :
          (x > 0 ? "Positive slope: increasing x increases f, so to make f smaller you would decrease x." : x < 0 ? "Negative slope: increasing x decreases f, so gradient descent would increase x." : "Slope 0: this is the minimum — gradient descent would stop here.") + " The gap always equals h exactly for x², so shrinking h makes the estimate as accurate as you like.") + '</p>';
    });
  };

  W["mean-median"] = function (el) {
    var out = shell(el, "edit the scores — watch the mean and the median",
      '<label class="wi-in wi-wide"><span>scores (separate with commas)</span><input type="text" data-k="xs" value="4, 6, 8, 10, 12" spellcheck="false" autocomplete="off"></label>',
      '<div class="wi-acts">' + btn("Typo: 12 → 52", "typo") + btn("Add a score of 8", "add8") + btn("Everyone +10", "plus") + btn("Double everyone", "dbl") + btn("Reset", "reset") + '</div>');
    var inp = el.querySelector('[data-k="xs"]');
    function get() { return inp.value.split(/[,;\s]+/).map(parseFloat).filter(function (v) { return isFinite(v); }); }
    function put(a) { inp.value = a.join(", "); el.dispatchEvent(new Event("input")); }
    el.addEventListener("click", function (e) { var a = e.target.getAttribute && e.target.getAttribute("data-act"), xs = get();
      if (a === "typo") { var i = xs.lastIndexOf(12); if (i < 0) i = xs.length - 1; xs[i] = 52; put(xs); }
      if (a === "add8") { xs.push(8); put(xs); } if (a === "plus") put(xs.map(function (v) { return v + 10; }));
      if (a === "dbl") put(xs.map(function (v) { return v * 2; })); if (a === "reset") put([4, 6, 8, 10, 12]); });
    wire(el, function () {
      var xs = get(); if (!xs.length) { out.innerHTML = "<p>Type at least one number.</p>"; return; }
      var n = xs.length, m = xs.reduce(function (s, v) { return s + v; }, 0) / n, s = xs.slice().sort(function (a, b) { return a - b; });
      var med = n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2, v = xs.reduce(function (t, x) { return t + (x - m) * (x - m); }, 0) / n, sd = Math.sqrt(v);
      var lo = Math.min(s[0], m), hi = Math.max(s[n - 1], m), span = hi - lo || 1, px = function (x) { return 4 + (x - lo) / span * 92; };
      var dots = s.map(function (x) { return '<circle cx="' + px(x) + '%" cy="22" r="6" class="wi-dot"></circle>'; }).join("");
      var above = xs.filter(function (x) { return x > m; }).length;
      out.innerHTML = '<svg class="wi-strip" width="100%" height="58" role="img" aria-label="The scores on a line, with the mean and median marked">' + dots +
        '<line x1="' + px(m) + '%" x2="' + px(m) + '%" y1="6" y2="40" class="wi-mean"></line><line x1="' + px(med) + '%" x2="' + px(med) + '%" y1="6" y2="40" class="wi-med"></line>' +
        '<text x="' + px(m) + '%" y="54" class="wi-lbl wi-mean-t" text-anchor="middle">mean</text><text x="' + px(med) + '%" y="' + (Math.abs(px(m) - px(med)) < 8 ? 6 : 54) + '" class="wi-lbl wi-med-t" text-anchor="middle">median</text></svg>' +
        '<p><b>mean ' + f(m) + '</b> · <b>median ' + f(med) + '</b> · standard deviation ' + f(sd) + ' · ' + n + ' scores, ' + above + ' above the mean</p>' +
        '<p class="wi-note">' + (n > 2 && Math.abs(m - med) > 0.12 * (s[n - 1] - s[0]) ? "The mean and median have split apart: an extreme value is pulling the mean towards it, while the median only cares about the middle position. Here the median describes a typical score better." :
          "Mean and median agree closely, so the data is roughly balanced around its centre.") + '</p>';
    });
  };

  W["zscore"] = function (el) {
    var out = shell(el, "how unusual is a value?", num("mu", "mean μ (cm)", 170) + num("sd", "standard deviation σ (cm)", 10) + num("x", "height x (cm)", 200));
    wire(el, function () {
      var mu = val(el, "mu"), sd = val(el, "sd"), x = val(el, "x");
      if (!(sd > 0)) { out.innerHTML = "<p>The standard deviation must be positive.</p>"; return; }
      var z = (x - mu) / sd, up = 1 - Phi(z), one = up > 0 ? Math.round(1 / up) : Infinity;
      out.innerHTML = '<p>z = (' + f(x) + ' − ' + f(mu) + ') / ' + f(sd) + ' = <b>' + f(z, 2) + '</b> standard deviations ' + (z >= 0 ? "above" : "below") + ' the mean.</p>' +
        '<p>Taller than this: <b>' + (up < 0.0001 ? up.toExponential(1) : f(100 * up, 2) + "%") + '</b>' + (z > 0 && isFinite(one) ? " (about 1 in " + one.toLocaleString("en") + ")" : "") + '. Within ±2σ: ' + f(mu - 2 * sd, 1) + '–' + f(mu + 2 * sd, 1) + ' cm (about 95% of people).</p>' +
        '<p class="wi-note">' + (Math.abs(z) >= 3 ? "|z| > 3: very unusual. In a dataset, check whether a value like this is real or an error." : Math.abs(z) >= 2 ? "|z| between 2 and 3: unusual, roughly the outer 5%." : "Within 2σ: an ordinary value.") + '</p>';
    });
  };

  function list(s) { return s.split(/[,;\s]+/).map(parseFloat).filter(function (v) { return isFinite(v); }); }
  function mean(a) { return a.reduce(function (s, v) { return s + v; }, 0) / a.length; }
  function pstd(a) { var m = mean(a); return Math.sqrt(mean(a.map(function (v) { return (v - m) * (v - m); }))); }
  function txt(id, label, v) { return '<label class="wi-in wi-wide"><span>' + label + '</span><input type="text" data-k="' + id + '" value="' + v + '" spellcheck="false" autocomplete="off"></label>'; }
  function tv(el, k) { return el.querySelector('[data-k="' + k + '"]').value; }
  function acts(el, map) { el.addEventListener("click", function (e) { var a = e.target.getAttribute && e.target.getAttribute("data-act"); if (a && map[a]) map[a](); }); }

  W["cv"] = function (el) {
    var out = shell(el, "compare two models across five folds", txt("a", "model A fold scores", "0.82, 0.85, 0.80, 0.84, 0.84") + txt("b", "model B fold scores", "0.84, 0.86, 0.82, 0.85, 0.83"),
      '<div class="wi-acts">' + btn("A has one bad fold (0.70)", "bad") + btn("Reset", "reset") + '</div>');
    acts(el, { bad: function () { setVals(el, { a: "0.82, 0.85, 0.70, 0.84, 0.84" }); }, reset: function () { setVals(el, { a: "0.82, 0.85, 0.80, 0.84, 0.84", b: "0.84, 0.86, 0.82, 0.85, 0.83" }); } });
    wire(el, function () {
      var a = list(tv(el, "a")), b = list(tv(el, "b")); if (a.length < 2 || b.length < 2) { out.innerHTML = "<p>Enter at least two scores for each model.</p>"; return; }
      var ma = mean(a), sa = pstd(a), mb = mean(b), sb = pstd(b), gap = Math.abs(ma - mb), noise = Math.max(sa, sb);
      out.innerHTML = '<p>Model A: <b>' + f(ma) + ' ± ' + f(sa) + '</b> · Model B: <b>' + f(mb) + ' ± ' + f(sb) + '</b> · gap ' + f(gap) + '</p>' +
        '<p class="wi-note">' + (gap < noise ? "The gap is smaller than the fold-to-fold spread, so this could easily be luck. Don't pick a winner on this evidence alone." :
          gap < 2 * noise ? "The gap is bigger than the spread, but not by much — suggestive, not conclusive." : "The gap is more than twice the spread: a fairly clear difference.") +
        (sa > 0.04 || sb > 0.04 ? " One model's scores vary a lot between folds — check that fold for unusual data." : "") + '</p>';
    });
  };

  W["lsfit"] = function (el) {
    var out = shell(el, "edit the points and watch the best line move", txt("x", "hours x", "1, 2, 3, 4, 5") + txt("y", "scores y", "2, 4, 5, 4, 5"),
      '<div class="wi-acts">' + btn("Last score 5 → 15", "o1") + btn("First score 2 → 12", "o2") + btn("Everyone +10", "p10") + btn("Reset", "reset") + '</div>');
    acts(el, { o1: function () { setVals(el, { y: "2, 4, 5, 4, 15" }); }, o2: function () { setVals(el, { y: "12, 4, 5, 4, 5" }); },
      p10: function () { setVals(el, { y: list(tv(el, "y")).map(function (v) { return v + 10; }).join(", ") }); }, reset: function () { setVals(el, { x: "1, 2, 3, 4, 5", y: "2, 4, 5, 4, 5" }); } });
    wire(el, function () {
      var x = list(tv(el, "x")), y = list(tv(el, "y")), n = Math.min(x.length, y.length); x = x.slice(0, n); y = y.slice(0, n);
      if (n < 2) { out.innerHTML = "<p>Enter at least two points.</p>"; return; }
      var mx = mean(x), my = mean(y), sxy = 0, sxx = 0, i; for (i = 0; i < n; i++) { sxy += (x[i] - mx) * (y[i] - my); sxx += (x[i] - mx) * (x[i] - mx); }
      if (sxx === 0) { out.innerHTML = "<p class='wi-note'>All x values are equal, so there is no unique best line: the slope can't be learned when x never varies.</p>"; return; }
      var w = sxy / sxx, b = my - w * mx, ss = 0, st = 0, res = []; for (i = 0; i < n; i++) { var r = y[i] - (w * x[i] + b); res.push(r); ss += r * r; st += (y[i] - my) * (y[i] - my); }
      var big = 0; res.forEach(function (r, k) { if (Math.abs(r) > Math.abs(res[big])) big = k; });
      var xmin = Math.min.apply(null, x), xmax = Math.max.apply(null, x), ymin = Math.min.apply(null, y.concat([w * xmin + b, w * xmax + b])), ymax = Math.max.apply(null, y.concat([w * xmin + b, w * xmax + b]));
      var X = function (v) { return 30 + (v - xmin) / ((xmax - xmin) || 1) * 300; }, Y = function (v) { return 130 - (v - ymin) / ((ymax - ymin) || 1) * 115; };
      var svg = '<svg class="wi-plot" viewBox="0 0 360 145" role="img" aria-label="Scatter plot of the points with the least-squares line"><line x1="' + X(xmin) + '" y1="' + Y(w * xmin + b) + '" x2="' + X(xmax) + '" y2="' + Y(w * xmax + b) + '" class="wi-line"></line>' +
        x.map(function (v, k) { return '<circle cx="' + X(v) + '" cy="' + Y(y[k]) + '" r="5" class="' + (k === big ? "wi-dot wi-hot" : "wi-dot") + '"></circle>'; }).join("") + '</svg>';
      out.innerHTML = svg + '<p>Best line: <b>ŷ = ' + f(w) + 'x ' + (b < 0 ? "− " + f(-b) : "+ " + f(b)) + '</b> · MSE ' + f(ss / n) + ' · R² ' + (st ? f(1 - ss / st) : "—") + '</p>' +
        '<p class="wi-note">Biggest residual: point ' + (big + 1) + ' (' + f(res[big]) + '), highlighted. ' + (w < 0 ? "The slope is negative: the fit now says more hours go with lower scores." : "") + '</p>';
    });
  };

  W["gd"] = function (el) {
    var out = shell(el, "run gradient descent on the five points", num("eta", "learning rate η", 0.05) + num("steps", "number of steps", 100, 1) + num("scale", "multiply x by", 1),
      '<div class="wi-acts">' + btn("η = 0.01", "e1") + btn("η = 0.08", "e8") + btn("η = 0.1", "e10") + btn("Reset", "reset") + '</div>');
    acts(el, { e1: function () { setVals(el, { eta: 0.01 }); }, e8: function () { setVals(el, { eta: 0.08 }); }, e10: function () { setVals(el, { eta: 0.1 }); }, reset: function () { setVals(el, { eta: 0.05, steps: 100, scale: 1 }); } });
    wire(el, function () {
      var eta = val(el, "eta"), steps = Math.max(0, Math.min(100000, Math.round(val(el, "steps")))), sc = val(el, "scale"), X = [1, 2, 3, 4, 5].map(function (v) { return v * sc; }), Y = [2, 4, 5, 4, 5];
      var w = 0, b = 0, hist = [], k, lossAt = function () { return mean(X.map(function (x, i) { var e = w * x + b - Y[i]; return e * e; })); };
      for (k = 0; k < steps; k++) { var gw = 0, gb = 0; X.forEach(function (x, i) { var e = w * x + b - Y[i]; gw += 2 * e * x / 5; gb += 2 * e / 5; }); w -= eta * gw; b -= eta * gb; if (!isFinite(w) || Math.abs(w) > 1e12) break; if (k < 6) hist.push(lossAt()); }
      var L = lossAt(), div = !isFinite(L) || L > 1e6;
      out.innerHTML = '<p>After ' + steps + ' steps: <b>w = ' + (div ? "—" : f(w)) + ', b = ' + (div ? "—" : f(b)) + '</b> · loss ' + (div ? "exploded" : f(L)) + '</p>' +
        '<p>Loss after steps 1–6: ' + hist.map(function (v) { return isFinite(v) && v < 1e9 ? f(v) : "huge"; }).join(", ") + '</p>' +
        '<p class="wi-note">' + (div ? "Diverged: each step overshoots by more than the last. Lower η, or scale the features down." :
          sc === 1 && Math.abs(w - 0.6) < 0.001 && Math.abs(b - 2.2) < 0.001 ? "Converged to the least-squares answer w = 0.6, b = 2.2 (from Lesson 6)." :
          sc === 1 ? "Not there yet (the answer is w = 0.6, b = 2.2). More steps, or a slightly larger η, would get closer." : "With rescaled x the best slope changes too (0.6 ÷ the scale).") + '</p>';
    });
  };

  W["sigmoid"] = function (el) {
    var out = shell(el, "probability and odds of passing", num("w", "weight w (per hour)", 1.354) + num("b", "bias b", -3.723) + num("x", "hours studied x", 2));
    wire(el, function () {
      var w = val(el, "w"), b = val(el, "b"), x = val(el, "x"), z = w * x + b, p = 1 / (1 + Math.exp(-z)), o = p / (1 - p), p1 = 1 / (1 + Math.exp(-(z + w)));
      out.innerHTML = '<p>z = ' + f(w) + ' × ' + f(x) + ' ' + (b < 0 ? "− " + f(-b) : "+ " + f(b)) + ' = <b>' + f(z) + '</b> → p = σ(z) = <b>' + f(p) + '</b> (' + f(100 * p, 1) + '% chance) · odds ' + f(o) + '</p>' +
        '<p>One more hour: odds × e<sup>w</sup> = × ' + f(Math.exp(w)) + ', so p becomes <b>' + f(p1) + '</b>. ' + (w !== 0 ? "50% point: x = " + f(-b / w, 2) + " hours." : "") + '</p>' +
        '<p class="wi-note">Log loss if this student passes: ' + f(-Math.log(p)) + '; if they fail: ' + f(-Math.log(1 - p)) + '. ' + (p > 0.95 || p < 0.05 ? "The model is very confident — a mistake here would be heavily penalised." : "") + '</p>';
    });
  };

  W["confusion"] = function (el) {
    var out = shell(el, "change the four counts — watch every metric", num("tp", "TP (sick, flagged)", 8, 1) + num("fn", "FN (sick, missed)", 2, 1) + num("fp", "FP (healthy, flagged)", 10, 1) + num("tn", "TN (healthy, cleared)", 80, 1),
      '<div class="wi-acts">' + btn("Flag 30, catch all 10", "more") + btn("Flag only 5", "fewer") + btn("Say “healthy” to everyone", "none") + btn("Reset", "reset") + '</div>');
    acts(el, { more: function () { setVals(el, { tp: 10, fn: 0, fp: 20, tn: 70 }); }, fewer: function () { setVals(el, { tp: 4, fn: 6, fp: 1, tn: 89 }); }, none: function () { setVals(el, { tp: 0, fn: 10, fp: 0, tn: 90 }); }, reset: function () { setVals(el, { tp: 8, fn: 2, fp: 10, tn: 80 }); } });
    wire(el, function () {
      var tp = val(el, "tp"), fn = val(el, "fn"), fp = val(el, "fp"), tn = val(el, "tn"), N = tp + fn + fp + tn;
      if (!(N > 0)) { out.innerHTML = "<p>Enter some counts.</p>"; return; }
      var acc = (tp + tn) / N, pr = tp + fp ? tp / (tp + fp) : NaN, rc = tp + fn ? tp / (tp + fn) : NaN, f1 = 2 * tp + fp + fn ? 2 * tp / (2 * tp + fp + fn) : NaN, fpr = fp + tn ? fp / (fp + tn) : NaN;
      out.innerHTML = '<p>accuracy <b>' + f(acc) + '</b> · precision <b>' + f(pr) + '</b> · recall <b>' + f(rc) + '</b> · F1 <b>' + f(f1) + '</b> · false-positive rate <b>' + f(fpr) + '</b></p>' +
        '<p class="wi-note">' + (tp + fp === 0 ? "Nobody is flagged: precision is undefined and recall is 0 — yet accuracy can still look high. This is the accuracy trap." :
          "Of " + (tp + fp) + " people flagged, " + tp + " are really sick (precision); of " + (tp + fn) + " sick people, " + tp + " were found (recall).") + '</p>';
    });
  };

  W["ridge"] = function (el) {
    var out = shell(el, "shrink the weight with the penalty λ", num("lam", "penalty λ", 1) + num("rep", "repeat the data (times)", 1, 1) + num("sc", "multiply x by", 1));
    wire(el, function () {
      var lam = val(el, "lam"), rep = Math.max(1, Math.round(val(el, "rep"))), sc = val(el, "sc"), x = [1, 2, 3].map(function (v) { return v * sc; }), y = [2, 4, 7];
      var sxy = rep * (x[0] * y[0] + x[1] * y[1] + x[2] * y[2]), sxx = rep * (x[0] * x[0] + x[1] * x[1] + x[2] * x[2]), w0 = sxy / sxx, w = sxy / (sxx + lam);
      out.innerHTML = '<p>w = Σxy / (Σx² + λ) = ' + f(sxy) + ' / (' + f(sxx) + ' + ' + f(lam) + ') = <b>' + f(w) + '</b> · without penalty ' + f(w0) + '</p>' +
        '<div class="wi-bar" role="img" aria-label="Weight kept: ' + f(100 * w / w0, 0) + ' percent of its unpenalised value"><span class="wi-b1" style="width:' + Math.max(0, Math.min(100, 100 * w / w0)) + '%"></span></div>' +
        '<p class="wi-note">The penalty keeps <b>' + f(100 * w / w0, 1) + '%</b> of the weight. ' + (rep > 1 ? "More data makes Σx² bigger, so the same λ matters less. " : "") + (sc !== 1 ? "Changing the scale of x changes how strongly λ bites — standardise features before regularising." : "") + '</p>';
    });
  };

  W["knn"] = function (el) {
    var P = [[1, 1, "red"], [2, 1, "red"], [4, 3, "blue"], [5, 4, "blue"], [3, 3.5, "blue"]], names = "ABCDE";
    var out = shell(el, "move the new point and change k", num("qx", "new point x", 2) + num("qy", "new point y", 2) + num("k", "k (1–5)", 3, 1),
      '<label class="wi-in"><span>voting</span><select data-k="wt"><option value="0">one vote each</option><option value="1">weighted by 1/distance</option></select></label>');
    wire(el, function () {
      var q = [val(el, "qx"), val(el, "qy")], k = Math.max(1, Math.min(5, Math.round(val(el, "k")))), wt = el.querySelector('[data-k="wt"]').value === "1";
      var d = P.map(function (p, i) { return { n: names[i], c: p[2], d: Math.hypot(p[0] - q[0], p[1] - q[1]), x: p[0], y: p[1] }; }).sort(function (a, b) { return a.d - b.d; });
      var votes = { red: 0, blue: 0 }; d.slice(0, k).forEach(function (o) { votes[o.c] += wt ? 1 / Math.max(o.d, 1e-9) : 1; });
      var win = votes.red > votes.blue ? "red" : votes.blue > votes.red ? "blue" : "a tie";
      var X = function (v) { return 20 + v * 50; }, Y = function (v) { return 230 - v * 50; }, r = d[k - 1].d;
      var svg = '<svg class="wi-plot" viewBox="0 0 320 250" role="img" aria-label="The five training points, the new point and a circle around its ' + k + ' nearest neighbours">' +
        '<circle cx="' + X(q[0]) + '" cy="' + Y(q[1]) + '" r="' + (r * 50 + 8) + '" class="wi-ring"></circle>' +
        d.map(function (o) { return '<circle cx="' + X(o.x) + '" cy="' + Y(o.y) + '" r="7" class="' + (o.c === "red" ? "wi-red" : "wi-blue") + '"></circle><text x="' + (X(o.x) + 10) + '" y="' + (Y(o.y) - 8) + '" class="wi-lbl">' + o.n + '</text>'; }).join("") +
        '<rect x="' + (X(q[0]) - 6) + '" y="' + (Y(q[1]) - 6) + '" width="12" height="12" class="wi-q"></rect></svg>';
      out.innerHTML = svg + '<p>Nearest first: ' + d.map(function (o, i) { return (i < k ? "<b>" : "") + o.n + " (" + o.c + ", " + f(o.d) + ")" + (i < k ? "</b>" : ""); }).join(", ") + '</p>' +
        '<p>Votes: red ' + f(votes.red) + ', blue ' + f(votes.blue) + ' → prediction: <b>' + win + '</b></p>' +
        '<p class="wi-note">' + (k === 5 && !wt ? "With k = 5 every point votes, so the majority class (blue) wins wherever the new point is. Try weighted voting." : (k < 5 && Math.abs(d[k - 1].d - d[k].d) < 1e-9 ? "Neighbours number " + k + " and " + (k + 1) + " are exactly the same distance away — a tie in who gets to vote." : (wt ? "Closer neighbours get bigger votes (1 ÷ distance), so near points outweigh far ones." : "Only the circled neighbours vote."))) + '</p>';
    });
  };

  W["fruit"] = function (el) {
    var out = shell(el, "apple or orange from weight alone", num("x", "weight (g)", 170) + num("pa", "share of apples on the belt (prior)", 0.5) +
      num("ma", "apple mean (g)", 150) + num("sa", "apple sd", 20) + num("mo", "orange mean (g)", 200) + num("so", "orange sd", 25));
    function dens(x, m, s) { return Math.exp(-0.5 * Math.pow((x - m) / s, 2)) / (s * Math.sqrt(2 * Math.PI)); }
    wire(el, function () {
      var x = val(el, "x"), pa = Math.max(0, Math.min(1, val(el, "pa"))), ma = val(el, "ma"), sa = val(el, "sa"), mo = val(el, "mo"), so = val(el, "so");
      if (!(sa > 0 && so > 0)) { out.innerHTML = "<p>Standard deviations must be positive.</p>"; return; }
      var la = dens(x, ma, sa), lo = dens(x, mo, so), pApple = pa * la / (pa * la + (1 - pa) * lo);
      out.innerHTML = '<p>Apple: z = ' + f((x - ma) / sa, 2) + ', density ' + f(la, 5) + ' · Orange: z = ' + f((x - mo) / so, 2) + ', density ' + f(lo, 5) + '</p>' +
        '<p>P(apple | ' + f(x) + ' g) = <b>' + f(pApple) + '</b> → ' + (pApple > 0.5 ? "apple" : pApple < 0.5 ? "orange" : "can't tell") + '</p>' +
        '<div class="wi-bar" role="img" aria-label="Apple ' + f(100 * pApple, 0) + ' percent, orange ' + f(100 - 100 * pApple, 0) + ' percent"><span class="wi-b1" style="width:' + (100 * pApple) + '%"></span><span class="wi-b2" style="width:' + (100 - 100 * pApple) + '%"></span></div>' +
        '<p class="wi-note">' + (Math.abs(pApple - 0.5) < 0.1 ? "Close to 50/50: this weight is about equally typical of both fruits. Another feature (colour, diameter) would help." : "The fruit is more typical of the " + (pApple > 0.5 ? "apples" : "oranges") + ", measured in standard deviations from each average.") + '</p>';
    });
  };

  W["split"] = function (el) {
    var out = shell(el, "score a split: how much purer are the children?", num("ly", "left: yes", 4, 1) + num("ln", "left: no", 0, 1) + num("ry", "right: yes", 2, 1) + num("rn", "right: no", 4, 1),
      '<div class="wi-acts">' + btn("Split A", "a") + btn("Split B (useless)", "b") + btn("Perfect split", "p") + btn("Peel off one", "one") + '</div>');
    acts(el, { a: function () { setVals(el, { ly: 4, ln: 0, ry: 2, rn: 4 }); }, b: function () { setVals(el, { ly: 3, ln: 2, ry: 3, rn: 2 }); }, p: function () { setVals(el, { ly: 6, ln: 0, ry: 0, rn: 4 }); }, one: function () { setVals(el, { ly: 1, ln: 0, ry: 5, rn: 4 }); } });
    function gini(y, n) { var t = y + n; return t ? 1 - Math.pow(y / t, 2) - Math.pow(n / t, 2) : 0; }
    function ent(y, n) { var t = y + n, h = 0; [y, n].forEach(function (c) { if (c > 0) h -= c / t * Math.log2(c / t); }); return h; }
    wire(el, function () {
      var ly = Math.max(0, val(el, "ly")), ln = Math.max(0, val(el, "ln")), ry = Math.max(0, val(el, "ry")), rn = Math.max(0, val(el, "rn")), Y = ly + ry, N = ln + rn, T = Y + N, L = ly + ln, R = ry + rn;
      if (!T) { out.innerHTML = "<p>Enter some counts.</p>"; return; }
      var gp = gini(Y, N), gw = (L * gini(ly, ln) + R * gini(ry, rn)) / T, hp = ent(Y, N), hw = (L * ent(ly, ln) + R * ent(ry, rn)) / T;
      out.innerHTML = '<p>Parent: ' + Y + ' yes / ' + N + ' no · Gini ' + f(gp) + ' · entropy ' + f(hp) + ' bits</p>' +
        '<p>Left (' + L + '): Gini ' + f(gini(ly, ln)) + ' · Right (' + R + '): Gini ' + f(gini(ry, rn)) + ' · weighted ' + f(gw) + '</p>' +
        '<p><b>Gini gain ' + f(gp - gw) + '</b> · information gain ' + f(hp - hw) + ' bits</p>' +
        '<p class="wi-note">' + (gp - gw < 1e-9 ? "No gain: the children are as mixed as the parent. The tree would never choose this question." : gp - gw >= gp - 1e-9 ? "Both children are pure — the best possible split." : (L <= 1 || R <= 1) ? "A pure leaf with a single example barely helps: tiny leaves are how deep trees overfit." : "A useful split. The tree tries every candidate and keeps the one with the biggest gain.") + '</p>';
    });
  };

  W["adaboost"] = function (el) {
    var out = shell(el, "how AdaBoost reweights after one stump", num("n", "examples", 10, 1) + num("m", "misclassified", 3, 1));
    wire(el, function () {
      var n = Math.max(2, Math.round(val(el, "n"))), m = Math.max(0, Math.min(n, Math.round(val(el, "m")))), e = m / n;
      if (m === 0 || m === n) { out.innerHTML = '<p class="wi-note">' + (m === 0 ? "A perfect stump: ε = 0 makes the vote infinite. Real implementations cap it." : "Every example wrong: ε = 1, so flipping the stump would be perfect.") + '</p>'; return; }
      var a = 0.5 * Math.log((1 - e) / e), w0 = 1 / n, ww = w0 * Math.exp(a), wc = w0 * Math.exp(-a), Z = m * ww + (n - m) * wc;
      out.innerHTML = '<p>Error ε = ' + m + '/' + n + ' = ' + f(e) + ' → vote α = ½ ln((1−ε)/ε) = <b>' + f(a) + '</b></p>' +
        '<p>New weights: each mistake <b>' + f(ww / Z) + '</b>, each correct example <b>' + f(wc / Z) + '</b> (were ' + f(w0) + ')</p>' +
        '<p>Mistakes now hold <b>' + f(100 * m * ww / Z, 1) + '%</b> of the weight (was ' + f(100 * e, 1) + '%).</p>' +
        '<p class="wi-note">' + (a < 0 ? "Worse than chance: the vote is negative, so this stump's answers are flipped." : Math.abs(a) < 1e-9 ? "A coin-flip stump gets no say at all." : "However good or bad the stump, its mistakes always end up with exactly half of the weight — so the next stump must focus on them.") + '</p>';
    });
  };

  W["hinge"] = function (el) {
    var out = shell(el, "hinge loss vs log loss for one point", num("s", "score w·x + b", 0.4) + '<label class="wi-in"><span>true class y</span><select data-k="y"><option value="1">+1</option><option value="-1">−1</option></select></label>');
    wire(el, function () {
      var s = val(el, "s"), y = +el.querySelector('[data-k="y"]').value, m = y * s, h = Math.max(0, 1 - m), ll = Math.log(1 + Math.exp(-m));
      out.innerHTML = '<p>y × score = ' + f(m) + ' → hinge loss max(0, 1 − ' + pn(m) + ') = <b>' + f(h) + '</b> · logistic loss ln(1 + e<sup>−' + pn(m) + '</sup>) = <b>' + f(ll) + '</b></p>' +
        '<p class="wi-note">' + (m >= 1 ? "Correct and outside the road: hinge loss is exactly 0, so this point doesn't affect the SVM at all. Logistic loss is small but never zero." :
          m > 0 ? "Correct side, but inside the road: a small hinge penalty. Points like this become support vectors." : "Wrong side of the boundary: the penalty grows in a straight line the further it goes.") + '</p>';
    });
  };

  W["kmeans1d"] = function (el) {
    var out = shell(el, "k-means on a line, one round at a time", txt("x", "points", "1, 2, 3, 8, 9, 10") + txt("c", "starting centroids (one per cluster)", "1, 2"),
      '<div class="wi-acts">' + btn("Good start (1, 10)", "good") + btn("Three clusters (2, 8, 10)", "three") + btn("Empty cluster (1, 5, 10)", "empty") + btn("Outlier 50, two depots", "out") + btn("Reset", "reset") + '</div>');
    acts(el, { good: function () { setVals(el, { c: "1, 10" }); }, three: function () { setVals(el, { c: "2, 8, 10" }); }, empty: function () { setVals(el, { c: "1, 5, 10" }); },
      out: function () { setVals(el, { x: "1, 2, 3, 8, 9, 10, 50", c: "1, 10" }); }, reset: function () { setVals(el, { x: "1, 2, 3, 8, 9, 10", c: "1, 2" }); } });
    wire(el, function () {
      var x = list(tv(el, "x")), c = list(tv(el, "c")); if (!x.length || !c.length) { out.innerHTML = "<p>Enter points and at least one centroid.</p>"; return; }
      var rows = "", lab, it, inertia;
      for (it = 1; it <= 20; it++) {
        lab = x.map(function (v) { var b = 0; c.forEach(function (m, j) { if (Math.abs(v - m) < Math.abs(v - c[b])) b = j; }); return b; });
        var nc = c.map(function (m, j) { var g = x.filter(function (_, i) { return lab[i] === j; }); return g.length ? mean(g) : m; });
        inertia = x.reduce(function (s, v, i) { return s + Math.pow(v - nc[lab[i]], 2); }, 0);
        rows += "<tr><td>" + it + "</td><td>" + c.map(function (_, j) { var g = x.filter(function (_, i) { return lab[i] === j; }); return "{" + g.join(", ") + "}"; }).join(" ") + "</td><td>" + nc.map(function (v) { return f(v, 2); }).join(", ") + "</td><td>" + f(inertia) + "</td></tr>";
        var same = nc.every(function (v, j) { return Math.abs(v - c[j]) < 1e-9; }); c = nc; if (same) break;
      }
      var empty = c.filter(function (_, j) { return !lab.some(function (l) { return l === j; }); }).length;
      out.innerHTML = '<div class="table-scroll"><table class="tbl"><thead><tr><th>round</th><th>clusters</th><th>new centroids</th><th>inertia</th></tr></thead><tbody>' + rows + '</tbody></table></div>' +
        '<p class="wi-note">Converged after ' + it + ' round' + (it > 1 ? "s" : "") + ' with inertia <b>' + f(inertia) + '</b>.' + (empty ? " " + empty + " centroid" + (empty > 1 ? "s" : "") + " ended up with no points — a wasted cluster caused by a poor start." : "") + '</p>';
    });
  };

  W["pca2"] = function (el) {
    var out = shell(el, "edit the points — how much does PC1 keep?", txt("p", "points as x,y pairs separated by semicolons", "1,2; 2,3; 3,5; 4,4; 5,6"),
      '<div class="wi-acts">' + btn("On a line", "line") + btn("Weakly related", "weak") + btn("Second feature ×10", "x10") + btn("Reset", "reset") + '</div>');
    acts(el, { line: function () { setVals(el, { p: "1,1; 2,2; 3,3; 4,4; 5,5" }); }, weak: function () { setVals(el, { p: "1,4; 2,2; 3,6; 4,4; 5,4" }); },
      x10: function () { setVals(el, { p: "1,20; 2,30; 3,50; 4,40; 5,60" }); }, reset: function () { setVals(el, { p: "1,2; 2,3; 3,5; 4,4; 5,6" }); } });
    wire(el, function () {
      var P = tv(el, "p").split(";").map(function (s) { return list(s); }).filter(function (a) { return a.length >= 2; });
      if (P.length < 2) { out.innerHTML = "<p>Enter at least two points like 1,2; 3,4.</p>"; return; }
      var n = P.length, mx = mean(P.map(function (p) { return p[0]; })), my = mean(P.map(function (p) { return p[1]; }));
      var a = 0, d = 0, b = 0; P.forEach(function (p) { a += (p[0] - mx) * (p[0] - mx); d += (p[1] - my) * (p[1] - my); b += (p[0] - mx) * (p[1] - my); }); a /= n - 1; d /= n - 1; b /= n - 1;
      var tr = a + d, disc = Math.sqrt(Math.pow((a - d) / 2, 2) + b * b), l1 = tr / 2 + disc, l2 = tr / 2 - disc;
      var vx = b !== 0 ? l1 - d : (a >= d ? 1 : 0), vy = b !== 0 ? b : (a >= d ? 0 : 1), nv = Math.hypot(vx, vy); vx /= nv; vy /= nv; if (vx < 0) { vx = -vx; vy = -vy; }
      var share = tr > 0 ? l1 / tr : 0;
      out.innerHTML = '<p>Covariance matrix: [[' + f(a) + ', ' + f(b) + '], [' + f(b) + ', ' + f(d) + ']] → eigenvalues <b>' + f(l1) + '</b> and <b>' + f(l2) + '</b></p>' +
        '<p>PC1 direction (' + f(vx) + ', ' + f(vy) + ') keeps <b>' + f(100 * share, 1) + '%</b> of the variance.</p>' +
        '<div class="wi-bar" role="img" aria-label="PC1 keeps ' + f(100 * share, 0) + ' percent of the variance"><span class="wi-b1" style="width:' + (100 * share) + '%"></span><span class="wi-b2" style="width:' + (100 - 100 * share) + '%"></span></div>' +
        '<p class="wi-note">' + (share > 0.99 ? "Almost everything lies along one direction" + (Math.abs(vy) > 0.99 || Math.abs(vx) > 0.99 ? " — but that direction is one of the original features, a sign that its large units are dominating. Standardise first." : ": one number per point loses almost nothing.") :
          share > 0.85 ? "One component keeps most of the information." : "The variance is spread out: keeping only PC1 would lose a lot.") + '</p>';
    });
  };

  W["neuron"] = function (el) {
    var out = shell(el, "the 2-2-1 network: change the inputs and weights",
      num("x1", "input x₁", 1) + num("x2", "input x₂", 0) + num("a1", "neuron 1 weight on x₁", 0.5) + num("b1", "neuron 1 weight on x₂", 0.3) + num("a2", "neuron 2 weight on x₁", -0.5) + num("b2", "neuron 2 weight on x₂", 0.8) + num("v1", "output weight v₁", 1) + num("v2", "output weight v₂", -1) +
      '<label class="wi-in"><span>hidden activation</span><select data-k="act"><option value="sig">sigmoid</option><option value="relu">ReLU</option><option value="tanh">tanh</option></select></label>',
      '<div class="wi-acts">' + btn("Input (0, 1)", "x01") + btn("All weights 0", "zero") + btn("Reset", "reset") + '</div>');
    acts(el, { x01: function () { setVals(el, { x1: 0, x2: 1 }); }, zero: function () { setVals(el, { a1: 0, b1: 0, a2: 0, b2: 0, v1: 0, v2: 0 }); },
      reset: function () { setVals(el, { x1: 1, x2: 0, a1: 0.5, b1: 0.3, a2: -0.5, b2: 0.8, v1: 1, v2: -1 }); el.querySelector('[data-k="act"]').value = "sig"; el.dispatchEvent(new Event("input")); } });
    function sg(z) { return 1 / (1 + Math.exp(-z)); }
    wire(el, function () {
      var act = el.querySelector('[data-k="act"]').value, g = act === "relu" ? function (z) { return Math.max(0, z); } : act === "tanh" ? Math.tanh : sg;
      var x1 = val(el, "x1"), x2 = val(el, "x2"), z1 = val(el, "a1") * x1 + val(el, "b1") * x2, z2 = val(el, "a2") * x1 + val(el, "b2") * x2, h1 = g(z1), h2 = g(z2), z = val(el, "v1") * h1 + val(el, "v2") * h2, p = sg(z);
      out.innerHTML = '<p>Hidden: z₁ = ' + f(z1) + ' → h₁ = <b>' + f(h1) + '</b> · z₂ = ' + f(z2) + ' → h₂ = <b>' + f(h2) + '</b></p>' +
        '<p>Output: z = ' + f(z) + ' → p = σ(z) = <b>' + f(p) + '</b> · loss if the truth is 1: ' + f(-Math.log(p)) + ', if 0: ' + f(-Math.log(1 - p)) + '</p>' +
        '<p class="wi-note">' + (Math.abs(h1 - h2) < 1e-9 && Math.abs(z1 - z2) < 1e-9 ? "Both hidden neurons compute exactly the same thing — they're redundant. With identical starting weights they would stay identical during training, which is why weights start random." :
          (act === "relu" && (h1 === 0 || h2 === 0)) ? "A ReLU neuron with a negative input outputs 0: it's switched off for this input." : p > 0.5 ? "The network leans towards 1." : p < 0.5 ? "The network leans towards 0." : "Exactly 50/50.") + '</p>';
    });
  };

  W["softmax"] = function (el) {
    var out = shell(el, "softmax: scores in, probabilities out", txt("s", "scores (one per option)", "0.707, 0, 0.707") + num("T", "temperature (divide scores by)", 1),
      '<div class="wi-acts">' + btn("Unscaled attention (1, 0, 1)", "u") + btn("Strong query (7.07, 0, 7.07)", "strong") + btn("Classifier scores (2, 1, 0)", "cls") + btn("Reset", "reset") + '</div>');
    acts(el, { u: function () { setVals(el, { s: "1, 0, 1", T: 1 }); }, strong: function () { setVals(el, { s: "7.07, 0, 7.07", T: 1 }); }, cls: function () { setVals(el, { s: "2, 1, 0", T: 1 }); }, reset: function () { setVals(el, { s: "0.707, 0, 0.707", T: 1 }); } });
    wire(el, function () {
      var s = list(tv(el, "s")), T = val(el, "T"); if (!s.length || !(T > 0)) { out.innerHTML = "<p>Enter scores and a positive temperature.</p>"; return; }
      var mx = Math.max.apply(null, s), e = s.map(function (v) { return Math.exp((v - mx) / T); }), Z = e.reduce(function (a, b) { return a + b; }, 0), p = e.map(function (v) { return v / Z; }), top = Math.max.apply(null, p);
      out.innerHTML = '<div class="table-scroll"><table class="tbl"><thead><tr><th>option</th><th>score</th><th>probability</th></tr></thead><tbody>' + s.map(function (v, i) { return "<tr><td>" + (i + 1) + "</td><td>" + f(v) + "</td><td><b>" + f(p[i]) + "</b></td></tr>"; }).join("") + '</tbody></table></div>' +
        '<p class="wi-note">' + (top > 0.95 ? "Almost all the weight on one option: softmax has become nearly all-or-nothing." : top - 1 / s.length < 0.05 ? "Close to equal weights: the scores barely distinguish the options." : Math.min.apply(null, p) < 0.01 ? "Low-scoring options get almost no weight — they are effectively ignored." : "Higher scores get more weight, but every option keeps some.") + ' Lower temperature sharpens; higher temperature flattens. Adding the same number to every score changes nothing.</p>';
    });
  };

  W["standardise"] = function (el) {
    var out = shell(el, "standardise with training statistics", txt("tr", "training tenure values (months)", "3, 12, 24") + num("x", "a new customer's tenure", 60),
      '<div class="wi-acts">' + btn("Add a 120-month customer to training", "out") + btn("Reset", "reset") + '</div>');
    acts(el, { out: function () { setVals(el, { tr: "3, 12, 24, 120" }); }, reset: function () { setVals(el, { tr: "3, 12, 24", x: 60 }); } });
    wire(el, function () {
      var t = list(tv(el, "tr")), x = val(el, "x"); if (t.length < 2) { out.innerHTML = "<p>Enter at least two training values.</p>"; return; }
      var m = mean(t), sd = pstd(t); if (!(sd > 0)) { out.innerHTML = "<p>The training values are all equal, so the standard deviation is 0 and z can't be computed.</p>"; return; }
      var z = (x - m) / sd, s = t.slice().sort(function (a, b) { return a - b; }), med = s.length % 2 ? s[(s.length - 1) / 2] : (s[s.length / 2 - 1] + s[s.length / 2]) / 2;
      out.innerHTML = '<p>Training mean <b>' + f(m, 2) + '</b>, standard deviation <b>' + f(sd, 2) + '</b> (median ' + f(med, 2) + ')</p>' +
        '<p>Training z-scores: ' + t.map(function (v) { return f((v - m) / sd, 2); }).join(", ") + '</p>' +
        '<p>New customer: z = (' + f(x) + ' − ' + f(m, 2) + ') / ' + f(sd, 2) + ' = <b>' + f(z, 2) + '</b></p>' +
        '<p class="wi-note">' + (Math.abs(z) > 3 ? "|z| > 3: far outside the training range — the model is being asked to extrapolate. " : "") + (Math.abs(m - med) > 0.25 * sd ? "The mean and median are far apart: an outlier is stretching the scale. A robust scaler (median and IQR) would cope better." : "Always reuse these training statistics for test and new data.") + '</p>';
    });
  };

  W["fairmetrics"] = function (el) {
    var g = ["A", "B"], ins = "";
    g.forEach(function (k, i) { var d = i ? [12, 4, 8, 76] : [40, 5, 10, 45]; ins += num("tp" + k, "group " + k + " TP", d[0], 1) + num("fp" + k, "group " + k + " FP", d[1], 1) + num("fn" + k, "group " + k + " FN", d[2], 1) + num("tn" + k, "group " + k + " TN", d[3], 1); });
    var out = shell(el, "audit two groups — change the counts", ins,
      '<div class="wi-acts">' + btn("Lower B's threshold (approve 32)", "lower") + btn("Small group B (10 people)", "small") + btn("Reset", "reset") + '</div>');
    acts(el, { lower: function () { setVals(el, { tpB: 16, fpB: 16, fnB: 4, tnB: 64 }); }, small: function () { setVals(el, { tpB: 1, fpB: 1, fnB: 1, tnB: 7 }); }, reset: function () { setVals(el, { tpA: 40, fpA: 5, fnA: 10, tnA: 45, tpB: 12, fpB: 4, fnB: 8, tnB: 76 }); } });
    function m(k) { var tp = val(el, "tp" + k), fp = val(el, "fp" + k), fn = val(el, "fn" + k), tn = val(el, "tn" + k), n = tp + fp + fn + tn;
      return { n: n, base: (tp + fn) / n, sel: (tp + fp) / n, tpr: tp + fn ? tp / (tp + fn) : NaN, fpr: fp + tn ? fp / (fp + tn) : NaN, ppv: tp + fp ? tp / (tp + fp) : NaN, acc: (tp + tn) / n }; }
    wire(el, function () {
      var A = m("A"), B = m("B"); if (!(A.n > 0 && B.n > 0)) { out.innerHTML = "<p>Each group needs some people.</p>"; return; }
      var rows = [["group size", "n", 0], ["base rate (would repay)", "base", 2], ["selection rate", "sel", 3], ["true-positive rate", "tpr", 3], ["false-positive rate", "fpr", 3], ["precision", "ppv", 3], ["accuracy", "acc", 3]];
      var ratio = Math.min(A.sel, B.sel) / Math.max(A.sel, B.sel);
      out.innerHTML = '<div class="table-scroll"><table class="tbl"><thead><tr><th>measure</th><th>group A</th><th>group B</th></tr></thead><tbody>' +
        rows.map(function (r) { return "<tr><td>" + r[0] + "</td><td>" + f(A[r[1]], 3) + "</td><td>" + f(B[r[1]], 3) + "</td></tr>"; }).join("") + '</tbody></table></div>' +
        '<p>Demographic-parity ratio <b>' + f(ratio) + '</b> ' + (ratio >= 0.8 ? "(passes the four-fifths rule of thumb)" : "(below 0.8)") + ' · TPR gap ' + f(Math.abs(A.tpr - B.tpr)) + ' · FPR gap ' + f(Math.abs(A.fpr - B.fpr)) + '</p>' +
        '<p class="wi-note">' + (Math.min(A.n, B.n) < 30 ? "One group is very small: a single person changes its rates by " + f(100 / Math.min(A.n, B.n), 0) + " points. Don't draw conclusions without a confidence interval." :
          "Notice that no setting makes every row equal while the base rates differ — that's the impossibility result.") + '</p>';
    });
  };

  window.MLA_WHATIF = W;
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".whatif[data-whatif]").forEach(function (el) { var fn = W[el.getAttribute("data-whatif")]; if (fn) { try { fn(el); } catch (e) { el.textContent = "Calculator failed to load: " + e.message; } } });
  });
})();
