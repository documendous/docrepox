import logging
import os
import uuid

from django.conf import settings
from django.utils import timezone


def delete_content_file(instance):  # pragma: no coverage
    """
    Deletes content file for types (instance) that has them
    """
    log = logging.getLogger(__name__)
    if settings.AUTO_DELETE_CONTENT_FILES:
        log.debug("  AUTO_DELETE_CONTENT_FILES is set to True")
        if instance.content_file:
            if os.path.isfile(instance.content_file.path):
                log.debug(
                    "  Deleting Content File: {} from file system".format(
                        instance.content_file.path
                    )
                )
                os.remove(instance.content_file.path)
            else:
                log.warning(
                    "  Content File: {} does not exist and cannot be deleted.".format(
                        instance.content_file.path
                    )
                )


def content_file_name(instance, filename):
    """
    Sets upload destination for content files
    """
    now = timezone.now()
    filename = f"{uuid.uuid4()}"
    return (
        f"content/{now.year}/{now.month}/{now.day}/{now.hour}/{now.minute}/{filename}"
    )
