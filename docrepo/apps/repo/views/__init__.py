import logging
from django.conf import settings
from .document import (
    AddDocumentView,
    CreateDocumentView,
    AddMultiDocumentsView,
)
from .version import AddVersionView
from .element import (
    ElementDetailsView,
    UpdateElementDetailsView,
    RecycleElementView,
    RestoreElementView,
    DeleteElementView,
)
from .folder import FolderView
from .index import IndexView
from .profile import UpdateProfileView


log = logging.getLogger(__name__)

if settings.ENABLE_EXTENSIONS:
    try:
        from extensions.apps.repo.views import *
    except ModuleNotFoundError:
        log.warning("Expected module: 'views' in extensions not found")
