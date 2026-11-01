/* ML Academy — course-wide search (works offline, no server) */
(function () {
  "use strict";
  var overlay, input, list, active = 0, results = [];
  function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function build() {
    overlay = document.createElement("div"); overlay.className = "search-overlay"; overlay.hidden = true;
    overlay.innerHTML = '<div class="search-panel" role="dialog" aria-modal="true" aria-label="Search the course">' +
      '<div class="search-bar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>' +
      '<input type="search" placeholder="Search lessons, sections and terms — e.g. gradient, overfitting, kernel" aria-label="Search">' +
      '<kbd>Esc</kbd></div><ul class="search-results" role="listbox"></ul>' +
      '<div class="search-foot">↑↓ to move · Enter to open · Esc to close</div></div>';
    document.body.appendChild(overlay);
    input = overlay.querySelector("input"); list = overlay.querySelector(".search-results");
    overlay.addEventListener("click", function (e) { if (e.target === overlay) close(); });
    input.addEventListener("input", run);
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
      else if (e.key === "Enter" && results[active]) { go(results[active]); }
      else if (e.key === "Escape") { close(); }
    });
  }
  function open() { if (!overlay) build(); overlay.hidden = false; input.value = ""; run(); setTimeout(function () { input.focus(); }, 10); }
  function close() { if (overlay) overlay.hidden = true; }
  function go(r) { close(); window.location.href = r.l || r.u; }
  function move(d) { if (!results.length) return; active = (active + d + results.length) % results.length; paint(); }
  function score(entry, terms) {
    var s = 0, t = entry.t.toLowerCase();
    for (var i = 0; i < terms.length; i++) {
      var w = terms[i]; if (entry.x.indexOf(w) === -1) return 0;
      if (t.indexOf(w) === 0) s += 12; else if (t.indexOf(w) > -1) s += 8;
      s += Math.min(5, entry.x.split(w).length - 1);
    }
    if (entry.k === "term") s += 3; if (entry.k === "lesson") s += 2;
    return s;
  }
  function hl(text, terms) {
    var out = esc(text);
    terms.forEach(function (w) { if (w.length < 2) return; out = out.replace(new RegExp("(" + w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "gi"), "<mark>$1</mark>"); });
    return out;
  }
  function run() {
    var q = input.value.trim().toLowerCase(), idx = window.MLA_INDEX || [];
    if (!q) { results = idx.filter(function (e) { return e.k === "lesson"; }).slice(0, 20); }
    else {
      var terms = q.split(/\s+/).filter(Boolean);
      results = idx.map(function (e) { return [score(e, terms), e]; }).filter(function (p) { return p[0] > 0; })
        .sort(function (a, b) { return b[0] - a[0]; }).slice(0, 14).map(function (p) { return p[1]; });
    }
    active = 0; paint();
  }
  function paint() {
    var terms = input.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    if (!results.length) { list.innerHTML = '<li class="search-empty">No matches. Try a shorter word, or check the glossary.</li>'; return; }
    list.innerHTML = results.map(function (r, i) {
      var kind = r.k === "term" ? "Glossary" : r.k === "lesson" ? "Lesson" : r.k === "iq" ? "Interview" : "Section";
      return '<li role="option" class="' + (i === active ? "on" : "") + '" data-i="' + i + '"><span class="sr-kind">' + kind + '</span><div><div class="sr-title">' + hl(r.t, terms) + '</div><div class="sr-sub">' + hl(r.s.slice(0, 150), terms) + '</div></div></li>';
    }).join("");
    [].forEach.call(list.children, function (li) {
      li.addEventListener("click", function () { go(results[+li.getAttribute("data-i")]); });
      li.addEventListener("mousemove", function () { var i = +li.getAttribute("data-i"); if (i !== active) { active = i; paint(); } });
    });
    var on = list.querySelector(".on"); if (on && on.scrollIntoView) on.scrollIntoView({ block: "nearest" });
  }
  document.addEventListener("DOMContentLoaded", function () {
    [].forEach.call(document.querySelectorAll("[data-search-open]"), function (b) { b.addEventListener("click", open); });
  });
  document.addEventListener("keydown", function (e) {
    var tag = (document.activeElement && document.activeElement.tagName) || "";
    var typing = /INPUT|TEXTAREA|SELECT/.test(tag);
    if ((e.key === "/" && !typing) || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k")) { e.preventDefault(); open(); }
  });
})();
