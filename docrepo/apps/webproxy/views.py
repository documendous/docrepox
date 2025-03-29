from django.conf import settings
from django.shortcuts import render

from apps.core.utils.paginator import get_paginated_objects
from apps.core.views import View, redirect_to_referer_or_default
from apps.repo.utils.system.object import get_system_root_folder
from apps.webproxy import rules
from apps.webproxy.models import ProxiedDocument

from .services import (
    create_proxied_document,
    download_proxied_document,
    remove_proxied_document,
)


class BaseWebProxyView(View):
    def dispatch(self, request, *args, **kwargs):
        rules.is_webproxy_share_enabled()
        return super().dispatch(request, *args, **kwargs)


class DownloadProxiedDocumentView(BaseWebProxyView):
    def get(self, request, document_id):
        return download_proxied_document(document_id)


class AddProxiedDocumentView(BaseWebProxyView):
    def get(self, request, document_id):
        create_proxied_document(request.user, document_id)
        return redirect_to_referer_or_default(request)


class RemoveProxiedDocumentView(BaseWebProxyView):
    def get(self, request, document_id):
        remove_proxied_document(request.user, document_id)
        return redirect_to_referer_or_default(request)


class ProxiedDocumentListView(BaseWebProxyView):
    def get(self, request):
        proxied_documents = ProxiedDocument.objects.filter(
            manager=request.user
        ).order_by("-created")

        paginated_proxies = get_paginated_objects(
            proxied_documents,
            page=request.GET.get("page", 1),
            paginate_by=settings.FOLDER_VIEW_PAGINATE_BY,
        )

        return render(
            request,
            "webproxy/document_list.html",
            {
                "proxied_documents": paginated_proxies,
                "home_folder_id": request.user.profile.home_folder.id,
                "root_folder_id": get_system_root_folder().id,
            },
        )
