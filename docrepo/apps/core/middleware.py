from django.shortcuts import redirect
from django.urls import reverse


EXEMPT_PATHS = {
    reverse("oidc_authentication_init"),
    reverse("oidc_authentication_callback"),
    reverse("ddocs:index"),
    reverse("ddocs:license"),
}  # Paths not subject to Django auth default authentication


class LoginRequiredMiddleware:
    def _requirements_met(self):
        return (
            self.request.path not in self.exempt_paths
            and not self.request.user.is_authenticated
        )

    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_paths = EXEMPT_PATHS

    def __call__(self, request):
        # Check if path is in exempt paths or starts with the exempt prefix
        self.request = request
        if self._requirements_met():
            login_url = reverse("login")
            if request.path != login_url:
                return redirect(f"{login_url}?next={request.path}")

        return self.get_response(request)
