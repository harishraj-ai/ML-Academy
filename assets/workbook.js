/* ML Academy — turns the lesson pages collected in workbook.html into a printable workbook. */
(function () {
  "use strict";
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function transform() {
    var appendix = document.getElementById("wb-answers");
    document.querySelectorAll(".wb-lesson").forEach(function (L) {
      var n = L.getAttribute("data-n"), title = L.getAttribute("data-title"), ans = el("section", "wb-ans-lesson");
      ans.appendChild(el("h2", null, "Lesson " + n + ": " + title));
      // interactive demos -> a pointer to the website
      L.querySelectorAll(".demo").forEach(function (d) {
        d.replaceWith(el("div", "wb-note", "<b>Interactive demo</b> — open <i>lesson-" + (n.length < 2 ? "0" : "") + n + ".html</i> on the website to try it."));
      });
      // walkthroughs -> final picture + the steps as a list
      L.querySelectorAll(".walk").forEach(function (w) {
        var frames = w.querySelectorAll(".wf"); frames.forEach(function (f, i) { if (i !== frames.length - 1) f.remove(); else f.classList.add("on"); });
        var ol = el("ol", "wb-steps"); w.querySelectorAll(".walk-cap").forEach(function (c) { ol.appendChild(el("li", null, c.innerHTML)); });
        var caps = w.querySelector(".walk-caps"); caps.replaceWith(ol);
        var ctl = w.querySelector(".walk-ctl"); if (ctl) ctl.remove();
        var tag = w.querySelector(".walk-tag"); if (tag) tag.textContent = "Walkthrough (final step shown)";
      });
      // step-by-step derivations: show every step, drop the buttons
      L.querySelectorAll(".st-controls").forEach(function (c) { c.remove(); });
      L.querySelectorAll("details.adv-box, details.hq").forEach(function (d) { d.open = true; });
      // reading levels: print the full (detailed) version only
      L.querySelectorAll(".simple-sum").forEach(function (s) { s.remove(); });
      // quiz -> lettered options; answers to the appendix
      var qa = el("ol", "wb-qa");
      L.querySelectorAll(".quiz .q").forEach(function (q, k) {
        var opts = q.querySelectorAll("button[data-opt]"), list = el("ol", "wb-opts"), correct = q.getAttribute("data-correct"), letter = "";
        opts.forEach(function (b, i) { var li = el("li", null, b.innerHTML); list.appendChild(li); if (b.getAttribute("data-opt") === correct) letter = "abcd"[i]; });
        var exp = q.querySelector(".q-explain");
        qa.appendChild(el("li", null, "<b>(" + letter + ")</b> " + (exp ? exp.innerHTML : "")));
        opts.forEach(function (b) { b.remove(); }); if (exp) exp.remove();
        q.appendChild(list);
      });
      if (qa.children.length) { ans.appendChild(el("h3", null, "Quiz answers")); ans.appendChild(qa); }
      // exercises -> blank working space; solutions to the appendix
      var sol = el("ol", "wb-sol");
      L.querySelectorAll("h2").forEach(function (h) { if (/Practice exercises/.test(h.textContent) && h.nextElementSibling && h.nextElementSibling.tagName === "P")
        h.nextElementSibling.innerHTML = "Work each exercise in the space provided, then compare with the solutions at the back of the workbook. The lesson's Jupyter notebook has two more coding challenges with automatic checks."; });
      L.querySelectorAll(".exercises .ex").forEach(function (x) {
        x.querySelectorAll(".chk").forEach(function (c) { c.remove(); });
        var d = x.querySelector("details"); if (d) { sol.appendChild(el("li", null, d.querySelector(".ex-sol").innerHTML)); d.remove(); }
        x.appendChild(el("div", "wb-work", "<span>Working</span>"));
      });
      if (sol.children.length) { ans.appendChild(el("h3", null, "Exercise solutions")); ans.appendChild(sol); }
      L.querySelectorAll(".gen, .whatif, .hq-more, .listen, .complete-row, .pager, .lesson-actions, .see-also, .adv-toggle, .chk, .part-end .btn").forEach(function (x) { x.remove(); });
      L.appendChild(el("div", "wb-notes", "<span>Notes</span>"));
      appendix.appendChild(ans);
    });
    // any leftover controls
    document.querySelectorAll(".wb-body button").forEach(function (b) { b.remove(); });
  }
  document.addEventListener("DOMContentLoaded", function () {
    transform();
    if (typeof renderMathInElement === "function")
      renderMathInElement(document.body, { delimiters: [{ left: "$$", right: "$$", display: true }, { left: "$", right: "$", display: false }], throwOnError: false,
        trust: function (ctx) { return ctx.command === "\\htmlClass"; } });
    document.documentElement.setAttribute("data-wb-ready", "1");
  });
})();
