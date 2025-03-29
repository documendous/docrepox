import logging

from django.conf import settings
from django.db.models import QuerySet

from .models.element.document import Document


def get_owned_documents(user) -> QuerySet:
    return Document.objects.filter(owner=user).order_by("-created")[
        : settings.MAX_CONTENT_ITEM_SIZE
    ]


log = logging.getLogger(__name__)

try:
    from extensions.apps.repo.querysets import *  # noqa: F403, F401
except ModuleNotFoundError:  # pragma: no coverage
    log.warning("Expected module: 'querysets' in extensions not found")
