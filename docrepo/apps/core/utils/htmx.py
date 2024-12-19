from django.http import HttpResponse

# See: https://htmx.org/reference/#response_headers for allowed HTMX headers

ALLOWED_HEADERS = {
    "HX-Redirect",  # Redirects the client to a new URL
    "HX-Location",  # Redirects with enhanced behavior like push state
    "HX-Trigger",  # Triggers client-side events
    "HX-Trigger-After-Swap",  # Triggers events after content swapping
    "HX-Trigger-After-Settle",  # Triggers events after settling the DOM
    "HX-Push",  # Pushes a new URL into browser history
    "HX-Refresh",  # Forces a full-page refresh
    "HX-Retarget",  # Changes the target for content insertion
    "HX-Reswap",  # Specifies how content should be swapped
    "HX-Replace-Url",  # Replaces the browser’s current URL
    "Content-Type",  # Specifies the response content type
}


def hx_response(status_code: int = 200, content: str = "", **kwargs) -> HttpResponse:
    """General HTMX response."""
    response = HttpResponse(content=content, status=status_code)
    for k, v in kwargs.items():
        if k in ALLOWED_HEADERS:
            response[k] = v
        else:
            raise ValueError(
                f"Header '{k}' is not allowed. Allowed headers are: {', '.join(ALLOWED_HEADERS)}."
            )

    return response


def htmx_redirect(
    url: str, status_code: int = 200, content: str = "", **kwargs
) -> HttpResponse:
    """Performs an HTMX redirect using response headers."""
    kwargs["HX-Redirect"] = url
    if "Content-Type" not in kwargs:
        kwargs["Content-Type"] = "text/html"
    return hx_response(status_code=status_code, content=content, **kwargs)
