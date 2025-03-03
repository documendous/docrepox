"""
Django settings for docrepo project.

Generated by 'django-admin startproject' using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import logging as py_logging

from apps.clipboard.settings import *
from apps.comms.settings import *
from apps.ddocs.settings import *
from apps.etags.settings import *

# DocrepoX settings
from apps.repo.settings import *
from apps.transformations.settings import *
from apps.ui.settings import *

from .admin import JAZZMIN_SETTINGS
from .apps import INSTALLED_APPS

# Expected Django Settings - explicitly loaded
from .base import (
    ALLOWED_HOSTS,
    ENABLE_EXTENSIONS,
    ROOT_URLCONF,
    TEMPLATES,
    VERSION,
    WSGI_APPLICATION,
)
from .dashlets import *
from .db import DATABASES
from .debug import ADD_TEST_OBJECTS, ADD_TEST_PROJECTS, DEBUG, DEBUG_TOOLBAR_CONFIG
from .locale import LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ
from .logging import LOGGING
from .middleware import MIDDLEWARE
from .security import AUTH_PASSWORD_VALIDATORS, SECRET_KEY, USE_KEYCLOAK
from .storage import (
    DEFAULT_AUTO_FIELD,
    MEDIA_ROOT,
    MEDIA_URL,
    STATIC_ROOT,
    STATIC_URL,
    STATICFILES_DIRS,
)
from .utils import BASE_DIR

# ## Uncomment to use elastic
# from .elastic import *

# ## Uncomment the following import to use Minio:  # noqa: E266
# Read the DocrepoX docs MinIO section before using!
# from .minio import (  # noqa: F811
#     INSTALLED_APPS,
#     DEFAULT_FILE_STORAGE,
#     MINIO_STORAGE_ENDPOINT,
#     MINIO_STORAGE_ACCESS_KEY,
#     MINIO_STORAGE_SECRET_KEY,
#     MINIO_STORAGE_USE_HTTPS,
#     MINIO_STORAGE_MEDIA_BUCKET_NAME,
#     MINIO_STORAGE_MEDIA_BACKUP_BUCKET,
#     MINIO_STORAGE_MEDIA_BACKUP_FORMAT,
#     MINIO_STORAGE_MEDIA_OBJECT_METADATA,
#     MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET,
# )


# ========================================
# This must remain last:
# ========================================
# This loads all settings from docrepo/global_settings.py
# These settings will override all of the above.
# If it does not load last, your overrides may not take effect.
# A git pull style upgrade/update will not overwrite your global_settings.py

log = py_logging.getLogger(__name__)
try:
    from global_settings import *
except ModuleNotFoundError:
    log.info("Optional global settings module not found.")

if USE_KEYCLOAK:
    from .oidc import *

if ENABLE_EXTENSIONS:
    _enable_extensions = ENABLE_EXTENSIONS  # Save the local value

    from extensions.settings import *

    ENABLE_EXTENSIONS = _enable_extensions  # Restore the local value

    TEMPLATES[0]["DIRS"].append(BASE_DIR / "extensions/templates")
