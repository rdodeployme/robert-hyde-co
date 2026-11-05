/* Robert Hyde & Co. — cinematic layer: header, 3D tokens, the home time-machine sequence,
   the 500-tons scale, and the scroll-driven story. Everything degrades to static content. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var NOW = new Date().getFullYear();
  var REC = /[?&]rec\b/.test(location.search);
  if (REC) document.documentElement.classList.add("rec");

  /* header goes solid once you leave the hero */
  var head = $(".site-head.over");
  if (head) {
    var onScroll = function () { head.classList.toggle("solid", window.scrollY > 40); };
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  }

  /* 3D tokens */
  var coins = {};
  $$("[data-coin]").forEach(function (el, i) {
    if (!window.RHCoin) return;
    RHCoin.mount(el, {
      idle: el.hasAttribute("data-coin-idle") || el.hasAttribute("data-coin-drag"),
      draggable: el.hasAttribute("data-coin-drag"),
      texture: el.offsetWidth > 260 ? 1024 : 512
    }).then(function (c) { if (c) coins[el.hasAttribute("data-story-coin") ? "story" : "c" + i] = c; });
  });

  /* 500 tons: fill the cars once, as one moment */
  var cars = $("[data-cars]");
  if (cars) {
    $$("i", cars).forEach(function (i, k) { i.style.transitionDelay = (reduce ? 0 : k * 3) + "ms"; });
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) {
        if (es[0].isIntersecting) { cars.classList.add("on"); io.disconnect(); }
      }, { threshold: 0.4 });
      io.observe(cars);
    } else cars.classList.add("on");
  }

  /* home: pinned 1858 → today sequence */
  var cine = $("#cine");
  if (cine && !reduce && window.gsap && window.ScrollTrigger) {
    gsap.registerPlugin(ScrollTrigger);
    cine.classList.add("pinned");
    var stage = $(".cine-stage", cine), yearEl = $(".cine-year span", cine);
    var s1 = $(".s1", cine), s2 = $(".s2", cine), s3 = $(".s3", cine);
    var yr = { v: 1858 };
    var setYear = function () { yearEl.textContent = Math.round(yr.v); };
    gsap.set([s2, s3], { autoAlpha: 0 });
    var tl = gsap.timeline({ defaults: { ease: "none" } });
    tl.to($(".bgwrap", s1) || $(".bg", s1), { scale: 1.16, duration: 1.4 }, 0)
      .to($(".copy", s1), { autoAlpha: 0, y: -40, duration: 0.25 }, 0.7)
      .to(s2, { autoAlpha: 1, duration: 0.3 }, 1.0)
      .fromTo($(".mount", s2), { y: 80, rotate: 3 }, { y: 0, rotate: -1.2, duration: 0.5, ease: "power2.out" }, 1.0)
      .fromTo($(".copy", s2), { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.35 }, 1.2)
      .to(yr, { v: 1862, duration: 0.5, onUpdate: setYear }, 1.0)
      .to($(".mount img", s2), { scale: 2.3, duration: 0.9, ease: "power1.inOut" }, 1.55)
      .to(s2, { autoAlpha: 0, duration: 0.25 }, 2.5)
      .to(s3, { autoAlpha: 1, duration: 0.3 }, 2.8)
      .fromTo($(".bg", s3), { filter: "grayscale(1) sepia(.7) brightness(.55)", scale: 1.12 }, { filter: "grayscale(0) sepia(0) brightness(.62)", scale: 1, duration: 0.9 }, 2.8)
      .to(yr, { v: NOW, duration: 0.8, onUpdate: setYear, ease: "power2.in" }, 2.8)
      .fromTo($(".copy", s3), { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 0.4 }, 3.3)
      .fromTo($(".coin", s3), { autoAlpha: 0, scale: .7 }, { autoAlpha: 1, scale: 1, duration: 0.5, ease: "power2.out" }, 3.2)
      .to($(".cine-progress i", cine), { scaleX: 1, duration: 3.8 }, 0);
    ScrollTrigger.create({ trigger: cine, start: "top top", end: "+=" + Math.round(window.innerHeight * 3.4), pin: stage, scrub: REC ? true : 0.6, animation: tl, anticipatePin: 1 });
    /* keyboard and link users jumping past: nothing is hidden for good, the last state is reachable by scroll */
  }

  /* story: era tracking with the sticky token */
  var eras = $$("[data-era]");
  if (eras.length) {
    var yearBox = $(".tm2-year"), links = $$("[data-era-link]"), current = -1;
    var activate = function (k) {
      if (k === current) return; current = k;
      var e = eras[k];
      links.forEach(function (a, j) { a.classList.toggle("on", j === k); if (j === k) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current"); });
      var nav = links[k] && links[k].parentNode.parentNode;
      if (nav && nav.scrollWidth > nav.clientWidth) nav.scrollTo({ left: links[k].offsetLeft - 40, behavior: reduce ? "auto" : "smooth" });
      if (yearBox) {
        yearBox.classList.add("swap");
        setTimeout(function () { yearBox.textContent = e.getAttribute("data-year"); yearBox.classList.remove("swap"); }, reduce ? 0 : 180);
      }
      var c = coins.story;
      if (c) c.turnTo(k === eras.length - 1 ? Math.PI * 8 : k * Math.PI);
    };
    if ("IntersectionObserver" in window) {
      var vis = {};
      var io2 = new IntersectionObserver(function (es) {
        es.forEach(function (en) { vis[eras.indexOf(en.target)] = en.isIntersecting; });
        for (var k = 0; k < eras.length; k++) if (vis[k]) { activate(k); break; }
      }, { rootMargin: "-45% 0px -50% 0px" });
      eras.forEach(function (e) { io2.observe(e); });
    }
    activate(0);
  }
})();
