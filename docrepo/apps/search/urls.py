from django.urls import path

from .views import AdvancedSearchView, SearchElementsView, SearchProjectsView

app_name = "search"


urlpatterns = [
    path("projects/", SearchProjectsView.as_view(), name="search_projects"),
    path(
        "elements/<uuid:folder_id>/",
        SearchElementsView.as_view(),
        name="search_elements",
    ),
    path("advanced/", AdvancedSearchView.as_view(), name="advanced_search"),
]
