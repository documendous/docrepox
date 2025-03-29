from django.conf import settings
from django.contrib.auth.models import User

from apps.comments.models import Comment
from apps.core.utils.handlers import response_handler
from apps.repo.utils.static.lookup import get_model

from ..conditions import is_manager
from ..utils import admin_override


def can_add_comment(user, instance, from_tag=False):
    """
    Determines if a user can add a comment to an instance:
    - A user can comment if they are a member of the associated project.
    - Public comments are allowed if the project is public and public comments are enabled.
    - If the instance is not part of a project, only the owner can comment.
    - Admins can add comments if allowed by global admin settings.
    - Comments are disallowed for:
    - Documents, folders, or projects if their respective comment settings are disabled.
    """
    accessible = False
    user = user
    project = getattr(instance, "parent_project", None)

    # Permission determinations
    if project:
        if project.is_member(user):
            return True

        if project.visibility == "public" and settings.ENABLE_PUBLIC_COMMENTS:
            return True

    else:
        if user == instance.owner:
            accessible = True

    # Explicit inclusions
    accessible = admin_override(user, accessible)

    # Explicit exclusions
    if instance.type == "document" and not settings.ENABLE_DOCUMENT_COMMENTS:
        accessible = False

    elif instance.type == "folder" and not settings.ENABLE_FOLDER_COMMENTS:
        accessible = False

    elif instance.type == "project" and not settings.ENABLE_PROJECT_COMMENTS:
        accessible = False

    return response_handler(accessible, from_tag)


def can_delete_comment(
    user: User,
    comment_id: int,
    element_type: str,
    element_id: int,
    from_tag=False,
) -> bool:
    """
    Determines if a user can delete a comment:
    - A user can delete the comment if they are the author of the comment.
    - The owner of the element associated with the comment can delete it.
    - A user can delete the comment if they are a manager in the associated project.
    - Admins can delete any comment if allowed by global admin settings.
    """
    accessible = False
    user = user
    Element = get_model(element_type=element_type)
    element = Element.objects.get(pk=element_id)
    project = getattr(element, "parent_project", None)
    comment = Comment.objects.get(pk=comment_id)

    if comment.author == user:
        accessible = True

    if element.owner == user:
        accessible = True

    if project:
        if is_manager(user, project):
            accessible = True

    accessible = admin_override(user, accessible)

    return response_handler(accessible, from_tag)
