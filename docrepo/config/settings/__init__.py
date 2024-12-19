"""
Django settings for docrepo project.

Generated by 'django-admin startproject' using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from .base import (
    ALLOWED_HOSTS,
    ENABLE_EXTENSIONS,
    ROOT_URLCONF,
    TEMPLATES,
    VERSION,
    WSGI_APPLICATION,
)
from .logging import LOGGING
from .apps import INSTALLED_APPS
from .dashlets import *
from .db import DATABASES
from .debug import DEBUG, ADD_TEST_OBJECTS, ADD_TEST_PROJECTS, DEBUG_TOOLBAR_CONFIG
from .locale import LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ
from .middleware import MIDDLEWARE

# ## Uncomment the following import to use Minio:  # noqa: E266
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

from .security import AUTH_PASSWORD_VALIDATORS, SECRET_KEY, USE_KEYCLOAK
from .storage import (
    STATIC_ROOT,
    STATIC_URL,
    STATICFILES_DIRS,
    MEDIA_ROOT,
    MEDIA_URL,
    DEFAULT_AUTO_FIELD,
)
from .unfold import UNFOLD
from .utils import BASE_DIR
from apps.repo.settings import *
from apps.clipboard.settings import *
from apps.comms.settings import *
from apps.ddocs.settings import *
from apps.etags.settings import *
from apps.transformations.settings import *
from apps.ui.settings import *

if USE_KEYCLOAK:
    from .oidc import *

if ENABLE_EXTENSIONS:
    from extensions.settings import *

# ## Uncomment to use elastic
# from .elastic import *
