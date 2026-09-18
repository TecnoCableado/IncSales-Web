/* Sistema IncSales · comportamiento. Sin dependencias, mejora progresiva:
   si esto no carga, la página se sigue leyendo entera. */
(function () {
  "use strict";
  document.documentElement.classList.add("js");
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var escritorio = function () { return window.matchMedia("(min-width: 1061px)").matches; };

  var nav = $(".nav");
  if (nav) {
    var fijar = function () { nav.classList.toggle("fija", window.scrollY > 4); };
    fijar(); window.addEventListener("scroll", fijar, { passive: true });
  }

  var hamb = $(".nav__hamburguesa"), menu = $("#menu");
  if (hamb && menu) {
    hamb.addEventListener("click", function () {
      var abierto = hamb.getAttribute("aria-expanded") === "true";
      hamb.setAttribute("aria-expanded", String(!abierto));
      menu.hidden = abierto;
    });
    window.addEventListener("resize", function () {
      if (escritorio()) { menu.hidden = false; hamb.setAttribute("aria-expanded", "false"); }
      else if (hamb.getAttribute("aria-expanded") !== "true") { menu.hidden = true; }
    });
    if (!escritorio()) menu.hidden = true;
  }

  var grupos = $$(".nav__grupo");
  var cerrar = function (menos) {
    grupos.forEach(function (g) {
      if (g === menos) return;
      var b = $(".nav__item", g), p = $(".panel", g);
      if (b && p) { b.setAttribute("aria-expanded", "false"); p.hidden = true; }
    });
  };
  grupos.forEach(function (g) {
    var b = $(".nav__item", g), p = $(".panel", g);
    if (!b || !p) return;
    p.hidden = true; b.setAttribute("aria-expanded", "false");
    b.addEventListener("click", function (e) {
      e.preventDefault();
      var abierto = b.getAttribute("aria-expanded") === "true";
      cerrar(g); b.setAttribute("aria-expanded", String(!abierto)); p.hidden = abierto;
    });
    var t;
    g.addEventListener("mouseenter", function () {
      if (!escritorio()) return;
      clearTimeout(t); cerrar(g); b.setAttribute("aria-expanded", "true"); p.hidden = false;
    });
    g.addEventListener("mouseleave", function () {
      if (!escritorio()) return;
      t = setTimeout(function () { b.setAttribute("aria-expanded", "false"); p.hidden = true; }, 130);
    });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".nav__grupo")) cerrar(null); });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    cerrar(null);
    if (hamb && hamb.getAttribute("aria-expanded") === "true") hamb.click();
  });

  var piezas = $$(".aparecer");
  if (piezas.length) {
    if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
      var v = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("visible"); v.unobserve(e.target); } });
      }, { rootMargin: "0px 0px -6% 0px", threshold: .06 });
      piezas.forEach(function (el) { v.observe(el); });
    } else { piezas.forEach(function (el) { el.classList.add("visible"); }); }
  }

  $$("[data-anio]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  $$("[data-tabs]").forEach(function (caja) {
    var bs = $$("[role=tab]", caja), ps = $$("[role=tabpanel]", caja);
    bs.forEach(function (b, i) {
      b.addEventListener("click", function () {
        bs.forEach(function (o, j) { o.setAttribute("aria-selected", String(i === j)); if (ps[j]) ps[j].hidden = i !== j; });
      });
    });
  });
})();
