import os

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def is_previewable(element) -> bool:  # pragma: no coverage
    """
    Return True if element is previewable
    """
    if element.is_document:
        _, ext = os.path.splitext(element.name)

        if ext in settings.ALLOWED_PREVIEW_TYPES:
            return True

    return False
