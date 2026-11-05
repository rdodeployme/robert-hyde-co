/* Robert Hyde & Co. — interactive extras:
   1. then-and-now sliders   2. Hyde's Melbourne map   3. depth on archive photos (WebGL)
   4. darkroom intro (once per visit). All degrade to plain content. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* 1. then and now ------------------------------------------------------- */
  $$("[data-tn]").forEach(function (box) {
    var range = $("input[type=range]", box);
    var set = function (v) {
      box.style.setProperty("--x", v + "%");
      range.setAttribute("aria-valuetext", v < 15 ? "Mostly today" : v > 85 ? "Mostly 1858" : v + "% 1858");
    };
    range.addEventListener("input", function () { set(range.value); });
    set(range.value);
    // a gentle one-off hint when it first comes into view
    if (!reduce && !/[?&]rec\b/.test(location.search) && "IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) {
        if (!es[0].isIntersecting) return; io.disconnect();
        var t0 = performance.now(), from = 50;
        (function tick(t) {
          var k = Math.min(1, (t - t0) / 1600), v = from + Math.sin(k * Math.PI * 2) * 18 * (1 - k);
          if (document.activeElement !== range) { range.value = Math.round(v); set(range.value); }
          if (k < 1) requestAnimationFrame(tick);
        })(t0);
      }, { threshold: 0.6 });
      io.observe(box);
    }
  });

  /* 2. Hyde's Melbourne map ------------------------------------------------ */
  var map = $("[data-hmap]");
  if (map) {
    var view = $(".hm-view", map), canvas = $(".hm-canvas", map), pins = $$(".hm-pin", map);
    var items = $$("[data-pin-item]"), panel = $(".hm-panel", map);
    var s = 1, x = 0, y = 0, MIN = 1, MAX = 3;
    var clamp = function () {
      var w = view.clientWidth, h = view.clientHeight;
      x = Math.min(0, Math.max(w - w * s, x)); y = Math.min(0, Math.max(h - h * s, y));
    };
    var apply = function (anim) {
      clamp();
      canvas.style.transition = anim && !reduce ? "transform .6s cubic-bezier(.16,1,.3,1)" : "none";
      canvas.style.transform = "translate(" + x + "px," + y + "px) scale(" + s + ")";
      map.style.setProperty("--inv", 1 / s);
    };
    var zoomAt = function (ns, cx, cy, anim) {
      ns = Math.max(MIN, Math.min(MAX, ns));
      x = cx - (cx - x) * ns / s; y = cy - (cy - y) * ns / s; s = ns; apply(anim);
    };
    $("[data-zoom-in]", map).addEventListener("click", function () { zoomAt(s * 1.5, view.clientWidth / 2, view.clientHeight / 2, true); });
    $("[data-zoom-out]", map).addEventListener("click", function () { zoomAt(s / 1.5, view.clientWidth / 2, view.clientHeight / 2, true); });
    $("[data-zoom-reset]", map).addEventListener("click", function () { s = 1; x = 0; y = 0; apply(true); });
    view.addEventListener("wheel", function (e) {
      if (!e.ctrlKey && !e.metaKey && s === 1 && e.deltaY > 0) return; // let the page scroll
      e.preventDefault();
      var r = view.getBoundingClientRect();
      zoomAt(s * (e.deltaY < 0 ? 1.18 : 1 / 1.18), e.clientX - r.left, e.clientY - r.top, false);
    }, { passive: false });
    var drag = null;
    view.addEventListener("pointerdown", function (e) {
      if (e.target.closest(".hm-pin") || s === 1) return;
      drag = { px: e.clientX, py: e.clientY, x: x, y: y }; view.setPointerCapture(e.pointerId); view.classList.add("dragging");
    });
    view.addEventListener("pointermove", function (e) { if (!drag) return; x = drag.x + e.clientX - drag.px; y = drag.y + e.clientY - drag.py; apply(false); });
    var end = function () { drag = null; view.classList.remove("dragging"); };
    view.addEventListener("pointerup", end); view.addEventListener("pointercancel", end);
    view.addEventListener("keydown", function (e) {
      var step = 60, k = e.key;
      if (k === "ArrowLeft") x += step; else if (k === "ArrowRight") x -= step; else if (k === "ArrowUp") y += step; else if (k === "ArrowDown") y -= step;
      else if (k === "+" || k === "=") return zoomAt(s * 1.5, view.clientWidth / 2, view.clientHeight / 2, true);
      else if (k === "-") return zoomAt(s / 1.5, view.clientWidth / 2, view.clientHeight / 2, true);
      else return;
      e.preventDefault(); apply(true);
    });
    var select = function (k, fly) {
      pins.forEach(function (p, j) { p.setAttribute("aria-pressed", j === k ? "true" : "false"); });
      items.forEach(function (it, j) { it.classList.toggle("on", j === k); });
      var src = items[k];
      panel.innerHTML = "<p class='hm-when'>" + src.getAttribute("data-when") + "</p><h3>" + $("b", src).innerHTML + "</h3><p>" + $("span", src).innerHTML + "</p>";
      if (fly) {
        var p = pins[k], px = parseFloat(p.style.left) / 100 * view.clientWidth, py = parseFloat(p.style.top) / 100 * view.clientHeight;
        s = 2.2; x = view.clientWidth / 2 - px * s; y = view.clientHeight / 2 - py * s; apply(true);
      }
    };
    pins.forEach(function (p, k) { p.addEventListener("click", function () { select(k, s < 1.5); }); });
    items.forEach(function (it, k) {
      var b = $("button", it); if (b) b.addEventListener("click", function () { select(k, true); map.scrollIntoView({ block: "nearest", behavior: reduce ? "auto" : "smooth" }); });
    });
    window.addEventListener("resize", function () { apply(false); });
    select(0, false); apply(false);
  }

  /* 3. depth on archive photos -------------------------------------------- */
  function depthify(img) {
    var c = document.createElement("canvas");
    var gl = c.getContext("webgl", { premultipliedAlpha: false, alpha: false });
    if (!gl) return;
    var horizon = parseFloat(img.getAttribute("data-depth") || "0.4");
    var pos = (img.style.objectPosition || "50% 50%").split(" ").map(function (v) { return parseFloat(v) / 100; });
    var vs = "attribute vec2 p;varying vec2 v;void main(){v=vec2(p.x*.5+.5,.5-p.y*.5);gl_Position=vec4(p,0.,1.);}";
    var fs = "precision mediump float;varying vec2 v;uniform sampler2D t,d;uniform vec2 sc,sh,o;" +
      "void main(){vec2 u=(v-.5)*sc+.5+sh;float z=texture2D(d,u).r;vec2 q=u+o*(z-.3);gl_FragColor=texture2D(t,q);}";
    function sh(type, src) { var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return s; }
    var pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(pr);
    if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) return;
    gl.useProgram(pr);
    var b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(pr, "p"); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    function texFrom(src, unit) {
      var tx = gl.createTexture(); gl.activeTexture(gl.TEXTURE0 + unit); gl.bindTexture(gl.TEXTURE_2D, tx);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, src); return tx;
    }
    // depth map: far above the horizon, nearer towards the bottom, with a soft curve
    var dm = document.createElement("canvas"); dm.width = 8; dm.height = 256;
    var dx = dm.getContext("2d"), gr = dx.createLinearGradient(0, 0, 0, 256);
    gr.addColorStop(0, "#000"); gr.addColorStop(Math.max(0.01, horizon - 0.05), "#080808");
    gr.addColorStop(Math.min(0.99, horizon + 0.12), "#555"); gr.addColorStop(1, "#fff");
    dx.fillStyle = gr; dx.fillRect(0, 0, 8, 256);
    texFrom(img, 0); texFrom(dm, 1);
    gl.uniform1i(gl.getUniformLocation(pr, "t"), 0); gl.uniform1i(gl.getUniformLocation(pr, "d"), 1);
    var uSc = gl.getUniformLocation(pr, "sc"), uSh = gl.getUniformLocation(pr, "sh"), uO = gl.getUniformLocation(pr, "o");
    c.className = img.className + " depth-canvas"; c.setAttribute("aria-hidden", "true");
    img.parentNode.insertBefore(c, img.nextSibling); img.classList.add("depth-src");
    var W = 0, H = 0;
    function size() {
      var r = img.getBoundingClientRect(), dpr = /[?&]rec\b/.test(location.search) ? 0.55 : Math.min(window.devicePixelRatio || 1, 1.5);
      W = Math.max(1, Math.round(r.width * dpr)); H = Math.max(1, Math.round(r.height * dpr));
      c.width = W; c.height = H; gl.viewport(0, 0, W, H);
      var ca = W / H, ia = img.naturalWidth / img.naturalHeight, sx = 1, sy = 1;
      if (ca > ia) sy = ia / ca; else sx = ca / ia;
      sx *= 0.94; sy *= 0.94;
      gl.uniform2f(uSc, sx, sy); gl.uniform2f(uSh, (1 - sx) * (pos[0] - .5), (1 - sy) * (pos[1] - .5));
    }
    size(); window.addEventListener("resize", size);
    var tx = 0, ty = 0, cx = 0, cy = 0, mouse = false, vis = true, raf = 0, t0 = performance.now();
    window.addEventListener("pointermove", function (e) {
      if (e.pointerType !== "mouse") return; mouse = true;
      tx = (e.clientX / window.innerWidth - .5) * -0.055; ty = (e.clientY / window.innerHeight - .5) * -0.03;
    }, { passive: true });
    function frame(t) {
      if (!mouse) { var k = (t - t0) / 1000; tx = Math.sin(k * 0.35) * 0.024; ty = Math.cos(k * 0.27) * 0.01; }
      cx += (tx - cx) * 0.06; cy += (ty - cy) * 0.06;
      gl.uniform2f(uO, cx, cy); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      raf = vis ? requestAnimationFrame(frame) : 0;
    }
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) {
      vis = es[0].isIntersecting; if (vis && !raf) raf = requestAnimationFrame(frame);
    }).observe(c);
    raf = requestAnimationFrame(frame);
  }
  if (!reduce) $$("img[data-depth]").forEach(function (img) {
    var go = function () { try { depthify(img); } catch (e) { /* keep the plain photo */ } };
    if (img.complete && img.naturalWidth) go(); else img.addEventListener("load", go, { once: true });
  });

  /* 4. darkroom intro, home page only, once per visit -------------------- */
  var intro = $("[data-intro]");
  if (intro) {
    var seen = false;
    try { seen = sessionStorage.getItem("rh-intro") === "1"; sessionStorage.setItem("rh-intro", "1"); } catch (e) { }
    if (/[?&]rec\b/.test(location.search)) intro.classList.add("run", "manual");
    else if (reduce || seen) intro.remove();
    else {
      intro.classList.add("run");
      setTimeout(function () { intro.remove(); }, 2300);
    }
  }
})();
