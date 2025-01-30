"""
Module for generating PDF and preview files for document versions.

This module contains utility functions to generate a PDF file from a document
version and to create preview files. These utilities are designed to integrate
with LibreOffice and Django models.

Functions:
    - generate_pdf_file(version): Generates a PDF file from a document version.
    - generate_preview_file(version, tmp_file, src_is_content_file): Creates a preview file.
"""

import logging
import os
import pathlib
import subprocess
import uuid

from django.conf import settings
from django.core.files import File

from apps.repo.models.element.version import Version
from apps.transformations.models import Preview


def generate_pdf_file(version: Version) -> None:
    """
    Generate a PDF file for the provided document version.

    This function checks for the LibreOffice executable, validates file size and
    extension, and uses LibreOffice to convert the file to a PDF format if applicable.
    If the file is already a PDF, it directly creates a preview file.

    Args:
        version (Version): The document version for which a PDF file is generated.

    Raises:
        FileNotFoundError: If the LibreOffice executable is not found.

    Warnings:
        - Skips the transformation if the file size exceeds the `MAX_PREVIEW_SIZE`.
        - Skips the transformation if the file extension is not in `ALLOWED_PREVIEW_TYPES`.
    """
    log = logging.getLogger(__name__)

    log.debug("Checking for SOFFICE_EXE install ...")
    if not os.path.isfile(settings.SOFFICE_EXE):
        log.error(f"LibreOffice executable not found at {settings.SOFFICE_EXE}.")
        raise FileNotFoundError(
            f"LibreOffice executable not found at {settings.SOFFICE_EXE}. Transformation with soffice aborted."
        )
    else:
        log.debug(f"{settings.SOFFICE_EXE} found.")

    extension = pathlib.Path(version.parent.name).suffix
    log.debug("File to be used for PDF generation: {}".format(version.content_file))
    log.debug("Document name is: {}".format(version.parent.name))
    log.debug("Logical path: {}".format(version.parent.get_full_path()))
    log.debug("File extension is: {}".format(extension))
    log.debug("File size is: {}".format(version.content_file.size))
    log.debug("SOFFICE path is set to: {}".format(settings.SOFFICE_EXE))

    if version.content_file.size >= settings.MAX_PREVIEW_SIZE:
        log.warning(
            "File: {} size is {}. Max size allowed for preview transformation is: {}. "
            "Preview transform will not be attempted.".format(
                version.content_file,
                version.content_file.size,
                settings.MAX_PREVIEW_SIZE,
            )
        )
        return

    if extension not in settings.ALLOWED_PREVIEW_TYPES:
        log.warning(
            "File: {} does not have an allowed extension type. Preview transform will not be attempted. "
            "Allowed transformations only for extensions: {}".format(
                version.content_file,
                ", ".join(settings.ALLOWED_PREVIEW_TYPES),
            )
        )
        return

    if extension == ".pdf":
        generate_preview_file(
            version,
            str(
                "{}/{}".format(
                    settings.MEDIA_ROOT,
                    version.content_file,
                )
            ),
            src_is_content_file=True,
        )
        return

    log.debug(
        "File: {} has an allowed extension type: {}. Preview transform will be attempted.".format(
            version.content_file, extension
        )
    )
    process = subprocess.Popen(
        [
            settings.SOFFICE_EXE,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            settings.SOFFICE_TEMP_DIR,
            f"{str(settings.MEDIA_ROOT) + os.path.sep + str(version.content_file)}",
        ],
    )

    full_command = (
        " ".join([str(arg) for arg in process.args])
        if isinstance(process.args, (list, tuple))
        else str(process.args)
    )
    log.debug("Using command for transform: {}".format(full_command))
    process.communicate()

    tmp_file = (
        str(settings.SOFFICE_TEMP_DIR)
        + os.path.sep
        + str(version.content_file).split("/")[-1].split(".")[0]
        + ".pdf"
    )
    log.debug("Temp file for upload is {}".format(tmp_file))
    generate_preview_file(version, tmp_file)


def generate_preview_file(
    version: Version, tmp_file: str, src_is_content_file: bool = False
) -> bool:
    """
    Generate a preview file from the given temporary file.

    This function creates a preview file for the specified document version. It saves
    the preview file as a binary file and removes the temporary file upon success.

    Args:
        version (Version): The document version for which a preview is created.
        tmp_file (str): Path to the temporary file to use for generating the preview.
        src_is_content_file (bool, optional): Indicates whether the source is the content file.

    Returns:
        bool: True if the preview file was created successfully, False otherwise.

    Raises:
        FileNotFoundError: If the temporary file does not exist.
    """
    log = logging.getLogger(__name__)
    try:
        log.debug("Generating preview file from {}".format(tmp_file))
        with open(tmp_file, "rb") as local_file:
            djangofile = File(local_file)
            preview_content_file = str(uuid.uuid4()) + ".bin"
            preview = Preview()
            preview.version = version
            log.debug(
                f"Attempting to save preview content file: {preview_content_file}"
            )
            preview.content_file.save(preview_content_file, djangofile)
            preview.save()
            log.debug("Preview content file saved.")

        log.debug(
            "Preview file creation successful. Removing temp file: {}".format(tmp_file)
        )
        if not src_is_content_file:
            os.remove(tmp_file)
        return True
    except FileNotFoundError as err:
        log.error(repr(err))
        log.error("Logging error to content file: {}".format(version.id))
        version.is_indexed = True
        version.index_error = "Error: {}".format(repr(err))
        version.save()
        return False
