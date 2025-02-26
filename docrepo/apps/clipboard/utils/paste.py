import logging

from django.contrib import messages
from django.db import IntegrityError
from django.forms import ValidationError
from django.http import HttpRequest
from django.template.defaultfilters import truncatechars

from apps.repo import rules
from apps.repo.models.element.document import Document
from apps.repo.models.element.folder import Folder
from apps.repo.models.element.version import Version
from apps.repo.utils.helpers import create_with_new_name
from apps.repo.utils.storage import copy_content_file

from ..models import Clipboard, PastedDocument, PastedFolder


def change_parent(request: HttpRequest, clipboard: Clipboard, parent: Folder) -> None:
    """
    Used to "move" an element
    """
    for p_document in clipboard.documents.all():
        rules.can_move_element(request, p_document.document)
        p_document.document.parent = parent

        try:
            p_document.document.save()
        except IntegrityError:  # pragma: no coverage
            versions = Version.objects.filter(parent=p_document.document)

            new_document = create_with_new_name(
                "document",
                p_document.document.name,
                p_document.document.owner,
                parent,
                set_pk_none=True,
            )

            for version in versions:
                new_version = version
                new_version.pk = None
                new_version.parent = new_document

                copy_content_file(version, new_version)

            p_document.document.delete()

        p_document.delete()

    for p_folder in clipboard.folders.all():
        rules.can_move_element(request, p_folder.folder)
        p_folder.folder.parent = parent

        try:
            p_folder.folder.save()

        except ValidationError:
            messages.error(
                request,
                f"Invalid move for folder '{truncatechars(p_folder.folder.name, 30)}'",
            )
            return
        except IntegrityError:  # pragma: no coverage
            create_with_new_name(
                "folder",
                p_folder.folder.name,
                p_folder.folder.owner,
                parent,
                set_pk_none=True,
            )

        p_folder.delete()

    messages.info(request, "Item(s) moved to new parent folder")


def copy_documents(request: HttpRequest, clipboard: Clipboard, parent: Folder) -> None:
    """
    Deep copies a document and sets each one's parent to 'parent'.
    """
    for pasted_document in clipboard.documents.all():
        rules.can_move_element(request, pasted_document.document)
        document = pasted_document.document
        _copy_document(document, parent)
        pasted_document.delete()


def copy_folders(request: HttpRequest, clipboard: Clipboard, parent: Folder) -> None:
    """
    Copies a document and sets each one's parent to 'parent'. Does not copy children
    """
    for pasted_folder in clipboard.folders.all():
        rules.can_move_element(request, pasted_folder.folder)
        folder = pasted_folder.folder
        _copy_folder(request, folder, parent)
        pasted_folder.delete()


def add_to_folders(
    request: HttpRequest, clipboard: Clipboard, pasted_element: Document | Folder
) -> None:
    """
    Add a folder to a user's clipboard
    """
    rules.can_add_element_to_clipboard(request, pasted_element.folder)
    if not clipboard.folders.filter(pk=pasted_element.pk).exists():
        clipboard.folders.add(pasted_element)

        messages.info(
            request,
            f'Folder "{truncatechars(pasted_element.folder.name, 30)}" was added to your clipboard.',
        )

    else:
        messages.warning(
            request,
            "This item already exists in your clipboard.",
        )


def add_to_documents(
    request: HttpRequest, clipboard: Clipboard, pasted_element: Document | Folder
) -> None:
    """
    Add a document to a user's clipboard
    """
    rules.can_add_element_to_clipboard(request, pasted_element.document)

    if not clipboard.documents.filter(pk=pasted_element.pk).exists():
        clipboard.documents.add(pasted_element)
        messages.info(
            request,
            f'Document "{truncatechars(pasted_element.document.name, 30)}" was added to your clipboard.',
        )
    else:
        messages.warning(
            request,
            "This item already exists in your clipboard.",
        )


def add_to_clipboard(request, clipboard, element):
    log = logging.getLogger(__name__)

    if element.type == "folder":
        element = Folder.objects.get(pk=element.id)

        pasted_element, _ = PastedFolder.objects.get_or_create(
            folder=element,
        )

        add_to_folders(request, clipboard, pasted_element)

    elif element.type == "document":
        element = Document.objects.get(pk=element.id)

        pasted_element, _ = PastedDocument.objects.get_or_create(
            document=element,
        )

        add_to_documents(request, clipboard, pasted_element)

    else:  # pragma: no coverage
        log.error(f"Invalid element type: {element.type}")

        return False

    return True


def _copy_document(document: Document, parent: Folder) -> None:
    """
    Make a deep copy of a document (new version)
    """
    versions = Version.objects.filter(parent=document)
    new_document = document
    new_document.pk = None
    new_document.parent = parent

    try:
        new_document.save()
    except IntegrityError:  # pragma: no coverage
        new_document = create_with_new_name(
            "document",
            document.name,
            document.owner,
            parent,
            set_pk_none=True,
        )

    for version in versions:
        new_version = version
        new_version.pk = None
        new_version.parent = new_document
        copy_content_file(version, new_version)


def _copy_folder(request, folder: Folder, parent: Folder) -> None:
    """
    Copy of a single folder
    """
    log = logging.getLogger(__name__)

    if folder == parent:
        error_msg = "Cannot copy a folder to same folder"
        messages.error(request, error_msg)
        log.error(error_msg)
        raise Exception(error_msg)

    child_documents = folder.get_child_documents()
    child_folders = folder.get_child_folders()
    new_folder = folder
    new_folder.pk = None
    new_folder.parent = parent

    try:
        new_folder.save()
    except IntegrityError:  # pragma: no coverage
        new_folder = create_with_new_name(
            "folder",
            folder.name,
            folder.owner,
            parent,
            set_pk_none=True,
        )

    for child_document in child_documents:
        _copy_document(child_document, new_folder)

    for child_folder in child_folders:
        _copy_folder(request, child_folder, new_folder)
