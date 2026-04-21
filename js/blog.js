(function () {
  var buttons = document.querySelectorAll("[data-blog-filter]");
  var cards = document.querySelectorAll("[data-blog-category]");
  if (!buttons.length || !cards.length) return;
  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var cat = btn.getAttribute("data-blog-filter") || "all";
      buttons.forEach(function (b) {
        b.classList.toggle("active", b === btn);
      });
      cards.forEach(function (card) {
        var c = card.getAttribute("data-blog-category") || "";
        var show = cat === "all" || c === cat;
        card.style.display = show ? "" : "none";
      });
    });
  });
})();
