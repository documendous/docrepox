"""
URL configuration for docrepo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path("ddocs/", include("apps.ddocs.urls")),
    path("ui/", include("apps.ui.urls")),
    path("repo/", include("apps.repo.urls")),
    path(
        "",
        RedirectView.as_view(
            url=reverse_lazy("repo:index"),
            permanent=False,
        ),
    ),
]

urlpatterns += [
    path("tz_detect/", include("tz_detect.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path(
        "auth/oidc/", include("mozilla_django_oidc.urls")
    ),  # Uncomment to use Keycloak
]
