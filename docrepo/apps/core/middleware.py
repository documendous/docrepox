from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode

EXEMPT_PATHS = {
    reverse("oidc_authentication_init"),
    reverse("oidc_authentication_callback"),
    reverse("ddocs:index"),
    reverse("ddocs:license"),
}  # Paths not subject to Django auth default authentication


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_paths = EXEMPT_PATHS

    def __call__(self, request):
        self.request = request
        login_url = reverse("login")

        if self._requirements_met() and request.path != login_url:
            return redirect(f"{login_url}?next={request.path}")

        response = self.get_response(request)

        if response.status_code == 403 and self._is_csrf_failure(
            request
        ):  # pragma: no coverage
            return redirect(
                f"{login_url}?{urlencode({'csrf_failed': 'true', 'next': request.path})}"
            )

        return response

    def _requirements_met(self):
        return (
            self.request.path not in self.exempt_paths
            and not self.request.user.is_authenticated
        )

    def _is_csrf_failure(self, request):  # pragma: no coverage
        """
        Checks if the request failed due to a CSRF issue.
        """
        reason = getattr(request, "csrf_processing_failed", False)
        return reason
