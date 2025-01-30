from django.urls import path

from .views import ModifySettingsView

app_name = "ui"


urlpatterns = [
    path(
        "settings/modify/<str:key>/<str:value>/",
        ModifySettingsView.as_view(),
        name="modify_setting",
    )
]
