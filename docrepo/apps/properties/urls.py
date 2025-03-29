from django.urls import path

from .views import (
    AddElementPropertiesView,
    DeleteElementPropertyView,
    UpdateElementPropertyView,
)

app_name = "properties"


urlpatterns = [
    path(
        "<str:element_type>/<uuid:element_id>/update/",
        AddElementPropertiesView.as_view(),
        name="add_properties",
    ),
    path(
        "<int:property_id>/delete/",
        DeleteElementPropertyView.as_view(),
        name="delete_property",
    ),
    path(
        "<int:property_id>/update/",
        UpdateElementPropertyView.as_view(),
        name="update_property",
    ),
]
