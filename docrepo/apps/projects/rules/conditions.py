from django.conf import settings

from apps.comms.models import Communication
from apps.core.utils.handlers import response_handler


def has_project_membership(user, parent, from_tag=False):
    accessible = False
    project = getattr(parent, "parent_project", None)

    if project:
        if project.is_member(user):
            accessible = True

        if settings.ADMIN_ALLOW_ALL and user.profile.is_admin_user():
            accessible = True

    return response_handler(accessible, from_tag)


def is_membership_pending(user, parent):
    project = getattr(parent, "parent_project", None)

    if not project or user in project.get_all_members():
        return False

    pending_requests = Communication.objects.filter(
        msg_from=user,
        msg_to__in=project.get_managers(),
        category="project_join_request",
        content_type__model="project",
        object_id=project.id,
    )

    result = pending_requests.exists()

    return result
