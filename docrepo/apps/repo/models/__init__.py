import logging

from django.conf import settings

from .element import Document, Folder, Mimetype, Version
from .profile import Profile

log = logging.getLogger(__name__)

if settings.ENABLE_EXTENSIONS:
    try:
        from extensions.apps.repo.models import *
    except ModuleNotFoundError:
        log.warning("Expected module: 'models' in extensions not found")
