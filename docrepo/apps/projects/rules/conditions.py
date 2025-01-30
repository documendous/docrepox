from django.conf import settings

from apps.comms.models import Communication
from apps.repo.rules.utils import response_handler


def has_project_membership(request, parent, from_tag=False):
    accessible = False
    project = getattr(parent, "parent_project", None)

    if project:
        if project.is_member(request.user):
            accessible = True
        if settings.ADMIN_ALLOW_ALL and request.user.profile.is_admin_user():
            accessible = True

    return response_handler(accessible, from_tag)


def is_membership_pending(request, parent):
    project = getattr(parent, "parent_project", None)

    if not project or request.user in project.get_all_members():
        return False

    pending_requests = Communication.objects.filter(
        msg_from=request.user,
        msg_to__in=project.get_managers(),
        category="project_join_request",
        content_type__model="project",
        object_id=project.id,
    )

    result = pending_requests.exists()
    return result
