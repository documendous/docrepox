function restoreElementAndRedirect(event, url) {
  let form = event.target.closest("form");
  let formData = new FormData(form);

  fetch(url, {
    method: "POST",
    headers: {
      "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
    },
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      if (confirm("After restore, redirect to restored element's parent folder?")) {
        window.location.href = data.redirect_original;
      } else {
        window.location.href = data.redirect_recycle;
      }
    }
  })
  .catch(error => console.error("Error:", error));
}
