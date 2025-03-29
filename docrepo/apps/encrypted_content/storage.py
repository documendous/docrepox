import logging
from io import BytesIO

from cryptography.fernet import Fernet
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

cipher = Fernet(settings.ENCRYPTION_KEY)


class EncryptedFileSystemStorage(FileSystemStorage):
    """Custom storage that encrypts files before saving and decrypts them on retrieval."""

    def _save(self, name, content):
        """Encrypts file content before saving."""
        log = logging.getLogger(__name__)

        log.debug("Encrypting content")
        encrypted_content = cipher.encrypt(content.read())
        encrypted_name = f"{name}.enc"

        log.debug("Saving encrypted content")
        return super()._save(encrypted_name, ContentFile(encrypted_content))

    def _open(self, name, mode="rb"):  # pragma: no coverage
        """Decrypts file content when retrieved."""
        log = logging.getLogger(__name__)

        if not name.endswith(".enc"):
            raise ValueError("Invalid encrypted file format.")

        log.debug("Reading encrypted file")
        encrypted_file = super()._open(name, mode)
        encrypted_data = encrypted_file.read()

        log.debug("Decrypting content")
        decrypted_data = cipher.decrypt(encrypted_data)

        return BytesIO(decrypted_data)
