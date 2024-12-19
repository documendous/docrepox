import logging
from django.conf import settings


log = logging.getLogger(__name__)


if settings.ENABLE_EXTENSIONS:  # pragma: no coverage
    try:
        from extensions.apps.dashlets.admin import *  # noqa: F403 F401
    except ModuleNotFoundError:
        log.warning("Expected module: 'admin' in extensions not found")
