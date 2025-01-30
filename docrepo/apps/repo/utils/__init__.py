import logging

from django.conf import settings

log = logging.getLogger(__name__)

if settings.ENABLE_EXTENSIONS:
    try:
        from extensions.apps.repo.utils import *
    except ModuleNotFoundError:
        log.warning("Expected module: 'utils' in extensions not found")
