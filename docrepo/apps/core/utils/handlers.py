from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404


def response_handler(accessible, from_tag):  # pragma: no coverage
    if accessible:
        return True

    else:
        if from_tag:
            return False

        if settings.DEBUG:
            raise PermissionDenied
        else:
            raise Http404
