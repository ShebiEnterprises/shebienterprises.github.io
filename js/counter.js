(function () {
  "use strict";

  function animateCounter(el) {
    const target = parseInt(el.getAttribute("data-target"), 10);
    if (isNaN(target)) return;
    const suffix = el.getAttribute("data-suffix") || "";
    const duration = 2000;
    const step = Math.max(target / (duration / 16), 1);
    let current = 0;

    const timer = setInterval(function () {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      el.textContent = Math.floor(current) + suffix;
    }, 16);
  }

  const counterObserver = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (
          entry.isIntersecting &&
          !entry.target.classList.contains("counted")
        ) {
          entry.target.classList.add("counted");
          animateCounter(entry.target);
        }
      });
    },
    { threshold: 0.4 }
  );

  document.querySelectorAll(".stat-number").forEach(function (counter) {
    counterObserver.observe(counter);
  });
})();
