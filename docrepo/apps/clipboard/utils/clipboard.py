import logging

from django.contrib.auth.models import User

from apps.core.models import Element
from apps.repo.models.element.document import Document
from apps.repo.models.element.folder import Folder

from ..models import Clipboard, PastedDocument, PastedFolder


def is_in_clipboard(user: User, element: Element) -> bool:
    log = logging.getLogger(__name__)

    try:
        clipboard = Clipboard.objects.get(user=user)
    except Clipboard.DoesNotExist:
        return False

    if isinstance(element, Document):
        return clipboard.documents.filter(document=element).exists()

    elif isinstance(element, Folder):
        return clipboard.folders.filter(folder=element).exists()

    else:
        log.warning(
            f"Element {element} not found in clipboard of {user}"
        )  # pragma: no coverage

    return False  # pragma: no coverage


def remove_from_clipboard(user: User, element: Element) -> None:
    log = logging.getLogger(__name__)

    try:
        clipboard = Clipboard.objects.get(user=user)
    except Clipboard.DoesNotExist:  # pragma: no coverage
        return None

    if isinstance(element, Document):
        pasted_document = PastedDocument.objects.get(document=element)
        clipboard.documents.remove(pasted_document)
        log.debug(f"Element {element} removed from clipboard of {user}")

    elif isinstance(element, Folder):
        pasted_folder = PastedFolder.objects.get(folder=element)
        clipboard.folders.remove(pasted_folder)
        log.debug(f"Element {element} removed from clipboard of {user}")

    else:
        log.error(
            f"Invalid element {element} not removed from clipboard"
        )  # pragma: no coverage

    clipboard.save()
