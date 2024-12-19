import logging

from django.conf import settings
from .keycloak import KeycloakOIDCAuthenticationBackend, provider_logout

log = logging.getLogger(__name__)

if settings.ENABLE_EXTENSIONS:
    try:
        from extensions.apps.authentication.backends.keycloak import *
    except ModuleNotFoundError:
        log.warning("Expected module: 'backends' in extensions not found")
