import logging

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from apps.bookmarks.models import Bookmark
from apps.repo import rules
from apps.repo.utils.static.lookup import get_model


def remove_bookmark(request, element_type, element_pk):
    Element = get_model(element_type)
    element = get_object_or_404(Element, pk=element_pk)

    rules.can_bookmark(request, element)

    content_type = ContentType.objects.get_for_model(element)
    bookmark = Bookmark.objects.get(
        owner=request.user,
        content_type=content_type,
        object_id=element.id,
    )
    bookmark.delete()


def add_bookmark(request, element_type, element_pk):
    log = logging.getLogger(__name__)

    Element = get_model(element_type)
    element = get_object_or_404(Element, pk=element_pk)

    rules.can_bookmark(request, element)

    content_type = ContentType.objects.get_for_model(element)
    if not Bookmark.objects.filter(
        owner=request.user,
        content_type=content_type,
        object_id=element.id,
    ).exists():
        Bookmark.objects.create(owner=request.user, content_object=element)
        log.debug(f"Created bookmark on {element} for {request.user}")
