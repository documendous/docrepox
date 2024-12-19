from django.urls import path
from .views import SearchElementsView, SearchProjectsView


app_name = "search"

urlpatterns = [
    path("projects/", SearchProjectsView.as_view(), name="search_projects"),
    path(
        "elements/<uuid:folder_id>/",
        SearchElementsView.as_view(),
        name="search_elements",
    ),
]
