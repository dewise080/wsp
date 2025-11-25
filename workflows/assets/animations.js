// Mark page as loaded to trigger fade-in
window.addEventListener("DOMContentLoaded", function () {
  document.documentElement.classList.remove("page-fade");
  document.documentElement.classList.add("page-loaded");

  // Auto-apply default animation to sections without explicit data-animate
  document.querySelectorAll("section").forEach(function (sec) {
    if (!sec.hasAttribute("data-animate")) {
      sec.setAttribute("data-animate", "fade-up");
    }
  });

  // IntersectionObserver to reveal elements
  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          // Optional per-element delay via data-animate-delay (e.g., "0.12s")
          var d = entry.target.getAttribute("data-animate-delay");
          if (d) {
            entry.target.style.transitionDelay = d;
          }
          entry.target.classList.add("in-view");
          observer.unobserve(entry.target);
        }
      });
    },
    { root: null, threshold: 0.15, rootMargin: "0px 0px -10% 0px" },
  );

  document.querySelectorAll("[data-animate]").forEach(function (el) {
    observer.observe(el);
  });

  // Parallax backgrounds on scroll
  var reduceMotion =
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var items = [];

  function measure() {
    items = Array.prototype.map.call(
      document.querySelectorAll("[data-parallax]"),
      function (el) {
        var speed = parseFloat(el.getAttribute("data-parallax"));
        if (isNaN(speed)) speed = 0.3;
        var rect = el.getBoundingClientRect();
        var start = rect.top + window.scrollY; // element's top relative to document
        return { el: el, speed: speed, start: start };
      },
    );
  }

  var ticking = false;
  function update() {
    ticking = false;
    if (reduceMotion) return;
    var y = window.scrollY || window.pageYOffset;
    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      // Translate based on scroll distance from element start
      var offset = (y - it.start) * it.speed;
      it.el.style.transform = "translate3d(0," + offset.toFixed(2) + "px,0)";
    }
  }

  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(update);
      ticking = true;
    }
  }

  // Initialize and bind events
  measure();
  update();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", function () {
    measure();
    update();
  });
});
