from config.settings.utils import BASE_DIR, env

# Admin settings

ADMIN_ALLOW_ALL = False  # If set to True, admin user can do everything in system. Use this for maintenance or emergency only.

ADMIN_USERNAME = env(
    "ADMIN_USERNAME", default="admin"
)  # DocrepoX admin username (def: "admin")

ADMIN_PASSWORD = env(
    "ADMIN_PASSWORD", default="admin"
)  # DocrepoX admin password (def: "admin")

ADMIN_EMAIL = env(
    "ADMIN_EMAIL", default="admin@localhost"
)  # DocrepoX admin email (def: "admin@localhost")

AUTO_DELETE_CONTENT_FILES = (
    False  # Delete content files when documents or previews are deleted
)

CREATE_DOC_USE_MODAL = (
    False  # Use a modal instead of a page to handle creating documents from hand
)

CREATE_DOC_AS_RTF = False  # When using the create document form (not modal) show the Quill rich text editor Quill docs: https://quilljs.com/docs/quickstart Defaults to using plain text edit.

CREATE_DOC_DEFAULT_MT = "text/plain"  # Default mimetype of hand created documents.

DATA_UPLOAD_MAX_NUMBER_FILES = 256  # Max upload of files using multi document upload. Set to None to disable this check.

DEFAULT_DOCUMENT_VERSION = "1.0"  # Default version tag when a new document is created

DEFAULT_MIMETYPE = "application/octet-stream"  # Default mimetype set for new document

DUPLICATE_PEER_MSG = (
    " An item in this folder named '{}' already exists or is a reserved name."
)

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

LOGIN_REDIRECT_URL = "/repo/"  # After login, the url the user is redirected to

LOGIN_URL = "/auth/login/"  # Default login url

LOGOUT_REDIRECT_URL = "/auth/login/"  # Default logout redirect url

MAX_BULK_UPLOAD_FILE_SIZE = 4000 * 1024 * 1024  # Max allowable bulk upload file size

DELETED_ORPHAN_FOLDER = BASE_DIR / "deleted"

UPDATE_MODEL_SUCCESS_MSG = "Your user info was saved."

UPDATE_MODEL_ERROR_MSG = "Unable to save your user info."

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
