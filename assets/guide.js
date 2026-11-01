/* ML Academy — algorithm decision guide */
(function () {
  "use strict";
  document.addEventListener("DOMContentLoaded", function () {
    var root = document.getElementById("guide"); if (!root || !window.MLA_GUIDE) return;
    var G = window.MLA_GUIDE, path = [];   // path: [{q: nodeId, a: optionIndex}]
    function esc(s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
    function lesson(n) { return '<a href="lesson-' + (n < 10 ? "0" : "") + n + '.html">Lesson ' + n + ": " + esc(G.titles[n - 1]) + "</a>"; }
    function render() {
      var cur = "start";
      path.forEach(function (p) { cur = G.q[p.q][2][p.a][2]; });
      var h = "";
      if (path.length) {
        h += '<ol class="g-trail">';
        path.forEach(function (p, k) { h += '<li><span class="g-tq">' + esc(G.q[p.q][0]) + '</span> <button type="button" class="g-change" data-k="' + k + '" title="Change this answer">' + esc(G.q[p.q][2][p.a][0]) + " ✎</button></li>"; });
        h += "</ol>";
      }
      if (G.q[cur]) {
        var q = G.q[cur];
        h += '<div class="g-card"><p class="g-step">Question ' + (path.length + 1) + '</p><h2 class="g-q" tabindex="-1">' + esc(q[0]) + "</h2>" + (q[1] ? '<p class="g-help">' + esc(q[1]) + "</p>" : "") + '<div class="g-opts">';
        q[2].forEach(function (o, j) { h += '<button type="button" class="g-opt" data-j="' + j + '"><b>' + esc(o[0]) + "</b>" + (o[1] ? "<span>" + esc(o[1]) + "</span>" : "") + "</button>"; });
        h += "</div></div>";
      } else {
        var r = G.r[cur];
        h += '<div class="g-card g-result"><p class="g-step">Recommendation</p><h2 class="g-q" tabindex="-1">' + esc(r[0]) + '</h2><ol class="g-models">';
        r[1].forEach(function (m) { h += "<li><b>" + esc(m[0]) + "</b><span>" + esc(m[2]) + ' <a href="lesson-' + (m[1] < 10 ? "0" : "") + m[1] + '.html">→ Lesson ' + m[1] + "</a></span></li>"; });
        h += '</ol><p class="g-read"><strong>Read first:</strong> ' + r[2].map(lesson).join(" · ") + '</p><p class="g-watch"><strong>Watch out:</strong> ' + esc(r[3]) + "</p>";
        h += '<p class="g-rule">Whatever you choose: start with a simple baseline, compare candidates with cross-validation (<a href="lesson-05.html">Lesson 5</a>) and the right metric (<a href="lesson-09.html">Lesson 9</a>), and keep preprocessing inside a pipeline (<a href="lesson-20.html">Lesson 20</a>).</p></div>';
      }
      h += '<div class="g-nav">' + (path.length ? '<button type="button" class="btn g-back">← Back</button><button type="button" class="btn g-restart">↺ Start over</button>' : "") + "</div>";
      root.innerHTML = h;
      var focusEl = root.querySelector(".g-q"); if (focusEl && path.length) focusEl.focus({ preventScroll: true });
    }
    root.addEventListener("click", function (e) {
      var t = e.target.closest("button"); if (!t) return;
      if (t.classList.contains("g-opt")) {
        var cur = "start"; path.forEach(function (p) { cur = G.q[p.q][2][p.a][2]; });
        path.push({ q: cur, a: +t.getAttribute("data-j") });
      } else if (t.classList.contains("g-back")) path.pop();
      else if (t.classList.contains("g-restart")) path = [];
      else if (t.classList.contains("g-change")) path = path.slice(0, +t.getAttribute("data-k"));
      render();
    });
    render();
  });
})();
