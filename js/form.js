(function () {
  "use strict";

  if (window.location.search.indexOf("success=true") !== -1) {
    var el = document.getElementById("successMsg");
    if (el) el.style.display = "block";
  }

  var forms = document.querySelectorAll('form[data-web3forms="true"]');
  forms.forEach(function (form) {
    form.addEventListener("submit", function (e) {
      var keyInput = form.querySelector('input[name="access_key"]');
      if (
        keyInput &&
        keyInput.value &&
        keyInput.value.indexOf("YOUR_ACCESS_KEY") !== -1
      ) {
        e.preventDefault();
        alert(
          "Please set your Web3Forms access key: replace YOUR_ACCESS_KEY in the form (see https://web3forms.com)."
        );
      }
    });
  });
})();
