import logging
from io import BytesIO
from pathlib import Path

from cryptography.fernet import Fernet
from django.conf import settings


def get_encrypted_file_handler(file_path: Path | str):  # pragma: no coverage
    log = logging.getLogger(__name__)
    log.debug("Preparing decrypt of document")

    cipher = Fernet(settings.ENCRYPTION_KEY)

    with open(file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()

    try:
        decrypted_data = cipher.decrypt(encrypted_data)
        log.debug("Decryption successful")
    except Exception as err:
        log.error(f"Decryption failed: {err}")

        return None

    return BytesIO(decrypted_data)
