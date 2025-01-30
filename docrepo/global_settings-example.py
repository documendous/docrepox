# To use these settings, copy this file to global_settings.py.
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
# Common settings that can be changed for DocrepoX

from config.settings import BASE_DIR

ALLOWED_HOSTS = [
    "localhost",
]

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tz_detect",
    "widget_tweaks",
    "apps.ddocs",
    "apps.core",
    "apps.dashlets",
    "apps.bookmarks",
    "apps.transformations",
    "apps.repo",
    "apps.ui",
    "apps.authentication",
    "apps.projects",
    "apps.clipboard",
    "apps.search",
    "apps.etags",
    "apps.comments",
    "apps.comms",
    "debug_toolbar",
]

# DEBUG = True # With debug turned off Django will not serve static files. Set to False, the production web server (Nginx) will serve them.


# Repo settings

ADMIN_ALLOW_ALL = False  # If set to True, admin user can do everything in system


ADMIN_EMAIL = "admin@localhost"  # DocrepoX admin email (def: "admin@localhost")

AUTO_DELETE_CONTENT_FILES = (
    False  # Delete content files when documents or previews are deleted
)

CREATE_DOC_AS_RTF = True  # When using the create document form (not modal) show the Quill rich text editor Quill docs: https://quilljs.com/docs/quickstart

CREATE_DOC_DEFAULT_MT = "text/plain"  # Default mimetype of hand created documents. The other viable option could be "text/rtf".

DATA_UPLOAD_MAX_NUMBER_FILES = 256  # Max upload of files using multi document upload. Set to None to disable this check.

DEFAULT_DOCUMENT_VERSION = "1.0"  # Default version tag when a new document is created


EDITOR_FONT_SIZE = (
    "16px"  # Quill editor's default font size if CREATE_DOC_USE_MODAL=False
)

ENABLE_DOCUMENT_COMMENTS = True  # Enable comments on document detail views

ENABLE_FOLDER_COMMENTS = True  # Enable comments on folder detail views

ENABLE_PROJECT_COMMENTS = True  # Enable comments on project detail views

ENABLE_PUBLIC_COMMENTS = (
    False  # Enables comments on public project elements (folders & documents)_
)

FOLDER_VIEW_PAGINATE_BY = 10  # Folder view's number of items per page

# Auth settings

LOGIN_REDIRECT_URL = "/repo/"  # After login, the url the user is redirected to

LOGIN_URL = "/auth/login/"  # Default login url

LOGOUT_REDIRECT_URL = "/auth/login/"  # Default logout redirect url

DELETED_ORPHAN_FOLDER = BASE_DIR / "deleted"

UPDATE_MODEL_SUCCESS_MSG = "Your user info was saved."
UPDATE_MODEL_ERROR_MSG = "Unable to save your user info."

# HX-Boost is an HTMX feature. This will redirect and refresh pages without a full page reload

USE_HX_BOOST_EXT = "false"  # Experimental! Use hx-boost for links outside current view - use a string true/false

USE_HX_BOOST_INT = "false"  # Experimental but mostly safe: Use hx-boost for links in current view - use a string true/false

USE_LOCAL_TZ = True  # USE_LOCAL_TZ if set to True will render date times in the browser to the user's local timezone.

TZ_DETECT_COUNTRIES = (
    "US",
    "CN",
    "GB",
    "IN",
    "JP",
    "BR",
    "RU",
    "DE",
    "FR",
)  # If USE_LOCAL_TZ is set to True, tz_detect will try these locale countries in the order set

# TZ_SESSION_KEY = "my-session-key"  # See https://pypi.org/project/django-tz-detect/ for more details


# Clipboard settings

DELETE_CLIPBOARD_ON_LOGOUT = (
    True  # If True, clears a user's clipboard when session ends
)


# Dashlets

USE_MOTD = False  # If True, displays the Message of the Day dashboard


# DDocs

ENABLE_CUSTOMIZATION_TIPS = (
    False  # Enables links to customization docs for specified sections in UI
)


# Locale

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"


# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s.%(funcName)s: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "transformations": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "mozilla_django_oidc": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}


# Security

USE_KEYCLOAK = False


# Tags

MAX_TAG_COUNT = (
    5  # Maxium number of tags allowed for element (document, folder or project)
)


# Transformations

SOFFICE_EXE = (
    "/usr/bin/soffice"  # Path to open/libre/star office executable for transformations
)

SOFFICE_TEMP_DIR = BASE_DIR / "mediafiles/content/tmp"  # Temp dir for soffice

ALLOWED_PREVIEW_TYPES = (
    ".conf",
    ".doc",
    ".docx",
    ".gif",
    ".jpg",
    ".jpeg",
    ".md",
    ".pdf",
    ".png",
    ".ppt",
    ".pptx",
    ".txt",
    ".xls",
    ".xlsx",
    ".xml",
)  # Allowed previewable types

MAX_PREVIEW_SIZE = 10000000  # Max size in bytes allowed for preview transformation

TRANSFORMABLE_TYPES = (
    ".doc",
    ".docx",
    ".md",
    ".ppt",
    ".pptx",
    ".txt",
    ".xls",
    ".xlsx",
)  # Allowed transformable types to PDF


# UI

MAX_CONTENT_ITEM_SIZE = (
    5  # number of items of content (projects or documents) on dashboard
)
