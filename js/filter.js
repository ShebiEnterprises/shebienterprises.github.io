(function () {
  "use strict";

  const portfolio = document.getElementById("portfolioFilters");
  if (!portfolio) return;

  let activeService = "all";
  let activeType = "all";

  const serviceBtns = portfolio.querySelectorAll("[data-service-filter]");
  const typeBtns = portfolio.querySelectorAll("[data-type-filter]");
  const projectCards = document.querySelectorAll(".project-card[data-service]");

  function setActive(group, btn) {
    group.forEach(function (b) {
      b.classList.remove("active");
    });
    btn.classList.add("active");
  }

  function applyFilters() {
    projectCards.forEach(function (card) {
      const s = (card.getAttribute("data-service") || "").trim();
      const t = (card.getAttribute("data-type") || "").trim();
      const okService =
        activeService === "all" || s === activeService || s.split(/\s+/).includes(activeService);
      const okType = activeType === "all" || t === activeType || t.split(/\s+/).includes(activeType);
      if (okService && okType) {
        card.style.display = "";
        card.style.animation = "fadeInUp 0.4s ease forwards";
      } else {
        card.style.display = "none";
      }
    });
  }

  serviceBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      setActive(serviceBtns, btn);
      activeService = btn.getAttribute("data-service-filter") || "all";
      applyFilters();
    });
  });

  typeBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      setActive(typeBtns, btn);
      activeType = btn.getAttribute("data-type-filter") || "all";
      applyFilters();
    });
  });
})();
