(function () {
  function initCarousel(root) {
    var wrapper = root.querySelector(".alice-carousel__wrapper");
    var stage = root.querySelector(".alice-carousel__stage");
    if (!wrapper || !stage) return;

    // Remove cloned items from previous library snapshot
    var items = Array.from(stage.children);
    var originals = items.filter(function (li) {
      return !li.classList.contains("__cloned");
    });
    if (originals.length && originals.length !== items.length) {
      var ul = document.createElement("ul");
      ul.className = "alice-carousel__stage";
      originals.forEach(function (li) {
        ul.appendChild(li);
      });
      stage.replaceWith(ul);
      stage = ul;
    }

    var index = 0;
    var per = 3;
    var autoTimer = null;

    function recalc() {
      var w = window.innerWidth || document.documentElement.clientWidth;
      per = w <= 640 ? 1 : w <= 1024 ? 2 : 3;
      clampIndex();
      applyTransform();
    }

    function maxIndex() {
      return Math.max(0, stage.children.length - per);
    }

    function clampIndex() {
      if (index > maxIndex()) index = 0;
      if (index < 0) index = maxIndex();
    }

    function applyTransform() {
      // Move by pixels based on wrapper width and items per view
      var itemWidth = wrapper.clientWidth / per;
      var shift = index * itemWidth;
      stage.style.transform = "translate3d(" + -shift + "px, 0, 0)";
    }

    function next() {
      index++;
      clampIndex();
      applyTransform();
    }
    function prev() {
      index--;
      clampIndex();
      applyTransform();
    }

    function startAuto() {
      stopAuto();
      autoTimer = setInterval(function () {
        index++;
        clampIndex();
        applyTransform();
      }, 3000);
    }
    function stopAuto() {
      if (autoTimer) {
        clearInterval(autoTimer);
        autoTimer = null;
      }
    }

    // Hover pause
    wrapper.addEventListener("mouseenter", stopAuto);
    wrapper.addEventListener("mouseleave", startAuto);

    // Basic swipe support
    var startX = 0,
      deltaX = 0,
      swiping = false;
    wrapper.addEventListener(
      "touchstart",
      function (e) {
        if (!e.touches || !e.touches.length) return;
        startX = e.touches[0].clientX;
        deltaX = 0;
        swiping = true;
        stopAuto();
      },
      { passive: true },
    );
    wrapper.addEventListener(
      "touchmove",
      function (e) {
        if (!swiping || !e.touches || !e.touches.length) return;
        deltaX = e.touches[0].clientX - startX;
      },
      { passive: true },
    );
    wrapper.addEventListener("touchend", function () {
      if (!swiping) return;
      swiping = false;
      var threshold = 40; // px
      if (deltaX > threshold) prev();
      else if (deltaX < -threshold) next();
      startAuto();
    });

    window.addEventListener("resize", recalc);
    recalc();
    startAuto();
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".alice-carousel").forEach(initCarousel);
  });
})();
