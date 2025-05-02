import logging
import os
import pathlib
import re
import uuid
from io import BytesIO

from django.conf import settings

from apps.core.utils.storage import content_file_name
from apps.encrypted_content.utils import get_encrypted_file_handler


def get_encrypted_tmp_file(content_file, content_file_path):  # pragma: no coverage
    log = logging.getLogger(__name__)
    encrypted_file_handler = get_encrypted_file_handler(content_file_path)

    if isinstance(encrypted_file_handler, BytesIO):
        decrypted_file_name = content_file_name(content_file, uuid.uuid4())

        decrypted_file_path = (
            str(settings.MEDIA_ROOT) + os.path.sep + decrypted_file_name
        )

        with open(decrypted_file_path, "wb") as output_file:
            log.debug(f"Writing to file: {decrypted_file_path}")
            output_file.write(encrypted_file_handler.getvalue())

        log.debug(
            f"Decrypted file exists: {pathlib.Path(decrypted_file_path).exists()}"
        )

        content_file_path = str(decrypted_file_path)

        tmp_file = (
            str(settings.SOFFICE_TEMP_DIR)
            + os.path.sep
            + str(decrypted_file_path).split("/")[-1].split(".")[0]
            + ".pdf"
        )

        content_file_path = str(decrypted_file_path)
        remove_content_file = True
        reason_for_removal = "decrypted temp file no longer needed"

        return tmp_file, remove_content_file, reason_for_removal, content_file_path


def get_tmp_file(content_file):  # pragma: no coverage
    tmp_file = (
        str(settings.SOFFICE_TEMP_DIR)
        + os.path.sep
        + str(content_file).split("/")[-1].split(".")[0]
        + ".pdf"
    )

    remove_content_file = False
    reason_for_removal = None

    return tmp_file, remove_content_file, reason_for_removal, None


def sanitize_txt_file(filepath):  # pragma: no coverage
    """
    Replaces problematic characters in a text file that interfere with LibreOffice PDF output.
    - Converts smart quotes to straight quotes
    - Replaces em/en dashes with regular dashes
    - Limits underscore sequences

    Args:
        filepath (str): Path to the text file
    """
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    replacements = {
        "‘": "'",
        "’": "'",
        "“": '"',
        "”": '"',
        "—": "--",
        "–": "-",
    }

    for target, replacement in replacements.items():
        text = text.replace(target, replacement)

    # Replace long underscore sequences with a shorter, consistent one
    text = re.sub(r"_{5,}", "____", text)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
