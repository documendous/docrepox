import logging
from typing import List

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet
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


def get_valid_bookmarks(bookmarks: QuerySet[Bookmark], user: User) -> List:
    """
    Filters out bookmarked documents that belong to projects the user no longer has access to.

    Args:
        bookmarks (QuerySet[Bookmark]): A queryset of Bookmark objects owned by the user.
        user (User): The user whose access to projects is being verified.

    Returns:
        List: A list of content objects (documents) that the user still has access to.
    """
    valid_children = []

    for bookmark in bookmarks:
        content_object = bookmark.content_object

        if hasattr(content_object, "parent_project"):
            parent_project = getattr(content_object, "parent_project", None)
            if parent_project and not parent_project.is_member(
                user
            ):  # pragma: no coverage
                continue  # Skip if the user is no longer a member

        valid_children.append(content_object)

    return valid_children
