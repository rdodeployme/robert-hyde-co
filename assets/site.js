/* Robert Hyde & Co. — site behaviour. No dependencies. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Where form submissions go. Leave empty for prototype mode (nothing is sent).
     Set to a form endpoint (e.g. a Google Apps Script web app) to go live. */
  var CONFIG = { endpoint: "" };

  function store(key, val) {
    try {
      if (val === undefined) return JSON.parse(localStorage.getItem(key) || "null");
      if (val === null) localStorage.removeItem(key); else localStorage.setItem(key, JSON.stringify(val));
    } catch (e) { return null; }
  }

  /* ---------- mobile nav ---------- */
  var btn = $(".menu-btn"), nav = $("#site-nav");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.textContent = open ? "Close" : "Menu";
    });
    nav.addEventListener("focusout", function (e) {
      if (nav.classList.contains("open") && !nav.contains(e.relatedTarget) && e.relatedTarget !== btn && e.relatedTarget) {
        nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); btn.textContent = "Menu";
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); btn.textContent = "Menu"; btn.focus(); }
    });
  }

  /* ---------- time machine ---------- */
  var tm = $("[data-tm]");
  if (tm) {
    var tabs = $$(".rail [role=tab]", tm);
    var stops = $$(".stop", tm);
    var dial = $(".tm-dial .token", tm);
    var yearEl = $(".tm-year", tm);
    var prev = $("[data-tm-prev]", tm), next = $("[data-tm-next]", tm);
    var idx = 0;
    var show = function (i, focus, fromHash) {
      idx = Math.max(0, Math.min(tabs.length - 1, i));
      tabs.forEach(function (t, k) {
        var on = k === idx;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        stops[k].hidden = !on;
      });
      var label = tabs[idx].getAttribute("data-year");
      if (yearEl) yearEl.textContent = label;
      if (dial) dial.style.transform = "rotate(" + (-idx * 47) + "deg)";
      if (prev) prev.disabled = idx === 0;
      if (next) { next.disabled = idx === tabs.length - 1; }
      if (document.activeElement === next && next && next.disabled && prev) prev.focus();
      if (document.activeElement === prev && prev && prev.disabled && next) next.focus();
      if (focus) tabs[idx].focus();
      if (!fromHash && history.replaceState) history.replaceState(null, "", "#" + tabs[idx].getAttribute("data-slug"));
    };
    tabs.forEach(function (t, k) {
      t.addEventListener("click", function () { show(k); });
      t.addEventListener("keydown", function (e) {
        if (e.key === "ArrowRight" || e.key === "ArrowDown") { e.preventDefault(); show(idx + 1, true); }
        if (e.key === "ArrowLeft" || e.key === "ArrowUp") { e.preventDefault(); show(idx - 1, true); }
        if (e.key === "Home") { e.preventDefault(); show(0, true); }
        if (e.key === "End") { e.preventDefault(); show(tabs.length - 1, true); }
      });
    });
    if (prev) prev.addEventListener("click", function () { show(idx - 1); });
    if (next) next.addEventListener("click", function () { show(idx + 1); });
    var fromHash = function () {
      var h = (location.hash || "").replace("#", "");
      var k = tabs.findIndex(function (t) { return t.getAttribute("data-slug") === h; });
      show(k >= 0 ? k : 0, false, true);
    };
    window.addEventListener("hashchange", fromHash);
    fromHash();
  }

  /* ---------- material filter ---------- */
  var chips = $$("[data-filter]");
  if (chips.length) {
    var items = $$(".items li[data-kind]");
    var count = $("[data-count]");
    var apply = function (kind) {
      var n = 0;
      items.forEach(function (li) {
        var show = kind === "all" || li.getAttribute("data-kind") === kind;
        li.hidden = !show; if (show) n++;
      });
      chips.forEach(function (c) { c.setAttribute("aria-pressed", c.getAttribute("data-filter") === kind ? "true" : "false"); });
      if (count) count.textContent = "Showing " + n + " of " + items.length + " items";
    };
    chips.forEach(function (c) { c.addEventListener("click", function () { apply(c.getAttribute("data-filter")); }); });
    var start = (location.hash || "").replace("#", "");
    apply(chips.some(function (c) { return c.getAttribute("data-filter") === start; }) ? start : "all");
  }

  /* ---------- validation helpers ---------- */
  function errFor(el) { return document.getElementById((el.name || el.id) + "-err"); }
  function setErr(el, msg) {
    var e = errFor(el);
    if (e) { e.textContent = msg || ""; el.setAttribute("aria-describedby", e.id); }
    if (el.type !== "checkbox" && el.type !== "radio") el.setAttribute("aria-invalid", msg ? "true" : "false");
  }
  function checkScope(scope) {
    var ok = true, first = null;
    $$("input, select, textarea", scope).forEach(function (el) {
      if (el.type === "checkbox" || el.type === "radio" || el.type === "file") return;
      var v = (el.value || "").trim(), msg = "";
      if (el.required && !v) msg = el.getAttribute("data-msg") || "Fill this in to continue.";
      else if (v && el.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) msg = "Enter an email like name@example.com.";
      else if (v && el.type === "tel" && v.replace(/[^\d]/g, "").length < 8) msg = "Enter a phone number with at least 8 digits.";
      else if (v && el.getAttribute("data-postcode") !== null && !/^(3|8)\d{3}$/.test(v)) msg = "Enter a Victorian postcode, like 3215.";
      setErr(el, msg);
      if (msg) { ok = false; first = first || el; }
    });
    $$("[data-min-one]", scope).forEach(function (group) {
      var name = group.getAttribute("data-min-one");
      var any = $$("input[name='" + name + "']", group).some(function (i) { return i.checked; });
      var e = document.getElementById(name + "-err");
      if (e) e.textContent = any ? "" : group.getAttribute("data-msg") || "Choose at least one.";
      if (!any) { ok = false; first = first || $("input", group); }
    });
    var radios = {};
    $$("input[type=radio]", scope).forEach(function (r) {
      if (r.closest("[hidden]")) return;
      radios[r.name] = radios[r.name] || [];
      radios[r.name].push(r);
    });
    Object.keys(radios).forEach(function (name) {
      var group = radios[name];
      if (!group.some(function (r) { return r.required; })) return;
      var any = group.some(function (r) { return r.checked; });
      var e = document.getElementById(name + "-err");
      if (e) e.textContent = any ? "" : (group[0].getAttribute("data-msg") || "Choose one option.");
      if (!any) { ok = false; first = first || group[0]; }
    });
    $$("input[type=checkbox][required]", scope).forEach(function (c) {
      var e = document.getElementById(c.name + "-err");
      if (e) e.textContent = c.checked ? "" : c.getAttribute("data-msg") || "Tick this to continue.";
      if (!c.checked) { ok = false; first = first || c; }
    });
    if (first) first.focus();
    return ok;
  }
  function liveClear(form) {
    form.addEventListener("input", function (e) { if (e.target.getAttribute("aria-invalid") === "true") setErr(e.target, ""); });
    form.addEventListener("change", function (e) {
      var g = e.target.closest("[data-min-one]");
      if (g) { var er = document.getElementById(g.getAttribute("data-min-one") + "-err"); if (er) er.textContent = ""; }
      if (e.target.type === "radio") { var re = document.getElementById(e.target.name + "-err"); if (re) re.textContent = ""; }
      if (e.target.type === "checkbox" && e.target.required) { var c = document.getElementById(e.target.name + "-err"); if (c && e.target.checked) c.textContent = ""; }
    });
  }
  function makeRef(prefix) {
    var d = new Date();
    var p = function (n) { return (n < 10 ? "0" : "") + n; };
    return prefix + "-" + String(d.getFullYear()).slice(2) + p(d.getMonth() + 1) + p(d.getDate()) + "-" + Math.floor(1000 + Math.random() * 9000);
  }
  function send(kind, data) {
    if (!CONFIG.endpoint) return Promise.resolve({ prototype: true });
    return fetch(CONFIG.endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ kind: kind, data: data }) })
      .then(function (r) { if (!r.ok) throw new Error("Send failed"); return { prototype: false }; });
  }
  function collect(form) {
    var out = {};
    $$("input, select, textarea", form).forEach(function (el) {
      if (!el.name || el.type === "file") return;
      if (el.closest("[data-when][hidden]")) return;
      if (el.type === "checkbox") { if (!el.checked) return; (out[el.name] = out[el.name] || []).push(el.value); return; }
      if (el.type === "radio") { if (el.checked) out[el.name] = el.value; return; }
      out[el.name] = el.value.trim();
    });
    return out;
  }

  /* ---------- multi-step sell form ---------- */
  var sell = $("form[data-steps]");
  if (sell) {
    var steps = $$(".step", sell);
    var bar = $$(".progress li", sell.parentNode);
    var back = $("[data-back]", sell), fwd = $("[data-next]", sell), submit = $("[data-submit]", sell);
    var cur = 0, KEY = "rh-sell-draft", photos = [], editing = false;
    var stepNames = bar.map(function (li) { return li.textContent.trim(); });
    var stepline = $("[data-stepline]", sell.parentNode);
    liveClear(sell);

    var draft = store(KEY);
    if (draft && Object.keys(draft).length) { var rn = $("[data-restored]", sell); if (rn) rn.hidden = false; }
    if (draft) {
      Object.keys(draft).forEach(function (k) {
        var v = draft[k];
        $$("[name='" + k + "']", sell).forEach(function (el) {
          if (el.type === "checkbox") el.checked = Array.isArray(v) && v.indexOf(el.value) > -1;
          else if (el.type === "radio") el.checked = el.value === v;
          else el.value = v;
        });
      });
    }
    sell.addEventListener("input", function () { store(KEY, collect(sell)); });
    sell.addEventListener("change", function () { store(KEY, collect(sell)); toggleMethod(); });

    function toggleMethod() {
      var m = (collect(sell).method) || "";
      $$("[data-when]", sell).forEach(function (el) {
        var on = el.getAttribute("data-when") === m;
        el.hidden = !on;
        $$("input,select,textarea", el).forEach(function (i) { if (i.hasAttribute("data-req")) i.required = on; });
      });
    }
    toggleMethod();

    function render(initial) {
      steps.forEach(function (s, k) { s.hidden = k !== cur; });
      bar.forEach(function (li, k) {
        li.className = k < cur ? "done" : (k === cur ? "now" : "");
        if (k === cur) li.setAttribute("aria-current", "step"); else li.removeAttribute("aria-current");
      });
      back.hidden = cur === 0;
      var last = cur === steps.length - 1;
      fwd.hidden = last; submit.hidden = !last;
      fwd.textContent = editing && !last ? "Back to review" : "Continue";
      if (stepline) stepline.textContent = "Step " + (cur + 1) + " of " + steps.length + ": " + stepNames[cur];
      if (last) buildReview();
      if (initial) return;
      var h = $("legend", steps[cur]);
      if (h) { h.tabIndex = -1; h.focus({ preventScroll: true }); }
      var top = sell.parentNode.getBoundingClientRect().top + window.scrollY - 90;
      if (window.scrollY > top) window.scrollTo({ top: top, behavior: reduce ? "auto" : "smooth" });
    }
    fwd.addEventListener("click", function () {
      if (!checkScope(steps[cur])) return;
      if (editing) { cur = steps.length - 1; editing = false; } else cur++;
      render();
    });
    back.addEventListener("click", function () { editing = false; cur--; render(); });

    function buildReview() {
      var d = collect(sell), dl = $("[data-review]", sell);
      var labelOf = function (name, val) {
        var el = $("input[name='" + name + "'][value='" + val + "']", sell);
        var lab = el && el.closest("label");
        return lab ? lab.firstChild && lab.querySelector("b") ? lab.querySelector("b").textContent : lab.textContent.trim() : val;
      };
      var rows = [
        ["What you have", (d.materials || []).map(function (v) { return labelOf("materials", v); }).join(", ") + (d.other ? "; " + d.other : ""), 0],
        ["How much", d.amount ? labelOf("amount", d.amount) : "", 0],
        ["Pickup or drop-off", d.method ? labelOf("method", d.method) : "", 1],
        [d.method === "pickup" ? "Pickup suburb" : "Your suburb", [d.suburb, d.postcode].filter(Boolean).join(" "), 1],
        ["Access notes", d.access || "", 1],
        ["Photos", photos.length ? photos.length + " attached" : "None", 2],
        ["Name", d.name, 3], ["Phone", d.phone, 3], ["Email", d.email || "", 3], ["Notes", d.notes || "", 3]
      ];
      dl.innerHTML = "";
      rows.forEach(function (r) {
        if (!r[1]) return;
        var dt = document.createElement("dt"); dt.textContent = r[0];
        var dd = document.createElement("dd"); dd.textContent = r[1] + " ";
        var a = document.createElement("button"); a.type = "button"; a.className = "edit linkish"; a.textContent = "Change";
        a.setAttribute("aria-label", "Change " + r[0].toLowerCase());
        a.addEventListener("click", function () { cur = r[2]; editing = true; render(); });
        dd.appendChild(a); dl.appendChild(dt); dl.appendChild(dd);
      });
    }

    /* photos */
    var file = $("input[type=file]", sell), thumbs = $(".thumbs", sell);
    if (file) file.addEventListener("change", function () {
      Array.prototype.slice.call(file.files).forEach(function (f) {
        if (!/^image\//.test(f.type) || photos.length >= 6) return;
        photos.push(f);
      });
      file.value = "";
      drawThumbs();
    });
    function drawThumbs() {
      thumbs.innerHTML = "";
      photos.forEach(function (f, k) {
        var fig = document.createElement("figure");
        var img = document.createElement("img"); img.alt = "Photo " + (k + 1) + ": " + f.name;
        img.src = URL.createObjectURL(f);
        var x = document.createElement("button"); x.type = "button"; x.textContent = "×"; x.setAttribute("aria-label", "Remove photo " + (k + 1));
        x.addEventListener("click", function () {
          photos.splice(k, 1); drawThumbs();
          var nb = thumbs.querySelector("button"); (nb || file).focus();
        });
        fig.appendChild(img); fig.appendChild(x); thumbs.appendChild(fig);
      });
      var n = $("[data-photo-count]", sell); if (n) n.textContent = photos.length ? photos.length + " of 6 added" : "";
    }

    sell.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!checkScope(steps[cur])) return;
      submit.disabled = true; submit.textContent = "Sending…";
      var data = collect(sell);
      send("sell", data).then(function (res) {
        var ref = makeRef("RH");
        store(KEY, null);
        var done = $("[data-done]");
        $(".ref", done).textContent = ref;
        $("[data-done-name]", done).textContent = (data.name || "").split(" ")[0] || "there";
        $("[data-done-proto]", done).hidden = !res.prototype;
        sell.hidden = true; $(".progress").hidden = true; done.hidden = false;
        var h = $("h2", done); h.tabIndex = -1; h.focus();
      }).catch(function () {
        submit.disabled = false; submit.textContent = "Send request";
        var e2 = $("[data-send-err]", sell); e2.textContent = "That didn't send. Check your connection and try again, or call us.";
      });
    });
    render(true);
  }

  /* ---------- simple forms (trade, contact) ---------- */
  $$("form[data-simple]").forEach(function (form) {
    liveClear(form);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!checkScope(form)) return;
      var b = $("[type=submit]", form); b.disabled = true; var label = b.textContent; b.textContent = "Sending…";
      send(form.getAttribute("data-simple"), collect(form)).then(function (res) {
        var done = document.getElementById(form.getAttribute("data-done"));
        $(".ref", done).textContent = makeRef(form.getAttribute("data-prefix") || "RH");
        $("[data-done-proto]", done).hidden = !res.prototype;
        form.hidden = true; done.hidden = false;
        var h = $("h2", done); h.tabIndex = -1; h.focus();
      }).catch(function () {
        b.disabled = false; b.textContent = label;
        var e2 = $("[data-send-err]", form); if (e2) e2.textContent = "That didn't send. Check your connection and try again.";
      });
    });
  });
})();
