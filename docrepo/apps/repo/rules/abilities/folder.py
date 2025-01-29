from apps.repo.utils.system.object import get_system_projects_folder

from ..conditions import is_editor
from ..utils import admin_override, response_handler


def get_accessible_by_project_or_owner(request, parent):
    """
    Determines if a user has access based on project membership or ownership.
    Returns:
    - True if the user is a member of the associated project or the owner of the parent.
    - False otherwise.
    """
    project = getattr(parent, "parent_project", None)
    if project:
        return project.is_member(request.user)
    return request.user == parent.owner


def can_view_folder(request, parent, from_tag=False):
    """
    Determines if a user can view a folder.
    """
    accessible = get_accessible_by_project_or_owner(request, parent)

    # Additional rules for public visibility and system folders
    project = getattr(parent, "parent_project", None)
    if project and project.visibility == "public":
        accessible = True

    if parent == get_system_projects_folder():
        accessible = True

    accessible = admin_override(request, accessible)
    return response_handler(accessible, from_tag)


def can_create_folder_children(request, parent, from_tag=False):
    """
    Determines if a user can create child folders within a parent folder.
    """
    project = getattr(parent, "parent_project", None)
    accessible = (
        project
        and is_editor(request, project)
        or not project
        and request.user == parent.owner
    )

    accessible = admin_override(request, accessible)
    return response_handler(accessible, from_tag)
