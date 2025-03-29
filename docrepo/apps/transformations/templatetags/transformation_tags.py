from django import template
from django.conf import settings

from apps.core.utils.core import get_extension

register = template.Library()


@register.simple_tag
def is_previewable(element) -> bool:  # pragma: no coverage
    """
    Return True if element is previewable
    """
    if element.is_document:
        if get_extension(file_name=element.name) in settings.ALLOWED_PREVIEW_TYPES:
            return True

    return False
