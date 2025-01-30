import logging

from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from apps.clipboard.utils.paste import (
    add_to_documents,
    add_to_folders,
    change_parent,
    copy_documents,
    copy_folders,
)
from apps.core.views import View
from apps.repo.models.element.document import Document
from apps.repo.models.element.folder import Folder

from .models import Clipboard, PastedDocument, PastedFolder


class PasteMoveElementsView(View):

    def post(self, request, folder_id):
        """
        View that moves a folder or document to another parent folder
        """
        parent = Folder.objects.get(pk=folder_id)
        clipboard = get_object_or_404(Clipboard, user=request.user)
        change_parent(request, clipboard, parent)

        return HttpResponseRedirect(
            reverse(
                "repo:folder",
                args=[
                    parent.pk,
                ],
            )
        )


class PasteCopyElementsView(View):
    def post(self, request, folder_id):
        """
        View that deep copies (sub folders and documents including version but not renditions) a folder or document to another parent folder
        """
        log = logging.getLogger(__name__)
        parent = Folder.objects.get(pk=folder_id)
        clipboard = get_object_or_404(Clipboard, user=request.user)

        try:
            copy_documents(request, clipboard, parent)
            copy_folders(request, clipboard, parent)
            messages.info(request, "Item(s) copied to new parent folder")
        except Exception as err:
            messages.error(request, "Unable to copy item(s) to new parent folder")
            log.error(err)

        return HttpResponseRedirect(
            reverse(
                "repo:folder",
                args=[
                    parent.pk,
                ],
            )
        )


class AddElementClipboardView(View):
    def post(self, request, element_type, element_id):
        """
        View that puts folder or document into user's clipboard
        """
        log = logging.getLogger(__name__)
        clipboard, _ = Clipboard.objects.get_or_create(user=request.user)
        page_number = int(request.GET.get("page", 1))

        if element_type == "folder":
            element = Folder.objects.get(pk=element_id)
            pasted_element, _ = PastedFolder.objects.get_or_create(
                folder=element,
            )
            add_to_folders(request, clipboard, pasted_element)

        elif element_type == "document":
            element = Document.objects.get(pk=element_id)
            pasted_element, _ = PastedDocument.objects.get_or_create(
                document=element,
            )
            add_to_documents(request, clipboard, pasted_element)

        else:  # pragma: no coverage
            log.error(f"Invalid element type: {element_type}")
            raise Http404

        url = reverse(
            "repo:folder",
            args=[element.parent.pk],
        )

        if page_number > 1:  # pragma: no coverage
            url += f"?page={page_number}"

        return HttpResponseRedirect(url)


class RemoveItemView(View):
    """
    Removes a document or folder from a user's active clipboard
    """

    def post(self, request, item_type, item_id):  # pragma: no coverage
        """
        View to remove document or folder from clipboard
        """
        if item_type == "document":
            Model = PastedDocument
        elif item_type == "folder":
            Model = PastedFolder
        else:
            raise Http404

        item = Model.objects.get(pk=item_id)
        item.delete()
        return HttpResponse("")
