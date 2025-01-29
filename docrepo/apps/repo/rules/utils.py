from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404

from apps.repo.utils.system.object import (
    get_system_home_folder,
    get_system_projects_folder,
    get_system_root_folder,
    get_system_sys_folder,
)


def get_immutable_folders():
    immutable_folders = (
        get_system_root_folder(),
        get_system_projects_folder(),
        get_system_home_folder(),
        get_system_sys_folder(),
    )
    return immutable_folders


def response_handler(accessible, from_tag):
    if accessible:
        return True
    else:
        if from_tag:
            return False
        if settings.DEBUG:
            raise PermissionDenied
        else:
            raise Http404


def admin_override(request, accessible):
    """
    Checks if the user has admin privileges and global admin overrides are enabled.
    """
    if settings.ADMIN_ALLOW_ALL and request.user.profile.is_admin_user():
        return True
    return accessible
