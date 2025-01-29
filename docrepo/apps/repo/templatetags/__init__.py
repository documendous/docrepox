import logging

from django.conf import settings

log = logging.getLogger(__name__)

if settings.ENABLE_EXTENSIONS:
    try:
        from extensions.apps.repo.templatetags import *
    except ModuleNotFoundError:
        log.warning("Expected module: 'views' in extensions not found")
