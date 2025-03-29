from django.urls import path

from .views import AcknowledgeCommView, CommListView, DeleteCommView

app_name = "comms"


urlpatterns = [
    path("", CommListView.as_view(), name="comm_list"),
    path(
        "acknowledge/<int:comm_id>/", AcknowledgeCommView.as_view(), name="acknowledge"
    ),
    path("delete/<int:comm_id>/", DeleteCommView.as_view(), name="delete"),
]
