import logging
from django.conf import settings


log = logging.getLogger(__name__)


if settings.ENABLE_EXTENSIONS:
    try:
        from extensions.apps.dashlets.forms import *  # noqa: F403 F401
    except ModuleNotFoundError:
        log.warning("Expected module: 'forms' in extensions not found")
