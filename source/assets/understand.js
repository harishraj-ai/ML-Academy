/* ML Academy — step-through derivations and formula decoders */
(function () {
  "use strict";
  // Reading level: applied immediately to avoid a flash of the wrong mode
  var root = document.documentElement;
  function getLevel() { try { return localStorage.getItem("mla-level") || "detailed"; } catch (e) { return "detailed"; } }
  function setLevel(l) { try { localStorage.setItem("mla-level", l); } catch (e) { /* ignore */ } }
  root.classList.toggle("level-simple", getLevel() === "simple");
  document.addEventListener("DOMContentLoaded", function () {
    var btns = document.querySelectorAll(".level-switch button");
    function paintLevel() { var l = getLevel(); root.classList.toggle("level-simple", l === "simple"); btns.forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-level") === l ? "true" : "false"); }); }
    btns.forEach(function (b) { b.addEventListener("click", function () { setLevel(b.getAttribute("data-level")); paintLevel(); }); });
    paintLevel();
    document.querySelectorAll(".adv-toggle").forEach(function (t) {
      t.addEventListener("click", function () {
        var body = document.getElementById(t.getAttribute("data-target")), open = !body.classList.contains("open");
        body.classList.toggle("open", open); t.setAttribute("aria-expanded", open ? "true" : "false");
        t.textContent = open ? "Hide the full maths ▴" : "Show the full maths ▾";
      });
    });
    // Step-through derivations
    document.querySelectorAll(".stepper").forEach(function (box) {
      var steps = box.querySelectorAll(".st"), shown = 1, count = box.querySelector(".st-count");
      var next = box.querySelector('[data-act="next"]');
      function paint() {
        steps.forEach(function (s, i) { s.classList.toggle("hidden", i >= shown); s.classList.toggle("latest", i === shown - 1 && shown > 1); });
        count.textContent = "Step " + shown + " of " + steps.length;
        next.disabled = shown >= steps.length;
        next.textContent = shown >= steps.length ? "Done ✓" : "Next step →";
      }
      box.querySelector(".st-controls").addEventListener("click", function (e) {
        var act = e.target.getAttribute && e.target.getAttribute("data-act"); if (!act) return;
        if (act === "next" && shown < steps.length) shown++;
        if (act === "all") shown = steps.length;
        if (act === "reset") shown = 1;
        paint();
        if (act === "next") { var l = steps[shown - 1]; if (l.scrollIntoView) l.scrollIntoView({ block: "nearest", behavior: "smooth" }); }
      });
      box.classList.add("js"); paint();
    });
    // Formula decoders
    document.querySelectorAll(".decode").forEach(function (box) {
      var items = box.querySelectorAll(".decode-legend li"), locked = null;
      function focus(p) {
        for (var k = 1; k <= 6; k++) box.classList.remove("focus-" + k);
        box.classList.toggle("focusing", !!p);
        if (p) box.classList.add("focus-" + p);
        items.forEach(function (li) { li.classList.toggle("on", li.getAttribute("data-p") === p); });
      }
      items.forEach(function (li) {
        var p = li.getAttribute("data-p");
        li.addEventListener("mouseenter", function () { if (!locked) focus(p); });
        li.addEventListener("mouseleave", function () { if (!locked) focus(null); });
        li.addEventListener("focus", function () { focus(p); });
        li.addEventListener("blur", function () { if (!locked) focus(null); });
        li.addEventListener("click", function () { locked = locked === p ? null : p; focus(locked); });
      });
      // hovering a coloured part of the formula highlights its legend entry
      box.querySelectorAll(".decode-math .enclosing").forEach(function (part) {
        var m = (part.className.match(/fd-(\d)/) || [])[1]; if (!m) return;
        part.addEventListener("mouseenter", function () { if (!locked) focus(m); });
        part.addEventListener("mouseleave", function () { if (!locked) focus(null); });
      });
    });
  });
})();
/* Animated walkthroughs: one SVG with a <g class="wf"> per frame, and one caption per frame */
(function () {
  "use strict";
  document.addEventListener("DOMContentLoaded", function () {
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    document.querySelectorAll(".walk").forEach(function (box) {
      var frames = box.querySelectorAll(".wf"), caps = box.querySelectorAll(".walk-cap"), n = frames.length, i = 0, timer = null;
      var play = box.querySelector(".wk-play"), prev = box.querySelector(".wk-prev"), next = box.querySelector(".wk-next"), count = box.querySelector(".wk-count");
      function show(k) {
        i = Math.max(0, Math.min(n - 1, k));
        frames.forEach(function (f, j) { f.classList.toggle("on", j === i); });
        caps.forEach(function (c, j) { c.classList.toggle("on", j === i); });
        count.textContent = "Step " + (i + 1) + " / " + n;
        prev.disabled = i === 0; next.disabled = i === n - 1;
      }
      function stop() { if (timer) { clearInterval(timer); timer = null; } play.textContent = "▶ Play"; play.setAttribute("aria-label", "Play"); }
      function start() {
        if (i === n - 1) show(0);
        play.textContent = "❚❚ Pause"; play.setAttribute("aria-label", "Pause");
        timer = setInterval(function () { if (i >= n - 1) { stop(); return; } show(i + 1); }, reduce ? 4500 : 3200);
      }
      play.addEventListener("click", function () { if (timer) stop(); else start(); });
      prev.addEventListener("click", function () { stop(); show(i - 1); });
      next.addEventListener("click", function () { stop(); show(i + 1); });
      box.querySelector(".wk-reset").addEventListener("click", function () { stop(); show(0); });
      box.addEventListener("keydown", function (e) {
        if (e.key === "ArrowRight") { stop(); show(i + 1); e.preventDefault(); }
        if (e.key === "ArrowLeft") { stop(); show(i - 1); e.preventDefault(); }
      });
      box.classList.add("js"); show(0);
    });
  });
})();
