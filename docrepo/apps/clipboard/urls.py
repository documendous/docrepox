from django.urls import path

from .views import (
    AddElementClipboardView,
    PasteCopyElementsView,
    PasteMoveElementsView,
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
]
