/* The Robert Hyde & Co. token in 3D (three.js r128).
   Faces are drawn on canvas from the 1857 inscription (an original redraw, not a museum photo),
   embossed with a bump map and lit as copper. Falls back to the SVG token if WebGL is missing. */
(function () {
  "use strict";
  var RAD = Math.PI / 180, FR = Math.PI / 2, BR = Math.PI / 2, BF = false;

  function arcText(ctx, text, cx, cy, r, centreAngle, size, spacing, outward) {
    ctx.save();
    ctx.font = "700 " + size + "px 'Zilla Slab', Georgia, serif";
    var widths = [], total = 0;
    for (var i = 0; i < text.length; i++) { var w = ctx.measureText(text[i]).width + spacing; widths.push(w); total += w; }
    total -= spacing;
    var angTotal = total / r;
    var a = outward ? centreAngle - angTotal / 2 : centreAngle + angTotal / 2;
    for (var j = 0; j < text.length; j++) {
      var half = (widths[j] - spacing) / 2 / r;
      var mid = outward ? a + half : a - half;
      ctx.save();
      ctx.translate(cx + r * Math.cos(mid), cy + r * Math.sin(mid));
      ctx.rotate(outward ? mid + Math.PI / 2 : mid - Math.PI / 2);
      ctx.textAlign = "center"; ctx.textBaseline = outward ? "alphabetic" : "hanging";
      ctx.fillText(text[j], 0, 0);
      ctx.restore();
      a += (outward ? 1 : -1) * widths[j] / r;
    }
    ctx.restore();
  }

  /* mode "height": white = raised, dark = field. mode "colour": copper with worn high points. */
  function drawFace(side, mode, N) {
    var c = document.createElement("canvas"); c.width = c.height = N;
    var x = c.getContext("2d"), s = N / 200, cx = N / 2;
    var raised = mode === "height" ? "#ffffff" : "#E0A271";
    var field = mode === "height" ? "#3a3a3a" : "#9A5326";
    // field
    x.fillStyle = field; x.fillRect(0, 0, N, N);
    if (mode === "colour") {
      var g = x.createRadialGradient(cx * .7, cx * .6, N * .05, cx, cx, N * .55);
      g.addColorStop(0, "rgba(255,190,130,.28)"); g.addColorStop(1, "rgba(60,20,5,.35)");
      x.fillStyle = g; x.fillRect(0, 0, N, N);
      // fine patina speckle
      for (var k = 0; k < 2600; k++) {
        x.fillStyle = Math.random() < .5 ? "rgba(40,15,4,.10)" : "rgba(255,200,150,.07)";
        x.fillRect(Math.random() * N, Math.random() * N, 1.5 * s, 1.5 * s);
      }
    }
    // rim
    x.strokeStyle = raised; x.lineWidth = 7 * s;
    x.beginPath(); x.arc(cx, cx, 96 * s, 0, 2 * Math.PI); x.stroke();
    // beads
    x.fillStyle = raised;
    for (var i = 0; i < 72; i++) {
      var a = 2 * Math.PI * i / 72;
      x.beginPath(); x.arc(cx + 88 * s * Math.cos(a), cx + 88 * s * Math.sin(a), 1.5 * s, 0, 2 * Math.PI); x.fill();
    }
    x.fillStyle = raised; x.strokeStyle = raised;
    if (side === "front") {
      x.lineWidth = 1.8 * s; x.beginPath(); x.arc(cx, cx, 57 * s, 0, 2 * Math.PI); x.stroke();
      arcText(x, "ROBERT HYDE & Co", cx, cx, 70 * s, -Math.PI / 2, 15 * s, 2.6 * s, true);
      arcText(x, "MELBOURNE", cx, cx, 70 * s, Math.PI / 2, 13 * s, 3.2 * s, false);
      x.beginPath(); x.arc(cx - 70 * s, cx, 2.4 * s, 0, 7); x.fill();
      x.beginPath(); x.arc(cx + 70 * s, cx, 2.4 * s, 0, 7); x.fill();
      var lines = [["GENERAL", 11.5, 71], ["MARINE", 11.5, 85], ["STORE", 11.5, 99], ["—", 9, 109], ["SHIPPERS OF", 8.8, 120], ["RAGS GLASS", 8.8, 131], ["METALS", 8.8, 142], ["&c.", 8.8, 153]];
      x.textAlign = "center"; x.textBaseline = "alphabetic";
      lines.forEach(function (l) { x.font = "700 " + l[1] * s + "px 'Zilla Slab', Georgia, serif"; x.fillText(l[0], cx, l[2] * s); });
    } else {
      arcText(x, "PEACE & PLENTY", cx, cx, 72 * s, -Math.PI / 2, 14 * s, 2.6 * s, true);
      arcText(x, "1857", cx, cx, 72 * s, Math.PI / 2, 15 * s, 4 * s, false);
      // ribbon
      x.lineWidth = 2 * s;
      x.beginPath(); x.moveTo(cx - 52 * s, cx + 38 * s); x.quadraticCurveTo(cx, cx + 52 * s, cx + 52 * s, cx + 38 * s);
      x.lineTo(cx + 50 * s, cx + 48 * s); x.quadraticCurveTo(cx, cx + 62 * s, cx - 50 * s, cx + 48 * s); x.closePath(); x.stroke();
      x.font = "700 " + 6.4 * s + "px 'Zilla Slab', Georgia, serif"; x.textAlign = "center";
      x.fillText("ADVANCE AUSTRALIA", cx, cx + 50.5 * s);
      // shield, quartered
      x.lineWidth = 2.2 * s;
      x.beginPath(); x.moveTo(cx - 24 * s, cx - 30 * s); x.lineTo(cx + 24 * s, cx - 30 * s); x.lineTo(cx + 24 * s, cx + 4 * s);
      x.quadraticCurveTo(cx + 24 * s, cx + 26 * s, cx, cx + 34 * s); x.quadraticCurveTo(cx - 24 * s, cx + 26 * s, cx - 24 * s, cx + 4 * s); x.closePath(); x.stroke();
      x.beginPath(); x.moveTo(cx, cx - 30 * s); x.lineTo(cx, cx + 34 * s); x.moveTo(cx - 24 * s, cx - 4 * s); x.lineTo(cx + 24 * s, cx - 4 * s); x.stroke();
      // quarters: fleece, ship, bull, anchor (simplified marks)
      x.beginPath(); x.ellipse(cx - 12 * s, cx - 17 * s, 7 * s, 4 * s, 0, 0, 7); x.fill();
      x.beginPath(); x.moveTo(cx + 6 * s, cx - 10 * s); x.lineTo(cx + 19 * s, cx - 10 * s); x.lineTo(cx + 16 * s, cx - 7 * s); x.lineTo(cx + 9 * s, cx - 7 * s); x.closePath(); x.fill();
      x.fillRect(cx + 12 * s, cx - 26 * s, 1.2 * s, 16 * s);
      x.beginPath(); x.ellipse(cx - 12 * s, cx + 9 * s, 7 * s, 4.5 * s, 0, 0, 7); x.fill();
      x.lineWidth = 1.8 * s; x.beginPath(); x.moveTo(cx + 12 * s, cx + 2 * s); x.lineTo(cx + 12 * s, cx + 20 * s);
      x.moveTo(cx + 6 * s, cx + 15 * s); x.quadraticCurveTo(cx + 12 * s, cx + 23 * s, cx + 18 * s, cx + 15 * s); x.moveTo(cx + 8 * s, cx + 6 * s); x.lineTo(cx + 16 * s, cx + 6 * s); x.stroke();
      // rising sun
      x.lineWidth = 1.4 * s;
      for (var r = 0; r < 9; r++) { var ang = Math.PI + r * Math.PI / 8; x.beginPath(); x.moveTo(cx + 9 * s * Math.cos(ang), cx - 36 * s + 9 * s * Math.sin(ang)); x.lineTo(cx + 15 * s * Math.cos(ang), cx - 36 * s + 15 * s * Math.sin(ang)); x.stroke(); }
      x.beginPath(); x.arc(cx, cx - 36 * s, 6 * s, Math.PI, 0); x.fill();
      // supporters: emu and kangaroo, as simple silhouettes
      x.beginPath(); x.ellipse(cx - 36 * s, cx - 2 * s, 7 * s, 10 * s, -.2, 0, 7); x.fill();
      x.fillRect(cx - 34 * s, cx - 24 * s, 2 * s, 14 * s); x.beginPath(); x.arc(cx - 33 * s, cx - 25 * s, 3 * s, 0, 7); x.fill();
      x.fillRect(cx - 38 * s, cx + 7 * s, 1.6 * s, 18 * s); x.fillRect(cx - 34 * s, cx + 7 * s, 1.6 * s, 18 * s);
      x.beginPath(); x.ellipse(cx + 36 * s, cx + 2 * s, 7 * s, 12 * s, .25, 0, 7); x.fill();
      x.beginPath(); x.ellipse(cx + 32 * s, cx - 14 * s, 3.5 * s, 4.5 * s, 0, 0, 7); x.fill();
      x.beginPath(); x.moveTo(cx + 40 * s, cx + 10 * s); x.quadraticCurveTo(cx + 52 * s, cx + 22 * s, cx + 46 * s, cx + 30 * s); x.lineWidth = 3 * s; x.stroke();
      x.fillRect(cx + 33 * s, cx + 12 * s, 2 * s, 14 * s);
    }
    if (mode === "height") {
      // soften so the bump map gives rounded relief rather than stair-steps
      var t = document.createElement("canvas"); t.width = t.height = N;
      var tx = t.getContext("2d"); tx.filter = "blur(" + (1.1 * s) + "px)"; tx.drawImage(c, 0, 0); return t;
    }
    return c;
  }

  function make(holder, opts) {
    opts = opts || {};
    if (!window.THREE) return null;
    var test = document.createElement("canvas");
    var gl = test.getContext("webgl") || test.getContext("experimental-webgl");
    if (!gl) return null;
    var THREE = window.THREE;
    var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: "low-power" });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.outputEncoding = THREE.sRGBEncoding;
    renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.15;
    renderer.domElement.setAttribute("aria-hidden", "true");
    renderer.domElement.className = "coin-canvas";
    holder.appendChild(renderer.domElement);
    holder.classList.add("is-3d");

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(26, 1, 0.1, 50); camera.position.set(0, 0, 9.2);
    var N = opts.texture || 1024;
    function tex(c, srgb) { var t = new THREE.CanvasTexture(c); if (srgb) t.encoding = THREE.sRGBEncoding; t.anisotropy = renderer.capabilities.getMaxAnisotropy(); return t; }
    function faceMat(side) {
      return new THREE.MeshStandardMaterial({
        map: tex(drawFace(side, "colour", N), true), bumpMap: tex(drawFace(side, "height", N)), bumpScale: 0.055,
        metalness: 0.9, roughness: 0.38, color: 0xffffff
      });
    }
    var edge = new THREE.MeshStandardMaterial({ color: 0xB06A36, metalness: 0.95, roughness: 0.32 });
    var front = faceMat("front"), back = faceMat("back");
    // CylinderGeometry groups: 0 side, 1 top, 2 bottom
    var geo = new THREE.CylinderGeometry(1.9, 1.9, 0.2, 128, 1);
    var coin = new THREE.Mesh(geo, [edge, front, back]);
    coin.rotation.x = Math.PI / 2;  // top face looks at the camera
    var pivot = new THREE.Group(); pivot.add(coin); scene.add(pivot);
    // texture orientation: rotate top face so text reads upright
    front.map.center.set(.5, .5); front.bumpMap.center.set(.5, .5);
    back.map.center.set(.5, .5); back.bumpMap.center.set(.5, .5);
    var uv = opts.uv || { fr: FR, br: BR, bflip: BF };
    front.map.rotation = front.bumpMap.rotation = uv.fr;
    back.map.rotation = back.bumpMap.rotation = uv.br;
    if (uv.bflip) [back.map, back.bumpMap].forEach(function (t) { t.repeat.set(-1, 1); });

    scene.add(new THREE.HemisphereLight(0xfff1e2, 0x1a1410, 0.55));
    var key = new THREE.DirectionalLight(0xffe0c0, 2.1); key.position.set(-3, 4, 5); scene.add(key);
    var rim = new THREE.DirectionalLight(0x9fd0c4, 0.9); rim.position.set(4, -2, -3); scene.add(rim);
    var glint = new THREE.PointLight(0xffffff, 1.4, 20); glint.position.set(2.5, 1.5, 4); scene.add(glint);

    var state = { y: 0, x: -0.12, targetY: opts.startY || 0, targetX: -0.12, idle: opts.idle !== false, drag: false };
    var visible = true, raf = 0, last = performance.now();
    function size() {
      var w = holder.clientWidth, h = holder.clientHeight || w;
      renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
    }
    size();
    if (window.ResizeObserver) new ResizeObserver(size).observe(holder); else window.addEventListener("resize", size);
    function frame(t) {
      var dt = Math.min(0.05, (t - last) / 1000); last = t;
      if (state.idle && !state.drag) state.targetY += dt * 0.35;
      state.y += (state.targetY - state.y) * Math.min(1, dt * 4.2);
      state.x += (state.targetX - state.x) * Math.min(1, dt * 4.2);
      pivot.rotation.y = state.y; pivot.rotation.x = state.x;
      renderer.render(scene, camera);
      raf = visible ? requestAnimationFrame(frame) : 0;
    }
    if (window.IntersectionObserver) {
      new IntersectionObserver(function (es) {
        visible = es[0].isIntersecting;
        if (visible && !raf) { last = performance.now(); raf = requestAnimationFrame(frame); }
      }).observe(holder);
    }
    raf = requestAnimationFrame(frame);

    // pointer: glint follows, drag spins
    var lastX = 0;
    holder.addEventListener("pointermove", function (e) {
      var r = holder.getBoundingClientRect();
      var nx = (e.clientX - r.left) / r.width - .5, ny = (e.clientY - r.top) / r.height - .5;
      glint.position.set(nx * 8, -ny * 8, 4);
      if (state.drag) { state.targetY += (e.clientX - lastX) * 0.012; lastX = e.clientX; }
      else state.targetX = -0.12 + ny * 0.25;
    });
    if (opts.draggable) {
      holder.addEventListener("pointerdown", function (e) { state.drag = true; lastX = e.clientX; holder.setPointerCapture(e.pointerId); });
      holder.addEventListener("pointerup", function () { state.drag = false; });
      holder.addEventListener("pointercancel", function () { state.drag = false; });
    }
    return {
      turnTo: function (rad) { state.idle = false; state.targetY = rad; },
      spin: function (on) { state.idle = on; },
      get y() { return state.targetY; }
    };
  }

  window.RHCoin = {
    mount: function (holder, opts) {
      var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      var o = opts || {}; if (reduce) o.idle = false;
      var go = function () { try { return make(holder, o); } catch (e) { return null; } };
      if (document.fonts && document.fonts.load) {
        return document.fonts.load("700 20px 'Zilla Slab'").then(go, go);
      }
      return Promise.resolve(go());
    }
  };
})();
