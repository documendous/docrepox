from .utils import env
from .apps import INSTALLED_APPS
from .middleware import MIDDLEWARE

# The following should be set in your .env file:
KC_HOST = env("KC_HOST")
REALM = env("KC_REALM")
OIDC_RP_CLIENT_ID = env("KC_CLIENT")
OIDC_RP_CLIENT_SECRET = env("KC_CLIENT_SECRET")

OIDC_RP_SIGN_ALGO = "RS256"

OIDC_OP_AUTHORIZATION_ENDPOINT = (
    f"{KC_HOST}/realms/{REALM}/protocol/openid-connect/auth"
)

OIDC_OP_TOKEN_ENDPOINT = f"{KC_HOST}/realms/{REALM}/protocol/openid-connect/token"

OIDC_OP_USER_ENDPOINT = f"{KC_HOST}/realms/{REALM}/protocol/openid-connect/userinfo"

OIDC_OP_JWKS_ENDPOINT = f"{KC_HOST}/realms/{REALM}/protocol/openid-connect/certs"

OIDC_STORE_ACCESS_TOKEN = True

OIDC_STORE_ID_TOKEN = True

OIDC_OP_LOGOUT_ENDPOINT = f"{KC_HOST}/realms/{REALM}/protocol/openid-connect/logout"

OIDC_OP_LOGOUT_URL_METHOD = "apps.authentication.backends.provider_logout"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "apps.authentication.backends.KeycloakOIDCAuthenticationBackend",
]

INSTALLED_APPS.append("mozilla_django_oidc")

"""
To ensure that users' sessions remain valid even if their OIDC account is disabled, use mozilla_django_oidc.middleware.SessionRefresh middleware to verify the id token's validity during each session.
"""
MIDDLEWARE.append("mozilla_django_oidc.middleware.SessionRefresh")

# The length of time it takes for an id token to expire (def. is 15 min)
OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = 30
