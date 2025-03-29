from config.settings.utils import env

DEFAULT_FILE_STORAGE = "apps.encrypted_content.storage.EncryptedFileSystemStorage"

ENCRYPTION_KEY = env("ENCRYPTION_KEY")

"""
How to obtain encryption key: ./manage.py simple_genkey
"""
