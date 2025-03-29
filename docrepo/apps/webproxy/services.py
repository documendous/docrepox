from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from apps.repo import rules
from apps.repo.models.element.document import Document
from apps.repo.utils.storage import handle_file_response

from .models import ProxiedDocument


def download_proxied_document(document_id: str) -> FileResponse:
    document = Document.objects.get(pk=document_id)

    proxied_document = get_object_or_404(
        ProxiedDocument, document=document, is_active=True
    )

    version = proxied_document.document.current_version

    content_type = (
        document.mimetype.name
        if hasattr(document.mimetype, "name")
        else settings.DEFAULT_MIMETYPE
    )

    return handle_file_response(
        file_path=version.content_file.path,
        file_name=document.name,
        content_type=content_type,
        action="attachment",
    )


def create_proxied_document(user, document_id):
    document = get_object_or_404(Document, pk=document_id)
    rules.can_retrieve_document(user, document)
    ProxiedDocument.objects.create(document=document, manager=user)


def remove_proxied_document(user, document_id):
    document = get_object_or_404(Document, pk=document_id)
    rules.can_retrieve_document(user, document)
    proxied_document = ProxiedDocument.objects.get(document=document, manager=user)
    proxied_document.delete()
