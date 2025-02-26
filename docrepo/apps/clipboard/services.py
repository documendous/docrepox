import logging

from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404

from apps.repo.models.element.folder import Folder

from .models import Clipboard, PastedDocument, PastedFolder
from .utils.paste import change_parent, copy_documents, copy_folders


def delete_clipboard_documents(user):
    clipboard = Clipboard.objects.get(user=user)
    clipboard.documents.all().delete()


def delete_clipboard_folders(user):
    clipboard = Clipboard.objects.get(user=user)
    clipboard.folders.all().delete()


def move_clipboard_elements_to_parent(request, parent_id):
    parent = Folder.objects.get(pk=parent_id)
    clipboard = get_object_or_404(Clipboard, user=request.user)
    change_parent(request, clipboard, parent)


def copy_clipboard_elements_to_parent(request, folder_id):
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


def remove_clipboard_item(item_type, item_id):
    log = logging.getLogger(__name__)

    if item_type == "document":
        Model = PastedDocument
    elif item_type == "folder":
        Model = PastedFolder
    else:  # pragma: no coverage
        raise Http404

    try:
        item = Model.objects.get(pk=item_id)
        item.delete()

    except Model.DoesNotExist as err:  # pragma: no coverage
        log.error(err)
