/* ML Academy — learning routes, time and quiz tracking, and the progress dashboard. Everything is stored in this browser only. */
(function () {
  "use strict";
  function load(k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* ignore */ } }
  function esc(s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
  function url(n) { return "lesson-" + (n < 10 ? "0" : "") + n + ".html"; }
  function fmtTime(sec) { sec = Math.round(sec || 0); if (sec < 60) return sec ? "<1 min" : "—"; var m = Math.round(sec / 60); return m < 60 ? m + " min" : Math.floor(m / 60) + " h " + (m % 60) + " min"; }
  var KEYS = ["mla-done", "mla-quiz", "mla-time", "mla-ex", "mla-tests", "mla-srs", "mla-route", "mla-level", "mla-a11y", "mla-theme", "mla-listen", "mla-notes"];

  document.addEventListener("DOMContentLoaded", function () {
    var D = window.MLA_DATA; if (!D) return;
    var cbtn = document.querySelector(".complete-btn[data-lesson]"), lesson = cbtn ? +cbtn.getAttribute("data-lesson") : null;
    var routeId = load("mla-route", ""), route = D.routes.filter(function (r) { return r.id === routeId; })[0] || null;

    if (lesson) {
      // ---- time on this lesson: counted in 15 s ticks while the tab is visible and the reader was active in the last 2 minutes
      var last = Date.now();
      ["scroll", "keydown", "pointerdown", "pointermove"].forEach(function (ev) { window.addEventListener(ev, function () { last = Date.now(); }, { passive: true }); });
      setInterval(function () {
        if (document.visibilityState !== "visible" || Date.now() - last > 120000) return;
        var T = load("mla-time", {}); T[lesson] = (T[lesson] || 0) + 15; save("mla-time", T);
      }, 15000);
      // ---- first answer to each lesson-quiz question
      var qs = document.querySelectorAll(".quiz:not(.deep-quiz) .q");
      document.addEventListener("click", function (e) {
        var b = e.target.closest && e.target.closest(".quiz:not(.deep-quiz) .q button[data-opt]"); if (!b) return;
        var q = b.closest(".q"); if (q.classList.contains("answered")) return;
        var Q = load("mla-quiz", {}), k = Array.prototype.indexOf.call(qs, q); Q[lesson] = Q[lesson] || {};
        if (!(k in Q[lesson])) { Q[lesson][k] = b.getAttribute("data-opt") === q.getAttribute("data-correct") ? 1 : 0; save("mla-quiz", Q); }
      }, true);
      // ---- route banner and "next on your route"
      if (route) {
        var i = route.lessons.indexOf(lesson), ban = document.querySelector(".route-banner"), nxt = document.querySelector(".route-next");
        if (ban) {
          ban.hidden = false;
          if (i === -1) ban.innerHTML = 'Your route: <b>' + esc(route.name) + '</b> — this lesson isn\'t on it (it\'s optional for you). <a href="map.html?route=' + route.id + '">See your route</a>';
          else ban.innerHTML = 'Your route: <b>' + esc(route.name) + '</b> · lesson ' + (i + 1) + ' of ' + route.lessons.length +
            (route.skipped.length && D.deps[lesson] && D.deps[lesson].some(function (d) { return route.lessons.indexOf(d) === -1; }) ? ' · this lesson builds on lessons your route skips; the "Before you start" box below recaps them.' : '') +
            ' <a href="map.html?route=' + route.id + '">Change</a>';
        }
        var nextN = i === -1 ? route.lessons.filter(function (l) { return l > lesson; })[0] : route.lessons[i + 1];
        if (nxt && nextN) { var L = D.lessons[nextN - 1]; nxt.hidden = false; nxt.innerHTML = '<span>Next on your route (' + esc(route.name) + ')</span><a href="' + url(nextN) + '">Lesson ' + nextN + ': ' + esc(L.t) + ' →</a>'; }
        else if (nxt && i === route.lessons.length - 1) { nxt.hidden = false; nxt.innerHTML = '<span>You\'ve reached the end of your route.</span><a href="progress.html">See your progress →</a>'; }
      }
    }

    // ---------------- course map: highlight a route ----------------
    var pick = document.querySelector(".route-pick");
    if (pick) {
      var panel = document.querySelector(".route-panel"), svg = document.querySelector(".course-map");
      function show(id) {
        var r = D.routes.filter(function (x) { return x.id === id; })[0] || null;
        pick.querySelectorAll("button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-route") === (id || "") ? "true" : "false"); });
        svg.classList.toggle("routing", !!r);
        svg.querySelectorAll(".m-order").forEach(function (x) { x.remove(); });
        svg.querySelectorAll(".m-node").forEach(function (a) {
          var n = +a.getAttribute("data-lesson"), k = r ? r.lessons.indexOf(n) : -1;
          a.classList.toggle("on-route", k !== -1);
          if (k !== -1) {
            var rc = a.querySelector("rect"), x = +rc.getAttribute("x") + +rc.getAttribute("width") - 4, y = +rc.getAttribute("y") + 4, ns = "http://www.w3.org/2000/svg";
            var g = document.createElementNS(ns, "g"); g.setAttribute("class", "m-order");
            var c = document.createElementNS(ns, "circle"); c.setAttribute("cx", x); c.setAttribute("cy", y); c.setAttribute("r", 12);
            var t = document.createElementNS(ns, "text"); t.setAttribute("x", x); t.setAttribute("y", y + 4); t.textContent = k + 1;
            g.appendChild(c); g.appendChild(t); a.appendChild(g);
          }
        });
        svg.querySelectorAll(".m-edge").forEach(function (p) { var f = +p.getAttribute("data-from"), t = +p.getAttribute("data-to");
          p.classList.toggle("on-route", !!r && r.lessons.indexOf(f) !== -1 && r.lessons.indexOf(t) !== -1); });
        if (!r) { panel.innerHTML = '<p>Showing all lessons. Pick a route above to highlight it.</p>'; return; }
        var done = load("mla-done", []).map(Number), nDone = r.lessons.filter(function (l) { return done.indexOf(l) !== -1; }).length, mine = load("mla-route", "") === r.id;
        panel.innerHTML = '<h2>' + esc(r.name) + '</h2><p>' + esc(r.blurb) + '</p><p class="route-meta">' + r.lessons.length + ' lessons · about ' + Math.round(r.mins / 60) + ' hours · ' + nDone + ' done</p>' +
          '<ol class="route-list">' + r.lessons.map(function (l) { var L = D.lessons[l - 1]; return '<li' + (done.indexOf(l) !== -1 ? ' class="done"' : '') + '><a href="' + url(l) + '">Lesson ' + l + ': ' + esc(L.t) + '</a> <span>~' + L.mins + ' min</span></li>'; }).join("") + '</ol>' +
          (r.skipped.length ? '<p class="route-skip">Skipped prerequisites: ' + r.skipped.map(function (l) { return '<a href="' + url(l) + '">Lesson ' + l + '</a>'; }).join(", ") + ' — each lesson\'s "Before you start" box recaps what you need from them.</p>' : '') +
          '<p><button type="button" class="btn ' + (mine ? '' : 'btn-primary ') + 'route-follow" data-route="' + r.id + '">' + (mine ? '✓ This is your route — stop following' : 'Follow this route') + '</button></p>';
      }
      pick.addEventListener("click", function (e) { var b = e.target.closest("button[data-route]"); if (!b) return; show(b.getAttribute("data-route")); history.replaceState(null, "", b.getAttribute("data-route") ? "?route=" + b.getAttribute("data-route") : location.pathname); });
      panel.addEventListener("click", function (e) {
        var b = e.target.closest(".route-follow"); if (!b) return; var id = b.getAttribute("data-route");
        save("mla-route", load("mla-route", "") === id ? "" : id); show(id);
      });
      var m = /[?&]route=([a-z]+)/.exec(location.search); show(m ? m[1] : (routeId || ""));
    }

    // ---------------- progress dashboard ----------------
    var P = document.getElementById("progress-app");
    if (P) {
      function render() {
        var done = load("mla-done", []).map(Number), Q = load("mla-quiz", {}), T = load("mla-time", {}), X = load("mla-ex", {}), TS = load("mla-tests", {}), S = load("mla-srs", {});
        var totTime = 0, qOk = 0, qAll = 0, exOk = 0, exAll = 0, exTried = 0, genOk = 0;
        var rows = D.lessons.map(function (L) {
          var q = Q[L.n] || {}, qa = Object.keys(q).length, qo = Object.keys(q).filter(function (k) { return q[k]; }).length; qAll += qa; qOk += qo;
          var eo = L.ex.filter(function (k) { return X[k] && X[k].ok; }).length, et = L.ex.filter(function (k) { return X[k]; }).length; exOk += eo; exTried += et; exAll += L.ex.length;
          var g = X["gen-" + L.n]; if (g && g.ok) genOk++;
          totTime += T[L.n] || 0;
          return { L: L, done: done.indexOf(L.n) !== -1, qa: qa, qo: qo, eo: eo, et: et, t: T[L.n] || 0, gen: g };
        });
        var srsIds = Object.keys(S), mastered = srsIds.filter(function (k) { return S[k].b >= 4; }).length, due = srsIds.filter(function (k) { return S[k].due <= Date.now(); }).length;
        var r = D.routes.filter(function (x) { return x.id === load("mla-route", ""); })[0] || D.routes[D.routes.length - 1];
        var next = r.lessons.filter(function (l) { return done.indexOf(l) === -1; })[0];
        var h = '<div class="pg-stats">' +
          '<div><b>' + done.length + '<small>/21</small></b><span>lessons completed</span></div>' +
          '<div><b>' + fmtTime(totTime) + '</b><span>time on lessons</span></div>' +
          '<div><b>' + (qAll ? Math.round(100 * qOk / qAll) + '%' : '—') + '</b><span>quiz answers right first time (' + qOk + '/' + qAll + ')</span></div>' +
          '<div><b>' + exOk + '<small>/' + exAll + '</small></b><span>exercises checked correct</span></div>' +
          '<div><b>' + Object.keys(TS).length + '<small>/5</small></b><span>part tests taken</span></div>' +
          '<div><b>' + mastered + '</b><span>review questions mastered · ' + due + ' due</span></div></div>';
        h += '<div class="pg-next">' + (next ? '<span>Next up on <b>' + esc(r.name) + '</b>:</span> <a class="btn btn-primary" href="' + url(next) + '">Lesson ' + next + ': ' + esc(D.lessons[next - 1].t) + ' →</a>' : '<span>You\'ve finished <b>' + esc(r.name) + '</b>.</span> <a href="map.html">Choose another route</a>') +
          (due ? ' <a class="btn" href="review.html">Review ' + due + ' due question' + (due > 1 ? 's' : '') + '</a>' : '') + '</div>';
        D.parts.forEach(function (part, pi) {
          var rs = rows.filter(function (x) { return x.L.p === pi; }), nDone = rs.filter(function (x) { return x.done; }).length;
          var pq = rs.reduce(function (a, x) { return a + x.qo; }, 0), pqa = rs.reduce(function (a, x) { return a + x.qa; }, 0);
          var pe = rs.reduce(function (a, x) { return a + x.eo; }, 0), pea = rs.reduce(function (a, x) { return a + x.L.ex.length; }, 0), test = TS[pi];
          var badges = [
            ["Finisher", "All " + rs.length + " lessons marked complete", nDone === rs.length],
            ["Quiz whizz", "At least 80% of the part's quiz questions right first time (all answered)", pqa === rs.length * 5 && pq / pqa >= 0.8],
            ["Practiser", "At least half of the part's checked exercises solved", pea && pe / pea >= 0.5],
            ["Test ace", "12 or more out of 15 in the part test", test && test.best >= 12]
          ];
          h += '<section class="pg-part"><div class="pg-part-head"><div><span class="eyebrow">' + esc(part.label) + '</span><h2>' + esc(part.title) + '</h2></div><div class="pg-bar" role="img" aria-label="' + nDone + ' of ' + rs.length + ' lessons complete"><i style="width:' + (100 * nDone / rs.length) + '%"></i></div><span class="pg-frac">' + nDone + '/' + rs.length + '</span></div>';
          h += '<ul class="pg-badges">' + badges.map(function (b) { return '<li class="' + (b[2] ? 'got' : '') + '" title="' + esc(b[1]) + '"><span class="pg-medal" aria-hidden="true">' + (b[2] ? '★' : '☆') + '</span><b>' + b[0] + '</b><small>' + esc(b[1]) + (b[2] ? ' — earned' : ' — not yet') + '</small></li>'; }).join("") + '</ul>';
          h += '<div class="table-scroll"><table class="tbl pg-tbl"><thead><tr><th>Lesson</th><th>Done</th><th>Quiz</th><th>Exercises</th><th>Time</th></tr></thead><tbody>' + rs.map(function (x) {
            return '<tr><td><a href="' + url(x.L.n) + '">' + x.L.n + '. ' + esc(x.L.t) + '</a></td><td>' + (x.done ? '<span class="pg-yes">✓</span>' : '—') + '</td><td>' + (x.qa ? x.qo + '/' + x.qa + (x.qa < 5 ? ' <small>(' + x.qa + ' of 5 answered)</small>' : '') : '—') + '</td><td>' +
              (x.L.ex.length ? x.eo + '/' + x.L.ex.length + (x.et > x.eo ? ' <small>(' + (x.et - x.eo) + ' tried)</small>' : '') : '—') + '</td><td>' + fmtTime(x.t) + '</td></tr>'; }).join("") +
            '</tbody></table></div>' + (test ? '<p class="pg-test">Part test: best <b>' + test.best + '/15</b>, last ' + test.last + '/15. <a href="tests.html?part=' + (pi + 1) + '">Retake</a></p>' : '<p class="pg-test"><a href="tests.html?part=' + (pi + 1) + '">Take the ' + esc(part.label) + ' test →</a></p>') + '</section>';
        });
        h += '<section class="pg-data"><h2>Your data</h2><p>Progress is stored only in this browser. To move it to another browser or computer, download it and restore it there.</p>' +
          '<p class="pg-actions"><button type="button" class="btn pg-export">⬇ Download my progress</button><label class="btn pg-import">⬆ Restore from file<input type="file" accept="application/json,.json" hidden></label><button type="button" class="btn pg-reset">Reset all progress</button></p><p class="pg-msg" aria-live="polite"></p></section>';
        P.innerHTML = h;
      }
      P.addEventListener("click", function (e) {
        var b = e.target.closest("button"); if (!b) return;
        if (b.classList.contains("pg-export")) {
          var data = { app: "ML Academy", saved: new Date().toISOString(), data: {} };
          KEYS.forEach(function (k) { try { var v = localStorage.getItem(k); if (v != null) data.data[k] = v; } catch (err) { /* ignore */ } });
          var u = URL.createObjectURL(new Blob([JSON.stringify(data, null, 1)], { type: "application/json" })), a = document.createElement("a");
          a.href = u; a.download = "ml-academy-progress.json"; document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(u); a.remove(); }, 1000);
        } else if (b.classList.contains("pg-reset")) {
          if (!window.confirm("Delete all progress saved in this browser (lessons, quiz answers, exercises, tests, review, time and notes)? Download a copy first if you might want it back.")) return;
          ["mla-done", "mla-quiz", "mla-time", "mla-ex", "mla-tests", "mla-srs", "mla-route", "mla-notes"].forEach(function (k) { try { localStorage.removeItem(k); } catch (err) { /* ignore */ } });
          render(); P.querySelector(".pg-msg").textContent = "Progress reset.";
        }
      });
      P.addEventListener("change", function (e) {
        var inp = e.target; if (inp.type !== "file" || !inp.files[0]) return;
        var fr = new FileReader();
        fr.onload = function () {
          try {
            var obj = JSON.parse(fr.result); if (!obj || obj.app !== "ML Academy" || typeof obj.data !== "object") throw new Error("not an ML Academy progress file");
            var n = 0; Object.keys(obj.data).forEach(function (k) { if (KEYS.indexOf(k) !== -1 && typeof obj.data[k] === "string") { JSON.parse(obj.data[k]); localStorage.setItem(k, obj.data[k]); n++; } });
            render(); P.querySelector(".pg-msg").textContent = "Restored " + n + " kinds of progress from " + inp.files[0].name + ".";
          } catch (err) { P.querySelector(".pg-msg").textContent = "Couldn't restore: " + err.message + "."; }
        };
        fr.readAsText(inp.files[0]);
      });
      render();
    }
  });
})();
