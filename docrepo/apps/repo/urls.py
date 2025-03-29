import logging

from django.urls import include, path

from .views import (
    AddDocumentView,
    AddMultiDocumentsView,
    AddVersionView,
    CreateDocumentView,
    DeleteElementView,
    ElementDetailsView,
    FolderView,
    IndexView,
    RecycleElementsView,
    RecycleElementView,
    RestoreElementView,
    UpdateProfileView,
)
from .views.document.retrieve import DocumentRetrieverView
from .views.document.update_content import UpdateDocumentContentView
from .views.element.recycle import EmptyRecycleFolderView
from .views.element.recycle.restore import RestoreElementsView
from .views.element.update import UpdateElementDetailsView

app_name = "repo"


urlpatterns = [
    path(
        "",
        IndexView.as_view(),
        name="index",
    ),
    path("avatars/", include("apps.avatars.urls")),
    path("bookmarks/", include("apps.bookmarks.urls")),
    path("clipboard/", include("apps.clipboard.urls")),
    path("comments/", include("apps.comments.urls")),
    path("comms/", include("apps.comms.urls")),
    path("projects/", include("apps.projects.urls")),
    path("properties/", include("apps.properties.urls")),
    path("search/", include("apps.search.urls")),
    path("webproxy/", include("apps.webproxy.urls")),
    path(
        "folder/<uuid:folder_id>/",
        FolderView.as_view(),
        name="folder",
    ),
    path(
        "folder/<uuid:folder_id>/document/add/",
        AddDocumentView.as_view(),
        name="add_document",
    ),
    path(
        "folder/<uuid:folder_id>/documents/add/",
        AddMultiDocumentsView.as_view(),
        name="add_multi_documents",
    ),
    path(
        "document/<uuid:document_id>/version/add/",
        AddVersionView.as_view(),
        name="add_version",
    ),
    path(
        "folder/<uuid:folder_id>/document/create/",
        CreateDocumentView.as_view(),
        name="create_document",
    ),
    path(
        "element/<str:element_type>/<uuid:element_id>/recycle/",
        RecycleElementView.as_view(),
        name="recycle_element",
    ),
    path(
        "element/recycle/<uuid:parent_id>/children/",
        RecycleElementsView.as_view(),
        name="recycle_elements",
    ),
    path(
        "element/<str:element_type>/<uuid:element_id>/restore/",
        RestoreElementView.as_view(),
        name="restore_element",
    ),
    path(
        "element/<uuid:parent_id>/restore/",
        RestoreElementsView.as_view(),
        name="restore_elements",
    ),
    path(
        "element/<str:element_type>/<uuid:element_id>/delete/",
        DeleteElementView.as_view(),
        name="delete_element",
    ),
    path(
        "trashcan/<uuid:folder_id>/empty/",
        EmptyRecycleFolderView.as_view(),
        name="empty_recycle_folder",
    ),
    path(
        "document/<uuid:document_id>/retrieve/",
        DocumentRetrieverView.as_view(),
        name="retrieve_document",
    ),
    path(
        "profile/update/",
        UpdateProfileView.as_view(),
        name="update_profile",
    ),
    path(
        "<str:element_type>/<uuid:element_id>/details/",
        ElementDetailsView.as_view(),
        name="element_details",
    ),
    path(
        "<str:element_type>/<uuid:element_id>/update/",
        UpdateElementDetailsView.as_view(),
        name="update_element",
    ),
    path(
        "document/content/<uuid:document_id>/update/",
        UpdateDocumentContentView.as_view(),
        name="update_document_content",
    ),
]


log = logging.getLogger(__name__)

try:
    from extensions.apps.repo.urls import *  # noqa: F403, F401
except ModuleNotFoundError:  # pragma: no coverage
    log.warning("Expected module: 'urls' in extensions not found")
