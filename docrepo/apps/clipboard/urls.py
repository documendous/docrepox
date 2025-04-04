from django.urls import path

from .views import (
    AddElementClipboardView,
    AddElementsClipboardView,
    PasteCopyElementsView,
    PasteMoveElementsView,
    RemoveDocumentsView,
    RemoveFoldersView,
    RemoveItemView,
)

app_name = "clipboard"


urlpatterns = [
    path(
        "<str:element_type>/<uuid:element_id>/add/",
        AddElementClipboardView.as_view(),
        name="add_element_to_clipboard",
    ),
    path(
        "<uuid:parent_id>/add/",
        AddElementsClipboardView.as_view(),
        name="add_elements_to_clipboard",
    ),
    path(
        "folder/<uuid:folder_id>/paste/move/",
        PasteMoveElementsView.as_view(),
        name="paste_move_elements",
    ),
    path(
        "folder/<uuid:folder_id>/paste/copy/",
        PasteCopyElementsView.as_view(),
        name="paste_copy_elements",
    ),
    path(
        "item/<str:item_type>/<int:item_id>/remove/",
        RemoveItemView.as_view(),
        name="remove_item",
    ),
    path(
        "documents/remove/",
        RemoveDocumentsView.as_view(),
        name="remove_documents",
    ),
    path(
        "folders/remove/",
        RemoveFoldersView.as_view(),
        name="remove_folders",
    ),
]
