from django.urls import path
from django.views.generic.base import TemplateView

app_name = "ddocs"


urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="ddocs/index.html"),
        name="index",
    ),
    path(
        "license/",
        TemplateView.as_view(template_name="ddocs/license.html"),
        name="license",
    ),
]
