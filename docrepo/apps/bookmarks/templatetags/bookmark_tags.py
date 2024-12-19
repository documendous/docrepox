from django import template
from django.contrib.contenttypes.models import ContentType
from apps.bookmarks.models import Bookmark

register = template.Library()


@register.filter
def is_bookmarked(element, user):  # pragma: no coverage
    if not user.is_authenticated:
        return False

    content_type = ContentType.objects.get_for_model(element)
    return Bookmark.objects.filter(
        owner=user, content_type=content_type, object_id=element.id
    ).exists()
