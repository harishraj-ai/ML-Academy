/* ML Academy — accessibility: reading settings, screen-reader descriptions for demos, keyboard control of canvas demos */
(function () {
  "use strict";
  var KEY = "mla-a11y", root = document.documentElement;
  function get() { try { return JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { return {}; } }
  function set(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) { /* ignore */ } }
  function apply(s) {
    root.classList.toggle("hc", s.contrast === "high");
    root.classList.toggle("dys", s.font === "dyslexic");
    root.classList.toggle("rm", s.motion === "reduce" || (s.motion !== "allow" && window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches));
    root.style.setProperty("--ts", String((s.size || 100) / 100));
    root.classList.toggle("big", (s.size || 100) >= 130 || s.font === "dyslexic");
  }
  apply(get());
  window.MLA_A11Y = { reduced: function () { return root.classList.contains("rm"); } };

  // What each demo shows, for screen readers (the numeric readout below each demo is announced as it changes).
  var D = {
    "fit-line": ["A scatter plot of example data with a straight line you adjust with the slope w and bias b sliders; the Show best fit button jumps to the least-squares line and the readout shows the error.", ""],
    "dot-product": ["Two arrows, a (green) and b (violet), drawn from the origin, with the projection of b onto a in yellow. The readout gives both vectors, their dot product, the angle between them and whether they point the same way.", "move the cursor and press Enter to move the nearest arrow tip there."],
    "tangent": ["The curve f(x) with its tangent line at a chosen point. The point x slider moves the point; the Step button takes one gradient-descent step x ← x − η·f′(x) with the learning rate set by the second slider.", ""],
    "bayes": ["1,000 people split by whether they have the disease and whether they test positive. Sliders set the disease rate, the test's sensitivity and its false-positive rate; the readout gives the chance that a positive result is real.", ""],
    "normal": ["A histogram of samples drawn from a normal distribution, compared with its bell curve. Sliders set the mean μ and standard deviation σ; buttons add 10 or 1,000 samples.", ""],
    "overfit": ["Noisy data points with a polynomial curve fitted through them. The degree slider shows underfitting at low degree and overfitting at high degree; the readout reports the errors.", ""],
    "least-squares": ["A scatter plot with the least-squares line through the points, the squared errors drawn as red squares and the mean point circled.", "move the cursor and press Enter to add a point there, or press Enter on an existing point to remove it."],
    "gd-contour": ["A contour map of the loss for slope and intercept, with the path gradient descent takes from its starting point towards the minimum. Buttons run steps; the slider sets the learning rate.", ""],
    "logistic": ["Two classes of points (green and purple) with the decision boundary that logistic regression learns when you press Train. The readout shows the weights, log loss and accuracy.", "choose a class with the buttons, move the cursor and press Enter to add a point of that class."],
    "threshold": ["Two overlapping score distributions (negatives and positives) with a movable threshold, the resulting confusion matrix and the ROC curve.", ""],
    "ridge": ["A degree-9 polynomial fitted to noisy data. As the λ slider increases the ridge penalty, the curve becomes smoother.", ""],
    "knn": ["Points from three classes and the kNN decision regions shaded behind them; a query point shows its k nearest neighbours and their vote.", "move the cursor and press Enter to place the query point there."],
    "naive-bayes": ["A text box where you type a message; the demo shows how its words affect the probability that it is spam.", ""],
    "tree": ["Two classes of points divided into rectangles by a decision tree; the depth slider adds splits one level at a time.", ""],
    "boosting": ["Data points with the gradient-boosting prediction, built one stump (one-split tree) at a time. Buttons add 1, 10 or 100 stumps; the slider sets the learning rate.", ""],
    "svm": ["Two classes of points with the soft-margin SVM boundary, the dashed margin lines and the support vectors ringed in yellow. The C slider changes how many margin violations are allowed.", "choose a class with the buttons, move the cursor and press Enter to add a point of that class."],
    "kmeans": ["Unlabelled points coloured by cluster with their centroids. The Step button alternates the assign and update phases of k-means; the k slider and dataset button change the setup.", ""],
    "pca": ["A cloud of correlated points with a line you rotate with the angle slider; the readout shows the variance captured along that line. Buttons snap it to the first or second principal component.", ""],
    "nn": ["A small neural network learning to separate two classes (XOR, circle or spiral data). The shaded regions show its predictions as it trains; the slider sets the number of hidden neurons.", ""],
    "conv": ["An 8×8 input image of a digit on the left and the 6×6 feature map produced by the selected 3×3 kernel on the right.", "move the cursor over the feature map and press Enter to see how that output value is calculated."],
    "prep": ["Two tables: raw data with a missing value and a category column, and the same data after imputing, scaling and one-hot encoding. Edit the raw cells to see the output change.", ""],
    "fairness": ["Model-score histograms for two groups: group A, where half the people would repay, and group B, where one in five would. Each group has its own approval threshold slider; buttons set the same threshold or equalise the selection rates or true-positive rates. The readout compares selection rate, TPR, FPR, precision and accuracy for the two groups and the demographic-parity ratio.", ""]
  };

  var STR = { contrast: [["normal", "Normal"], ["high", "High contrast"]], font: [["standard", "Standard"], ["dyslexic", "Dyslexia-friendly"]], motion: [["system", "Follow my system"], ["reduce", "Reduce motion"], ["allow", "Allow motion"]] };
  function panelHTML(s) {
    function group(key, title) {
      return '<fieldset><legend>' + title + '</legend>' + STR[key].map(function (o) {
        var cur = s[key] || STR[key][0][0];
        return '<label><input type="radio" name="a11y-' + key + '" value="' + o[0] + '"' + (cur === o[0] ? " checked" : "") + "> " + o[1] + "</label>"; }).join("") + "</fieldset>";
    }
    return '<div class="a11y-head"><b id="a11y-title">Reading settings</b><button type="button" class="a11y-close" aria-label="Close reading settings">✕</button></div>' +
      group("contrast", "Contrast") + group("font", "Font") +
      '<fieldset><legend>Text size</legend><div class="a11y-size"><button type="button" data-size="-10" aria-label="Smaller text">A−</button><output aria-live="polite">' + (s.size || 100) + '%</output><button type="button" data-size="10" aria-label="Larger text">A+</button><button type="button" data-size="0">Reset</button></div></fieldset>' +
      group("motion", "Animation") + '<p class="a11y-note">Saved in this browser. The light/dark switch is the ☀/☾ button.</p>';
  }

  document.addEventListener("DOMContentLoaded", function () {
    // ---------- settings panel ----------
    var btn = document.querySelector(".a11y-btn");
    if (btn) {
      var panel = document.createElement("div"); panel.className = "a11y-panel"; panel.id = "a11y-panel"; panel.hidden = true;
      panel.setAttribute("role", "dialog"); panel.setAttribute("aria-labelledby", "a11y-title");
      document.body.appendChild(panel); btn.setAttribute("aria-controls", "a11y-panel");
      function open(o) {
        if (o) { panel.innerHTML = panelHTML(get()); }
        panel.hidden = !o; btn.setAttribute("aria-expanded", o ? "true" : "false");
        if (o) panel.querySelector("input:checked").focus(); else btn.focus();
      }
      btn.addEventListener("click", function () { open(panel.hidden); });
      panel.addEventListener("change", function (e) {
        var t = e.target; if (t.type !== "radio") return; var s = get(); s[t.name.replace("a11y-", "")] = t.value; set(s); apply(s);
        window.dispatchEvent(new Event("mla-a11y"));
      });
      panel.addEventListener("click", function (e) {
        var t = e.target.closest("button"); if (!t) return;
        if (t.classList.contains("a11y-close")) { open(false); return; }
        if (t.hasAttribute("data-size")) {
          var s = get(), d = +t.getAttribute("data-size"); s.size = d === 0 ? 100 : Math.max(80, Math.min(160, (s.size || 100) + d)); set(s); apply(s);
          panel.querySelector("output").textContent = s.size + "%"; window.dispatchEvent(new Event("resize"));
        }
      });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden) open(false); });
      document.addEventListener("click", function (e) { if (!panel.hidden && !panel.contains(e.target) && !btn.contains(e.target)) open(false); });
    }

    // ---------- "More" menu: close on outside click / Escape ----------
    document.querySelectorAll(".nav-more").forEach(function (d) {
      document.addEventListener("click", function (e) { if (d.open && !d.contains(e.target)) d.open = false; });
      d.addEventListener("keydown", function (e) { if (e.key === "Escape") { d.open = false; d.querySelector("summary").focus(); } });
    });
    // ---------- demos: descriptions, live readouts, keyboard cursor ----------
    document.querySelectorAll(".demo[data-demo]").forEach(function (el, n) {
      var name = el.getAttribute("data-demo"), d = D[name] || ["An interactive demo.", ""], canvas = el.querySelector("canvas");
      var desc = document.createElement("p"); desc.className = "sr-only"; desc.id = "demo-desc-" + n;
      desc.textContent = d[0] + (d[1] ? " Keyboard: Tab to the plot, use the arrow keys to move the cursor (hold Shift for bigger steps), then " + d[1] : "") + " The readout below the controls updates as you change things.";
      el.insertBefore(desc, el.firstChild);
      el.setAttribute("role", "group"); el.setAttribute("aria-label", (el.querySelector(".demo-head") || {}).textContent || "Interactive demo");
      el.setAttribute("aria-describedby", desc.id);
      var ro = el.querySelector(".demo-readout"); if (ro) { ro.setAttribute("aria-live", "polite"); ro.setAttribute("aria-atomic", "true"); }
      if (!canvas) return;
      canvas.setAttribute("role", "img"); canvas.setAttribute("aria-label", d[0]);
      if (!d[1]) return;
      // keyboard cursor: arrows move a crosshair, Enter/Space acts like a click there
      canvas.tabIndex = 0; canvas.setAttribute("aria-roledescription", "interactive plot");
      canvas.setAttribute("aria-label", d[0] + " Use the arrow keys to move the cursor, then " + d[1]);
      el.style.position = "relative";
      var cur = document.createElement("span"); cur.className = "kb-cursor"; cur.hidden = true; cur.setAttribute("aria-hidden", "true"); el.appendChild(cur);
      var hint = document.createElement("span"); hint.className = "kb-hint"; hint.hidden = true; hint.setAttribute("aria-hidden", "true");
      hint.textContent = "Arrow keys move the cursor · Shift = bigger steps · Enter = " + (name === "dot-product" ? "move arrow tip" : name === "knn" ? "place query" : name === "conv" ? "inspect" : "add / remove point"); el.appendChild(hint);
      var fx = 0.5, fy = 0.5;
      function place() {
        var w = canvas.clientWidth, h = canvas.clientHeight;
        cur.style.left = (canvas.offsetLeft + fx * w) + "px"; cur.style.top = (canvas.offsetTop + fy * h) + "px";
        hint.style.left = canvas.offsetLeft + 8 + "px"; hint.style.top = canvas.offsetTop + 8 + "px";
      }
      function fire(type) {
        var r = canvas.getBoundingClientRect(), x = r.left + fx * r.width, y = r.top + fy * r.height;
        var ev; try { ev = new PointerEvent(type, { clientX: x, clientY: y, bubbles: true, pointerId: 1, isPrimary: true }); } catch (e) { ev = new MouseEvent(type, { clientX: x, clientY: y, bubbles: true }); }
        canvas.dispatchEvent(ev);
      }
      canvas.addEventListener("focus", function () { cur.hidden = false; hint.hidden = false; place(); if (name === "conv") fire("pointermove"); });
      canvas.addEventListener("blur", function () { cur.hidden = true; hint.hidden = true; });
      canvas.addEventListener("keydown", function (e) {
        var st = e.shiftKey ? 0.08 : 0.02, moved = true;
        if (e.key === "ArrowLeft") fx -= st; else if (e.key === "ArrowRight") fx += st;
        else if (e.key === "ArrowUp") fy -= st; else if (e.key === "ArrowDown") fy += st;
        else if (e.key === "Enter" || e.key === " ") { moved = false; fire("pointerdown"); fire("pointerup"); }
        else return;
        e.preventDefault();
        fx = Math.max(0.02, Math.min(0.98, fx)); fy = Math.max(0.02, Math.min(0.98, fy)); place();
        if (moved && name === "conv") fire("pointermove");
      });
      window.addEventListener("resize", place);
    });

    // buttons whose only content is maths: give them a spoken label from the TeX source
    var nScroll = 0;
    function fixScroll() {
      document.querySelectorAll("pre, .run-table, .table-scroll, .map-wrap, .demo > div").forEach(function (el) {
        if (el.scrollWidth > el.clientWidth + 1 && !el.hasAttribute("tabindex")) { el.tabIndex = 0; if (!el.getAttribute("role")) { nScroll++; el.setAttribute("role", "region"); el.setAttribute("aria-label", (el.tagName === "PRE" ? "Code block " : "Scrollable content ") + nScroll + " (scrollable)"); } }
      });
    }
    fixScroll(); window.addEventListener("resize", fixScroll);
    function labelMathButtons() {
      document.querySelectorAll("button").forEach(function (b) {
        if (b.getAttribute("aria-label") || !b.querySelector(".katex")) return;
        var c = b.cloneNode(true);
        c.querySelectorAll(".katex").forEach(function (k) { var a = k.querySelector("annotation"); k.replaceWith(document.createTextNode(a ? a.textContent.replace(/\\(?:text|mathrm|mathbf|operatorname)\{([^}]*)\}/g, "$1").replace(/\\([a-zA-Z]+)/g, "$1").replace(/[{}]/g, "").replace(/\s+/g, " ").trim() : k.textContent)); });
        b.setAttribute("aria-label", c.textContent.replace(/\s+/g, " ").trim());
      });
    }
    labelMathButtons(); setTimeout(function () { labelMathButtons(); fixScroll(); }, 600);
    // walkthrough captions are announced when stepping
    document.querySelectorAll(".walk-caps").forEach(function (c) { c.setAttribute("aria-live", "polite"); });
  });
})();
