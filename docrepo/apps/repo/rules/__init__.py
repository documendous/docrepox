import logging

from django.conf import settings

from .abilities.comment import *
from .abilities.document import *
from .abilities.element import *
from .abilities.folder import *
from .conditions import *

log = logging.getLogger(__name__)

if settings.ENABLE_EXTENSIONS:
    try:
        from extensions.apps.repo.rules import *
    except ModuleNotFoundError:
        log.warning("Expected module: 'rules' in extensions not found")
