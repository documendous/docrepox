import re

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode

EXEMPT_PATHS = {
    reverse("oidc_authentication_init"),
    reverse("oidc_authentication_callback"),
    reverse("ddocs:index"),
    reverse("ddocs:license"),
}  # Paths not subject to Django auth default authentication

EXEMPT_PATTERNS = {re.compile(r"^/repo/webproxy/document/")}


class LoginRequiredMiddleware:  # pragma: no coverage
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = reverse("login")

        if self._should_redirect_to_login(request, login_url):
            return redirect(
                f"{login_url}?{urlencode({'next': request.get_full_path()})}"
            )

        try:
            response = self.get_response(request)
        except Exception as e:
            return self._handle_exception(request, e)

        if response.status_code == 403 and self._is_csrf_failure(request):
            return redirect(
                f"{login_url}?{urlencode({'csrf_failed': 'true', 'next': request.get_full_path()})}"
            )

        return response

    def _should_redirect_to_login(self, request, login_url):
        """Checks if the request should be redirected to login."""
        if request.path == login_url or request.user.is_authenticated:
            return False

        if request.path in EXEMPT_PATHS:
            return False

        for pattern in EXEMPT_PATTERNS:
            if pattern.search(request.path):
                return False

        return True

    def _is_csrf_failure(self, request):  # pragma: no coverage
        """Checks if the request failed due to a CSRF issue."""
        return getattr(request, "csrf_processing_failed", False)

    def _handle_exception(self, request, exception):
        """Handles unexpected middleware exceptions."""
        login_url = reverse("login")
        return redirect(f"{login_url}?{urlencode({'error': 'unexpected'})}")
