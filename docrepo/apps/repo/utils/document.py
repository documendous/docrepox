import logging

from django.core.files.base import ContentFile
from django.db import IntegrityError
from django.utils.datastructures import MultiValueDict

from apps.core.utils.core import get_extension

from ..models.element.document import Document
from ..models.element.mimetype import Mimetype
from ..models.element.version import Version
from ..settings import DEFAULT_MIMETYPE
from ..utils.version import update_version_tag

UPDATEABLE_CONTENT_EXTENSIONS = [".txt", ".csv", ".html"]


def set_mimetype(document, mimetype=None):  # pragma: no coverage
    """
    Sets mimetype for a document
    """
    if mimetype:  # pragma: no coverage
        mimetype = Mimetype.objects.get(name=mimetype)
        document.mimetype = mimetype
    else:
        mimetype_set = Mimetype.objects.filter(
            extension_list__icontains=get_extension(file_name=document.name),
        )
        document.mimetype = (
            mimetype_set.first()
            if mimetype_set
            else Mimetype.objects.get(name=DEFAULT_MIMETYPE)
        )

    document.save()


def create_version(document, content_file, mimetype=None):
    """
    Creates the versioned file for a document
    """
    version = Version()
    version.content_file = content_file
    version.parent = document
    version.save()
    set_mimetype(document, mimetype=mimetype)


def create_document(
    name,
    owner,
    parent,
    content_file,
    title=None,
    description=None,
):  # pragma: no coverage
    log = logging.getLogger(__name__)
    try:
        new_document = Document.objects.create(
            name=name,
            title=title,
            description=description,
            owner=owner,
            parent=parent,
        )
        create_version(new_document, content_file)
        return new_document
    except IntegrityError:  # pragma: no coverage
        log.error(f"This document already exists in this folder: {parent}")
    return None


def update_document_content(
    document: Document, content: str, files: MultiValueDict, change_type: str = "minor"
) -> None:
    content_file = ContentFile(content.encode("utf-8"), name=document.name)
    files_data = files.copy()
    files_data["content_file"] = content_file
    new_version_tag = update_version_tag(change_type, document)

    Version.objects.create(
        parent=document, content_file=content_file, tag=new_version_tag
    )
