/* ML Academy — hover / tap definitions for glossary terms inside lesson text */
(function () {
  "use strict";
  var tip = null, current = null;
  function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
  function makeTip() {
    tip = document.createElement("div"); tip.className = "term-tip"; tip.setAttribute("role", "tooltip"); tip.hidden = true;
    document.body.appendChild(tip);
    tip.addEventListener("mouseenter", function () { clearTimeout(tip._t); });
    tip.addEventListener("mouseleave", hideSoon);
  }
  function show(el) {
    if (!tip) makeTip();
    clearTimeout(tip._t); if (current !== el) tip._shownAt = Date.now(); current = el;
    var e = el._entry, here = location.pathname.split("/").pop(), target = e.l.split("#")[0];
    tip.innerHTML = "<div class='tt-term'>" + e.t + "</div><div class='tt-def'>" + e.d + "</div>" +
      (target === here ? "<div class='tt-link'>Explained in this lesson</div>" : "<a class='tt-link' href='" + e.l + "'>Explained in Lesson " + e.n + " →</a>");
    tip.hidden = false; if (!tip._shownAt) tip._shownAt = Date.now();
    var r = el.getBoundingClientRect(), tw = Math.min(320, window.innerWidth - 24);
    tip.style.width = tw + "px";
    var left = Math.max(12, Math.min(window.innerWidth - tw - 12, r.left + r.width / 2 - tw / 2));
    var top = r.bottom + 8 + window.scrollY;
    if (r.bottom + tip.offsetHeight + 16 > window.innerHeight) top = r.top + window.scrollY - tip.offsetHeight - 8;
    tip.style.left = left + window.scrollX + "px"; tip.style.top = top + "px";
  }
  function hideSoon() { if (tip) tip._t = setTimeout(function () { tip.hidden = true; current = null; }, 180); }
  document.addEventListener("DOMContentLoaded", function () {
    var root = document.querySelector("article.prose"); var idx = window.MLA_INDEX || [];
    if (!root || !idx.length) return;
    var map = {}, alts = [];
    idx.forEach(function (e) { if (e.k === "term" && e.a) e.a.forEach(function (a) { map[a.toLowerCase()] = e; alts.push(a); }); });
    alts.sort(function (a, b) { return b.length - a.length; });
    var re = new RegExp("(?<![\\w-])(" + alts.map(esc).join("|") + ")(?:e?s)?(?![\\w-])", "i");
    var used = {};
    var SKIP = /^(CODE|PRE|A|BUTTON|H1|H2|H3|H4|SCRIPT|STYLE|SUMMARY|FIGCAPTION|SVG|TEXT|KBD|MARK)$/;
    function skip(node) {
      for (var p = node.parentNode; p && p !== root; p = p.parentNode) {
        if (SKIP.test(p.nodeName.toUpperCase()) || (p.classList && (p.classList.contains("katex") || p.classList.contains("demo") || p.classList.contains("q") || p.classList.contains("term") || p.classList.contains("context-box") || p.classList.contains("fig") || p.classList.contains("decode") || p.classList.contains("stepper")))) return true;
      }
      return false;
    }
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null), nodes = [], n;
    while ((n = walker.nextNode())) if (n.nodeValue.trim().length > 2 && !skip(n)) nodes.push(n);
    nodes.forEach(function (node) {
      var text = node.nodeValue, m, guard = 0;
      while ((m = re.exec(text)) && guard++ < 20) {
        var entry = map[m[1].toLowerCase()];
        if (!entry || used[entry.t]) {
          // look for a later, unused match in the rest of this text node
          var rest = text.slice(m.index + m[0].length), off = m.index + m[0].length, found = null, mm;
          var re2 = new RegExp(re.source, "gi");
          while ((mm = re2.exec(rest))) { var en = map[mm[1].toLowerCase()]; if (en && !used[en.t]) { found = mm; break; } }
          if (!found) break;
          m = { index: off + found.index, 0: found[0], 1: found[1] }; entry = map[found[1].toLowerCase()];
        }
        used[entry.t] = 1;
        var before = text.slice(0, m.index), word = m[0], after = text.slice(m.index + word.length);
        var span = document.createElement("span"); span.className = "term"; span.tabIndex = 0; span.textContent = word; span._entry = entry;
        span.setAttribute("aria-label", word + ": " + entry.d);
        var parent = node.parentNode;
        parent.insertBefore(document.createTextNode(before), node);
        parent.insertBefore(span, node);
        node.nodeValue = after; text = after;
      }
    });
    root.addEventListener("mouseover", function (e) { var t = e.target.closest && e.target.closest(".term"); if (t) show(t); });
    root.addEventListener("mouseout", function (e) { var t = e.target.closest && e.target.closest(".term"); if (t) hideSoon(); });
    root.addEventListener("focusin", function (e) { if (e.target.classList && e.target.classList.contains("term")) show(e.target); });
    root.addEventListener("focusout", function (e) { if (e.target.classList && e.target.classList.contains("term")) hideSoon(); });
    root.addEventListener("click", function (e) { var t = e.target.closest && e.target.closest(".term"); if (t) { e.preventDefault(); if (current === t && tip && !tip.hidden && Date.now() - (tip._shownAt || 0) > 500) { tip.hidden = true; current = null; } else show(t); } });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && tip) tip.hidden = true; });
    document.addEventListener("click", function (e) { if (tip && !tip.hidden && !(e.target.closest && (e.target.closest(".term") || e.target.closest(".term-tip")))) { tip.hidden = true; current = null; } });
    window.addEventListener("scroll", function () { if (tip && !tip.hidden && current) show(current); }, { passive: true });
  });
})();
