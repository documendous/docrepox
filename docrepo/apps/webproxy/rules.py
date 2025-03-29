from django.conf import settings

from apps.core.utils.handlers import response_handler


def is_webproxy_share_enabled(from_tag=False):  # pragma: no coverage
    accessible = False

    if settings.WEBPROXY_SHARE_ENABLED:
        accessible = True

    return response_handler(accessible, from_tag)
