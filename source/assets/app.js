/* ML Academy — shared behaviour (no dependencies) */
(function () {
  "use strict";

  // ---------- Theme ----------
  var root = document.documentElement;
  function getSaved() { try { return localStorage.getItem("mla-theme"); } catch (e) { return null; } }
  function save(v) { try { localStorage.setItem("mla-theme", v); } catch (e) { /* ignore */ } }
  var saved = getSaved();
  if (saved) root.setAttribute("data-theme", saved);
  else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches) root.setAttribute("data-theme", "light");

  document.addEventListener("DOMContentLoaded", function () {
    var toggle = document.getElementById("theme-toggle");
    if (toggle) toggle.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
      root.setAttribute("data-theme", next);
      save(next);
    });

    renderMath();
    highlightCode();
    initQuiz();
    initCompletion();
    addCopyButtons();
    initProgressAndTop();
    initScrollSpy();
    initCurriculumSearch();
  });

  // ---------- Tiny Python highlighter ----------
  function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function highlightCode() {
    var KW = /\b(import|from|as|def|return|for|in|if|else|elif|while|class|with|True|False|None|and|or|not|print|lambda)\b/;
    document.querySelectorAll("pre code").forEach(function (el) {
      var src = el.textContent, out = "", i = 0;
      var re = /(#[^\n]*)|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(\b\d+(?:\.\d+)?(?:e-?\d+)?\b)|([A-Za-z_]\w*)(?=\()|([A-Za-z_]\w*)/g, m;
      while ((m = re.exec(src))) {
        out += esc(src.slice(i, m.index));
        if (m[1]) out += '<span class="tok-com">' + esc(m[1]) + "</span>";
        else if (m[2]) out += '<span class="tok-str">' + esc(m[2]) + "</span>";
        else if (m[3]) out += '<span class="tok-num">' + m[3] + "</span>";
        else if (m[4]) out += KW.test(m[4]) && m[4] !== "print" ? '<span class="tok-kw">' + m[4] + "</span>" : '<span class="tok-fn">' + m[4] + "</span>";
        else if (m[5]) out += KW.test(m[5]) ? '<span class="tok-kw">' + m[5] + "</span>" : m[5];
        i = re.lastIndex;
      }
      el.innerHTML = out + esc(src.slice(i));
    });
  }

  // ---------- Copy buttons ----------
  function addCopyButtons() {
    document.querySelectorAll("pre").forEach(function (pre) {
      if (pre.closest(".terminal")) return;
      var wrap = document.createElement("div");
      wrap.className = "code-wrap";
      pre.parentNode.insertBefore(wrap, pre);
      wrap.appendChild(pre);
      var btn = document.createElement("button");
      btn.className = "copy-btn"; btn.type = "button"; btn.textContent = "Copy";
      btn.addEventListener("click", function () {
        var text = pre.innerText;
        var done = function () { btn.textContent = "Copied"; btn.classList.add("copied");
          setTimeout(function () { btn.textContent = "Copy"; btn.classList.remove("copied"); }, 1600); };
        if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () {});
      });
      wrap.appendChild(btn);
    });
  }

  // ---------- Reading progress + back to top ----------
  function initProgressAndTop() {
    var bar = document.querySelector(".progress");
    var top = document.querySelector(".to-top");
    if (!bar && !top) return;
    function onScroll() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      var p = h > 0 ? (window.scrollY / h) * 100 : 0;
      if (bar) bar.style.width = p + "%";
      if (top) top.classList.toggle("show", window.scrollY > 600);
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    if (top) top.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
  }

  // ---------- TOC scroll-spy ----------
  function initScrollSpy() {
    var links = Array.prototype.slice.call(document.querySelectorAll(".toc a[href^='#']"));
    if (!links.length) return;
    var targets = links.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
    function update() {
      var idx = 0;
      for (var i = 0; i < targets.length; i++) {
        if (targets[i] && targets[i].getBoundingClientRect().top <= 140) idx = i;
      }
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) idx = targets.length - 1;
      links.forEach(function (a, j) { a.classList.toggle("active", j === idx); });
    }
    window.addEventListener("scroll", update, { passive: true });
    update();
  }

  // ---------- Curriculum search & filter (index page) ----------
  function initCurriculumSearch() {
    var input = document.getElementById("module-search");
    var cards = Array.prototype.slice.call(document.querySelectorAll(".module"));
    if (!input || !cards.length) return;
    var chips = Array.prototype.slice.call(document.querySelectorAll(".chip"));
    var empty = document.querySelector(".no-results");
    var level = "all";

    cards.forEach(function (c) {
      c.querySelectorAll("[data-searchable]").forEach(function (el) { el.setAttribute("data-orig", el.innerHTML); });
    });

    function escRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
    function apply() {
      var q = input.value.trim().toLowerCase();
      var shown = 0;
      cards.forEach(function (c) {
        var text = c.textContent.toLowerCase();
        var okLevel = level === "all" || c.getAttribute("data-level") === level;
        var okQ = !q || text.indexOf(q) !== -1;
        var show = okLevel && okQ;
        c.style.display = show ? "" : "none";
        c.querySelectorAll("[data-searchable]").forEach(function (el) {
          var orig = el.getAttribute("data-orig");
          el.innerHTML = q && show ? orig.replace(new RegExp("(" + escRe(q) + ")(?![^<]*>)", "gi"), "<mark>$1</mark>") : orig;
        });
        if (show && q && c.querySelector(".module-body mark")) c.open = true;
        if (show) shown++;
      });
      if (empty) empty.style.display = shown ? "none" : "block";
    }
    input.addEventListener("input", apply);
    chips.forEach(function (ch) {
      ch.addEventListener("click", function () {
        level = ch.getAttribute("data-level");
        chips.forEach(function (x) { x.setAttribute("aria-pressed", x === ch ? "true" : "false"); });
        apply();
      });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "/" && document.activeElement !== input) { e.preventDefault(); input.focus(); }
    });
  }

  // ---------- Math (KaTeX auto-render, bundled locally) ----------
  function renderMath() {
    if (typeof renderMathInElement !== "function") return;
    var target = document.querySelector(".prose") || document.body;
    renderMathInElement(target, {
      delimiters: [{ left: "$$", right: "$$", display: true }, { left: "$", right: "$", display: false }],
      throwOnError: false,
      trust: function (ctx) { return ctx.command === "\\htmlClass"; }
    });
  }

  // ---------- Quizzes ----------
  function initQuiz() {
    document.querySelectorAll(".quiz").forEach(function (quiz) {
      var qs = quiz.querySelectorAll(".q"), score = 0, answered = 0;
      var out = document.createElement("p"); out.className = "quiz-score";
      quiz.appendChild(out);
      function show() { out.textContent = answered ? "Score: " + score + " / " + answered + (answered === qs.length ? "  ·  quiz complete" : "") : "Pick an answer for each question."; }
      show();
      qs.forEach(function (q) {
        var correct = q.getAttribute("data-correct");
        var exp = q.querySelector(".q-explain");
        q.querySelectorAll("button[data-opt]").forEach(function (b) {
          b.addEventListener("click", function () {
            if (q.classList.contains("answered")) return;
            var ok = b.getAttribute("data-opt") === correct;
            q.classList.add("answered"); answered++; if (ok) score++;
            q.querySelectorAll("button[data-opt]").forEach(function (x) {
              x.disabled = true;
              if (x.getAttribute("data-opt") === correct) x.classList.add("correct");
            });
            if (!ok) b.classList.add("wrong");
            if (exp) {
              var v = document.createElement("span"); v.className = "q-verdict";
              v.textContent = ok ? "Correct!" : "Not quite.";
              v.style.color = ok ? "var(--accent)" : "#f87171";
              exp.insertBefore(v, exp.firstChild);
            }
            show();
          });
        });
      });
    });
  }

  // ---------- Lesson completion (saved in this browser only) ----------
  function readDone() { try { return JSON.parse(localStorage.getItem("mla-done") || "[]"); } catch (e) { return []; } }
  function writeDone(a) { try { localStorage.setItem("mla-done", JSON.stringify(a)); } catch (e) { /* ignore */ } }
  function initCompletion() {
    var done = readDone();
    var btn = document.querySelector(".complete-btn");
    if (btn) {
      var id = btn.getAttribute("data-lesson");
      var paint = function () {
        var isDone = done.indexOf(id) !== -1;
        btn.classList.toggle("done", isDone);
        btn.textContent = isDone ? "✓ Completed" : "Mark lesson as complete";
      };
      paint();
      btn.addEventListener("click", function () {
        var i = done.indexOf(id);
        if (i === -1) done.push(id); else done.splice(i, 1);
        writeDone(done); paint();
      });
    }
    var cards = document.querySelectorAll(".lesson-card[data-lesson]");
    if (cards.length) {
      var n = 0;
      var counted = 0;
      cards.forEach(function (c) { var isZero = c.classList.contains("lesson-zero"); if (!isZero) counted++;
        if (done.indexOf(c.getAttribute("data-lesson")) !== -1) { c.classList.add("is-done"); if (!isZero) n++; } });
      var bar = document.querySelector(".overall-bar i"), lbl = document.querySelector(".overall-label");
      if (bar) bar.style.width = (100 * n / counted) + "%";
      if (lbl) lbl.textContent = n + " of " + counted + " lessons completed";
    }
  }
})();
