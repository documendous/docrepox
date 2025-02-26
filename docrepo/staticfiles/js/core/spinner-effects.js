let spinnerTimeout;

document.body.addEventListener("htmx:beforeRequest", function () {
  spinnerTimeout = setTimeout(() => {
    document.getElementById("spinner").style.opacity = "1";
  }, 2000);
});

document.body.addEventListener("htmx:afterRequest", function () {
  clearTimeout(spinnerTimeout);
  document.getElementById("spinner").style.opacity = "0";
});
