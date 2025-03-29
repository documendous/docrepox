import logging
import os
from shutil import copyfile
from urllib.parse import quote

from django.conf import settings
from django.http import FileResponse

from apps.core.utils.storage import content_file_name
from apps.encrypted_content.utils import get_encrypted_file_handler


def copy_content_file(version, new_version):
    """
    Copies the content file associated with a version to a new version.

    This function takes a `version` object with an associated content file,
    creates a copy of that file for a `new_version` object, and updates the
    `new_version` to reference the copied file. If the destination directory
    does not exist, it is created.

    Parameters:
        version: An object representing the current version, expected to have
                 a `content_file` attribute with a file name and path.
        new_version: An object representing the new version that will receive
                     the copied content file.

    Process:
        1. Verifies if the `version` object has a `content_file`.
        2. Determines the source and new file paths based on `settings.MEDIA_ROOT`.
        3. Creates the destination directory if it does not already exist.
        4. Copies the content file from the source to the destination.
        5. Updates the `new_version` object's `content_file` path.
        6. Saves the `new_version` object to persist the changes.

    Notes:
        - Requires `settings.MEDIA_ROOT` to be configured in the Django project.
        - Uses the `content_file_name` function to generate the new file name.

    Exceptions:
        - Will raise an OSError if there is an issue with file or directory operations.
        - Ensure proper error handling if calling this function in a production environment.

    Example Usage:
        copy_content_file(old_version_instance, new_version_instance)
    """
    log = logging.getLogger(__name__)

    if version.content_file:
        source_file_path = os.path.join(settings.MEDIA_ROOT, version.content_file.name)

        new_file_path = os.path.join(
            settings.MEDIA_ROOT,
            content_file_name(new_version, version.content_file.name),
        )

        destination_dir = os.path.dirname(new_file_path)

        if not os.path.exists(destination_dir):  # pragma: no coverage
            os.makedirs(destination_dir)

        try:
            copyfile(source_file_path, new_file_path)
            new_version.content_file.name = os.path.relpath(
                new_file_path, settings.MEDIA_ROOT
            )
        except FileNotFoundError:  # pragma: no coverage
            log.error(
                "File not found while copying: {source_file_path} to {new_file_path}"
            )

    new_version.save()


def handle_file_response(file_path, file_name, content_type, action):
    if settings.ENCRYPT_CONTENT:  # pragma: no coverage
        file_handler = get_encrypted_file_handler(file_path)
    else:
        file_handler = open(file_path, "rb")

    response = FileResponse(file_handler, content_type=content_type)
    quoted_file_name = quote(file_name)
    response["Content-Disposition"] = f'{action}filename="{quoted_file_name}"'
    response["X-Frame-Options"] = "SAMEORIGIN"
    response["Content-Security-Policy"] = "frame-ancestors 'self';"

    return response
