/* ML Academy — interactive demos (plain canvas, no dependencies) */
(function () {
  "use strict";

  function css(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
  function light() { return document.documentElement.getAttribute("data-theme") === "light"; }
  function colors() {
    return { bg: css("--bg-2"), grid: css("--border"), text: css("--muted"), ink: css("--text"),
             accent: css("--accent"), accent2: css("--accent-2"), warn: css("--warn"), bad: light() ? "#dc2626" : "#f87171", violet: light() ? "#7c3aed" : "#a78bfa" };
  }

  // Build demo chrome: title, canvas, controls, readout
  function shell(el, title, aspect) {
    el.innerHTML = "";
    var head = document.createElement("div"); head.className = "demo-head"; head.textContent = "Interactive · " + title;
    var canvas = document.createElement("canvas");
    var controls = document.createElement("div"); controls.className = "demo-controls";
    var readout = document.createElement("div"); readout.className = "demo-readout";
    el.appendChild(head); el.appendChild(canvas); el.appendChild(controls); el.appendChild(readout);
    var ctx = canvas.getContext("2d");
    var state = { W: 0, H: 0 };
    function resize() {
      var w = el.clientWidth, h = Math.round(w * aspect);
      var dpr = window.devicePixelRatio || 1;
      canvas.width = w * dpr; canvas.height = h * dpr; canvas.style.height = h + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      state.W = w; state.H = h;
    }
    resize();
    return { canvas: canvas, ctx: ctx, controls: controls, readout: readout, state: state, resize: resize };
  }
  function slider(parent, label, min, max, step, value, fmt, onInput) {
    var l = document.createElement("label");
    var t = document.createElement("span");
    var r = document.createElement("input");
    r.type = "range"; r.min = min; r.max = max; r.step = step; r.value = value;
    l.appendChild(document.createTextNode(label)); l.appendChild(r); l.appendChild(t);
    var show = function () { t.textContent = fmt(+r.value); };
    r.addEventListener("input", function () { show(); onInput(+r.value); });
    show(); parent.appendChild(l);
    return { input: r, set: function (v) { r.value = v; show(); } };
  }
  function button(parent, text, onClick) {
    var b = document.createElement("button"); b.type = "button"; b.textContent = text;
    b.addEventListener("click", onClick); parent.appendChild(b); return b;
  }
  // Map data coords <-> pixels
  function axes(W, H, xmin, xmax, ymin, ymax, pad) {
    pad = pad || 36;
    return {
      x: function (v) { return pad + (v - xmin) / (xmax - xmin) * (W - pad * 1.5); },
      y: function (v) { return H - pad - (v - ymin) / (ymax - ymin) * (H - pad * 1.6); },
      ix: function (px) { return xmin + (px - pad) / (W - pad * 1.5) * (xmax - xmin); },
      iy: function (py) { return ymin + (H - pad - py) / (H - pad * 1.6) * (ymax - ymin); },
      xmin: xmin, xmax: xmax, ymin: ymin, ymax: ymax, pad: pad
    };
  }
  function drawGrid(ctx, A, W, H, c, xstep, ystep, xlabel, ylabel) {
    ctx.fillStyle = c.bg; ctx.fillRect(0, 0, W, H);
    ctx.strokeStyle = c.grid; ctx.lineWidth = 1; ctx.font = "11px JetBrains Mono, monospace"; ctx.fillStyle = c.text;
    for (var x = Math.ceil(A.xmin / xstep) * xstep; x <= A.xmax + 1e-9; x += xstep) {
      ctx.beginPath(); ctx.moveTo(A.x(x), A.y(A.ymin)); ctx.lineTo(A.x(x), A.y(A.ymax)); ctx.stroke();
      ctx.fillText(+x.toFixed(2), A.x(x) - 6, H - A.pad + 16);
    }
    for (var y = Math.ceil(A.ymin / ystep) * ystep; y <= A.ymax + 1e-9; y += ystep) {
      ctx.beginPath(); ctx.moveTo(A.x(A.xmin), A.y(y)); ctx.lineTo(A.x(A.xmax), A.y(y)); ctx.stroke();
      ctx.fillText(+y.toFixed(2), 4, A.y(y) + 4);
    }
    if (xlabel) { ctx.fillText(xlabel, W - ctx.measureText(xlabel).width - 8, H - 6); }
    if (ylabel) { ctx.fillText(ylabel, A.pad + 4, 14); }
  }
  function dot(ctx, x, y, r, fill) { ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fillStyle = fill; ctx.fill(); }
  function arrow(ctx, x0, y0, x1, y1, color, width) {
    var a = Math.atan2(y1 - y0, x1 - x0), h = 11;
    ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = width || 3;
    ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1 - Math.cos(a) * h * 0.6, y1 - Math.sin(a) * h * 0.6); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x1, y1);
    ctx.lineTo(x1 - h * Math.cos(a - 0.4), y1 - h * Math.sin(a - 0.4));
    ctx.lineTo(x1 - h * Math.cos(a + 0.4), y1 - h * Math.sin(a + 0.4)); ctx.closePath(); ctx.fill();
  }
  function onResize(fn) { var t; window.addEventListener("resize", function () { clearTimeout(t); t = setTimeout(fn, 120); }); }
  function onTheme(fn) { new MutationObserver(fn).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] }); }

  // ---------------- Demo: fit a line (Lesson 1) ----------------
  function fitLine(el) {
    var S = shell(el, "fit a line by hand", 0.56);
    var X = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5];
    var Y = [2.3, 2.6, 3.9, 4.1, 5.2, 5.0, 6.4, 6.6, 7.9, 8.1];
    var w = 0.5, b = 1;
    // least squares solution
    var n = X.length, mx = X.reduce(function (s, v) { return s + v; }, 0) / n, my = Y.reduce(function (s, v) { return s + v; }, 0) / n;
    var sxy = 0, sxx = 0; for (var i = 0; i < n; i++) { sxy += (X[i] - mx) * (Y[i] - my); sxx += (X[i] - mx) * (X[i] - mx); }
    var wBest = sxy / sxx, bBest = my - wBest * mx;
    function mse(w, b) { var s = 0; for (var i = 0; i < n; i++) { var e = w * X[i] + b - Y[i]; s += e * e; } return s / n; }
    var bestMse = mse(wBest, bBest);
    var sw = slider(S.controls, "slope w", -1, 3, 0.01, w, function (v) { return v.toFixed(2); }, function (v) { w = v; draw(); });
    var sb = slider(S.controls, "bias b", -3, 5, 0.01, b, function (v) { return v.toFixed(2); }, function (v) { b = v; draw(); });
    button(S.controls, "Show best fit", function () { w = wBest; b = bBest; sw.set(w); sb.set(b); draw(); });
    button(S.controls, "Reset", function () { w = 0.5; b = 1; sw.set(w); sb.set(b); draw(); });
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx;
      var A = axes(W, H, 0, 6, 0, 10);
      drawGrid(ctx, A, W, H, c, 1, 2, "size (100 m²)", "price (100k)");
      ctx.lineWidth = 2;
      for (var i = 0; i < n; i++) {
        ctx.strokeStyle = c.bad; ctx.beginPath(); ctx.moveTo(A.x(X[i]), A.y(Y[i])); ctx.lineTo(A.x(X[i]), A.y(w * X[i] + b)); ctx.stroke();
      }
      ctx.strokeStyle = c.accent; ctx.lineWidth = 3; ctx.beginPath();
      ctx.moveTo(A.x(0), A.y(b)); ctx.lineTo(A.x(6), A.y(w * 6 + b)); ctx.stroke();
      for (i = 0; i < n; i++) dot(ctx, A.x(X[i]), A.y(Y[i]), 6, c.accent2);
      var m = mse(w, b);
      var ratio = m / bestMse;
      S.readout.innerHTML = "<span>model: <b>ŷ = " + w.toFixed(2) + "·x + " + b.toFixed(2) + "</b></span><span>MSE: <b class='" + (ratio < 1.05 ? "good" : "") + "'>" + m.toFixed(3) + "</b></span><span>best possible MSE: <b>" + bestMse.toFixed(3) + "</b></span>" +
        (ratio < 1.05 ? "<span class='good'>✓ Excellent — within 5% of the best line!</span>" : "");
    }
    draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: dot product (Lesson 2) ----------------
  function dotProduct(el) {
    var S = shell(el, "drag the arrow tips", 0.62);
    var a = { x: 3, y: 1 }, bv = { x: 1, y: 3 }, drag = null, A;
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx;
      var span = 5, ratio = W / H;
      A = axes(W, H, -span * ratio * 0.62, span * ratio * 0.62, -span * 0.75, span, 30);
      drawGrid(ctx, A, W, H, c, 1, 1);
      ctx.strokeStyle = c.text; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.moveTo(A.x(A.xmin), A.y(0)); ctx.lineTo(A.x(A.xmax), A.y(0)); ctx.moveTo(A.x(0), A.y(A.ymin)); ctx.lineTo(A.x(0), A.y(A.ymax)); ctx.stroke();
      // projection of b onto a
      var dp = a.x * bv.x + a.y * bv.y, na = Math.hypot(a.x, a.y), nb = Math.hypot(bv.x, bv.y);
      if (na > 0.01) {
        var k = dp / (na * na), px = a.x * k, py = a.y * k;
        ctx.setLineDash([5, 5]); ctx.strokeStyle = c.text; ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.moveTo(A.x(bv.x), A.y(bv.y)); ctx.lineTo(A.x(px), A.y(py)); ctx.stroke(); ctx.setLineDash([]);
        ctx.strokeStyle = c.warn; ctx.lineWidth = 5; ctx.globalAlpha = 0.6;
        ctx.beginPath(); ctx.moveTo(A.x(0), A.y(0)); ctx.lineTo(A.x(px), A.y(py)); ctx.stroke(); ctx.globalAlpha = 1;
      }
      arrow(ctx, A.x(0), A.y(0), A.x(a.x), A.y(a.y), c.accent, 3);
      arrow(ctx, A.x(0), A.y(0), A.x(bv.x), A.y(bv.y), c.violet, 3);
      ctx.font = "bold 14px Inter, sans-serif";
      ctx.fillStyle = c.accent; ctx.fillText("a", A.x(a.x) + 8, A.y(a.y) - 8);
      ctx.fillStyle = c.violet; ctx.fillText("b", A.x(bv.x) + 8, A.y(bv.y) - 8);
      dot(ctx, A.x(a.x), A.y(a.y), 7, c.accent); dot(ctx, A.x(bv.x), A.y(bv.y), 7, c.violet);
      var cos = na * nb > 0 ? dp / (na * nb) : 0, ang = Math.acos(Math.max(-1, Math.min(1, cos))) * 180 / Math.PI;
      var sign = Math.abs(dp) < 0.05 ? "perpendicular (≈ 0)" : dp > 0 ? "same general direction (> 0)" : "opposite directions (< 0)";
      S.readout.innerHTML = "<span>a = <b>(" + a.x.toFixed(1) + ", " + a.y.toFixed(1) + ")</b></span><span>b = <b>(" + bv.x.toFixed(1) + ", " + bv.y.toFixed(1) + ")</b></span>" +
        "<span>a·b = " + a.x.toFixed(1) + "×" + bv.x.toFixed(1) + " + " + a.y.toFixed(1) + "×" + bv.y.toFixed(1) + " = <b>" + dp.toFixed(2) + "</b></span>" +
        "<span>angle θ = <b>" + ang.toFixed(0) + "°</b></span><span>cos θ = <b>" + cos.toFixed(2) + "</b></span><span>→ <b>" + sign + "</b></span>";
    }
    function pos(e) { var r = S.canvas.getBoundingClientRect(); return { x: A.ix(e.clientX - r.left), y: A.iy(e.clientY - r.top) }; }
    S.canvas.addEventListener("pointerdown", function (e) {
      var p = pos(e), da = Math.hypot(p.x - a.x, p.y - a.y), db = Math.hypot(p.x - bv.x, p.y - bv.y);
      drag = da < db ? a : bv; try { S.canvas.setPointerCapture(e.pointerId); } catch (err) { /* keyboard-generated event */ }
      drag.x = Math.round(p.x * 2) / 2; drag.y = Math.round(p.y * 2) / 2; draw();
    });
    S.canvas.addEventListener("pointermove", function (e) {
      if (!drag) return; var p = pos(e);
      drag.x = Math.max(A.xmin + 0.3, Math.min(A.xmax - 0.3, Math.round(p.x * 2) / 2));
      drag.y = Math.max(A.ymin + 0.3, Math.min(A.ymax - 0.3, Math.round(p.y * 2) / 2)); draw();
    });
    S.canvas.addEventListener("pointerup", function () { drag = null; });
    button(S.controls, "Make perpendicular", function () { bv.x = -a.y; bv.y = a.x; draw(); });
    button(S.controls, "Make opposite", function () { bv.x = -a.x; bv.y = -a.y; draw(); });
    button(S.controls, "Reset", function () { a.x = 3; a.y = 1; bv.x = 1; bv.y = 3; draw(); });
    var hint = document.createElement("span"); hint.style.cssText = "font-size:.85rem;color:var(--muted)";
    hint.textContent = "Yellow = projection of b onto a"; S.controls.appendChild(hint);
    draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: tangent + gradient descent (Lesson 3) ----------------
  function tangent(el) {
    var S = shell(el, "derivative & gradient descent", 0.56);
    var f = function (x) { return (x - 1) * (x - 1) + 0.5; }, df = function (x) { return 2 * (x - 1); };
    var x0 = -1.5, lr = 0.2, trail = [];
    var sx = slider(S.controls, "point x", -2, 4, 0.01, x0, function (v) { return v.toFixed(2); }, function (v) { x0 = v; trail = []; draw(); });
    slider(S.controls, "learning rate η", 0.01, 1.05, 0.01, lr, function (v) { return v.toFixed(2); }, function (v) { lr = v; });
    button(S.controls, "Step: x ← x − η·f′(x)", function () { trail.push(x0); x0 = x0 - lr * df(x0); x0 = Math.max(-2, Math.min(4, x0)); sx.set(x0); draw(); });
    button(S.controls, "Reset", function () { x0 = -1.5; trail = []; sx.set(x0); draw(); });
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx;
      var A = axes(W, H, -2, 4, 0, 10);
      drawGrid(ctx, A, W, H, c, 1, 2, "x", "f(x)");
      ctx.strokeStyle = c.accent2; ctx.lineWidth = 3; ctx.beginPath();
      for (var px = 0; px <= 200; px++) { var x = -2 + 6 * px / 200, y = f(x); if (px === 0) ctx.moveTo(A.x(x), A.y(y)); else ctx.lineTo(A.x(x), A.y(Math.min(y, 10.5))); }
      ctx.stroke();
      // tangent
      var s = df(x0), y0 = f(x0);
      ctx.strokeStyle = c.warn; ctx.lineWidth = 2.5; ctx.beginPath();
      ctx.moveTo(A.x(x0 - 1.2), A.y(y0 - 1.2 * s)); ctx.lineTo(A.x(x0 + 1.2), A.y(y0 + 1.2 * s)); ctx.stroke();
      trail.forEach(function (t, i) { ctx.globalAlpha = 0.25 + 0.5 * i / Math.max(1, trail.length); dot(ctx, A.x(t), A.y(f(t)), 5, c.violet); });
      ctx.globalAlpha = 1;
      dot(ctx, A.x(x0), A.y(y0), 8, c.accent);
      // direction hint arrow along x axis
      if (Math.abs(s) > 0.02) { var dir = s > 0 ? -1 : 1; arrow(ctx, A.x(x0), A.y(0.4), A.x(x0) + dir * 46, A.y(0.4), c.accent, 2.5); }
      var word = Math.abs(s) < 0.02 ? "flat — this is the minimum!" : s < 0 ? "negative → going down; move RIGHT" : "positive → going up; move LEFT";
      S.readout.innerHTML = "<span>x = <b>" + x0.toFixed(3) + "</b></span><span>f(x) = <b>" + y0.toFixed(3) + "</b></span><span>slope f′(x) = 2(x−1) = <b>" + s.toFixed(3) + "</b></span><span>→ <b class='" + (Math.abs(s) < 0.02 ? "good" : "") + "'>" + word + "</b></span>" +
        (lr > 1 ? "<span style='color:#f87171'>η &gt; 1 here: steps overshoot and grow — try it!</span>" : "") + (trail.length ? "<span>steps taken: <b>" + trail.length + "</b></span>" : "");
    }
    draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: Bayes with 1000 people (Lesson 4) ----------------
  function bayes(el) {
    var S = shell(el, "Bayes' theorem with 1,000 people", 0.44);
    var prev = 0.01, sens = 0.9, fpr = 0.05;
    slider(S.controls, "disease rate", 0.001, 0.3, 0.001, prev, function (v) { return (v * 100).toFixed(1) + "%"; }, function (v) { prev = v; draw(); });
    slider(S.controls, "sensitivity", 0.5, 1, 0.01, sens, function (v) { return (v * 100).toFixed(0) + "%"; }, function (v) { sens = v; draw(); });
    slider(S.controls, "false-positive rate", 0, 0.3, 0.005, fpr, function (v) { return (v * 100).toFixed(1) + "%"; }, function (v) { fpr = v; draw(); });
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx;
      ctx.fillStyle = c.bg; ctx.fillRect(0, 0, W, H);
      var sick = Math.round(1000 * prev), tp = Math.round(sick * sens), healthy = 1000 - sick, fp = Math.round(healthy * fpr);
      var cols = 50, rows = 20, legendH = 30, cell = Math.min((W - 20) / cols, (H - 20 - legendH) / rows), ox = (W - cell * cols) / 2, oy = 10;
      // order: TP, FN (sick), FP, TN
      for (var i = 0; i < 1000; i++) {
        var col, kind;
        if (i < tp) { col = c.accent; } else if (i < sick) { col = c.violet; } else if (i < sick + fp) { col = c.bad; } else { col = c.grid; }
        var r = Math.floor(i / cols), k = i % cols;
        ctx.fillStyle = col; ctx.fillRect(ox + k * cell + 1, oy + r * cell + 1, cell - 2, cell - 2);
      }
      var items = [[c.accent, "sick & test +"], [c.violet, "sick & test −"], [c.bad, "healthy & test +"], [c.grid, "healthy & test −"]];
      ctx.font = "12px Inter, sans-serif"; var lx = ox, ly = oy + rows * cell + 20;
      items.forEach(function (it) { ctx.fillStyle = it[0]; ctx.fillRect(lx, ly - 10, 12, 12); ctx.fillStyle = c.text; ctx.fillText(it[1], lx + 17, ly); lx += ctx.measureText(it[1]).width + 40; });
      var pos = tp + fp, post = pos ? tp / pos : 0;
      var exact = (sens * prev) / (sens * prev + fpr * (1 - prev) || 1);
      S.readout.innerHTML = "<span>sick: <b>" + sick + "</b></span><span>positive tests: <b>" + pos + "</b> (" + tp + " sick + " + fp + " healthy)</span>" +
        "<span>P(sick | positive) = " + tp + " / " + pos + " ≈ <b class='good'>" + (post * 100).toFixed(1) + "%</b></span><span>exact Bayes: <b>" + (exact * 100).toFixed(1) + "%</b></span>";
    }
    draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: normal distribution sampling (Lesson 4) ----------------
  function normal(el) {
    var S = shell(el, "sampling a normal distribution", 0.5);
    var mu = 0, sigma = 1, samples = [];
    function randn() { var u = 0, v = 0; while (u === 0) u = Math.random(); while (v === 0) v = Math.random(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
    slider(S.controls, "mean μ", -2, 2, 0.1, mu, function (v) { return v.toFixed(1); }, function (v) { mu = v; samples = []; draw(); });
    slider(S.controls, "std σ", 0.4, 2, 0.1, sigma, function (v) { return v.toFixed(1); }, function (v) { sigma = v; samples = []; draw(); });
    button(S.controls, "+10 samples", function () { add(10); });
    button(S.controls, "+1,000 samples", function () { add(1000); });
    button(S.controls, "Clear", function () { samples = []; draw(); });
    function add(k) { for (var i = 0; i < k; i++) samples.push(mu + sigma * randn()); draw(); }
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx;
      var A = axes(W, H, -6, 6, 0, 0.5);
      drawGrid(ctx, A, W, H, c, 1, 0.1, "x", "density");
      var bw = 0.25, bins = {};
      samples.forEach(function (s) { var k = Math.floor(s / bw); bins[k] = (bins[k] || 0) + 1; });
      ctx.fillStyle = c.accent; ctx.globalAlpha = 0.55;
      Object.keys(bins).forEach(function (k) {
        var d = bins[k] / (samples.length * bw), x0 = k * bw;
        if (x0 < -6 || x0 > 6) return;
        ctx.fillRect(A.x(x0) + 1, A.y(Math.min(d, 0.5)), A.x(x0 + bw) - A.x(x0) - 2, A.y(0) - A.y(Math.min(d, 0.5)));
      });
      ctx.globalAlpha = 1;
      // shaded ±1σ band
      ctx.fillStyle = c.accent2; ctx.globalAlpha = 0.08; ctx.fillRect(A.x(mu - sigma), A.y(0.5), A.x(mu + sigma) - A.x(mu - sigma), A.y(0) - A.y(0.5)); ctx.globalAlpha = 1;
      ctx.strokeStyle = c.accent2; ctx.lineWidth = 2.5; ctx.beginPath();
      for (var px = 0; px <= 300; px++) {
        var x = -6 + 12 * px / 300, y = Math.exp(-((x - mu) * (x - mu)) / (2 * sigma * sigma)) / (sigma * Math.sqrt(2 * Math.PI));
        if (px === 0) ctx.moveTo(A.x(x), A.y(Math.min(y, 0.5))); else ctx.lineTo(A.x(x), A.y(Math.min(y, 0.5)));
      }
      ctx.stroke();
      var n = samples.length, within = 0, mean = 0, v = 0;
      samples.forEach(function (s) { mean += s; if (Math.abs(s - mu) <= sigma) within++; }); mean = n ? mean / n : 0;
      samples.forEach(function (s) { v += (s - mean) * (s - mean); }); var sd = n ? Math.sqrt(v / n) : 0;
      S.readout.innerHTML = "<span>samples: <b>" + n + "</b></span><span>sample mean: <b>" + (n ? mean.toFixed(3) : "—") + "</b></span><span>sample std: <b>" + (n ? sd.toFixed(3) : "—") + "</b></span>" +
        "<span>within ±1σ (shaded): <b class='good'>" + (n ? (100 * within / n).toFixed(1) + "%" : "—") + "</b> (theory ≈ 68.3%)</span>";
    }
    draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------- helpers for batch 2 ----------
  function seeded(seed) { var s = seed >>> 0; return function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
  function gaussFrom(rand) { return function () { var u = 0, v = 0; while (u === 0) u = rand(); v = rand(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }; }
  function solve(A, bvec) { // Gaussian elimination with partial pivoting
    var n = bvec.length, M = A.map(function (r, i) { return r.slice().concat([bvec[i]]); });
    for (var c = 0; c < n; c++) {
      var piv = c; for (var r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[piv][c])) piv = r;
      var t = M[c]; M[c] = M[piv]; M[piv] = t;
      if (Math.abs(M[c][c]) < 1e-14) M[c][c] = 1e-14;
      for (r = c + 1; r < n; r++) { var f = M[r][c] / M[c][c]; for (var k = c; k <= n; k++) M[r][k] -= f * M[c][k]; }
    }
    var x = new Array(n);
    for (var i = n - 1; i >= 0; i--) { var s = M[i][n]; for (var j = i + 1; j < n; j++) s -= M[i][j] * x[j]; x[i] = s / M[i][i]; }
    return x;
  }
  function polyFit(xs, ys, d) {
    var A = [], bb = [];
    for (var i = 0; i <= d; i++) { A.push(new Array(d + 1).fill(0)); bb.push(0); }
    xs.forEach(function (x, k) {
      var pw = []; for (var i = 0; i <= d; i++) pw.push(Math.pow(x, i));
      for (i = 0; i <= d; i++) { bb[i] += pw[i] * ys[k]; for (var j = 0; j <= d; j++) A[i][j] += pw[i] * pw[j]; }
    });
    for (i = 0; i <= d; i++) A[i][i] += 1e-10;
    return solve(A, bb);
  }
  function polyEval(c, x) { var s = 0, p = 1; for (var i = 0; i < c.length; i++) { s += c[i] * p; p *= x; } return s; }

  // ---------------- Demo: overfitting (Lesson 5) ----------------
  function overfit(el) {
    var S = shell(el, "underfitting vs overfitting", 0.58);
    var deg = 1, seed = 7, tr, te, errs;
    var truth = function (x) { return Math.sin(2.6 * x) + 0.3 * x; };
    function makeData() {
      var r = seeded(seed), g = gaussFrom(r); tr = { x: [], y: [] }; te = { x: [], y: [] };
      for (var i = 0; i < 12; i++) { var x = -1 + 2 * (i + 0.15 + 0.7 * r()) / 12; tr.x.push(x); tr.y.push(truth(x) + 0.25 * g()); }
      for (i = 0; i < 30; i++) { x = -1 + 2 * r(); te.x.push(x); te.y.push(truth(x) + 0.25 * g()); }
      errs = [];
      for (var d = 0; d <= 11; d++) errs.push(evalDeg(d));
    }
    function mse(c, D) { var s = 0; D.x.forEach(function (x, i) { var e = polyEval(c, x) - D.y[i]; s += e * e; }); return s / D.x.length; }
    function evalDeg(d) { var c = polyFit(tr.x, tr.y, d); return { c: c, tr: mse(c, tr), te: mse(c, te) }; }
    slider(S.controls, "polynomial degree", 0, 11, 1, deg, function (v) { return String(v); }, function (v) { deg = v; draw(); });
    button(S.controls, "New random data", function () { seed = Math.floor(Math.random() * 1e9); makeData(); draw(); });
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx;
      var mainW = W * 0.66;
      var A = axes(mainW, H, -1, 1, -2, 2, 34);
      drawGrid(ctx, A, mainW, H, c, 0.5, 1, "x", "y");
      var e = errs[deg];
      // true curve (dashed)
      ctx.setLineDash([6, 5]); ctx.strokeStyle = c.text; ctx.lineWidth = 1.5; ctx.beginPath();
      for (var px = 0; px <= 200; px++) { var x = -1 + 2 * px / 200; px ? ctx.lineTo(A.x(x), A.y(truth(x))) : ctx.moveTo(A.x(x), A.y(truth(x))); } ctx.stroke(); ctx.setLineDash([]);
      // fitted
      ctx.save(); ctx.beginPath(); ctx.rect(A.x(-1), A.y(2), A.x(1) - A.x(-1), A.y(-2) - A.y(2)); ctx.clip();
      ctx.strokeStyle = c.accent; ctx.lineWidth = 3; ctx.beginPath();
      for (px = 0; px <= 300; px++) { x = -1 + 2 * px / 300; var y = Math.max(-5, Math.min(5, polyEval(e.c, x))); px ? ctx.lineTo(A.x(x), A.y(y)) : ctx.moveTo(A.x(x), A.y(y)); } ctx.stroke(); ctx.restore();
      te.x.forEach(function (x, i) { dot(ctx, A.x(x), A.y(te.y[i]), 4, c.warn); });
      tr.x.forEach(function (x, i) { dot(ctx, A.x(x), A.y(tr.y[i]), 6, c.accent2); });
      // error-vs-degree chart
      var ox = mainW + 10, cw = W - ox - 8;
      ctx.fillStyle = c.bg; ctx.fillRect(mainW, 0, W - mainW, H);
      var maxE = 0.6, B = { x: function (d) { return ox + 26 + d / 11 * (cw - 34); }, y: function (v) { return H - 34 - Math.min(v, maxE) / maxE * (H - 70); } };
      ctx.strokeStyle = c.grid; ctx.lineWidth = 1; ctx.strokeRect(ox + 26, 36, cw - 34, H - 70);
      ctx.fillStyle = c.text; ctx.font = "11px Inter, sans-serif"; ctx.fillText("error vs degree", ox + 26, 24);
      ctx.fillText("0", ox + 14, H - 30); ctx.fillText("11", B.x(11) - 6, H - 18); ctx.fillText("degree", B.x(5) - 14, H - 18);
      [["tr", c.accent2], ["te", c.warn]].forEach(function (k) {
        ctx.strokeStyle = k[1]; ctx.lineWidth = 2; ctx.beginPath();
        errs.forEach(function (er, d) { d ? ctx.lineTo(B.x(d), B.y(er[k[0]])) : ctx.moveTo(B.x(d), B.y(er[k[0]])); }); ctx.stroke();
      });
      ctx.strokeStyle = c.accent; ctx.setLineDash([3, 3]); ctx.beginPath(); ctx.moveTo(B.x(deg), 36); ctx.lineTo(B.x(deg), H - 34); ctx.stroke(); ctx.setLineDash([]);
      var verdict = deg <= 1 ? "underfitting: too simple" : e.te > 2.5 * Math.min.apply(null, errs.map(function (q) { return q.te; })) ? "overfitting: chasing noise" : "reasonable fit";
      S.readout.innerHTML = "<span style='color:" + c.accent2 + "'>● training points (12)</span><span style='color:" + c.warn + "'>● test points (30)</span><span>- - true curve</span>" +
        "<span>train MSE: <b>" + e.tr.toFixed(3) + "</b></span><span>test MSE: <b>" + (e.te > 99 ? e.te.toExponential(1) : e.te.toFixed(3)) + "</b></span><span>→ <b>" + verdict + "</b></span>";
    }
    makeData(); draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: least squares with squares (Lesson 6) ----------------
  function leastSquares(el) {
    var S = shell(el, "click to add or remove points", 0.58);
    var P = [[1, 2], [2, 4], [3, 5], [4, 4], [5, 5]], A, showSq = true;
    var cb = document.createElement("label"); var ci = document.createElement("input"); ci.type = "checkbox"; ci.checked = true; ci.style.flex = "0";
    ci.addEventListener("change", function () { showSq = ci.checked; draw(); }); cb.appendChild(ci); cb.appendChild(document.createTextNode("show squared errors")); cb.style.flex = "0 1 auto"; S.controls.appendChild(cb);
    button(S.controls, "Add an outlier", function () { P.push([9, 1]); draw(); });
    button(S.controls, "Reset to Lesson example", function () { P = [[1, 2], [2, 4], [3, 5], [4, 4], [5, 5]]; draw(); });
    button(S.controls, "Clear", function () { P = []; draw(); });
    function fit() {
      var n = P.length; if (n < 2) return null;
      var mx = 0, my = 0; P.forEach(function (p) { mx += p[0]; my += p[1]; }); mx /= n; my /= n;
      var sxy = 0, sxx = 0, syy = 0; P.forEach(function (p) { sxy += (p[0] - mx) * (p[1] - my); sxx += (p[0] - mx) * (p[0] - mx); syy += (p[1] - my) * (p[1] - my); });
      if (sxx < 1e-9) return null; var w = sxy / sxx, b = my - w * mx, sse = 0;
      P.forEach(function (p) { var r = p[1] - (w * p[0] + b); sse += r * r; });
      return { w: w, b: b, mse: sse / n, r2: syy > 0 ? 1 - sse / syy : 1, mx: mx, my: my, sxy: sxy, sxx: sxx };
    }
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx;
      A = axes(W, H, 0, 10, 0, 8, 34);
      drawGrid(ctx, A, W, H, c, 1, 1, "x", "y");
      var f = fit();
      if (f) {
        if (showSq) P.forEach(function (p) {
          var yh = f.w * p[0] + f.b, side = Math.abs(A.y(yh) - A.y(p[1]));
          ctx.fillStyle = c.bad; ctx.globalAlpha = 0.18; ctx.fillRect(A.x(p[0]), Math.min(A.y(yh), A.y(p[1])), side, side); ctx.globalAlpha = 1;
          ctx.strokeStyle = c.bad; ctx.lineWidth = 1; ctx.strokeRect(A.x(p[0]), Math.min(A.y(yh), A.y(p[1])), side, side);
        });
        ctx.strokeStyle = c.accent; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(A.x(0), A.y(f.b)); ctx.lineTo(A.x(10), A.y(f.w * 10 + f.b)); ctx.stroke();
        ctx.strokeStyle = c.text; ctx.setLineDash([3, 4]); ctx.beginPath(); ctx.arc(A.x(f.mx), A.y(f.my), 9, 0, 7); ctx.stroke(); ctx.setLineDash([]);
      }
      P.forEach(function (p) { dot(ctx, A.x(p[0]), A.y(p[1]), 6, c.accent2); });
      S.readout.innerHTML = f ? "<span>points: <b>" + P.length + "</b></span><span>w = Σ(x−x̄)(y−ȳ) / Σ(x−x̄)² = " + f.sxy.toFixed(2) + " / " + f.sxx.toFixed(2) + " = <b>" + f.w.toFixed(3) + "</b></span><span>b = ȳ − w·x̄ = <b>" + f.b.toFixed(3) + "</b></span><span>MSE: <b>" + f.mse.toFixed(3) + "</b></span><span>R²: <b>" + f.r2.toFixed(3) + "</b></span><span>(dashed circle = mean point)</span>"
        : "<span>Add at least two points with different x values.</span>";
    }
    S.canvas.addEventListener("pointerdown", function (e) {
      var r = S.canvas.getBoundingClientRect(), px = e.clientX - r.left, py = e.clientY - r.top;
      for (var i = 0; i < P.length; i++) if (Math.hypot(A.x(P[i][0]) - px, A.y(P[i][1]) - py) < 10) { P.splice(i, 1); draw(); return; }
      var x = A.ix(px), y = A.iy(py); if (x < 0 || x > 10 || y < 0 || y > 8) return;
      P.push([Math.round(x * 10) / 10, Math.round(y * 10) / 10]); draw();
    });
    draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: gradient descent on a contour map (Lesson 7) ----------------
  function gdContour(el) {
    var S = shell(el, "gradient descent on the loss surface", 0.5);
    var X0 = [1, 2, 3, 4, 5], Y = [2, 4, 5, 4, 5], std = false, lr = 0.03, w = -0.8, b = 0.2, path = [], timer = null, diverged = false;
    var mean = 3, sd = Math.sqrt(2);
    function xs() { return X0.map(function (x) { return std ? (x - mean) / sd : x; }); }
    function loss(w, b) { var X = xs(), s = 0; for (var i = 0; i < 5; i++) { var e = w * X[i] + b - Y[i]; s += e * e; } return s / 5; }
    function grad(w, b) { var X = xs(), gw = 0, gb = 0; for (var i = 0; i < 5; i++) { var e = w * X[i] + b - Y[i]; gw += 2 * e * X[i] / 5; gb += 2 * e / 5; } return [gw, gb]; }
    var WR = [-1.5, 3], BR = [-1, 5.5], heat = null, heatKey = "";
    slider(S.controls, "learning rate η", 0.001, 0.1, 0.001, lr, function (v) { return v.toFixed(3); }, function (v) { lr = v; });
    button(S.controls, "Step", function () { step(1); draw(); });
    var runBtn = button(S.controls, "Run 200 steps", function () { run(200); });
    button(S.controls, "Reset", function () { stop(); w = -0.8; b = 0.2; path = []; diverged = false; draw(); });
    var cb = document.createElement("label"); var ci = document.createElement("input"); ci.type = "checkbox"; ci.style.flex = "0";
    ci.addEventListener("change", function () { std = ci.checked; stop(); w = -0.8; b = 0.2; path = []; diverged = false; heat = null; draw(); });
    cb.appendChild(ci); cb.appendChild(document.createTextNode("standardise x")); cb.style.flex = "0 1 auto"; S.controls.appendChild(cb);
    function step(k) {
      for (var i = 0; i < k && !diverged; i++) {
        path.push([w, b]); var g = grad(w, b); w -= lr * g[0]; b -= lr * g[1];
        if (!isFinite(w) || Math.abs(w) > 1e4 || Math.abs(b) > 1e4) { diverged = true; }
      }
      if (path.length > 2000) path = path.slice(-2000);
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    function run(n) { stop(); var left = n; timer = setInterval(function () { step(2); left -= 2; draw(); if (left <= 0 || diverged) stop(); }, 16); }
    function optimum() { // closed form in current coordinates
      var X = xs(), mx = X.reduce(function (s, v) { return s + v; }, 0) / 5, my = 4, sxy = 0, sxx = 0;
      for (var i = 0; i < 5; i++) { sxy += (X[i] - mx) * (Y[i] - my); sxx += (X[i] - mx) * (X[i] - mx); } var ww = sxy / sxx; return [ww, my - ww * mx];
    }
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx;
      ctx.fillStyle = c.bg; ctx.fillRect(0, 0, W, H);
      var LW = Math.floor(W * 0.55), pad = 30;
      var Ax = function (v) { return pad + (v - WR[0]) / (WR[1] - WR[0]) * (LW - pad - 8); };
      var Ay = function (v) { return H - pad - (v - BR[0]) / (BR[1] - BR[0]) * (H - pad - 10); };
      // heat / contour bands
      var key = W + "x" + H + std + document.documentElement.getAttribute("data-theme");
      if (!heat || heatKey !== key) {
        heat = document.createElement("canvas"); heat.width = LW; heat.height = H; var hc = heat.getContext("2d"); heatKey = key;
        var cell = 3, acc = c.accent2;
        for (var py = 10; py < H - pad; py += cell) for (var px = pad; px < LW - 8; px += cell) {
          var ww = WR[0] + (px - pad) / (LW - pad - 8) * (WR[1] - WR[0]), bb = BR[0] + (H - pad - py) / (H - pad - 10) * (BR[1] - BR[0]);
          var Lv = Math.log(loss(ww, bb) + 1e-3), band = Math.floor(Lv * 3);
          hc.fillStyle = acc; hc.globalAlpha = Math.max(0.03, 0.42 - 0.035 * (Lv + 1)) * (band % 2 ? 1 : 0.7);
          hc.fillRect(px, py, cell, cell);
        }
      }
      ctx.drawImage(heat, 0, 0, LW, H);
      ctx.strokeStyle = c.grid; ctx.strokeRect(pad, 10, LW - pad - 8, H - pad - 10);
      ctx.fillStyle = c.text; ctx.font = "11px JetBrains Mono, monospace";
      ctx.fillText("w →", LW - 40, H - 8); ctx.fillText("b ↑", 4, 20);
      [-1, 0, 1, 2, 3].forEach(function (v) { ctx.fillText(v, Ax(v) - 3, H - pad + 14); });
      [0, 2, 4].forEach(function (v) { ctx.fillText(v, pad - 14, Ay(v) + 4); });
      var o = optimum();
      ctx.fillStyle = c.warn; ctx.font = "18px sans-serif"; ctx.fillText("★", Ax(o[0]) - 7, Ay(o[1]) + 6);
      ctx.strokeStyle = c.violet; ctx.lineWidth = 2; ctx.beginPath();
      var pts = path.concat([[w, b]]);
      pts.forEach(function (p, i) { var X = Math.max(-50, Math.min(LW + 50, Ax(p[0]))), Yp = Math.max(-50, Math.min(H + 50, Ay(p[1]))); i ? ctx.lineTo(X, Yp) : ctx.moveTo(X, Yp); }); ctx.stroke();
      dot(ctx, Math.max(0, Math.min(LW, Ax(w))), Math.max(0, Math.min(H, Ay(b))), 6, c.accent);
      // right panel: data + line in original x
      var R = axes(W - LW, H, 0, 6, 0, 7, 30); ctx.save(); ctx.translate(LW, 0);
      ctx.strokeStyle = c.grid; ctx.lineWidth = 1; ctx.strokeRect(R.x(0), R.y(7), R.x(6) - R.x(0), R.y(0) - R.y(7));
      ctx.fillStyle = c.text; ctx.font = "11px JetBrains Mono, monospace"; [0, 2, 4, 6].forEach(function (v) { ctx.fillText(v, R.x(v) - 3, H - 14); });
      ctx.save(); ctx.beginPath(); ctx.rect(R.x(0), R.y(7), R.x(6) - R.x(0), R.y(0) - R.y(7)); ctx.clip();
      ctx.strokeStyle = c.accent; ctx.lineWidth = 3; ctx.beginPath();
      var pred = function (x) { return w * (std ? (x - mean) / sd : x) + b; };
      ctx.moveTo(R.x(0), R.y(pred(0))); ctx.lineTo(R.x(6), R.y(pred(6))); ctx.stroke(); ctx.restore();
      X0.forEach(function (x, i) { dot(ctx, R.x(x), R.y(Y[i]), 5, c.accent2); }); ctx.restore();
      var L = loss(w, b);
      S.readout.innerHTML = "<span>step: <b>" + path.length + "</b></span><span>w = <b>" + (isFinite(w) ? w.toFixed(3) : "∞") + "</b></span><span>b = <b>" + (isFinite(b) ? b.toFixed(3) : "∞") + "</b></span><span>loss = <b class='" + (L - 0.48 < 0.001 ? "good" : "") + "'>" + (isFinite(L) && L < 1e6 ? L.toFixed(4) : "exploded") + "</b></span><span>minimum loss: <b>0.4800</b> at ★</span>" +
        (diverged ? "<span style='color:#f87171'>Diverged! The learning rate is too large for this landscape.</span>" : "");
    }
    draw(); onResize(function () { S.resize(); heat = null; draw(); }); onTheme(function () { heat = null; draw(); });
  }

  // ---------------- Demo: logistic regression classifier (Lesson 8) ----------------
  function logistic(el) {
    var S = shell(el, "click to add points, then train", 0.62);
    var preset = function () {
      var r = seeded(3), g = gaussFrom(r), P = [];
      for (var i = 0; i < 18; i++) P.push([-0.35 + 0.28 * g(), -0.25 + 0.28 * g(), 0]);
      for (i = 0; i < 18; i++) P.push([0.35 + 0.28 * g(), 0.3 + 0.28 * g(), 1]);
      return P;
    };
    var P = preset(), cls = 1, w1 = 0, w2 = 0, b = 0, steps = 0, timer = null, A;
    var bA = button(S.controls, "Adding: class 1 (green)", function () { cls = 1 - cls; bA.textContent = cls ? "Adding: class 1 (green)" : "Adding: class 0 (purple)"; });
    button(S.controls, "Train", function () { run(400); });
    button(S.controls, "Reset weights", function () { stop(); w1 = w2 = b = 0; steps = 0; draw(); });
    button(S.controls, "Example data", function () { stop(); P = preset(); w1 = w2 = b = 0; steps = 0; draw(); });
    button(S.controls, "Clear points", function () { stop(); P = []; w1 = w2 = b = 0; steps = 0; draw(); });
    function sig(z) { return 1 / (1 + Math.exp(-z)); }
    function stats() { var L = 0, acc = 0; P.forEach(function (p) { var q = sig(w1 * p[0] + w2 * p[1] + b); q = Math.min(1 - 1e-9, Math.max(1e-9, q)); L += -(p[2] * Math.log(q) + (1 - p[2]) * Math.log(1 - q)); if ((q >= 0.5 ? 1 : 0) === p[2]) acc++; }); return { L: P.length ? L / P.length : 0, acc: P.length ? acc / P.length : 0 }; }
    function step(k) {
      if (!P.length) return; var lr = 1.5;
      for (var t = 0; t < k; t++) {
        var g1 = 0, g2 = 0, gb = 0;
        P.forEach(function (p) { var e = sig(w1 * p[0] + w2 * p[1] + b) - p[2]; g1 += e * p[0]; g2 += e * p[1]; gb += e; });
        w1 -= lr * g1 / P.length; w2 -= lr * g2 / P.length; b -= lr * gb / P.length; steps++;
      }
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    function run(n) { stop(); var left = n; timer = setInterval(function () { step(4); left -= 4; draw(); if (left <= 0) stop(); }, 16); }
    function hexToRgb(h) { h = h.replace("#", ""); if (h.length === 3) h = h.split("").map(function (ch) { return ch + ch; }).join(""); var n = parseInt(h, 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; }
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx;
      A = axes(W, H, -1.4 * W / H * 0.62, 1.4 * W / H * 0.62, -1, 1, 12);
      ctx.fillStyle = c.bg; ctx.fillRect(0, 0, W, H);
      var g = hexToRgb(c.accent.indexOf("#") === 0 ? c.accent : "#4ade80"), v = [167, 139, 250], cell = 6;
      for (var py = 0; py < H; py += cell) for (var px = 0; px < W; px += cell) {
        var q = sig(w1 * A.ix(px + cell / 2) + w2 * A.iy(py + cell / 2) + b), col = q >= 0.5 ? g : v;
        ctx.fillStyle = "rgba(" + col[0] + "," + col[1] + "," + col[2] + "," + (Math.abs(q - 0.5) * 0.55).toFixed(3) + ")"; ctx.fillRect(px, py, cell, cell);
      }
      if (Math.abs(w2) > 1e-6 || Math.abs(w1) > 1e-6) {
        ctx.strokeStyle = c.ink; ctx.lineWidth = 2.5; ctx.beginPath();
        if (Math.abs(w2) > Math.abs(w1)) { ctx.moveTo(A.x(A.xmin), A.y(-(w1 * A.xmin + b) / w2)); ctx.lineTo(A.x(A.xmax), A.y(-(w1 * A.xmax + b) / w2)); }
        else { ctx.moveTo(A.x(-(w2 * A.ymin + b) / w1), A.y(A.ymin)); ctx.lineTo(A.x(-(w2 * A.ymax + b) / w1), A.y(A.ymax)); }
        ctx.stroke();
      }
      P.forEach(function (p) { dot(ctx, A.x(p[0]), A.y(p[1]), 7, c.bg); dot(ctx, A.x(p[0]), A.y(p[1]), 5.5, p[2] ? c.accent : c.violet); });
      var s = stats();
      S.readout.innerHTML = "<span>steps: <b>" + steps + "</b></span><span>z = <b>" + w1.toFixed(2) + "·x₁ + " + w2.toFixed(2) + "·x₂ + " + b.toFixed(2) + "</b></span><span>log loss: <b>" + s.L.toFixed(3) + "</b></span><span>accuracy: <b class='" + (s.acc === 1 ? "good" : "") + "'>" + (s.acc * 100).toFixed(0) + "%</b></span><span>line = decision boundary (p = 0.5)</span>";
    }
    S.canvas.addEventListener("pointerdown", function (e) {
      var r = S.canvas.getBoundingClientRect(); P.push([A.ix(e.clientX - r.left), A.iy(e.clientY - r.top), cls]); draw();
    });
    draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: threshold, confusion matrix & ROC (Lesson 9) ----------------
  function thresholdDemo(el) {
    var S = shell(el, "threshold, confusion matrix & ROC", 0.5);
    var thr = 0.5, sep = 0.3, neg = [], pos = [];
    function gen() {
      var r = seeded(11), g = gaussFrom(r); neg = []; pos = [];
      for (var i = 0; i < 300; i++) neg.push(Math.min(0.999, Math.max(0.001, 0.5 - sep / 2 + 0.14 * g())));
      for (i = 0; i < 100; i++) pos.push(Math.min(0.999, Math.max(0.001, 0.5 + sep / 2 + 0.14 * g())));
    }
    slider(S.controls, "threshold", 0, 1, 0.01, thr, function (v) { return v.toFixed(2); }, function (v) { thr = v; draw(); });
    slider(S.controls, "class separation", 0, 0.7, 0.01, sep, function (v) { return v.toFixed(2); }, function (v) { sep = v; gen(); draw(); });
    function counts(t) { var tp = 0, fp = 0; pos.forEach(function (s) { if (s >= t) tp++; }); neg.forEach(function (s) { if (s >= t) fp++; }); return { tp: tp, fn: pos.length - tp, fp: fp, tn: neg.length - fp }; }
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx;
      ctx.fillStyle = c.bg; ctx.fillRect(0, 0, W, H);
      var LW = W * 0.6, pad = 30, bins = 25, hn = new Array(bins).fill(0), hp = new Array(bins).fill(0);
      neg.forEach(function (s) { hn[Math.min(bins - 1, Math.floor(s * bins))]++; }); pos.forEach(function (s) { hp[Math.min(bins - 1, Math.floor(s * bins))]++; });
      var mx = Math.max.apply(null, hn.concat(hp)), bw = (LW - pad - 10) / bins, base = H - pad;
      for (var i = 0; i < bins; i++) {
        var x0 = pad + i * bw;
        ctx.globalAlpha = 0.65; ctx.fillStyle = c.violet; var hN = hn[i] / mx * (H - pad - 30); ctx.fillRect(x0 + 1, base - hN, bw - 2, hN);
        ctx.fillStyle = c.accent; var hP = hp[i] / mx * (H - pad - 30); ctx.fillRect(x0 + 1, base - hP, bw - 2, hP); ctx.globalAlpha = 1;
      }
      ctx.strokeStyle = c.grid; ctx.beginPath(); ctx.moveTo(pad, base); ctx.lineTo(LW - 10, base); ctx.stroke();
      ctx.fillStyle = c.text; ctx.font = "11px JetBrains Mono, monospace"; [0, 0.5, 1].forEach(function (v) { ctx.fillText(v, pad + v * (LW - pad - 10) - 6, base + 15); });
      ctx.fillText("model score", LW - 90, H - 4);
      var tx = pad + thr * (LW - pad - 10); ctx.strokeStyle = c.warn; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(tx, 18); ctx.lineTo(tx, base); ctx.stroke();
      ctx.fillStyle = c.warn; ctx.fillText("predict + →", tx + 5, 28); ctx.fillText("← predict −", tx - 84, 28);
      ctx.fillStyle = c.violet; ctx.fillText("■ negatives (300)", pad + 4, 44); ctx.fillStyle = c.accent; ctx.fillText("■ positives (100)", pad + 4, 58);
      // ROC
      var R0 = LW + 30, size = Math.min(W - R0 - 16, H - 60), oy = 20;
      ctx.strokeStyle = c.grid; ctx.lineWidth = 1; ctx.strokeRect(R0, oy, size, size);
      ctx.setLineDash([4, 4]); ctx.beginPath(); ctx.moveTo(R0, oy + size); ctx.lineTo(R0 + size, oy); ctx.stroke(); ctx.setLineDash([]);
      var pts = [], auc = 0, prev = null;
      for (var t = 1.001; t >= -0.001; t -= 0.005) { var k = counts(t); pts.push([k.fp / neg.length, k.tp / pos.length]); }
      ctx.strokeStyle = c.accent2; ctx.lineWidth = 2.5; ctx.beginPath();
      pts.forEach(function (p, j) { var X = R0 + p[0] * size, Y = oy + size - p[1] * size; j ? ctx.lineTo(X, Y) : ctx.moveTo(X, Y); if (prev) auc += (p[0] - prev[0]) * (p[1] + prev[1]) / 2; prev = p; });
      ctx.stroke();
      var k0 = counts(thr), fpr = k0.fp / neg.length, tpr = k0.tp / pos.length;
      dot(ctx, R0 + fpr * size, oy + size - tpr * size, 7, c.warn);
      ctx.fillStyle = c.text; ctx.font = "11px JetBrains Mono, monospace";
      ctx.fillText("ROC curve (AUC " + auc.toFixed(3) + ")", R0, oy - 6); ctx.fillText("FPR →", R0 + size - 40, oy + size + 14); ctx.save(); ctx.translate(R0 - 8, oy + size - 4); ctx.rotate(-Math.PI / 2); ctx.fillText("TPR →", 0, 0); ctx.restore();
      var prec = k0.tp + k0.fp ? k0.tp / (k0.tp + k0.fp) : 0, rec = tpr, f1 = 2 * k0.tp / (2 * k0.tp + k0.fp + k0.fn), acc = (k0.tp + k0.tn) / 400;
      S.readout.innerHTML = "<span>TP <b>" + k0.tp + "</b> · FN <b>" + k0.fn + "</b> · FP <b>" + k0.fp + "</b> · TN <b>" + k0.tn + "</b></span><span>accuracy <b>" + acc.toFixed(3) + "</b></span><span>precision <b>" + (k0.tp + k0.fp ? prec.toFixed(3) : "—") + "</b></span><span>recall <b>" + rec.toFixed(3) + "</b></span><span>F1 <b>" + f1.toFixed(3) + "</b></span><span>FPR <b>" + fpr.toFixed(3) + "</b></span>";
    }
    gen(); draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: ridge regularization (Lesson 10) ----------------
  function ridgeDemo(el) {
    var S = shell(el, "ridge regularization on a degree-9 polynomial", 0.58);
    var D = 9, logLam = -8, tr, te, curve = [];
    var truth = function (x) { return Math.sin(2.6 * x) + 0.3 * x; };
    (function () { var r = seeded(7), g = gaussFrom(r); tr = { x: [], y: [] }; te = { x: [], y: [] };
      for (var i = 0; i < 12; i++) { var x = -1 + 2 * (i + 0.15 + 0.7 * r()) / 12; tr.x.push(x); tr.y.push(truth(x) + 0.25 * g()); }
      for (i = 0; i < 30; i++) { x = -1 + 2 * r(); te.x.push(x); te.y.push(truth(x) + 0.25 * g()); } })();
    function ridgeFit(lam) {
      var A = [], bb = [], i, j;
      for (i = 0; i <= D; i++) { A.push(new Array(D + 1).fill(0)); bb.push(0); }
      tr.x.forEach(function (x, k) { var pw = []; for (var i = 0; i <= D; i++) pw.push(Math.pow(x, i)); for (i = 0; i <= D; i++) { bb[i] += pw[i] * tr.y[k]; for (var j = 0; j <= D; j++) A[i][j] += pw[i] * pw[j]; } });
      for (i = 1; i <= D; i++) A[i][i] += lam; A[0][0] += 1e-12;
      return solve(A, bb);
    }
    function mse(c, Dd) { var s = 0; Dd.x.forEach(function (x, i) { var e = polyEval(c, x) - Dd.y[i]; s += e * e; }); return s / Dd.x.length; }
    for (var L = -8; L <= 1.001; L += 0.25) { var cc = ridgeFit(Math.pow(10, L)); curve.push({ L: L, tr: mse(cc, tr), te: mse(cc, te) }); }
    slider(S.controls, "log₁₀ λ", -8, 1, 0.05, logLam, function (v) { return "λ = " + Math.pow(10, v).toExponential(0); }, function (v) { logLam = v; draw(); });
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx, mainW = W * 0.66;
      var A = axes(mainW, H, -1, 1, -2, 2, 34); drawGrid(ctx, A, mainW, H, c, 0.5, 1, "x", "y");
      var co = ridgeFit(Math.pow(10, logLam));
      ctx.setLineDash([6, 5]); ctx.strokeStyle = c.text; ctx.lineWidth = 1.5; ctx.beginPath();
      for (var px = 0; px <= 200; px++) { var x = -1 + 2 * px / 200; px ? ctx.lineTo(A.x(x), A.y(truth(x))) : ctx.moveTo(A.x(x), A.y(truth(x))); } ctx.stroke(); ctx.setLineDash([]);
      ctx.save(); ctx.beginPath(); ctx.rect(A.x(-1), A.y(2), A.x(1) - A.x(-1), A.y(-2) - A.y(2)); ctx.clip();
      ctx.strokeStyle = c.accent; ctx.lineWidth = 3; ctx.beginPath();
      for (px = 0; px <= 300; px++) { x = -1 + 2 * px / 300; var y = Math.max(-5, Math.min(5, polyEval(co, x))); px ? ctx.lineTo(A.x(x), A.y(y)) : ctx.moveTo(A.x(x), A.y(y)); } ctx.stroke(); ctx.restore();
      te.x.forEach(function (x, i) { dot(ctx, A.x(x), A.y(te.y[i]), 4, c.warn); });
      tr.x.forEach(function (x, i) { dot(ctx, A.x(x), A.y(tr.y[i]), 6, c.accent2); });
      ctx.fillStyle = c.bg; ctx.fillRect(mainW, 0, W - mainW, H);
      var ox = mainW + 36, cw = W - ox - 10, maxE = 0.6, B = { x: function (L) { return ox + (L + 8) / 9 * cw; }, y: function (v) { return H - 34 - Math.min(v, maxE) / maxE * (H - 70); } };
      ctx.strokeStyle = c.grid; ctx.lineWidth = 1; ctx.strokeRect(ox, 36, cw, H - 70);
      ctx.fillStyle = c.text; ctx.font = "11px Inter, sans-serif"; ctx.fillText("error vs λ", ox, 24); ctx.fillText("small λ", ox, H - 18); ctx.fillText("large λ", ox + cw - 40, H - 18);
      [["tr", c.accent2], ["te", c.warn]].forEach(function (k) { ctx.strokeStyle = k[1]; ctx.lineWidth = 2; ctx.beginPath(); curve.forEach(function (p, i) { i ? ctx.lineTo(B.x(p.L), B.y(p[k[0]])) : ctx.moveTo(B.x(p.L), B.y(p[k[0]])); }); ctx.stroke(); });
      ctx.strokeStyle = c.accent; ctx.setLineDash([3, 3]); ctx.beginPath(); ctx.moveTo(B.x(logLam), 36); ctx.lineTo(B.x(logLam), H - 34); ctx.stroke(); ctx.setLineDash([]);
      var norm = 0; for (var i = 1; i < co.length; i++) norm += co[i] * co[i]; norm = Math.sqrt(norm);
      var etr = mse(co, tr), ete = mse(co, te), best = Math.min.apply(null, curve.map(function (p) { return p.te; }));
      var verdict = logLam > -0.6 ? "underfitting: weights crushed" : ete > 1.8 * best ? "overfitting: λ too small" : "good balance";
      S.readout.innerHTML = "<span>train MSE <b>" + etr.toFixed(3) + "</b></span><span>test MSE <b>" + (ete > 99 ? ete.toExponential(1) : ete.toFixed(3)) + "</b></span><span>size of weights ‖w‖ <b>" + (norm > 9999 ? norm.toExponential(1) : norm.toFixed(1)) + "</b></span><span>→ <b>" + verdict + "</b></span>";
    }
    draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: kNN decision regions (Lesson 11) ----------------
  function knnDemo(el) {
    var S = shell(el, "k-nearest neighbours decision regions", 0.6);
    var k = 1, P = [], q = null, A;
    (function () { var r = seeded(5), g = gaussFrom(r), C = [[-0.5, 0.35], [0.45, 0.4], [0.05, -0.45]];
      C.forEach(function (cc, ci) { for (var i = 0; i < 22; i++) P.push([cc[0] + 0.3 * g(), cc[1] + 0.27 * g(), ci]); });
      for (var i = 0; i < 6; i++) P.push([0.9 * (r() * 2 - 1), 0.85 * (r() * 2 - 1), Math.floor(r() * 3)]); })();
    slider(S.controls, "k (neighbours)", 1, 31, 2, k, function (v) { return String(v); }, function (v) { k = v; draw(); });
    var hint = document.createElement("span"); hint.style.cssText = "font-size:.85rem;color:var(--muted)"; hint.textContent = "Click the chart to place a query point."; S.controls.appendChild(hint);
    function nearest(x, y, kk) { return P.map(function (p, i) { return [Math.hypot(p[0] - x, p[1] - y), i]; }).sort(function (a, b) { return a[0] - b[0]; }).slice(0, kk); }
    function vote(nb) { var v = [0, 0, 0]; nb.forEach(function (n) { v[P[n[1]][2]]++; }); var best = 0; for (var i = 1; i < 3; i++) if (v[i] > v[best]) best = i; return { cls: best, v: v }; }
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx, cols = [c.accent, c.violet, c.warn], cell = 7;
      A = axes(W, H, -1.25 * W / H * 0.6, 1.25 * W / H * 0.6, -1, 1, 8);
      ctx.fillStyle = c.bg; ctx.fillRect(0, 0, W, H);
      for (var py = 0; py < H; py += cell) for (var px = 0; px < W; px += cell) {
        var vv = vote(nearest(A.ix(px + cell / 2), A.iy(py + cell / 2), k)); ctx.fillStyle = cols[vv.cls]; ctx.globalAlpha = 0.16 + 0.14 * (vv.v[vv.cls] / k); ctx.fillRect(px, py, cell, cell);
      }
      ctx.globalAlpha = 1;
      if (q) { var nb = nearest(q[0], q[1], k); ctx.strokeStyle = c.ink; ctx.lineWidth = 1; nb.forEach(function (n) { ctx.beginPath(); ctx.moveTo(A.x(q[0]), A.y(q[1])); ctx.lineTo(A.x(P[n[1]][0]), A.y(P[n[1]][1])); ctx.stroke(); });
        var rad = nb[nb.length - 1][0]; ctx.setLineDash([4, 4]); ctx.beginPath(); ctx.arc(A.x(q[0]), A.y(q[1]), Math.abs(A.x(rad) - A.x(0)), 0, 7); ctx.stroke(); ctx.setLineDash([]); }
      P.forEach(function (p) { dot(ctx, A.x(p[0]), A.y(p[1]), 6.5, c.bg); dot(ctx, A.x(p[0]), A.y(p[1]), 5, cols[p[2]]); });
      var out = "<span>k = <b>" + k + "</b></span><span style='color:" + cols[0] + "'>● class A</span><span style='color:" + cols[1] + "'>● class B</span><span style='color:" + cols[2] + "'>● class C</span>";
      if (q) { var vt = vote(nearest(q[0], q[1], k)); ctx.fillStyle = c.ink; ctx.font = "bold 18px sans-serif"; ctx.fillText("✚", A.x(q[0]) - 7, A.y(q[1]) + 6);
        out += "<span>query votes: A <b>" + vt.v[0] + "</b> · B <b>" + vt.v[1] + "</b> · C <b>" + vt.v[2] + "</b> → predicted <b>" + "ABC"[vt.cls] + "</b></span>"; }
      S.readout.innerHTML = out;
    }
    S.canvas.addEventListener("pointerdown", function (e) { var r = S.canvas.getBoundingClientRect(); q = [A.ix(e.clientX - r.left), A.iy(e.clientY - r.top)]; draw(); });
    draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: Naive Bayes spam filter (Lesson 12) ----------------
  function nbDemo(el) {
    el.innerHTML = "";
    var head = document.createElement("div"); head.className = "demo-head"; head.textContent = "Interactive · a Naive Bayes spam filter";
    var controls = document.createElement("div"); controls.className = "demo-controls";
    var input = document.createElement("input"); input.type = "text"; input.value = "free money now"; input.setAttribute("aria-label", "Message to classify");
    input.style.cssText = "flex:1;min-width:200px;padding:10px 12px;border-radius:8px;border:1px solid var(--border);background:var(--bg-2);color:var(--text);font:inherit";
    controls.appendChild(input);
    var body = document.createElement("div"); body.style.cssText = "padding:14px 16px;display:grid;gap:8px";
    var readout = document.createElement("div"); readout.className = "demo-readout";
    el.appendChild(head); el.appendChild(controls); el.appendChild(body); el.appendChild(readout);
    ["win a free lunch", "team meeting now", "claim your prize"].forEach(function (t) { button(controls, t, function () { input.value = t; run(); }); });
    var spam = ["win money now", "free money offer", "win a free prize now", "claim your free prize"];
    var ham = ["meeting at noon", "lunch with the team now", "project meeting notes", "see you at lunch", "your project report is ready", "notes from the team meeting"];
    function count(docs) { var c = {}, n = 0; docs.forEach(function (d) { d.split(" ").forEach(function (w) { c[w] = (c[w] || 0) + 1; n++; }); }); return { c: c, n: n }; }
    var cs = count(spam), ch = count(ham), V = {}; Object.keys(cs.c).concat(Object.keys(ch.c)).forEach(function (w) { V[w] = 1; }); var nV = Object.keys(V).length;
    function run() {
      var words = input.value.toLowerCase().match(/[a-z]+/g) || [];
      var ls = Math.log(0.4), lh = Math.log(0.6), rows = [["(prior)", Math.log(0.4 / 0.6), "P(spam)=0.4, P(ham)=0.6"]];
      words.forEach(function (w) {
        if (!V[w]) { rows.push([w, null, "not in training vocabulary — ignored"]); return; }
        var ps = ((cs.c[w] || 0) + 1) / (cs.n + nV), ph = ((ch.c[w] || 0) + 1) / (ch.n + nV);
        ls += Math.log(ps); lh += Math.log(ph); rows.push([w, Math.log(ps / ph), "P(w|spam)=" + ps.toFixed(4) + "  P(w|ham)=" + ph.toFixed(4)]);
      });
      body.innerHTML = "";
      rows.forEach(function (r) {
        var row = document.createElement("div"); row.style.cssText = "display:grid;grid-template-columns:90px 1fr;gap:10px;align-items:center;font-size:.86rem";
        var lab = document.createElement("b"); lab.textContent = r[0]; lab.style.fontFamily = "var(--font-mono)";
        var barWrap = document.createElement("div"); barWrap.style.cssText = "position:relative;height:22px;border-left:1px solid var(--border);margin-left:50%";
        var info = document.createElement("div"); info.style.cssText = "font-size:.75rem;color:var(--muted);font-family:var(--font-mono);margin-top:2px"; info.textContent = r[2];
        var cell = document.createElement("div"); cell.appendChild(barWrap); cell.appendChild(info);
        if (r[1] !== null) { var bar = document.createElement("div"), wpx = Math.min(48, Math.abs(r[1]) * 18);
          bar.style.cssText = "position:absolute;top:3px;height:16px;border-radius:4px;width:" + wpx + "%;" + (r[1] >= 0 ? "left:0;background:var(--accent)" : "right:100%;background:#a78bfa");
          barWrap.appendChild(bar); }
        row.appendChild(lab); row.appendChild(cell); body.appendChild(row);
      });
      var p = 1 / (1 + Math.exp(lh - ls));
      readout.innerHTML = "<span>log score spam <b>" + ls.toFixed(2) + "</b></span><span>log score ham <b>" + lh.toFixed(2) + "</b></span><span>P(spam | message) = <b class='" + (p >= 0.5 ? "good" : "") + "'>" + (p * 100).toFixed(1) + "%</b></span><span>→ <b>" + (p >= 0.5 ? "SPAM" : "not spam") + "</b></span><span>(green → spam, purple → ham)</span>";
    }
    input.addEventListener("input", run); run();
  }

  // ---------------- Demo: decision tree growth (Lesson 13) ----------------
  function treeDemo(el) {
    var S = shell(el, "a decision tree carving up the space", 0.6);
    var depth = 1, P = [], A;
    (function () { var r = seeded(21), g = gaussFrom(r);
      for (var i = 0; i < 90; i++) { var x = r() * 2 - 1, y = r() * 2 - 1, cls = (y > 0.6 * x + 0.15 * Math.sin(5 * x)) ? 1 : 0; if (r() < 0.08) cls = 1 - cls; P.push([x, y, cls]); } })();
    function gini(idx) { if (!idx.length) return 0; var c = 0; idx.forEach(function (i) { c += P[i][2]; }); var p = c / idx.length; return 1 - p * p - (1 - p) * (1 - p); }
    function build(idx, d) {
      var ones = 0; idx.forEach(function (i) { ones += P[i][2]; });
      var node = { n: idx.length, pred: ones * 2 >= idx.length ? 1 : 0, p1: idx.length ? ones / idx.length : 0, g: gini(idx) };
      if (d >= depth || node.g === 0 || idx.length < 2) return node;
      var best = null;
      for (var f = 0; f < 2; f++) {
        var vals = idx.map(function (i) { return P[i][f]; }).sort(function (a, b) { return a - b; });
        for (var k = 1; k < vals.length; k++) {
          if (vals[k] === vals[k - 1]) continue; var t = (vals[k] + vals[k - 1]) / 2, L = [], R = [];
          idx.forEach(function (i) { (P[i][f] <= t ? L : R).push(i); });
          var sc = (L.length * gini(L) + R.length * gini(R)) / idx.length;
          if (!best || sc < best.sc - 1e-12) best = { f: f, t: t, sc: sc, L: L, R: R };
        }
      }
      if (!best || best.sc >= node.g - 1e-12) return node;
      node.f = best.f; node.t = best.t; node.gain = node.g - best.sc;
      node.left = build(best.L, d + 1); node.right = build(best.R, d + 1); return node;
    }
    function predict(node, x, y) { while (node.left) node = ([x, y][node.f] <= node.t) ? node.left : node.right; return node; }
    function count(node) { return node.left ? count(node.left) + count(node.right) : 1; }
    function describe(node, ind, out, lim) {
      if (out.length >= lim) return;
      if (!node.left) { out.push(ind + "→ leaf: predict " + (node.pred ? "green" : "purple") + " (" + node.n + " pts)"); return; }
      out.push(ind + "is " + "xy"[node.f] + " ≤ " + node.t.toFixed(2) + "?  gini " + node.g.toFixed(3) + " → gain " + node.gain.toFixed(3));
      describe(node.left, ind + "   yes: ", out, lim); describe(node.right, ind + "   no:  ", out, lim);
    }
    slider(S.controls, "max depth", 1, 10, 1, depth, function (v) { return String(v); }, function (v) { depth = v; draw(); });
    var list = document.createElement("pre"); list.style.cssText = "margin:0;padding:10px 16px;font-size:.78rem;line-height:1.6;border-top:1px solid var(--border);background:var(--surface);color:var(--muted);white-space:pre-wrap;max-height:180px;overflow:auto";
    el.appendChild(list);
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx, root = build(P.map(function (_, i) { return i; }), 0), cell = 5;
      A = axes(W, H, -1.25 * W / H * 0.6, 1.25 * W / H * 0.6, -1.05, 1.05, 6);
      ctx.fillStyle = c.bg; ctx.fillRect(0, 0, W, H);
      for (var py = 0; py < H; py += cell) for (var px = 0; px < W; px += cell) { var lf = predict(root, A.ix(px + 2), A.iy(py + 2)); ctx.fillStyle = lf.pred ? c.accent : c.violet; ctx.globalAlpha = 0.12 + 0.2 * Math.abs(lf.p1 - 0.5) * 2; ctx.fillRect(px, py, cell, cell); }
      ctx.globalAlpha = 1;
      P.forEach(function (p) { dot(ctx, A.x(p[0]), A.y(p[1]), 6, c.bg); dot(ctx, A.x(p[0]), A.y(p[1]), 4.5, p[2] ? c.accent : c.violet); });
      var acc = 0; P.forEach(function (p) { if (predict(root, p[0], p[1]).pred === p[2]) acc++; });
      S.readout.innerHTML = "<span>depth limit <b>" + depth + "</b></span><span>leaves <b>" + count(root) + "</b></span><span>training accuracy <b class='" + (acc === P.length ? "good" : "") + "'>" + (100 * acc / P.length).toFixed(0) + "%</b></span>" + (depth >= 7 ? "<span style='color:#f87171'>tiny boxes around single points = overfitting</span>" : "");
      var out = []; describe(root, "", out, 9); list.textContent = out.join("\n") + (out.length >= 9 ? "\n…" : "");
    }
    draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: gradient boosting with stumps (Lesson 14) ----------------
  function boostingDemo(el) {
    var S = shell(el, "gradient boosting, one stump at a time", 0.62);
    var X = [], Y = [], lr = 0.3, F0, stumps = [];
    (function () { var r = seeded(9), g = gaussFrom(r); for (var i = 0; i < 40; i++) { var x = 10 * (i + r()) / 40; X.push(x); Y.push(Math.sin(x) * 2 + 0.25 * x + 0.35 * g()); } })();
    F0 = Y.reduce(function (s, v) { return s + v; }, 0) / Y.length;
    function F(x) { var s = F0; stumps.forEach(function (st) { s += st.lr * (x <= st.t ? st.l : st.r); }); return s; }
    function resid() { return Y.map(function (y, i) { return y - F(X[i]); }); }
    function addStump() {
      var r = resid(), best = null;
      for (var k = 1; k < X.length; k++) {
        var t = (X[k] + X[k - 1]) / 2, sl = 0, nl = 0, sr = 0, nr = 0;
        for (var i = 0; i < X.length; i++) { if (X[i] <= t) { sl += r[i]; nl++; } else { sr += r[i]; nr++; } }
        var l = sl / nl, rr = sr / nr, sse = 0; for (i = 0; i < X.length; i++) { var e = r[i] - (X[i] <= t ? l : rr); sse += e * e; }
        if (!best || sse < best.sse) best = { t: t, l: l, r: rr, sse: sse };
      }
      best.lr = lr; stumps.push(best);
    }
    slider(S.controls, "learning rate η", 0.05, 1, 0.05, lr, function (v) { return v.toFixed(2); }, function (v) { lr = v; });
    button(S.controls, "+1 tree", function () { addStump(); draw(); });
    button(S.controls, "+10 trees", function () { for (var i = 0; i < 10; i++) addStump(); draw(); });
    button(S.controls, "+100 trees", function () { for (var i = 0; i < 100; i++) addStump(); draw(); });
    button(S.controls, "Reset", function () { stumps = []; draw(); });
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx, topH = Math.round(H * 0.66);
      var A = axes(W, topH, 0, 10, -3, 5, 30); drawGrid(ctx, A, W, topH, c, 2, 2, "x", "y");
      ctx.strokeStyle = c.accent; ctx.lineWidth = 3; ctx.beginPath();
      for (var px = 0; px <= 400; px++) { var x = 10 * px / 400; px ? ctx.lineTo(A.x(x), A.y(F(x))) : ctx.moveTo(A.x(x), A.y(F(x))); } ctx.stroke();
      X.forEach(function (x, i) { dot(ctx, A.x(x), A.y(Y[i]), 4.5, c.accent2); });
      ctx.fillStyle = c.bg; ctx.fillRect(0, topH, W, H - topH);
      var r = resid(), B = axes(W, H - topH, 0, 10, -3, 3, 30);
      ctx.save(); ctx.translate(0, topH);
      ctx.strokeStyle = c.grid; ctx.beginPath(); ctx.moveTo(B.x(0), B.y(0)); ctx.lineTo(B.x(10), B.y(0)); ctx.stroke();
      ctx.fillStyle = c.text; ctx.font = "11px Inter, sans-serif"; ctx.fillText("residuals y − F(x) — what the next tree will fit", B.x(0), 14);
      r.forEach(function (v, i) { var vv = Math.max(-3, Math.min(3, v)); ctx.fillStyle = v >= 0 ? c.accent : c.bad; ctx.fillRect(B.x(X[i]) - 3, Math.min(B.y(0), B.y(vv)), 6, Math.abs(B.y(vv) - B.y(0))); });
      ctx.restore();
      var mse = r.reduce(function (s, v) { return s + v * v; }, 0) / r.length;
      S.readout.innerHTML = "<span>trees <b>" + stumps.length + "</b></span><span>start F₀ = mean = <b>" + F0.toFixed(2) + "</b></span><span>training MSE <b>" + mse.toFixed(3) + "</b></span>" + (stumps.length > 300 ? "<span style='color:#f87171'>many trees: it starts fitting the noise</span>" : "");
    }
    draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: linear soft-margin SVM (Lesson 15) ----------------
  function svmDemo(el) {
    var S = shell(el, "soft-margin SVM: margin and C", 0.6);
    var P = [], logC = 0, cls = 1, w = [0, 0], b = 0, A;
    function preset() { var r = seeded(4), g = gaussFrom(r); P = [];
      for (var i = 0; i < 20; i++) P.push([-0.4 + 0.22 * g(), -0.25 + 0.22 * g(), -1]);
      for (i = 0; i < 20; i++) P.push([0.4 + 0.22 * g(), 0.3 + 0.22 * g(), 1]); }
    function train() {
      var n = P.length; if (!n) { w = [0, 0]; b = 0; return; }
      var C = Math.pow(10, logC), lam = 1 / (n * C), ww = [0, 0], bb = 0, avg = [0, 0, 0], T = 4000;
      for (var t = 1; t <= T; t++) {
        var eta = 1 / (lam * t + 10), g0 = lam * ww[0], g1 = lam * ww[1], gb = 0;
        for (var i = 0; i < n; i++) { var p = P[i], m = p[2] * (ww[0] * p[0] + ww[1] * p[1] + bb); if (m < 1) { g0 -= p[2] * p[0] / n; g1 -= p[2] * p[1] / n; gb -= p[2] / n; } }
        ww[0] -= eta * g0; ww[1] -= eta * g1; bb -= eta * gb;
        if (t > T / 2) { avg[0] += ww[0]; avg[1] += ww[1]; avg[2] += bb; }
      }
      w = [avg[0] / (T / 2), avg[1] / (T / 2)]; b = avg[2] / (T / 2);
    }
    slider(S.controls, "log₁₀ C", -2, 2, 0.1, logC, function (v) { return "C = " + Math.pow(10, v).toPrecision(2); }, function (v) { logC = v; train(); draw(); });
    var bA = button(S.controls, "Adding: class +1 (green)", function () { cls = -cls; bA.textContent = cls > 0 ? "Adding: class +1 (green)" : "Adding: class −1 (purple)"; });
    button(S.controls, "Example data", function () { preset(); train(); draw(); });
    function line(ctx, off) {
      if (Math.abs(w[1]) > Math.abs(w[0])) { ctx.moveTo(A.x(A.xmin), A.y((off - b - w[0] * A.xmin) / w[1])); ctx.lineTo(A.x(A.xmax), A.y((off - b - w[0] * A.xmax) / w[1])); }
      else { ctx.moveTo(A.x((off - b - w[1] * A.ymin) / w[0]), A.y(A.ymin)); ctx.lineTo(A.x((off - b - w[1] * A.ymax) / w[0]), A.y(A.ymax)); }
    }
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx;
      A = axes(W, H, -1.3 * W / H * 0.6, 1.3 * W / H * 0.6, -1.1, 1.1, 6);
      ctx.fillStyle = c.bg; ctx.fillRect(0, 0, W, H);
      var nw = Math.hypot(w[0], w[1]), nSV = 0;
      if (nw > 1e-6) {
        ctx.fillStyle = c.warn; ctx.globalAlpha = 0.08; ctx.beginPath();
        // shade the road
        var pts = []; for (var s = -1; s <= 1; s += 2) { var tmp = []; [A.xmin, A.xmax].forEach(function (x) { tmp.push([x, (s - b - w[0] * x) / w[1]]); }); pts.push(tmp); }
        if (Math.abs(w[1]) > 1e-6) { ctx.moveTo(A.x(pts[0][0][0]), A.y(pts[0][0][1])); ctx.lineTo(A.x(pts[0][1][0]), A.y(pts[0][1][1])); ctx.lineTo(A.x(pts[1][1][0]), A.y(pts[1][1][1])); ctx.lineTo(A.x(pts[1][0][0]), A.y(pts[1][0][1])); ctx.fill(); }
        ctx.globalAlpha = 1;
        ctx.strokeStyle = c.ink; ctx.lineWidth = 2.5; ctx.beginPath(); line(ctx, 0); ctx.stroke();
        ctx.setLineDash([6, 5]); ctx.lineWidth = 1.5; ctx.beginPath(); line(ctx, 1); line(ctx, -1); ctx.stroke(); ctx.setLineDash([]);
      }
      P.forEach(function (p) {
        var m = p[2] * (w[0] * p[0] + w[1] * p[1] + b);
        if (m <= 1.001) { nSV++; ctx.strokeStyle = c.warn; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(A.x(p[0]), A.y(p[1]), 10, 0, 7); ctx.stroke(); }
        dot(ctx, A.x(p[0]), A.y(p[1]), 6, c.bg); dot(ctx, A.x(p[0]), A.y(p[1]), 4.8, p[2] > 0 ? c.accent : c.violet);
      });
      var err = 0; P.forEach(function (p) { if (p[2] * (w[0] * p[0] + w[1] * p[1] + b) <= 0) err++; });
      S.readout.innerHTML = "<span>w = <b>(" + w[0].toFixed(2) + ", " + w[1].toFixed(2) + ")</b>, b = <b>" + b.toFixed(2) + "</b></span><span>margin 2/‖w‖ = <b>" + (nw > 1e-6 ? (2 / nw).toFixed(3) : "∞") + "</b></span><span>support vectors (ringed) <b>" + nSV + "</b></span><span>training errors <b>" + err + "</b></span>";
    }
    S.canvas.addEventListener("pointerdown", function (e) { var r = S.canvas.getBoundingClientRect(); P.push([A.ix(e.clientX - r.left), A.iy(e.clientY - r.top), cls]); train(); draw(); });
    preset(); train(); draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: k-means step by step (Lesson 16) ----------------
  function kmeansDemo(el) {
    var S = shell(el, "k-means, step by step", 0.6);
    var k = 4, data = "blobs", P = [], C = [], lab = [], phase = "assign", iter = 0, done = false, A, rnd = seeded(77);
    function gen() { var r = seeded(data === "blobs" ? 31 : 32), g = gaussFrom(r); P = [];
      if (data === "blobs") { [[-0.55, 0.45], [0.5, 0.5], [-0.35, -0.5], [0.55, -0.45]].forEach(function (cc) { for (var i = 0; i < 45; i++) P.push([cc[0] + 0.15 * g(), cc[1] + 0.15 * g()]); }); }
      else { for (var i = 0; i < 90; i++) { var t = Math.PI * r(); P.push([0.6 * Math.cos(t) - 0.3 + 0.04 * g(), 0.6 * Math.sin(t) - 0.15 + 0.04 * g()]); t = Math.PI * r(); P.push([0.6 - 0.6 * Math.cos(t) - 0.3 + 0.04 * g(), -0.6 * Math.sin(t) + 0.2 + 0.04 * g()]); } } }
    function init() { C = []; var used = {}; while (C.length < k) { var i = Math.floor(rnd() * P.length); if (!used[i]) { used[i] = 1; C.push(P[i].slice()); } } lab = P.map(function () { return -1; }); phase = "assign"; iter = 0; done = false; }
    function assign() { var changed = false; P.forEach(function (p, i) { var best = 0, bd = 1e9; C.forEach(function (c, j) { var d = (p[0] - c[0]) * (p[0] - c[0]) + (p[1] - c[1]) * (p[1] - c[1]); if (d < bd) { bd = d; best = j; } }); if (lab[i] !== best) changed = true; lab[i] = best; }); return changed; }
    function update() { C = C.map(function (c, j) { var sx = 0, sy = 0, n = 0; P.forEach(function (p, i) { if (lab[i] === j) { sx += p[0]; sy += p[1]; n++; } }); return n ? [sx / n, sy / n] : c; }); }
    function step() { if (done) return; if (phase === "assign") { var ch = assign(); if (!ch && iter > 0) { done = true; } phase = "update"; iter++; } else { update(); phase = "assign"; } }
    var ks = slider(S.controls, "k", 2, 6, 1, k, function (v) { return String(v); }, function (v) { k = v; init(); draw(); });
    button(S.controls, "Step", function () { step(); draw(); });
    button(S.controls, "Run to convergence", function () { for (var i = 0; i < 200 && !done; i++) step(); draw(); });
    button(S.controls, "New random start", function () { init(); draw(); });
    var dsel = button(S.controls, "Dataset: blobs", function () { data = data === "blobs" ? "moons" : "blobs"; dsel.textContent = "Dataset: " + data; gen(); k = data === "moons" ? 2 : 4; ks.set(k); init(); draw(); });
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx, cols = [c.accent, c.violet, c.warn, c.accent2, c.bad, "#f472b6"];
      A = axes(W, H, -1.2 * W / H * 0.6, 1.2 * W / H * 0.6, -1.05, 1.05, 6);
      ctx.fillStyle = c.bg; ctx.fillRect(0, 0, W, H);
      P.forEach(function (p, i) { dot(ctx, A.x(p[0]), A.y(p[1]), 4.5, lab[i] >= 0 ? cols[lab[i]] : c.text); });
      C.forEach(function (cc, j) { ctx.fillStyle = c.ink; ctx.font = "bold 24px sans-serif"; ctx.fillText("✚", A.x(cc[0]) - 9, A.y(cc[1]) + 9); ctx.fillStyle = cols[j]; ctx.font = "bold 18px sans-serif"; ctx.fillText("✚", A.x(cc[0]) - 7, A.y(cc[1]) + 7); });
      var inertia = 0; P.forEach(function (p, i) { if (lab[i] >= 0) { var cc = C[lab[i]]; inertia += (p[0] - cc[0]) * (p[0] - cc[0]) + (p[1] - cc[1]) * (p[1] - cc[1]); } });
      S.readout.innerHTML = "<span>iteration <b>" + iter + "</b></span><span>next step: <b>" + (done ? "—" : phase === "assign" ? "assign points to nearest centroid" : "move centroids to cluster means") + "</b></span><span>inertia <b>" + (lab[0] >= 0 ? inertia.toFixed(2) : "—") + "</b></span>" + (done ? "<span class='good'>✓ converged</span>" : "");
    }
    gen(); init(); draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: PCA projection (Lesson 17) ----------------
  function pcaDemo(el) {
    var S = shell(el, "find the direction of maximum variance", 0.6);
    var P = [], ang = 100, A;
    (function () { var r = seeded(17), g = gaussFrom(r); for (var i = 0; i < 45; i++) { var t = 0.55 * g(), u = 0.16 * g(); P.push([t * 0.87 - u * 0.5, t * 0.5 + u * 0.87]); }
      var mx = 0, my = 0; P.forEach(function (p) { mx += p[0]; my += p[1]; }); mx /= P.length; my /= P.length; P = P.map(function (p) { return [p[0] - mx, p[1] - my]; }); })();
    var n = P.length, a = 0, b = 0, c = 0; P.forEach(function (p) { a += p[0] * p[0]; b += p[0] * p[1]; c += p[1] * p[1]; }); a /= n - 1; b /= n - 1; c /= n - 1;
    var l1 = (a + c) / 2 + Math.sqrt((a - c) * (a - c) / 4 + b * b), l2 = (a + c) / 2 - Math.sqrt((a - c) * (a - c) / 4 + b * b);
    var pcAng = Math.atan2(l1 - a, b) * 180 / Math.PI; if (pcAng < 0) pcAng += 180;
    var sl = slider(S.controls, "line angle", 0, 180, 1, ang, function (v) { return v.toFixed(0) + "°"; }, function (v) { ang = v; draw(); });
    button(S.controls, "Snap to PC1", function () { ang = Math.round(pcAng * 10) / 10; sl.set(ang); draw(); });
    button(S.controls, "Snap to PC2", function () { ang = Math.round(((pcAng + 90) % 180) * 10) / 10; sl.set(ang); draw(); });
    function draw() {
      var col = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx;
      A = axes(W, H, -1.4 * W / H * 0.6, 1.4 * W / H * 0.6, -1.2, 1.2, 8);
      ctx.fillStyle = col.bg; ctx.fillRect(0, 0, W, H);
      var th = ang * Math.PI / 180, u = [Math.cos(th), Math.sin(th)], vr = 0, res = 0;
      ctx.strokeStyle = col.warn; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(A.x(-3 * u[0]), A.y(-3 * u[1])); ctx.lineTo(A.x(3 * u[0]), A.y(3 * u[1])); ctx.stroke();
      P.forEach(function (p) {
        var t = p[0] * u[0] + p[1] * u[1], q = [t * u[0], t * u[1]]; vr += t * t; res += (p[0] - q[0]) * (p[0] - q[0]) + (p[1] - q[1]) * (p[1] - q[1]);
        ctx.strokeStyle = col.bad; ctx.globalAlpha = 0.6; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(A.x(p[0]), A.y(p[1])); ctx.lineTo(A.x(q[0]), A.y(q[1])); ctx.stroke(); ctx.globalAlpha = 1;
        dot(ctx, A.x(q[0]), A.y(q[1]), 3, col.warn);
      });
      P.forEach(function (p) { dot(ctx, A.x(p[0]), A.y(p[1]), 4.5, col.accent2); });
      vr /= n - 1;
      var pct = 100 * vr / (l1 + l2), best = Math.abs(vr - l1) < 1e-3;
      S.readout.innerHTML = "<span>variance along line <b class='" + (best ? "good" : "") + "'>" + vr.toFixed(4) + "</b> (" + pct.toFixed(1) + "% of total)</span><span>squared projection error <b>" + res.toFixed(3) + "</b></span><span>eigenvalues λ₁ = <b>" + l1.toFixed(4) + "</b>, λ₂ = <b>" + l2.toFixed(4) + "</b></span>" + (best ? "<span class='good'>✓ this is PC1</span>" : "");
    }
    draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: neural network playground (Lesson 18) ----------------
  function nnDemo(el) {
    var S = shell(el, "neural network playground", 0.6);
    var data = "xor", hid = 4, P = [], net, steps = 0, timer = null, A;
    function gen() { var r = seeded(data === "xor" ? 1 : data === "circle" ? 2 : 3), g = gaussFrom(r); P = [];
      if (data === "xor") { [[-0.5, 0.5, 1], [0.5, -0.5, 1], [-0.5, -0.5, 0], [0.5, 0.5, 0]].forEach(function (cc) { for (var i = 0; i < 25; i++) P.push([cc[0] + 0.17 * g(), cc[1] + 0.17 * g(), cc[2]]); }); }
      else if (data === "circle") { for (var i = 0; i < 120; i++) { var rad = i < 60 ? 0.3 * Math.sqrt(r()) : 0.55 + 0.35 * r(), t = 2 * Math.PI * r(); P.push([rad * Math.cos(t), rad * Math.sin(t), i < 60 ? 1 : 0]); } }
      else { for (var k = 0; k < 2; k++) for (i = 0; i < 70; i++) { var s = i / 70, t2 = 1.2 * s * 2 * Math.PI + k * Math.PI, rr = 0.95 * s; P.push([rr * Math.cos(t2) + 0.03 * g(), rr * Math.sin(t2) + 0.03 * g(), k]); } } }
    function init() { var r = seeded(5 + hid), g = gaussFrom(r); net = { W1: [], b1: [], W2: [], b2: 0, m: null };
      for (var j = 0; j < hid; j++) { net.W1.push([g() * 1.5, g() * 1.5]); net.b1.push(g() * 0.5); net.W2.push(g()); }
      net.m = { W1: net.W1.map(function () { return [0, 0]; }), b1: net.b1.map(function () { return 0; }), W2: net.W2.map(function () { return 0; }), b2: 0 }; steps = 0; }
    function fwd(x, y) { var h = []; for (var j = 0; j < hid; j++) h.push(Math.tanh(net.W1[j][0] * x + net.W1[j][1] * y + net.b1[j])); var z = net.b2; for (j = 0; j < hid; j++) z += net.W2[j] * h[j]; return { h: h, p: 1 / (1 + Math.exp(-z)) }; }
    function step(k) {
      var lr = 0.3, mu = 0.9;
      for (var t = 0; t < k; t++) {
        var gW1 = net.W1.map(function () { return [0, 0]; }), gb1 = net.b1.map(function () { return 0; }), gW2 = net.W2.map(function () { return 0; }), gb2 = 0;
        P.forEach(function (p) { var f = fwd(p[0], p[1]), d = (f.p - p[2]) / P.length; gb2 += d;
          for (var j = 0; j < hid; j++) { gW2[j] += d * f.h[j]; var dh = d * net.W2[j] * (1 - f.h[j] * f.h[j]); gW1[j][0] += dh * p[0]; gW1[j][1] += dh * p[1]; gb1[j] += dh; } });
        for (var j = 0; j < hid; j++) {
          net.m.W2[j] = mu * net.m.W2[j] - lr * gW2[j]; net.W2[j] += net.m.W2[j];
          net.m.b1[j] = mu * net.m.b1[j] - lr * gb1[j]; net.b1[j] += net.m.b1[j];
          for (var q = 0; q < 2; q++) { net.m.W1[j][q] = mu * net.m.W1[j][q] - lr * gW1[j][q]; net.W1[j][q] += net.m.W1[j][q]; }
        }
        net.m.b2 = mu * net.m.b2 - lr * gb2; net.b2 += net.m.b2; steps++;
      }
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    function run() { stop(); var left = 6000; timer = setInterval(function () { step(40); left -= 40; draw(); if (left <= 0) stop(); }, 16); }
    var dsel = button(S.controls, "Dataset: XOR", function () { stop(); data = data === "xor" ? "circle" : data === "circle" ? "spiral" : "xor"; dsel.textContent = "Dataset: " + (data === "xor" ? "XOR" : data); gen(); init(); draw(); });
    slider(S.controls, "hidden neurons", 1, 8, 1, hid, function (v) { return String(v); }, function (v) { stop(); hid = v; init(); draw(); });
    button(S.controls, "Train", run);
    button(S.controls, "Reset weights", function () { stop(); init(); draw(); });
    function hexToRgb(h) { h = h.replace("#", ""); if (h.length === 3) h = h.split("").map(function (ch) { return ch + ch; }).join(""); var n = parseInt(h, 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; }
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx, cell = 6;
      A = axes(W, H, -1.15 * W / H * 0.6, 1.15 * W / H * 0.6, -1.05, 1.05, 6);
      var g1 = hexToRgb(c.accent.indexOf("#") === 0 ? c.accent : "#4ade80"), v = [167, 139, 250];
      ctx.fillStyle = c.bg; ctx.fillRect(0, 0, W, H);
      for (var py = 0; py < H; py += cell) for (var px = 0; px < W; px += cell) { var q = fwd(A.ix(px + 3), A.iy(py + 3)).p, cc = q >= 0.5 ? g1 : v; ctx.fillStyle = "rgba(" + cc[0] + "," + cc[1] + "," + cc[2] + "," + (Math.abs(q - 0.5) * 0.6).toFixed(3) + ")"; ctx.fillRect(px, py, cell, cell); }
      var L = 0, acc = 0;
      P.forEach(function (p) { var q = Math.min(1 - 1e-9, Math.max(1e-9, fwd(p[0], p[1]).p)); L -= p[2] * Math.log(q) + (1 - p[2]) * Math.log(1 - q); if ((q >= 0.5 ? 1 : 0) === p[2]) acc++;
        dot(ctx, A.x(p[0]), A.y(p[1]), 6, c.bg); dot(ctx, A.x(p[0]), A.y(p[1]), 4.5, p[2] ? c.accent : c.violet); });
      S.readout.innerHTML = "<span>network: <b>2 → " + hid + " tanh → 1 sigmoid</b></span><span>parameters <b>" + (hid * 3 + hid + 1) + "</b></span><span>steps <b>" + steps + "</b></span><span>log loss <b>" + (L / P.length).toFixed(3) + "</b></span><span>accuracy <b class='" + (acc === P.length ? "good" : "") + "'>" + (100 * acc / P.length).toFixed(0) + "%</b></span>";
    }
    gen(); init(); draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: convolution explorer (Lesson 19) ----------------
  function convDemo(el) {
    var S = shell(el, "convolution on a real handwritten digit", 0.5);
    var IMG = [[0,0,5,13,9,1,0,0],[0,0,13,15,10,15,5,0],[0,3,15,2,0,11,8,0],[0,4,12,0,0,8,8,0],[0,5,8,0,0,9,8,0],[0,4,11,0,1,12,7,0],[0,2,14,5,10,12,0,0],[0,0,6,13,10,0,0,0]];
    var KS = { "vertical edge": [[-1,0,1],[-1,0,1],[-1,0,1]], "horizontal edge": [[-1,-1,-1],[0,0,0],[1,1,1]], "blur (average)": [[1/9,1/9,1/9],[1/9,1/9,1/9],[1/9,1/9,1/9]], "sharpen": [[0,-1,0],[-1,5,-1],[0,-1,0]] };
    var kname = "vertical edge", hover = null, geo = null;
    Object.keys(KS).forEach(function (k) { button(S.controls, k, function () { kname = k; draw(); }); });
    function conv() { var K = KS[kname], out = []; for (var i = 0; i < 6; i++) { var row = []; for (var j = 0; j < 6; j++) { var s = 0; for (var u = 0; u < 3; u++) for (var v = 0; v < 3; v++) s += IMG[i + u][j + v] * K[u][v]; row.push(s); } out.push(row); } return out; }
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx, out = conv(), K = KS[kname];
      ctx.fillStyle = c.bg; ctx.fillRect(0, 0, W, H);
      var cs = Math.min((W * 0.42) / 8, (H - 40) / 8), ox = W * 0.04, oy = 28, cs2 = Math.min((W * 0.4) / 6, (H - 40) / 6), ox2 = W * 0.56;
      geo = { ox2: ox2, oy: oy, cs2: cs2 };
      ctx.fillStyle = c.text; ctx.font = "12px Inter, sans-serif"; ctx.fillText("input 8×8 (pixel intensity 0–16)", ox, 18); ctx.fillText("feature map 6×6 — kernel: " + kname, ox2, 18);
      for (var i = 0; i < 8; i++) for (var j = 0; j < 8; j++) { var v = IMG[i][j] / 16; ctx.fillStyle = "rgb(" + Math.round(20 + 220 * v) + "," + Math.round(20 + 220 * v) + "," + Math.round(20 + 220 * v) + ")"; ctx.fillRect(ox + j * cs, oy + i * cs, cs - 1, cs - 1); }
      var mx = 0; out.forEach(function (r) { r.forEach(function (v) { mx = Math.max(mx, Math.abs(v)); }); });
      for (i = 0; i < 6; i++) for (j = 0; j < 6; j++) { var o = out[i][j] / (mx || 1); ctx.fillStyle = o >= 0 ? "rgba(74,222,128," + (0.1 + 0.9 * o).toFixed(3) + ")" : "rgba(248,113,113," + (0.1 + 0.9 * -o).toFixed(3) + ")"; ctx.fillRect(ox2 + j * cs2, oy + i * cs2, cs2 - 1, cs2 - 1);
        if (cs2 > 26) { ctx.fillStyle = c.ink; ctx.font = "10px JetBrains Mono, monospace"; ctx.fillText(Math.round(out[i][j]), ox2 + j * cs2 + 3, oy + i * cs2 + cs2 / 2 + 3); } }
      var info = "<span>kernel <b>" + kname + "</b>: " + K.map(function (r) { return "[" + r.map(function (v) { return Math.abs(v - 1 / 9) < 1e-9 ? "1/9" : v; }).join(", ") + "]"; }).join(" ") + "</span>";
      if (hover) { var hi = hover[0], hj = hover[1];
        ctx.strokeStyle = c.warn; ctx.lineWidth = 3; ctx.strokeRect(ox + hj * cs, oy + hi * cs, 3 * cs, 3 * cs); ctx.strokeRect(ox2 + hj * cs2, oy + hi * cs2, cs2, cs2);
        var terms = []; for (var u = 0; u < 3; u++) for (var w = 0; w < 3; w++) if (K[u][w] !== 0 && IMG[hi + u][hj + w] !== 0) terms.push(IMG[hi + u][hj + w] + "×" + (Math.abs(K[u][w] - 1 / 9) < 1e-9 ? "1/9" : K[u][w]));
        info += "<span>output[" + hi + "," + hj + "] = " + (terms.length ? terms.join(" + ") : "0") + " = <b>" + out[hi][hj].toFixed(1) + "</b></span>"; }
      else info += "<span>Hover (or tap) over the feature map to see the calculation.</span>";
      S.readout.innerHTML = info;
    }
    function pick(e) { var r = S.canvas.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top, j = Math.floor((x - geo.ox2) / geo.cs2), i = Math.floor((y - geo.oy) / geo.cs2); hover = (i >= 0 && i < 6 && j >= 0 && j < 6) ? [i, j] : null; draw(); }
    S.canvas.addEventListener("pointermove", pick); S.canvas.addEventListener("pointerdown", pick);
    draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: preprocessing playground (Lesson 20) ----------------
  function prepDemo(el) {
    el.innerHTML = "";
    var head = document.createElement("div"); head.className = "demo-head"; head.textContent = "Interactive · impute → scale → one-hot encode";
    var wrap = document.createElement("div"); wrap.style.cssText = "display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;padding:16px;overflow-x:auto";
    var readout = document.createElement("div"); readout.className = "demo-readout";
    el.appendChild(head); el.appendChild(wrap); el.appendChild(readout);
    var rows = [[3, 95, "month-to-month"], [12, "", "one-year"], [24, 60, "two-year"], [6, 80, "month-to-month"], [40, 45, "two-year"]];
    var cats = ["month-to-month", "one-year", "two-year"];
    var left = document.createElement("div"), right = document.createElement("div"); wrap.appendChild(left); wrap.appendChild(right);
    var cellCss = "padding:6px 8px;border:1px solid var(--border);font-size:.85rem;font-family:var(--font-mono)";
    function build() {
      left.innerHTML = "<div style='font:600 .75rem var(--font-mono);letter-spacing:.1em;color:var(--muted);margin-bottom:6px'>RAW DATA (EDITABLE)</div>";
      var t = document.createElement("table"); t.style.borderCollapse = "collapse";
      t.innerHTML = "<tr><th style='" + cellCss + "'>tenure</th><th style='" + cellCss + "'>monthly charge</th><th style='" + cellCss + "'>contract</th></tr>";
      rows.forEach(function (r, i) {
        var tr = document.createElement("tr");
        [0, 1].forEach(function (k) { var td = document.createElement("td"); td.style.cssText = cellCss; var inp = document.createElement("input"); inp.value = r[k]; inp.setAttribute("aria-label", (k ? "Monthly charge" : "Tenure") + ", row " + (i + 1)); inp.style.cssText = "width:70px;background:var(--bg-2);color:var(--text);border:1px solid var(--border);border-radius:5px;padding:3px 5px;font:inherit"; inp.placeholder = "(missing)";
          inp.addEventListener("input", function () { r[k] = inp.value; compute(); }); td.appendChild(inp); tr.appendChild(td); });
        var td = document.createElement("td"); td.style.cssText = cellCss; var sel = document.createElement("select"); sel.setAttribute("aria-label", "Contract type, row " + (i + 1)); sel.style.cssText = "background:var(--bg-2);color:var(--text);border:1px solid var(--border);border-radius:5px;padding:3px;font:inherit";
        cats.forEach(function (cc) { var o = document.createElement("option"); o.value = o.textContent = cc; if (cc === r[2]) o.selected = true; sel.appendChild(o); });
        sel.addEventListener("change", function () { r[2] = sel.value; compute(); }); td.appendChild(sel); tr.appendChild(td); t.appendChild(tr);
      });
      left.appendChild(t);
    }
    function num(v) { var x = parseFloat(v); return isFinite(x) ? x : null; }
    function stats(col) { var v = rows.map(function (r) { return num(r[col]); }).filter(function (x) { return x !== null; }); return v; }
    function median(a) { var s = a.slice().sort(function (x, y) { return x - y; }), m = Math.floor(s.length / 2); return s.length ? (s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2) : 0; }
    function compute() {
      var t0 = stats(0), c0 = stats(1), medT = median(t0), medC = median(c0);
      var T = rows.map(function (r) { var x = num(r[0]); return x === null ? medT : x; }), C = rows.map(function (r) { var x = num(r[1]); return x === null ? medC : x; });
      function ms(a) { var m = a.reduce(function (s, v) { return s + v; }, 0) / a.length, sd = Math.sqrt(a.reduce(function (s, v) { return s + (v - m) * (v - m); }, 0) / a.length) || 1; return [m, sd]; }
      var mt = ms(T), mc = ms(C);
      right.innerHTML = "<div style='font:600 .75rem var(--font-mono);letter-spacing:.1em;color:var(--muted);margin-bottom:6px'>WHAT THE MODEL RECEIVES</div>";
      var t = document.createElement("table"); t.style.borderCollapse = "collapse";
      var hdr = "<tr><th style='" + cellCss + "'>tenure_z</th><th style='" + cellCss + "'>charge_z</th>" + cats.map(function (cc) { return "<th style='" + cellCss + "'>" + cc.replace("month-to-month", "m2m") + "</th>"; }).join("") + "</tr>";
      t.innerHTML = hdr + rows.map(function (r, i) {
        var imp = num(r[1]) === null || num(r[0]) === null;
        return "<tr><td style='" + cellCss + (num(r[0]) === null ? ";color:var(--warn)" : "") + "'>" + ((T[i] - mt[0]) / mt[1]).toFixed(2) + "</td><td style='" + cellCss + (num(r[1]) === null ? ";color:var(--warn)" : "") + "'>" + ((C[i] - mc[0]) / mc[1]).toFixed(2) + "</td>" +
          cats.map(function (cc) { return "<td style='" + cellCss + (r[2] === cc ? ";color:var(--accent);font-weight:700" : "") + "'>" + (r[2] === cc ? 1 : 0) + "</td>"; }).join("") + "</tr>";
      }).join("");
      right.appendChild(t);
      readout.innerHTML = "<span>learned from these rows → tenure: median <b>" + medT + "</b>, mean <b>" + mt[0].toFixed(2) + "</b>, std <b>" + mt[1].toFixed(2) + "</b></span><span>charge: median <b>" + medC + "</b>, mean <b>" + mc[0].toFixed(2) + "</b>, std <b>" + mc[1].toFixed(2) + "</b></span><span style='color:var(--warn)'>yellow = value was missing, filled with the median</span>";
    }
    build(); compute();
  }

  // ---------------- Demo: fairness with per-group thresholds (Lesson 21) ----------------
  function fairnessDemo(el) {
    var S = shell(el, "one model, two groups, two thresholds", 0.62);
    var tA = 0.5, tB = 0.5, G = { A: { yes: [], no: [] }, B: { yes: [], no: [] } };
    (function () { var r = seeded(21), g = gaussFrom(r);
      function sc(m) { return Math.min(0.999, Math.max(0.001, m + 0.13 * g())); }
      for (var i = 0; i < 200; i++) { (i < 100 ? G.A.yes : G.A.no).push(sc(i < 100 ? 0.62 : 0.4)); }
      for (i = 0; i < 200; i++) { (i < 40 ? G.B.yes : G.B.no).push(sc(i < 40 ? 0.62 : 0.4)); } })();
    function m(grp, t) {
      var tp = 0, fp = 0; grp.yes.forEach(function (s) { if (s >= t) tp++; }); grp.no.forEach(function (s) { if (s >= t) fp++; });
      var P = grp.yes.length, N = grp.no.length, fn = P - tp, tn = N - fp;
      return { sel: (tp + fp) / (P + N), tpr: tp / P, fpr: fp / N, ppv: tp + fp ? tp / (tp + fp) : null, acc: (tp + tn) / (P + N) };
    }
    var sa = slider(S.controls, "threshold A", 0, 1, 0.01, tA, function (v) { return v.toFixed(2); }, function (v) { tA = v; draw(); });
    var sb = slider(S.controls, "threshold B", 0, 1, 0.01, tB, function (v) { return v.toFixed(2); }, function (v) { tB = v; draw(); });
    function search(fn) { var best = tB, bd = 1e9; for (var t = 0; t <= 1.0001; t += 0.01) { var d = Math.abs(fn(t)); if (d < bd) { bd = d; best = t; } } tB = +best.toFixed(2); sb.set(tB); draw(); }
    button(S.controls, "Same threshold", function () { tB = tA; sb.set(tB); draw(); });
    button(S.controls, "Equalise selection rates", function () { var a = m(G.A, tA).sel; search(function (t) { return m(G.B, t).sel - a; }); });
    button(S.controls, "Equalise TPR", function () { var a = m(G.A, tA).tpr; search(function (t) { return m(G.B, t).tpr - a; }); });
    function strip(ctx, c, grp, t, y0, h, W, label) {
      var pad = 30, bins = 25, hy = new Array(bins).fill(0), hn = new Array(bins).fill(0), bw = (W - pad - 14) / bins;
      grp.yes.forEach(function (s) { hy[Math.min(bins - 1, Math.floor(s * bins))]++; }); grp.no.forEach(function (s) { hn[Math.min(bins - 1, Math.floor(s * bins))]++; });
      var mx = 22, base = y0 + h;
      for (var i = 0; i < bins; i++) {
        var x0 = pad + i * bw; ctx.globalAlpha = 0.65;
        ctx.fillStyle = c.violet; var a = Math.min(hn[i], mx) / mx * (h - 20); ctx.fillRect(x0 + 1, base - a, bw - 2, a);
        ctx.fillStyle = c.accent; var b = Math.min(hy[i], mx) / mx * (h - 20); ctx.fillRect(x0 + 1, base - b, bw - 2, b); ctx.globalAlpha = 1;
      }
      ctx.strokeStyle = c.grid; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(pad, base); ctx.lineTo(W - 14, base); ctx.stroke();
      var tx = pad + t * (W - pad - 14); ctx.strokeStyle = c.warn; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(tx, y0 + 4); ctx.lineTo(tx, base); ctx.stroke();
      ctx.fillStyle = c.ink; ctx.font = "bold 12px Inter, sans-serif"; ctx.fillText(label, pad, y0 + 12);
      ctx.fillStyle = c.warn; ctx.font = "11px JetBrains Mono, monospace"; ctx.fillText("approve →", tx + 5, y0 + 26);
    }
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx;
      ctx.fillStyle = c.bg; ctx.fillRect(0, 0, W, H);
      var h = (H - 50) / 2;
      strip(ctx, c, G.A, tA, 6, h, W, "Group A — 100 of 200 would repay");
      strip(ctx, c, G.B, tB, h + 22, h, W, "Group B — 40 of 200 would repay");
      ctx.font = "11px JetBrains Mono, monospace"; ctx.fillStyle = c.text; ctx.fillText("model score 0 → 1", W - 140, H - 6);
      ctx.fillStyle = c.accent; ctx.fillText("■ would repay", 30, H - 6); ctx.fillStyle = c.violet; ctx.fillText("■ would not", 140, H - 6);
      var a = m(G.A, tA), b = m(G.B, tB), f = function (v) { return v === null ? "—" : v.toFixed(2); };
      var ratio = Math.max(a.sel, b.sel) ? Math.min(a.sel, b.sel) / Math.max(a.sel, b.sel) : 1;
      S.readout.innerHTML = "<span>selection A <b>" + f(a.sel) + "</b> · B <b>" + f(b.sel) + "</b></span><span>TPR A <b>" + f(a.tpr) + "</b> · B <b>" + f(b.tpr) + "</b></span><span>FPR A <b>" + f(a.fpr) + "</b> · B <b>" + f(b.fpr) + "</b></span><span>precision A <b>" + f(a.ppv) + "</b> · B <b>" + f(b.ppv) + "</b></span><span>accuracy A <b>" + f(a.acc) + "</b> · B <b>" + f(b.acc) + "</b></span><span>parity ratio <b class='" + (ratio >= 0.8 ? "good" : "") + "'>" + ratio.toFixed(2) + "</b>" + (ratio >= 0.8 ? " ✓ ≥ 0.8" : " (< 0.8)") + "</span>";
    }
    draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  // ---------------- Demo: SQL joins (Lesson 22) ----------------
  function joinDemo(el) {
    el.innerHTML = "";
    var head = document.createElement("div"); head.className = "demo-head"; head.textContent = "Interactive · joining two tables";
    var controls = document.createElement("div"); controls.className = "demo-controls";
    var wrap = document.createElement("div"); wrap.style.cssText = "display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;padding:16px;overflow-x:auto";
    var readout = document.createElement("div"); readout.className = "demo-readout";
    el.appendChild(head); el.appendChild(controls); el.appendChild(wrap); el.appendChild(readout);
    var houses = [[1, "Central", 58], [2, "Central", 82], [3, "Central", 95], [4, "Suburb", 55], [9, "Outskirts", 42]];
    var views = [[1, 3], [1, 9], [2, 2], [4, 1], [4, 4], [4, 8], [7, 6]];
    var mode = "inner", agg = false;
    var cell = "padding:5px 8px;border:1px solid var(--border);font-size:.82rem;font-family:var(--font-mono)";
    function table(title, cols, rows, hl) {
      return "<div><div style='font:600 .72rem var(--font-mono);letter-spacing:.1em;color:var(--muted);margin-bottom:6px'>" + title + "</div><table style='border-collapse:collapse'><tr>" +
        cols.map(function (c) { return "<th style='" + cell + "'>" + c + "</th>"; }).join("") + "</tr>" +
        rows.map(function (r, i) { return "<tr>" + r.map(function (v) { return "<td style='" + cell + (v === null ? ";color:var(--warn)" : "") + (hl && hl(r, i) ? ";color:var(--accent);font-weight:700" : "") + "'>" + (v === null ? "NULL" : v) + "</td>"; }).join("") + "</tr>"; }).join("") + "</table></div>";
    }
    var group = document.createElement("div"); group.setAttribute("role", "group"); group.setAttribute("aria-label", "Join type");
    [["inner", "INNER JOIN"], ["left", "LEFT JOIN"]].forEach(function (o) {
      var b = button(group, o[1], function () { mode = o[0]; draw(); }); b.dataset.mode = o[0];
    });
    controls.appendChild(group);
    var ab = button(controls, "Count viewings per house (GROUP BY)", function () { agg = !agg; draw(); });
    function draw() {
      group.querySelectorAll("button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.mode === mode ? "true" : "false"); b.style.fontWeight = b.dataset.mode === mode ? "700" : ""; });
      ab.setAttribute("aria-pressed", agg ? "true" : "false"); ab.style.fontWeight = agg ? "700" : "";
      var out = [];
      houses.forEach(function (h) {
        var m = views.filter(function (v) { return v[0] === h[0]; });
        if (m.length) m.forEach(function (v) { out.push([h[0], h[1], h[2], v[1]]); });
        else if (mode === "left") out.push([h[0], h[1], h[2], null]);
      });
      var res, cols;
      if (agg) {
        var by = {}; out.forEach(function (r) { by[r[0]] = by[r[0]] || [r[0], r[1], 0]; if (r[3] !== null) by[r[0]][2]++; });
        res = Object.keys(by).map(function (k) { return by[k]; }); cols = ["id", "area", "COUNT(day)"];
      } else { res = out; cols = ["id", "area", "price", "day"]; }
      wrap.innerHTML = table("HOUSES", ["id", "area", "price"], houses) + table("VIEWINGS", ["house_id", "day"], views, function (r) { return !houses.some(function (h) { return h[0] === r[0]; }); }) +
        table("RESULT (" + res.length + " ROWS)", cols, res);
      var missing = houses.filter(function (h) { return !views.some(function (v) { return v[0] === h[0]; }); }).map(function (h) { return h[0]; });
      readout.innerHTML = "<span>" + (mode === "inner" ? "INNER keeps only matches: houses <b>" + missing.join(", ") + "</b> disappear" : "LEFT keeps every house: houses <b>" + missing.join(", ") + "</b> get NULL") +
        "</span><span>viewing of house <b>7</b> has no house row, so it never appears</span><span>" + (agg ? "one row per house" : "house 4 appears <b>3</b> times: one row per matching viewing") + "</span>";
    }
    draw();
  }

  // ---------------- Demo: grid vs random search (Lesson 23) ----------------
  function searchDemo(el) {
    var S = shell(el, "grid search vs random search on a validation-score landscape", 0.55);
    var budget = 9, seed = 1, rnd;
    function rng() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
    // score depends strongly on x (log learning rate) and only weakly on y (a minor setting)
    function score(x, y) { return 0.93 * Math.exp(-Math.pow((x - 0.63) / 0.09, 2)) + 0.03 * Math.sin(3 * y) + 0.03; }
    function draws() { rnd = []; for (var i = 0; i < budget; i++) rnd.push([rng(), rng()]); }
    function gridPts() { var k = Math.round(Math.sqrt(budget)), g = []; for (var i = 0; i < k; i++) for (var j = 0; j < k; j++) g.push([(i + 0.5) / k, (j + 0.5) / k]); return g; }
    function best(pts) { var b = pts[0]; pts.forEach(function (p) { if (score(p[0], p[1]) > score(b[0], b[1])) b = p; }); return b; }
    slider(S.controls, "Budget (tries)", 4, 36, 1, budget, function (v) { var k = Math.round(Math.sqrt(v)); return v + " (grid " + k + "×" + k + ")"; }, function (v) { budget = v; draws(); draw(); });
    button(S.controls, "New random draws ↻", function () { draws(); draw(); });
    function draw() {
      var c = colors(), W = S.state.W, H = S.state.H, ctx = S.ctx, half = (W - 30) / 2;
      ctx.fillStyle = c.bg; ctx.fillRect(0, 0, W, H);
      [["Grid search", gridPts()], ["Random search", rnd]].forEach(function (pp, k) {
        var x0 = 10 + k * (half + 10), y0 = 22, w = half, h = H - 66, pts = pp[1];
        for (var i = 0; i < 60; i++) { var v = score((i + 0.5) / 60, 0.5); ctx.fillStyle = c.accent; ctx.globalAlpha = 0.08 + 0.5 * v; ctx.fillRect(x0 + i * w / 60, y0, w / 60 + 1, h); }
        ctx.globalAlpha = 1; ctx.strokeStyle = c.grid; ctx.strokeRect(x0, y0, w, h);
        var b = best(pts);
        pts.forEach(function (p) { dot(ctx, x0 + p[0] * w, y0 + (1 - p[1]) * h, p === b ? 6 : 4, p === b ? c.warn : c.ink); });
        ctx.fillStyle = c.ink; ctx.font = "bold 12px Inter, sans-serif"; ctx.fillText(pp[0] + " — best score " + score(b[0], b[1]).toFixed(3), x0, 15);
        var xs = {}; pts.forEach(function (p) { xs[p[0].toFixed(3)] = 1; });
        ctx.fillStyle = c.text; ctx.font = "11px JetBrains Mono, monospace"; ctx.fillText(Object.keys(xs).length + " distinct learning rates", x0 + 4, y0 + h + 16);
      });
      ctx.fillStyle = c.text; ctx.fillText("← learning rate (log scale) →   bright band = good validation score", 12, H - 4);
      var g = best(gridPts()), r = best(rnd);
      S.readout.innerHTML = "<span>grid best <b>" + score(g[0], g[1]).toFixed(3) + "</b></span><span>random best <b>" + score(r[0], r[1]).toFixed(3) + "</b></span><span>best possible <b>" + score(0.63, Math.PI / 6).toFixed(3) + "</b></span>";
    }
    draws(); draw(); onResize(function () { S.resize(); draw(); }); onTheme(draw);
  }

  var REGISTRY = { "fit-line": fitLine, "dot-product": dotProduct, "tangent": tangent, "bayes": bayes, "normal": normal,
    "overfit": overfit, "least-squares": leastSquares, "gd-contour": gdContour, "logistic": logistic,
    "threshold": thresholdDemo, "ridge": ridgeDemo, "knn": knnDemo, "naive-bayes": nbDemo,
    "tree": treeDemo, "boosting": boostingDemo, "svm": svmDemo, "kmeans": kmeansDemo,
    "pca": pcaDemo, "nn": nnDemo, "conv": convDemo, "prep": prepDemo, "fairness": fairnessDemo, "join": joinDemo, "search": searchDemo };
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".demo[data-demo]").forEach(function (el) {
      var fn = REGISTRY[el.getAttribute("data-demo")];
      if (fn) { try { fn(el); } catch (e) { el.textContent = "Demo failed to load: " + e.message; } }
    });
  });
})();
