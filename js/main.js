(function () {
  "use strict";

  const navbar = document.getElementById("navbar");
  if (navbar) {
    const isHeroPage = document.querySelector(".hero") !== null;

    if (isHeroPage) {
      navbar.classList.add("transparent");
    } else {
      navbar.classList.add("scrolled");
    }

    window.addEventListener("scroll", function () {
      if (isHeroPage) {
        if (window.scrollY > 80) {
          navbar.classList.remove("transparent");
          navbar.classList.add("scrolled");
        } else {
          navbar.classList.remove("scrolled");
          navbar.classList.add("transparent");
        }
      }
    });
  }

  const hamburger = document.getElementById("hamburger");
  const mobileMenu = document.getElementById("mobileMenu");
  if (hamburger && mobileMenu) {
    hamburger.addEventListener("click", function () {
      mobileMenu.classList.toggle("open");
      hamburger.classList.toggle("active");
    });
  }

  const currentPath = window.location.pathname.replace(/\/$/, "") || "/";
  document.querySelectorAll(".navbar-links a[href]").forEach(function (link) {
    const href = link.getAttribute("href");
    if (!href || href.startsWith("#")) return;
    const normalized = href.replace(/^\//, "");
    const pathFile = currentPath.split("/").pop() || "";
    if (href === currentPath || currentPath.endsWith(href)) {
      link.classList.add("active");
    } else if (
      (normalized === "index.html" || href === "/" || href === "") &&
      (currentPath === "/" || pathFile === "" || pathFile === "index.html")
    ) {
      link.classList.add("active");
    }
  });

  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener("click", function (e) {
      const id = this.getAttribute("href");
      if (!id || id === "#") return;
      const target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
        if (mobileMenu) mobileMenu.classList.remove("open");
        if (hamburger) hamburger.classList.remove("active");
      }
    });
  });

  document.querySelectorAll(".faq-question").forEach(function (question) {
    question.addEventListener("click", function () {
      const item = question.closest(".faq-item");
      if (!item) return;
      const answer = item.querySelector(".faq-answer");
      const isOpen = item.classList.contains("open");

      document.querySelectorAll(".faq-item").forEach(function (i) {
        i.classList.remove("open");
        const a = i.querySelector(".faq-answer");
        if (a) a.style.maxHeight = "0";
      });

      if (!isOpen && answer) {
        item.classList.add("open");
        const inner = answer.querySelector(".faq-answer-inner");
        const h = inner ? inner.scrollHeight : answer.scrollHeight;
        answer.style.maxHeight = h + 24 + "px";
      }
    });
  });
})();
