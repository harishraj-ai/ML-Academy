/* ML Academy — "Listen to this lesson": reads the lesson aloud with the browser's built-in text-to-speech (works offline). */
(function () {
  "use strict";
  var synth = window.speechSynthesis;
  function texOf(k) {   // spoken form of a KaTeX formula, from its TeX source
    var a = k.querySelector("annotation"); if (!a) return k.textContent;
    var t = a.textContent;
    var W = { sigma: "sigma", mu: "mu", lambda: "lambda", theta: "theta", eta: "eta", alpha: "alpha", beta: "beta", gamma: "gamma", delta: "delta", varepsilon: "epsilon", epsilon: "epsilon",
      sum: "the sum of", prod: "the product of", partial: "partial", nabla: "nabla", sqrt: "square root of", cdot: "times", times: "times", approx: "approximately", ne: "not equal to",
      le: "less than or equal to", ge: "greater than or equal to", leq: "less than or equal to", geq: "greater than or equal to", to: "to", infty: "infinity", ln: "log", log: "log", exp: "exp", Rightarrow: "so", mid: "given", pm: "plus or minus", hat: "", bar: "", mathbf: "", boldsymbol: "", text: "", mathrm: "", operatorname: "", frac: "" };
    t = t.replace(/\\frac\{([^{}]*)\}\{([^{}]*)\}/g, " $1 over $2 ").replace(/\^2(?![0-9])/g, " squared ").replace(/\^\{?T\}?/g, " transpose ").replace(/\^\{([^{}]*)\}/g, " to the power $1 ").replace(/\^(\w)/g, " to the power $1 ")
         .replace(/_\{([^{}]*)\}/g, " $1 ").replace(/_(\w)/g, " $1 ")
         .replace(/\\([a-zA-Z]+)/g, function (m, w) { return W.hasOwnProperty(w) ? " " + W[w] + " " : " " + w + " "; })
         .replace(/[{}\\]/g, " ").replace(/=/g, " equals ").replace(/\+/g, " plus ").replace(/(\s)-(\s)/g, " minus ").replace(/\|/g, " ").replace(/\s+/g, " ");
    return t.trim();
  }
  function spoken(el) {
    var c = el.cloneNode(true);
    c.querySelectorAll(".katex").forEach(function (k, i) { var orig = el.querySelectorAll(".katex")[i]; k.replaceWith(document.createTextNode(" " + texOf(orig) + " ")); });
    c.querySelectorAll(".sr-only, .term-tip, button, .chk, .q-verdict, .listen-here").forEach(function (x) { x.remove(); });
    return c.textContent.replace(/\s+/g, " ").trim();
  }
  function chunks(text) {     // Chrome stops long utterances, so speak sentence-sized pieces
    var out = [], parts = text.match(/[^.!?]+[.!?]+["')\]]*\s*|[^.!?]+$/g) || [text], cur = "";
    parts.forEach(function (p) { if ((cur + p).length > 220 && cur) { out.push(cur); cur = p; } else cur += p; });
    if (cur.trim()) out.push(cur);
    return out;
  }
  function visible(el) { return !!(el.offsetParent || el.getClientRects().length); }
  function collect() {
    var prose = document.querySelector("article.prose"); if (!prose) return [];
    var items = [], h1 = document.querySelector(".module-hero h1"), lead = document.querySelector(".module-hero h1 + p");
    if (h1) items.push({ el: h1, text: "Lesson. " + h1.textContent + "." + (lead ? " " + lead.textContent : "") });
    prose.querySelectorAll("h2, h3, p, li, figcaption, .box-title, .walk-cap.on, .st-why").forEach(function (el) {
      if (el.closest(".decode-hint, .walk-ctl, .demo, pre, .quiz, .exercises, .gen, .sources, .pager, .complete-row, .toc, .run-out-label, .decode-legend, table, .listen")) return;
      if (el.tagName === "LI" && el.querySelector("p")) return;            // its paragraphs are read on their own
      if (!visible(el)) return;
      var t = spoken(el); if (!t) return;
      if (/^H[23]$/.test(el.tagName)) t = t.replace(/^\d+\.\s*/, "") + ".";
      if (el.tagName === "FIGCAPTION") t = "Figure: " + t;
      items.push({ el: el, text: t });
    });
    return items;
  }

  document.addEventListener("DOMContentLoaded", function () {
    var box = document.querySelector(".listen"); if (!box) return;
    if (!synth || typeof SpeechSynthesisUtterance === "undefined") {
      box.innerHTML = '<span class="listen-na">Listening isn\'t available in this browser. Try Chrome, Edge or Safari.</span>'; return;
    }
    box.innerHTML =
      '<div class="listen-row">' +
        '<button type="button" class="listen-play" aria-label="Listen to this lesson">▶ Listen to this lesson</button>' +
        '<span class="listen-nav" hidden>' +
          '<button type="button" data-go="sec-1" aria-label="Previous section" title="Previous section ({)">⏮</button>' +
          '<button type="button" data-go="par-1" aria-label="Previous paragraph" title="Previous paragraph ([)">◀</button>' +
          '<button type="button" data-go="par+1" aria-label="Next paragraph" title="Next paragraph (])">▶</button>' +
          '<button type="button" data-go="sec+1" aria-label="Next section" title="Next section (})">⏭</button>' +
        '</span>' +
        '<button type="button" class="listen-stop" aria-label="Stop reading" hidden>■ Stop</button>' +
        '<label class="listen-from">Start from <select aria-label="Start reading from section"></select></label>' +
      '</div>' +
      '<div class="listen-row listen-prog" hidden><input type="range" min="0" max="0" value="0" step="1" aria-label="Reading position"><span class="listen-pos" aria-live="polite"></span></div>' +
      '<div class="listen-row listen-opts">' +
        '<label class="listen-rate">Speed <select aria-label="Reading speed"><option value="0.8">0.8×</option><option value="1" selected>1×</option><option value="1.2">1.2×</option><option value="1.5">1.5×</option><option value="1.8">1.8×</option></select></label>' +
        '<label class="listen-voice">Voice <select aria-label="Voice"></select></label>' +
        '<span class="listen-keys">Keys while listening: [ ] paragraph · { } section</span>' +
      '</div>';
    var play = box.querySelector(".listen-play"), stopB = box.querySelector(".listen-stop"), rateSel = box.querySelector(".listen-rate select"),
        voiceSel = box.querySelector(".listen-voice select"), pos = box.querySelector(".listen-pos"), fromSel = box.querySelector(".listen-from select"),
        nav = box.querySelector(".listen-nav"), prog = box.querySelector(".listen-prog"), range = prog.querySelector("input");
    var items = [], i = 0, parts = [], j = 0, state = "idle", voices = [], gen = 0;
    var saved = {}; try { saved = JSON.parse(localStorage.getItem("mla-listen") || "{}"); } catch (e) { /* ignore */ }
    if (saved.rate) rateSel.value = saved.rate;
    function store() { try { localStorage.setItem("mla-listen", JSON.stringify({ rate: rateSel.value, voiceName: saved.voiceName || "" })); } catch (e) { /* ignore */ } }
    function loadVoices() {
      voices = synth.getVoices().filter(function (v) { return /^en/i.test(v.lang); });
      if (!voices.length) voices = synth.getVoices();
      voiceSel.innerHTML = '<option value="">Default</option>' + voices.map(function (v, k) { return '<option value="' + k + '"' + (saved.voiceName === v.name ? " selected" : "") + ">" + v.name + " (" + v.lang + ")</option>"; }).join("");
      box.querySelector(".listen-voice").hidden = voices.length < 2;
    }
    loadVoices(); if ("onvoiceschanged" in synth) synth.onvoiceschanged = loadVoices;
    // sections = indexes of the h2 items (plus the title)
    function sections(list) { var out = []; list.forEach(function (it, k) { if (k === 0 || it.el.tagName === "H2") out.push({ k: k, name: k === 0 ? "Beginning" : it.text.replace(/\.$/, "") }); }); return out; }
    function secOf(k, secs) { var s = 0; secs.forEach(function (x, n) { if (x.k <= k) s = n; }); return s; }
    function fillFrom() {
      var secs = sections(collect());
      fromSel.innerHTML = secs.map(function (x, n) { return '<option value="' + x.k + '">' + (n ? n + ". " : "") + x.name.replace(/</g, "&lt;") + "</option>"; }).join("");
    }
    fillFrom();
    function mark(el) {
      document.querySelectorAll(".tts-on").forEach(function (x) { x.classList.remove("tts-on"); });
      if (el) { el.classList.add("tts-on"); var r = el.getBoundingClientRect(); if (r.top < 80 || r.bottom > window.innerHeight - 140) el.scrollIntoView({ block: "center", behavior: document.documentElement.classList.contains("rm") ? "auto" : "smooth" }); }
    }
    function showPos() {
      var secs = sections(items), s = secOf(i, secs);
      range.max = Math.max(0, items.length - 1); range.value = i;
      pos.textContent = "Part " + (i + 1) + " of " + items.length + (secs[s] ? " · " + secs[s].name : "");
      for (var n = 0; n < fromSel.options.length; n++) if (+fromSel.options[n].value <= i) fromSel.selectedIndex = n;
    }
    var pending = false;
    function speakNext() {
      if (state === "paused") { pending = true; return; }   // a sentence ended just as we paused: continue on resume
      if (state !== "playing") return;
      if (j >= parts.length) { i++; j = 0; if (i >= items.length) { finish(); return; } parts = chunks(items[i].text); mark(items[i].el); }
      showPos();
      var u = new SpeechSynthesisUtterance(parts[j]), my = gen;
      u.rate = +rateSel.value; u.lang = "en";
      if (voiceSel.value !== "" && voices[+voiceSel.value]) u.voice = voices[+voiceSel.value];
      u.onend = function () { if (my !== gen) return; j++; speakNext(); };
      u.onerror = function (e) { if (my !== gen || e.error === "interrupted" || e.error === "canceled") return; j++; speakNext(); };
      synth.speak(u);
    }
    function startFrom(k) {
      gen++; pending = false; synth.cancel(); items = collect(); if (!items.length) return;
      i = Math.max(0, Math.min(k, items.length - 1)); j = 0; parts = chunks(items[i].text); mark(items[i].el);
      state = "playing"; paint(); showPos(); speakNext();
    }
    function jump(how) {
      if (state === "idle") return;
      var secs = sections(items), s = secOf(i, secs), k = i;
      if (how === "par-1") k = i - 1; else if (how === "par+1") k = i + 1;
      else if (how === "sec+1") k = secs[s + 1] ? secs[s + 1].k : items.length - 1;
      else if (how === "sec-1") k = (i - secs[s].k > 1 || s === 0) ? secs[s].k : secs[s - 1].k;   // like a music player: first back to the start of this section
      startFrom(k);
    }
    function finish() { state = "idle"; gen++; synth.cancel(); mark(null); pos.textContent = "Finished."; paint(); }
    function paint() {
      play.textContent = state === "playing" ? "❚❚ Pause" : state === "paused" ? "▶ Resume" : "▶ Listen to this lesson";
      play.setAttribute("aria-label", state === "playing" ? "Pause reading" : state === "paused" ? "Resume reading" : "Listen to this lesson");
      stopB.hidden = nav.hidden = prog.hidden = state === "idle"; box.classList.toggle("on", state !== "idle");
      document.body.classList.toggle("listening", state !== "idle");
    }
    play.addEventListener("click", function () {
      if (state === "idle") {   // start at the first paragraph on screen
        var all = collect(), k = 0; for (var n = 0; n < all.length; n++) { if (all[n].el.getBoundingClientRect().bottom > 90) { k = n; break; } }
        startFrom(k);
      } else if (state === "playing") { state = "paused"; synth.pause(); paint(); }
      else { state = "playing"; synth.resume(); paint(); if (pending) { pending = false; speakNext(); } }
    });
    stopB.addEventListener("click", finish);
    nav.addEventListener("click", function (e) { var b = e.target.closest("button[data-go]"); if (b) jump(b.getAttribute("data-go")); });
    fromSel.addEventListener("change", function () { startFrom(+fromSel.value); });
    range.addEventListener("input", function () { var k = +range.value; pos.textContent = "Jump to part " + (k + 1) + " of " + items.length; });
    range.addEventListener("change", function () { startFrom(+range.value); });
    rateSel.addEventListener("change", function () { store(); if (state === "playing") startFrom(i); });
    voiceSel.addEventListener("change", function () { saved.voiceName = voiceSel.value !== "" && voices[+voiceSel.value] ? voices[+voiceSel.value].name : ""; store(); if (state === "playing") startFrom(i); });
    // "Listen from here" buttons on every section heading
    var prose = document.querySelector("article.prose");
    prose.querySelectorAll("h2[id]").forEach(function (h) {
      if (h.closest(".quiz, .exercises")) return;
      var b = document.createElement("button"); b.type = "button"; b.className = "listen-here"; b.textContent = "▶";
      b.setAttribute("aria-label", "Listen from here: " + h.textContent.replace(/^\d+\.\s*/, "")); b.title = "Listen from here";
      b.addEventListener("click", function (ev) { ev.preventDefault(); var all = collect(); for (var n = 0; n < all.length; n++) if (all[n].el === h) { startFrom(n); return; } });
      h.appendChild(b);
    });
    // double-click any paragraph while listening to jump there
    prose.addEventListener("dblclick", function (e) {
      if (state === "idle") return; var t = e.target.closest("p, li, h2, h3"); if (!t) return;
      var all = collect(); for (var n = 0; n < all.length; n++) if (all[n].el === t) { startFrom(n); return; }
    });
    document.addEventListener("keydown", function (e) {
      if (state === "idle" || e.ctrlKey || e.metaKey || e.altKey) return;
      if (/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName) || e.target.isContentEditable) return;
      var m = { "[": "par-1", "]": "par+1", "{": "sec-1", "}": "sec+1" }[e.key]; if (!m) return;
      e.preventDefault(); jump(m);
    });
    window.addEventListener("beforeunload", function () { synth.cancel(); });
    window.MLA_LISTEN = { collect: collect, chunks: chunks, texOf: texOf, jump: jump, startFrom: startFrom, state: function () { return { state: state, i: i, n: items.length }; } };
  });
})();
