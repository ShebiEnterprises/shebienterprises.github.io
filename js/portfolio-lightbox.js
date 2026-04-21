(function () {
  "use strict";

  var lightbox = document.getElementById("portfolioLightbox");
  var lbImg = document.getElementById("portfolioLightboxImg");
  var counterEl = document.getElementById("portfolioLightboxCounter");
  var btnClose = lightbox && lightbox.querySelector(".portfolio-lightbox-close");
  var btnPrev = lightbox && lightbox.querySelector(".portfolio-lightbox-prev");
  var btnNext = lightbox && lightbox.querySelector(".portfolio-lightbox-next");

  if (!lightbox || !lbImg) return;

  var imgs = [];
  var index = 0;

  function collect() {
    imgs = Array.prototype.slice.call(
      document.querySelectorAll("img.portfolio-lightbox-img")
    );
  }

  function show(i) {
    if (!imgs.length) return;
    index = (i + imgs.length) % imgs.length;
    var el = imgs[index];
    lbImg.src = el.currentSrc || el.src;
    lbImg.alt = el.getAttribute("alt") || "";
    if (counterEl) {
      counterEl.textContent = index + 1 + " / " + imgs.length;
    }
  }

  function open(atIndex) {
    collect();
    if (!imgs.length) return;
    lightbox.classList.add("is-open");
    lightbox.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    show(atIndex);
    if (btnClose) btnClose.focus();
  }

  function close() {
    lightbox.classList.remove("is-open");
    lightbox.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    lbImg.removeAttribute("src");
  }

  document.addEventListener(
    "click",
    function (e) {
      var t = e.target;
      if (!(t && t.closest)) return;
      if (t.closest(".project-card-cta")) return;
      var img = t.closest && t.closest("img.portfolio-lightbox-img");
      if (!img) return;
      collect();
      var i = imgs.indexOf(img);
      if (i === -1) return;
      e.preventDefault();
      open(i);
    },
    true
  );

  if (btnClose) {
    btnClose.addEventListener("click", close);
  }
  if (btnPrev) {
    btnPrev.addEventListener("click", function () {
      show(index - 1);
    });
  }
  if (btnNext) {
    btnNext.addEventListener("click", function () {
      show(index + 1);
    });
  }

  lightbox.addEventListener("click", function (e) {
    if (e.target === lightbox) close();
  });

  document.addEventListener("keydown", function (e) {
    if (!lightbox.classList.contains("is-open")) return;
    if (e.key === "Escape") {
      close();
    } else if (e.key === "ArrowLeft") {
      show(index - 1);
    } else if (e.key === "ArrowRight") {
      show(index + 1);
    }
  });
})();
