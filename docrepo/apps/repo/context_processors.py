import logging

from django.conf import settings


def global_settings(request):
    keycloak_is_available = (
        "apps.authentication.backends.KeycloakOIDCAuthenticationBackend"
        in settings.AUTHENTICATION_BACKENDS
    )
    return {
        "use_local_tz": settings.USE_LOCAL_TZ,
        "keycloak_is_available": keycloak_is_available,
        "customization_tips_enabled": settings.ENABLE_CUSTOMIZATION_TIPS,
        "app_version": settings.VERSION,
        "support_url": settings.SUPPORT_URL,
    }


log = logging.getLogger(__name__)

try:
    from extensions.apps.repo.context_processors import *  # noqa: F403, F401
except ModuleNotFoundError:  # pragma: no coverage
    log.warning("Expected module: 'context_processors' in extensions not found")
