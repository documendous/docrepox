# To use these settings, copy this file to global_settings.py.
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
# Below are common and sane settings that can be changed for DocrepoX

ALLOWED_HOSTS = [
    "localhost",
]

# DEBUG = True # With debug turned off Django will not serve static files. Set to False, the production web server (Nginx) will serve them.

# Repo settings (see repo/settings.py for more settings)

ADMIN_EMAIL = "admin@localhost"  # DocrepoX admin email (def: "admin@localhost")

# See 'Auto-Deleting Previews' and 'Managing Orphaned Content Files' in docs for more info.
AUTO_DELETE_CONTENT_FILES = (
    False  # Delete content files when documents or previews are deleted
)

DATA_UPLOAD_MAX_NUMBER_FILES = 256  # Max upload of files using multi document upload. Set to None to disable this check.


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
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",  # Suppress all root-level logs unless warning or higher
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",  # Suppress general Django logs
            "propagate": False,
        },
        # "apps.authentication": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # "apps.avatars": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # "apps.bookmarks": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # "apps.clipboard": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # "apps.comments": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # "apps.comms": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # "apps.core": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # "apps.dashlets": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # "apps.ddocs": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # "apps.encrypted_content": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # "apps.etags": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # "apps.projects": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # "apps.properties": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # "apps.repo": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # "apps.search": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # "apps.transformations": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # "apps.ui": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # "apps.webproxy": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",
        #     "propagate": False,
        # },
        # Ensure all other apps are not logging by default
        "apps": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
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
