import logging

from config.settings import ENABLE_EXTENSIONS

from .document import AddDocumentView, AddMultiDocumentsView, CreateDocumentView
from .element import (
    DeleteElementView,
    ElementDetailsView,
    RecycleElementsView,
    RecycleElementView,
    RestoreElementView,
    UpdateElementDetailsView,
)
from .folder import FolderView
from .index import IndexView
from .profile import UpdateProfileView
from .version import AddVersionView

log = logging.getLogger(__name__)

if ENABLE_EXTENSIONS:
    try:
        from extensions.apps.repo.views import *
    except ModuleNotFoundError:
        log.warning("Expected module: 'views' in extensions not found")
