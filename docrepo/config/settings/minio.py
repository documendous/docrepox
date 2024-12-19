from config.settings import INSTALLED_APPS
from .utils import env


minio_storage_app = "minio_storage"

if minio_storage_app in INSTALLED_APPS:
    INSTALLED_APPS.remove(minio_storage_app)

staticfiles_index = INSTALLED_APPS.index("django.contrib.staticfiles")
INSTALLED_APPS.insert(staticfiles_index + 1, minio_storage_app)

# Minio

DEFAULT_FILE_STORAGE = "minio_storage.storage.MinioMediaStorage"

MINIO_STORAGE_ENDPOINT = "minio:9000"

MINIO_STORAGE_ACCESS_KEY = env("STORAGE_ACCESS_KEY")

MINIO_STORAGE_SECRET_KEY = env("STORAGE_SECRET_KEY")

MINIO_STORAGE_USE_HTTPS = False

MINIO_STORAGE_MEDIA_OBJECT_METADATA = {"Cache-Control": "max-age=1000"}

MINIO_STORAGE_MEDIA_BUCKET_NAME = env("STORAGE_MEDIA_BUCKET_NAME")

MINIO_STORAGE_MEDIA_BACKUP_BUCKET = "Recycle Bin"

MINIO_STORAGE_MEDIA_BACKUP_FORMAT = "%c/"

MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True

# Following static settings are NOT supported

# STATICFILES_STORAGE = "minio_storage.storage.MinioStaticStorage"

# MINIO_STORAGE_STATIC_BUCKET_NAME = "docrepo"

# MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True
