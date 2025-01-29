import logging

from django.conf import settings

from .element import AddDocumentForm, AddFolderForm, AddVersionForm, UpdateElementForm
from .user import UpdateProfileForm, UpdateUserForm

log = logging.getLogger(__name__)

if settings.ENABLE_EXTENSIONS:
    try:
        from extensions.apps.repo.forms import *
    except ModuleNotFoundError:
        log.warning("Expected module: 'forms' in extensions not found")
