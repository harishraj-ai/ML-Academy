/* ML Academy — spaced review (Leitner boxes) and end-of-part tests. Everything is saved in this browser only. */
(function () {
  "use strict";
  var DAY = 864e5, INTERVAL = [0, 1, 3, 7, 16, 35];   // days until the next review, per box
  function load(k, d) { try { return JSON.parse(localStorage.getItem(k) || d); } catch (e) { return JSON.parse(d); } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* ignore */ } }
  function record(id, ok) {
    var S = load("mla-srs", "{}"), s = S[id] || { b: 0, r: 0, w: 0 }, now = Date.now();
    if (ok) { s.b = Math.min(s.b + 1, 5); s.r++; } else { s.b = 1; s.w++; }
    s.due = ok ? now + INTERVAL[s.b] * DAY : now; s.t = now; S[id] = s; save("mla-srs", S);
  }
  function enroll(ids) {
    var S = load("mla-srs", "{}"), now = Date.now(), added = 0;
    ids.forEach(function (id) { if (!S[id]) { S[id] = { b: 0, r: 0, w: 0, due: now, t: now }; added++; } });
    save("mla-srs", S); return added;
  }
  window.MLA_SRS = { record: record, enroll: enroll, load: function () { return load("mla-srs", "{}"); } };
  function math(el) {
    if (typeof renderMathInElement === "function") renderMathInElement(el, { delimiters: [{ left: "$$", right: "$$", display: true }, { left: "$", right: "$", display: false }], throwOnError: false });
  }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function lessonUrl(n, s) { return "lesson-" + (n < 10 ? "0" : "") + n + ".html" + (s ? "#" + s : ""); }
  function esc(s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
  function when(ms) {
    var d = ms - Date.now(); if (d <= 0) return "now";
    var h = d / 36e5; if (h < 24) return "in " + Math.max(1, Math.round(h)) + " h";
    return "in " + Math.round(h / 24) + " day" + (Math.round(h / 24) === 1 ? "" : "s");
  }

  document.addEventListener("DOMContentLoaded", function () {
    // --- record answers given in lesson quizzes, and enrol a lesson's questions when it's marked complete
    var cbtn = document.querySelector(".complete-btn[data-lesson]");
    if (cbtn) {
      var n = cbtn.getAttribute("data-lesson"), qs = document.querySelectorAll(".quiz .q");
      document.addEventListener("click", function (e) {
        var b = e.target.closest && e.target.closest(".quiz .q button[data-opt]"); if (!b) return;
        var q = b.closest(".q"); if (q.classList.contains("answered")) return;
        var k = Array.prototype.indexOf.call(qs, q);
        record("L" + n + "-" + k, b.getAttribute("data-opt") === q.getAttribute("data-correct"));
      }, true);
      cbtn.addEventListener("click", function () {
        setTimeout(function () {                        // let app.js toggle first: enrol only when the lesson was just marked complete
          if (!cbtn.classList.contains("done")) return;
          var ids = []; for (var k = 0; k < qs.length; k++) ids.push("L" + n + "-" + k);
          enroll(ids);
        }, 0);
      });
    }

    var B = window.MLA_QBANK;
    // ---------------- Review page ----------------
    var R = document.getElementById("review-app");
    if (R && B) {
      var queue = [], pos = 0, right = 0, requeued = {};
      function stats() {
        var S = load("mla-srs", "{}"), ids = Object.keys(S).filter(function (id) { return B[id]; }), now = Date.now();
        var due = ids.filter(function (id) { return S[id].due <= now; }), boxes = [0, 0, 0, 0, 0, 0];
        ids.forEach(function (id) { boxes[S[id].b]++; });
        var next = ids.filter(function (id) { return S[id].due > now; }).map(function (id) { return S[id].due; }).sort()[0];
        return { S: S, ids: ids, due: due, boxes: boxes, next: next };
      }
      function home() {
        var st = stats(), h = '<div class="rv-stats"><div><b>' + st.due.length + '</b><span>due now</span></div><div><b>' + st.ids.length + '</b><span>in your deck</span></div><div><b>' + st.boxes[5] + '</b><span>mastered</span></div><div><b>' + (st.next ? when(st.next) : "—") + '</b><span>next due</span></div></div>';
        if (st.ids.length) {
          h += '<div class="rv-boxes" aria-label="Questions per box">' + [1, 2, 3, 4, 5].map(function (b) {
            var c = st.boxes[b] + (b === 1 ? st.boxes[0] : 0); return '<div><i style="height:' + (st.ids.length ? Math.max(4, 100 * c / st.ids.length) : 4) + '%"></i><span>Box ' + b + "<br>" + c + "</span></div>"; }).join("") + "</div>";
          h += '<p class="rv-note">Box 1 is reviewed daily, then every 3, 7, 16 and 35 days. A right answer moves a question up one box; a wrong answer sends it back to box 1.</p>';
        }
        h += st.due.length ? '<button type="button" class="btn btn-primary rv-start">Start review (' + Math.min(st.due.length, 20) + " question" + (st.due.length === 1 ? "" : "s") + ")</button>"
          : '<p class="rv-empty">' + (st.ids.length ? "Nothing is due right now — come back " + when(st.next) + "." : "Your review deck is empty.") + "</p>";
        h += '<details class="rv-add"' + (st.ids.length ? "" : " open") + '><summary>Add questions from lessons</summary><p>Questions are added automatically when you answer a lesson quiz, take an end-of-part test, or mark a lesson as complete. You can also add a lesson\'s quiz here:</p><div class="rv-lessons">';
        var nums = Object.keys(B).filter(function (id) { return id[0] === "L"; }).map(function (id) { return B[id].n; }).filter(function (v, i, a) { return v > 0 && a.indexOf(v) === i; }).sort(function (a, b) { return a - b; });
        nums.forEach(function (n) {
          var ids = Object.keys(B).filter(function (id) { return B[id].n === n && id[0] === "L"; }), have = ids.filter(function (id) { return st.S[id]; }).length;
          h += '<label><input type="checkbox" value="' + n + '"' + (have === ids.length ? " checked disabled" : "") + "> Lesson " + n + "</label>";
        });
        h += '</div><button type="button" class="btn rv-addbtn">Add selected</button></details>';
        if (st.ids.length) h += '<p><button type="button" class="rv-reset">Reset all review data</button></p>';
        R.innerHTML = h;
      }
      function card() {
        if (pos >= queue.length) {
          R.innerHTML = '<div class="rv-card"><p class="g-step">Session complete</p><h2 class="g-q">' + right + " / " + (queue.length - Object.keys(requeued).length) + " right first time</h2><p>" +
            (!Object.keys(requeued).length ? "Perfect — these questions move up a box and come back later." : "Questions you missed went back to box 1 and will return tomorrow; the links above each one lead to the section to re-read.") +
            '</p><button type="button" class="btn rv-home">Back to review overview</button></div>';
          return;
        }
        var id = queue[pos], q = B[id], order = shuffle(q.o.map(function (_, i) { return i; }));
        var src = id[0] === "L" ? "Lesson " + q.n + " quiz" : "Part " + id.slice(1).split("-")[0] + " test";
        R.innerHTML = '<div class="rv-card" data-id="' + id + '"><p class="g-step">Question ' + (pos + 1) + " of " + queue.length + ' · <a href="' + lessonUrl(q.n, q.s) + '">' + src + "</a></p>" +
          '<p class="rv-q">' + q.q + '</p><div class="rv-opts">' + order.map(function (i) { return '<button type="button" class="rv-opt" data-i="' + i + '">' + q.o[i] + "</button>"; }).join("") +
          '</div><div class="rv-exp" hidden></div><button type="button" class="btn btn-primary rv-next" hidden>Next →</button></div>';
        math(R);
      }
      R.addEventListener("click", function (e) {
        var t = e.target.closest("button"); if (!t) return;
        if (t.classList.contains("rv-start")) {
          var st = stats(); queue = st.due.sort(function (a, b) { return st.S[a].due - st.S[b].due; }).slice(0, 20); pos = 0; right = 0; requeued = {}; card();
        } else if (t.classList.contains("rv-opt")) {
          var id = queue[pos], q = B[id], i = +t.getAttribute("data-i"), ok = i === q.c;
          R.querySelectorAll(".rv-opt").forEach(function (b) { b.disabled = true; if (+b.getAttribute("data-i") === q.c) b.classList.add("correct"); });
          if (!ok) t.classList.add("wrong");
          if (!requeued[id]) { record(id, ok); if (ok) right++; }
          else if (ok) { var S2 = load("mla-srs", "{}"); if (S2[id]) { S2[id].due = Date.now() + DAY; save("mla-srs", S2); } }   // missed earlier, now right: see it again tomorrow
          if (!ok && !requeued[id]) { requeued[id] = 1; queue.push(id); }
          var ex = R.querySelector(".rv-exp"); ex.hidden = false;
          ex.innerHTML = "<strong>" + (ok ? "Correct!" : "Not quite.") + "</strong> " + q.x + (ok ? "" : ' <a href="' + lessonUrl(q.n, q.s) + '">Re-read this in Lesson ' + q.n + " →</a>") + (!ok && requeued[id] && queue.indexOf(id) !== pos ? ' <em>It will come back at the end of this session.</em>' : "");
          math(ex); R.querySelector(".rv-next").hidden = false; R.querySelector(".rv-next").focus();
        } else if (t.classList.contains("rv-next")) { pos++; card(); }
        else if (t.classList.contains("rv-home")) home();
        else if (t.classList.contains("rv-addbtn")) {
          var ids = []; R.querySelectorAll(".rv-lessons input:checked:not(:disabled)").forEach(function (c) {
            Object.keys(B).forEach(function (id) { if (id[0] === "L" && B[id].n === +c.value) ids.push(id); }); });
          enroll(ids); home();
        } else if (t.classList.contains("rv-reset")) {
          if (window.confirm("Delete all spaced-review progress saved in this browser? Lesson completion and test scores are kept.")) { save("mla-srs", {}); home(); }
        }
      });
      home();
    }

    // ---------------- Tests page ----------------
    var T = document.getElementById("tests-app");
    if (T && B && window.MLA_PARTS) {
      var P = window.MLA_PARTS, cur = null;
      function overview() {
        var res = load("mla-tests", "{}");
        T.innerHTML = '<div class="tp-grid">' + P.map(function (p, k) {
          var r = res[k];
          return '<div class="tp-card"><span class="eyebrow">' + esc(p.label) + "</span><h2 class=\"tp-title\">" + esc(p.title) + '</h2><p class="tp-lessons">Lessons ' + p.lessons[0] + "–" + p.lessons[p.lessons.length - 1] + " · 15 questions · ~15 min</p>" +
            (r ? '<p class="tp-score">Best: <b>' + r.best + "/15</b> · last: " + r.last + "/15</p>" : '<p class="tp-score">Not taken yet</p>') +
            '<button type="button" class="btn btn-primary tp-start" data-p="' + k + '">' + (r ? "Retake" : "Start") + " test</button></div>";
        }).join("") + "</div>";
      }
      function start(k) {
        var ids = Object.keys(B).filter(function (id) { return id.indexOf("P" + (k + 1) + "-") === 0; });
        cur = { k: k, ids: ids, order: ids.map(function (id) { return shuffle(B[id].o.map(function (_, i) { return i; })); }), ans: {} };
        var h = '<div class="tp-head"><h2>' + esc(P[k].label + ": " + P[k].title) + '</h2><p>Answer all 15, then press <strong>Submit</strong> at the bottom. You get the explanations and a list of sections to review afterwards.</p></div><ol class="tp-qs">';
        ids.forEach(function (id, j) {
          var q = B[id];
          h += '<li class="tp-q" data-j="' + j + '"><p class="rv-q">' + q.q + '</p><div class="rv-opts">' + cur.order[j].map(function (i) {
            return '<button type="button" class="rv-opt" data-j="' + j + '" data-i="' + i + '" aria-pressed="false">' + q.o[i] + "</button>"; }).join("") + '</div><div class="rv-exp" hidden></div></li>';
        });
        h += '</ol><div class="tp-submit"><button type="button" class="btn btn-primary tp-go">Submit test</button><span class="tp-left"></span><button type="button" class="btn tp-back">Cancel</button></div>';
        T.innerHTML = h; math(T); left(); T.scrollIntoView({ block: "start" });
      }
      function left() { var n = cur.ids.length - Object.keys(cur.ans).length; T.querySelector(".tp-left").textContent = n ? n + " unanswered" : "All answered"; }
      function submit() {
        var score = 0, weak = {}, order = [];
        cur.ids.forEach(function (id, j) {
          var q = B[id], li = T.querySelector('.tp-q[data-j="' + j + '"]'), a = cur.ans[j], ok = a === q.c;
          if (ok) score++;
          record(id, ok);
          li.classList.add(ok ? "ok" : "bad");
          li.querySelectorAll(".rv-opt").forEach(function (b) { b.disabled = true; var i = +b.getAttribute("data-i"); if (i === q.c) b.classList.add("correct"); else if (i === a) b.classList.add("wrong"); });
          var ex = li.querySelector(".rv-exp"); ex.hidden = false;
          ex.innerHTML = "<strong>" + (ok ? "Correct." : a == null ? "Not answered." : "Not quite.") + "</strong> " + q.x + ' <a href="' + lessonUrl(q.n, q.s) + '">Lesson ' + q.n + " →</a>";
          if (!ok) { var key = q.n + "#" + q.s; if (!weak[key]) { weak[key] = { n: q.n, s: q.s, t: q.st, c: 0 }; order.push(key); } weak[key].c++; }
        });
        math(T);
        var res = load("mla-tests", "{}"), r = res[cur.k] || { best: 0 };
        r.best = Math.max(r.best, score); r.last = score; r.t = Date.now(); res[cur.k] = r; save("mla-tests", res);
        var pct = Math.round(100 * score / cur.ids.length);
        var msg = pct >= 87 ? "Excellent — you've got this part." : pct >= 67 ? "Good work. Review the sections below to close the gaps." : "Worth another pass: re-read the sections below, then retake the test.";
        var box = '<div class="tp-result"><p class="g-step">Your score</p><h2 class="g-q">' + score + " / " + cur.ids.length + " (" + pct + "%)</h2><p>" + msg + "</p>";
        if (order.length) box += '<h3>Review these sections</h3><ul class="tp-weak">' + order.map(function (k) { var w = weak[k]; return '<li><a href="' + lessonUrl(w.n, w.s) + '">Lesson ' + w.n + ": " + esc(w.t) + "</a>" + (w.c > 1 ? " (" + w.c + " questions)" : "") + "</li>"; }).join("") + "</ul>";
        box += '<p class="rv-note">Missed questions were added to your <a href="review.html">spaced review</a> deck.</p><div class="tp-submit"><button type="button" class="btn btn-primary tp-retake">Retake (new order)</button><button type="button" class="btn tp-back">All tests</button></div></div>';
        T.querySelector(".tp-submit").outerHTML = "";
        T.insertAdjacentHTML("afterbegin", box); T.scrollIntoView({ block: "start" });
      }
      T.addEventListener("click", function (e) {
        var t = e.target.closest("button"); if (!t) return;
        if (t.classList.contains("tp-start")) start(+t.getAttribute("data-p"));
        else if (t.classList.contains("rv-opt") && !t.disabled) {
          var j = +t.getAttribute("data-j"); cur.ans[j] = +t.getAttribute("data-i");
          t.parentNode.querySelectorAll(".rv-opt").forEach(function (b) { b.classList.toggle("picked", b === t); b.setAttribute("aria-pressed", b === t ? "true" : "false"); });
          left();
        } else if (t.classList.contains("tp-go")) {
          var n = cur.ids.length - Object.keys(cur.ans).length;
          if (n && !window.confirm(n + " question" + (n > 1 ? "s are" : " is") + " unanswered and will count as wrong. Submit anyway?")) return;
          submit();
        } else if (t.classList.contains("tp-retake")) start(cur.k);
        else if (t.classList.contains("tp-back")) { overview(); T.scrollIntoView({ block: "start" }); }
      });
      var m = /[?&]part=(\d)/.exec(location.search);
      if (m && P[+m[1] - 1]) start(+m[1] - 1); else overview();
    }
  });
})();
