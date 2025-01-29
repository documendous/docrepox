from django.urls import path

from .views import AddBookmarkView, BookmarkListView, RemoveBookmarkView

app_name = "bookmarks"


urlpatterns = [
    path(
        "",
        BookmarkListView.as_view(),
        name="bookmark_list",
    ),
    path(
        "<str:element_type>/<uuid:element_pk>/add/",
        AddBookmarkView.as_view(),
        name="set_bookmark",
    ),
    path(
        "<str:element_type>/<uuid:element_pk>/remove/",
        RemoveBookmarkView.as_view(),
        name="remove_bookmark",
    ),
]
