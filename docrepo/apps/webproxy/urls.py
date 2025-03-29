from django.urls import path

from .views import (
    AddProxiedDocumentView,
    DownloadProxiedDocumentView,
    ProxiedDocumentListView,
    RemoveProxiedDocumentView,
)

app_name = "webproxy"


urlpatterns = [
    path(
        "document/<uuid:document_id>/",
        DownloadProxiedDocumentView.as_view(),
        name="download_proxied_document",
    ),
    path(
        "document/<uuid:document_id>/add/",
        AddProxiedDocumentView.as_view(),
        name="add_webproxy_document",
    ),
    path(
        "document/<uuid:document_id>/remove/",
        RemoveProxiedDocumentView.as_view(),
        name="remove_webproxy_document",
    ),
    path(
        "documents/",
        ProxiedDocumentListView.as_view(),
        name="proxied_document_list",
    ),
]
