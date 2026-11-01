/* Hidden interview questions: filters and "I know this" progress (stored per browser). */
(function () {
  "use strict";
  var KEY = "mla-iq", known = {};
  try { known = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { known = {}; }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(known)); } catch (e) {} }
  var part = document.getElementById("iq-part"), lvl = document.getElementById("iq-lvl"), hide = document.getElementById("iq-hide"), count = document.querySelector(".iq-count");
  var cards = [].slice.call(document.querySelectorAll(".iq"));
  cards.forEach(function (c) {
    var cb = c.querySelector("input[data-q]"); cb.checked = !!known[cb.getAttribute("data-q")]; c.classList.toggle("is-known", cb.checked);
    cb.addEventListener("change", function () { var id = cb.getAttribute("data-q"); if (cb.checked) known[id] = 1; else delete known[id]; save(); c.classList.toggle("is-known", cb.checked); apply(); });
  });
  function apply() {
    var shown = 0, k = 0;
    document.querySelectorAll(".iq-sec").forEach(function (sec) {
      var okPart = !part.value || sec.getAttribute("data-part") === part.value, any = false;
      sec.querySelectorAll(".iq").forEach(function (c) {
        var isK = c.classList.contains("is-known"), ok = okPart && (!lvl.value || c.getAttribute("data-lvl") === lvl.value) && !(hide.checked && isK);
        c.style.display = ok ? "" : "none"; if (ok) { shown++; any = true; }
      });
      sec.style.display = any ? "" : "none";
    });
    cards.forEach(function (c) { if (c.classList.contains("is-known")) k++; });
    count.textContent = shown + " shown · you know " + k + " of " + cards.length;
  }
  [part, lvl, hide].forEach(function (el) { el.addEventListener("change", apply); });
  // open the targeted question when arriving from search or a lesson
  function openHash() { var h = location.hash.slice(1); if (!h) return; var el = document.getElementById(h); if (el && el.classList.contains("iq")) { part.value = ""; lvl.value = ""; hide.checked = false; apply(); var d = el.querySelector("details"); if (d) d.open = false; el.classList.add("iq-target"); } }
  window.addEventListener("hashchange", openHash);
  apply(); openHash();
})();
