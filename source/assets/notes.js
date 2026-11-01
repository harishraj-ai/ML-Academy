/* ML Academy — highlights and personal notes, saved in this browser only. */
(function () {
  "use strict";
  var KEY = "mla-notes";
  var SKIP = ".route-banner, .route-next, .chk, .gen, .demo, .walk-ctl, .listen, .quiz-score, .q-verdict, .sr-only, .term-tip, .complete-row, .st-count, .st-controls, .notes-box, .katex-mathml, .hl-pop, .hl-bar, button, input, textarea, select, script, style, .wk-count";
  var COLORS = [["yellow", "Yellow"], ["green", "Green"], ["pink", "Pink"]];
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { return {}; } }
  function save(d) { try { localStorage.setItem(KEY, JSON.stringify(d)); return true; } catch (e) { return false; } }
  function page() { return location.pathname.split("/").pop() || "index.html"; }
  function esc(s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
  window.MLA_NOTES = { load: load };

  // ---- text model: the visible text of the article as one string, with a map back to text nodes
  function textMap(root) {
    var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, { acceptNode: function (n) { return n.parentElement && n.parentElement.closest(SKIP) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT; } });
    var nodes = [], full = "", n;
    while ((n = w.nextNode())) { nodes.push({ node: n, start: full.length, end: full.length + n.data.length }); full += n.data; }
    return { nodes: nodes, full: full };
  }
  function pointToIndex(M, container, offset) {
    var r = document.createRange(); r.setStart(container, offset); r.collapse(true);
    for (var k = 0; k < M.nodes.length; k++) {
      var x = M.nodes[k];
      if (x.node === container) return x.start + offset;
      if (r.comparePoint(x.node, x.node.data.length) <= 0) continue;   // this text node ends before the boundary
      return x.start;
    }
    return M.full.length;
  }
  function wrap(root, s, e, h) {
    var M = textMap(root), first = null;
    M.nodes.filter(function (x) { return x.end > s && x.start < e; }).forEach(function (x) {
      var node = x.node, a = Math.max(0, s - x.start), b = Math.min(node.data.length, e - x.start);
      if (b <= a || !node.data.slice(a, b).trim()) return;
      if (b < node.data.length) node.splitText(b);
      var mid = a > 0 ? node.splitText(a) : node;
      var m = document.createElement("mark"); m.className = "hl hl-" + h.color + (h.note ? " has-note" : ""); m.setAttribute("data-hl", h.id);
      m.tabIndex = 0; m.setAttribute("role", "button"); m.setAttribute("aria-label", "Highlighted text" + (h.note ? " with a note" : "") + ". Press Enter to edit.");
      mid.parentNode.insertBefore(m, mid); m.appendChild(mid);
      if (!first) first = m;
    });
    return first;
  }
  function locate(M, h) {   // find the stored quote again, using the text around it to choose between repeats
    var best = -1, bestScore = -1, i = M.full.indexOf(h.exact);
    while (i !== -1) {
      var sc = 0, pre = M.full.slice(Math.max(0, i - h.prefix.length), i), suf = M.full.slice(i + h.exact.length, i + h.exact.length + h.suffix.length);
      for (var k = 1; k <= Math.min(pre.length, h.prefix.length) && pre[pre.length - k] === h.prefix[h.prefix.length - k]; k++) sc++;
      for (k = 0; k < Math.min(suf.length, h.suffix.length) && suf[k] === h.suffix[k]; k++) sc++;
      sc -= Math.abs(i - h.start) / 1e6;
      if (sc > bestScore) { bestScore = sc; best = i; }
      i = M.full.indexOf(h.exact, i + 1);
    }
    return best;
  }
  function unwrap(id) {
    document.querySelectorAll('mark.hl[data-hl="' + id + '"]').forEach(function (m) { var p = m.parentNode; while (m.firstChild) p.insertBefore(m.firstChild, m); p.removeChild(m); p.normalize(); });
  }

  document.addEventListener("DOMContentLoaded", function () {
    // ---------------- My notes page ----------------
    var NP = document.getElementById("notes-app");
    if (NP) { renderNotesPage(NP); return; }

    var root = document.querySelector("article.prose"); if (!root) return;
    var P = page(), title = (document.querySelector(".module-hero h1") || document.querySelector("h1") || {}).textContent || P;
    function rec() { var d = load(); d[P] = d[P] || { title: title, hl: [], note: "" }; d[P].title = title; return d; }

    setTimeout(function () {   // after maths and terms have been rendered
      var d = load(), lost = 0;
      ((d[P] && d[P].hl) || []).forEach(function (h) { var M = textMap(root), i = locate(M, h); if (i === -1) { lost++; return; } wrap(root, i, i + h.exact.length, h); });
      if (lost) { var warn = document.createElement("p"); warn.className = "hl-lost"; warn.textContent = lost + " of your highlights on this page couldn't be placed (the text has changed). They're still listed on the My notes page."; root.insertBefore(warn, root.firstChild); }
      var m = /#hl=([\w-]+)/.exec(location.hash);
      if (m) { var t = document.querySelector('mark.hl[data-hl="' + m[1] + '"]'); if (t) { t.scrollIntoView({ block: "center" }); t.classList.add("hl-flash"); setTimeout(function () { t.classList.remove("hl-flash"); }, 2500); } }
    }, 500);

    // ---------------- selection toolbar ----------------
    var bar = document.createElement("div"); bar.className = "hl-bar"; bar.hidden = true; bar.setAttribute("role", "toolbar"); bar.setAttribute("aria-label", "Highlight the selected text");
    bar.innerHTML = COLORS.map(function (c) { return '<button type="button" class="hl-sw hl-' + c[0] + '" data-color="' + c[0] + '" aria-label="Highlight ' + c[1].toLowerCase() + '"></button>'; }).join("") + '<button type="button" class="hl-addnote" data-color="yellow" data-note="1">✎ Add note</button>';
    document.body.appendChild(bar);
    var pending = null;
    function selInfo() {
      var sel = window.getSelection(); if (!sel || sel.rangeCount === 0 || sel.isCollapsed) return null;
      var r = sel.getRangeAt(0); if (!root.contains(r.commonAncestorContainer)) return null;
      var anc = r.commonAncestorContainer.nodeType === 1 ? r.commonAncestorContainer : r.commonAncestorContainer.parentElement;
      if (anc.closest(SKIP) || anc.closest("mark.hl")) return null;
      var M = textMap(root), s = pointToIndex(M, r.startContainer, r.startOffset), e = pointToIndex(M, r.endContainer, r.endOffset);
      var text = M.full.slice(s, e); var lead = text.length - text.replace(/^\s+/, "").length, trail = text.length - text.replace(/\s+$/, "").length;
      s += lead; e -= trail; if (e - s < 2 || e - s > 3000) return null;
      return { s: s, e: e, rect: r.getBoundingClientRect(), M: M };
    }
    function showBar() {
      var info = selInfo(); if (!info) { bar.hidden = true; pending = null; return; }
      pending = info; bar.hidden = false;
      var top = info.rect.top + window.scrollY - bar.offsetHeight - 10, left = info.rect.left + window.scrollX + info.rect.width / 2 - bar.offsetWidth / 2;
      if (info.rect.top < 70) top = info.rect.bottom + window.scrollY + 10;
      bar.style.top = Math.max(window.scrollY + 4, top) + "px"; bar.style.left = Math.max(8, Math.min(left, document.documentElement.clientWidth - bar.offsetWidth - 8)) + "px";
    }
    document.addEventListener("mouseup", function (ev) { if (bar.contains(ev.target)) return; setTimeout(showBar, 10); });
    document.addEventListener("keyup", function (ev) { if (ev.shiftKey || ev.key === "Shift") setTimeout(showBar, 10); if (ev.key === "Escape") { bar.hidden = true; closePop(); } });
    document.addEventListener("selectionchange", function () { if (!bar.hidden && !selInfo()) setTimeout(function () { if (!selInfo() && !bar.contains(document.activeElement)) bar.hidden = true; }, 150); });
    document.addEventListener("touchend", function () { setTimeout(showBar, 350); });
    bar.addEventListener("mousedown", function (ev) { ev.preventDefault(); });   // keep the selection
    bar.addEventListener("click", function (ev) {
      var b = ev.target.closest("button"); if (!b || !pending) return;
      var M = pending.M, s = pending.s, e2 = pending.e;
      var h = { id: "h" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6), exact: M.full.slice(s, e2), prefix: M.full.slice(Math.max(0, s - 40), s), suffix: M.full.slice(e2, e2 + 40), start: s, color: b.getAttribute("data-color"), note: "", t: Date.now() };
      var d = rec(); d[P].hl.push(h);
      if (!save(d)) { window.alert("Couldn't save: this browser's storage is full or turned off."); return; }
      window.getSelection().removeAllRanges(); bar.hidden = true; pending = null;
      var m = wrap(root, s, e2, h);
      if (b.hasAttribute("data-note") && m) openPop(m);
    });

    // ---------------- highlight popover: note, colour, remove ----------------
    var pop = document.createElement("div"); pop.className = "hl-pop"; pop.hidden = true; pop.setAttribute("role", "dialog"); pop.setAttribute("aria-label", "Highlight note");
    document.body.appendChild(pop);
    var current = null;
    function closePop() { if (!pop.hidden) { pop.hidden = true; if (current) { var m = document.querySelector('mark.hl[data-hl="' + current + '"]'); current = null; if (m) m.focus(); } } }
    function openPop(m) {
      var id = m.getAttribute("data-hl"), d = rec(), h = d[P].hl.filter(function (x) { return x.id === id; })[0]; if (!h) return;
      current = id;
      pop.innerHTML = '<label class="hl-pop-l" for="hl-note">Your note</label><textarea id="hl-note" rows="3" placeholder="Why does this matter? What would you ask?">' + esc(h.note || "") + '</textarea>' +
        '<div class="hl-pop-row">' + COLORS.map(function (c) { return '<button type="button" class="hl-sw hl-' + c[0] + (h.color === c[0] ? ' on' : '') + '" data-color="' + c[0] + '" aria-label="' + c[1] + '" aria-pressed="' + (h.color === c[0]) + '"></button>'; }).join("") +
        '<button type="button" class="hl-del">Remove</button><button type="button" class="hl-done">Done</button></div>';
      var r = m.getBoundingClientRect(); pop.hidden = false;
      pop.style.top = (r.bottom + window.scrollY + 8) + "px"; pop.style.left = Math.max(8, Math.min(r.left + window.scrollX, document.documentElement.clientWidth - pop.offsetWidth - 8)) + "px";
      var ta = pop.querySelector("textarea"); ta.focus();
      ta.addEventListener("input", function () { var d2 = rec(); d2[P].hl.forEach(function (x) { if (x.id === id) x.note = ta.value; }); save(d2);
        document.querySelectorAll('mark.hl[data-hl="' + id + '"]').forEach(function (mm) { mm.classList.toggle("has-note", !!ta.value.trim()); }); });
    }
    pop.addEventListener("click", function (ev) {
      var b = ev.target.closest("button"); if (!b || !current) return; var id = current, d = rec();
      if (b.classList.contains("hl-done")) { closePop(); return; }
      if (b.classList.contains("hl-del")) { d[P].hl = d[P].hl.filter(function (x) { return x.id !== id; }); save(d); unwrap(id); current = null; pop.hidden = true; return; }
      var c = b.getAttribute("data-color"); if (!c) return;
      d[P].hl.forEach(function (x) { if (x.id === id) x.color = c; }); save(d);
      document.querySelectorAll('mark.hl[data-hl="' + id + '"]').forEach(function (mm) { COLORS.forEach(function (cc) { mm.classList.remove("hl-" + cc[0]); }); mm.classList.add("hl-" + c); });
      pop.querySelectorAll(".hl-sw").forEach(function (s) { s.classList.toggle("on", s === b); s.setAttribute("aria-pressed", s === b ? "true" : "false"); });
    });
    root.addEventListener("click", function (ev) { var m = ev.target.closest("mark.hl"); if (m && window.getSelection().isCollapsed) openPop(m); });
    root.addEventListener("keydown", function (ev) { var m = ev.target.closest && ev.target.closest("mark.hl"); if (m && (ev.key === "Enter" || ev.key === " ")) { ev.preventDefault(); openPop(m); } });
    document.addEventListener("mousedown", function (ev) { if (!pop.hidden && !pop.contains(ev.target) && !ev.target.closest("mark.hl")) closePop(); });
    pop.addEventListener("keydown", function (ev) { if (ev.key === "Escape") closePop(); });

    // ---------------- free-form notes for the whole lesson ----------------
    var anchor = root.querySelector(".complete-row");
    if (anchor) {
      var box = document.createElement("section"); box.className = "notes-box";
      box.innerHTML = '<h2 class="notes-title">My notes for this lesson</h2><p class="notes-help">Anything you want to remember. Select text anywhere above to highlight it. Saved in this browser; see all your notes on <a href="notes.html">My notes</a>.</p>' +
        '<textarea rows="5" aria-label="My notes for this lesson" placeholder="Write your own summary, questions, or links…"></textarea><p class="notes-status" aria-live="polite"></p>';
      root.insertBefore(box, anchor);
      var ta = box.querySelector("textarea"), stat = box.querySelector(".notes-status"), tm = null;
      ta.value = (load()[P] || {}).note || "";
      ta.addEventListener("input", function () { clearTimeout(tm); tm = setTimeout(function () { var d = rec(); d[P].note = ta.value; stat.textContent = save(d) ? "Saved" : "Couldn't save (browser storage unavailable)"; }, 400); });
    }
  });

  // ---------------- My notes page ----------------
  function renderNotesPage(NP) {
    var d = load(), pages = Object.keys(d).filter(function (k) { return (d[k].hl && d[k].hl.length) || (d[k].note && d[k].note.trim()); }).sort();
    if (!pages.length) { NP.innerHTML = '<p class="rv-empty">No notes or highlights yet. Open any lesson, select some text and choose a colour — or write in the "My notes for this lesson" box near the end.</p>'; return; }
    var nh = 0; pages.forEach(function (k) { nh += (d[k].hl || []).length; });
    var h = '<p class="notes-sum">' + nh + ' highlight' + (nh === 1 ? '' : 's') + ' across ' + pages.length + ' page' + (pages.length === 1 ? '' : 's') + '.</p><p class="pg-actions"><button type="button" class="btn notes-md">⬇ Download as Markdown</button><button type="button" class="btn notes-clear">Delete all notes</button></p>';
    pages.forEach(function (k) {
      var r = d[k];
      h += '<section class="notes-page"><h2><a href="' + k + '">' + esc(r.title || k) + '</a></h2>' + (r.note && r.note.trim() ? '<div class="notes-free">' + esc(r.note).replace(/\n/g, "<br>") + '</div>' : '');
      h += '<ul class="notes-list">' + (r.hl || []).slice().sort(function (a, b) { return a.start - b.start; }).map(function (x) {
        return '<li class="hlq-' + x.color + '"><blockquote><a href="' + k + '#hl=' + x.id + '">' + esc(x.exact.length > 400 ? x.exact.slice(0, 400) + "…" : x.exact) + '</a></blockquote>' + (x.note ? '<p>' + esc(x.note).replace(/\n/g, "<br>") + '</p>' : '') + '</li>'; }).join("") + '</ul></section>';
    });
    NP.innerHTML = h;
    NP.querySelector(".notes-md").addEventListener("click", function () {
      var md = "# My ML Academy notes\n\n";
      pages.forEach(function (k) { var r = d[k]; md += "## " + (r.title || k) + "\n\n"; if (r.note && r.note.trim()) md += r.note.trim() + "\n\n";
        (r.hl || []).slice().sort(function (a, b) { return a.start - b.start; }).forEach(function (x) { md += "> " + x.exact.replace(/\s+/g, " ") + "\n\n" + (x.note ? x.note.trim() + "\n\n" : ""); }); });
      var u = URL.createObjectURL(new Blob([md], { type: "text/markdown" })), a = document.createElement("a"); a.href = u; a.download = "ml-academy-notes.md"; document.body.appendChild(a); a.click();
      setTimeout(function () { URL.revokeObjectURL(u); a.remove(); }, 1000);
    });
    NP.querySelector(".notes-clear").addEventListener("click", function () { if (window.confirm("Delete all highlights and notes saved in this browser?")) { save({}); renderNotesPage(NP); } });
  }
})();
