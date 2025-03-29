import logging
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.models import User

# Classes to override default OIDCAuthenticationBackend (Keycloak authentication)
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class KeycloakOIDCAuthenticationBackend(
    OIDCAuthenticationBackend
):  # pragma: no coverage
    """
    Backend for Keycloak OIDC authentication
    """

    def _get_username(self, claims) -> str:
        """
        Returns username from "preferred_username" for Keycloak user
        """
        log = logging.getLogger(__name__)
        username = claims.get("preferred_username")
        log.debug(f"Username found: {username}")
        return username

    def create_user(self, claims) -> User:
        """Overrides Authentication Backend so that Django users are
        created with the keycloak preferred_username.
        If nothing found matching the email, then try the username.
        """
        log = logging.getLogger(__name__)
        user = super(KeycloakOIDCAuthenticationBackend, self).create_user(claims)
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.email = claims.get("email")
        user.username = self._get_username(claims)
        user.save()
        log.debug(f"User created: {user}")
        return user

    def filter_users_by_claims(self, claims):
        """Return all users matching the specified email.
        If nothing found matching the email, then try the username
        """
        email = claims.get("email")
        preferred_username = claims.get("preferred_username")

        if not email:
            return self.UserModel.objects.none()
        users = self.UserModel.objects.filter(email__iexact=email)

        if len(users) < 1:
            if not preferred_username:
                return self.UserModel.objects.none()
            users = self.UserModel.objects.filter(username__iexact=preferred_username)
        return users

    def update_user(self, user: User, claims) -> User:
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.email = claims.get("email")
        user.username = self._get_username(claims)
        user.save()
        return user


def provider_logout(request) -> str:  # pragma: no coverage
    """Create the user's OIDC logout URL.
    These must have the following settings in settings/oidc.py:
    OIDC_STORE_ACCESS_TOKEN = True
    OIDC_STORE_ID_TOKEN = True
    OIDC_OP_LOGOUT_ENDPOINT = f"{KC_HOST}/realms/{REALM}/protocol/openid-connect/logout"
    OIDC_OP_LOGOUT_URL_METHOD = "apps.repo.auth_backends.provider_logout"
    """
    log = logging.getLogger(__name__)
    oidc_id_token = request.session.get("oidc_id_token", None)

    if oidc_id_token:
        logout_url = (
            settings.OIDC_OP_LOGOUT_ENDPOINT
            + "?"
            + urlencode(
                {
                    "id_token_hint": oidc_id_token,
                    "post_logout_redirect_uri": request.build_absolute_uri(
                        location=settings.LOGOUT_REDIRECT_URL
                    ),
                }
            )
        )
    else:
        logout_url = settings.LOGOUT_REDIRECT_URL

    log.debug(f"logout_url: {logout_url}")

    return logout_url
