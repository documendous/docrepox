from ....repo.rules.conditions import is_manager, is_reader
from ....repo.rules.utils import admin_override, response_handler


def get_project_for_element(element):
    """
    Retrieves the parent project for the given element, if available.
    """
    return getattr(element, "parent_project", None)


def check_accessible_by_role(request, project, role_check):
    """
    Checks if a user has access to a project based on a specific role.
    - `role_check` should be a callable (e.g., `is_reader`, `is_manager`).
    """
    return role_check(request, project) if project else False


def can_view_project_members(request, project, from_tag=False):
    """
    Determines if a user can view the members of a project.
    """
    accessible = project.type == "project" and project.is_member(request.user)

    return response_handler(accessible, from_tag)


def can_view_project_details(request, element, from_tag=False):
    """
    Determines if a user can view the details of a project.
    """
    accessible = False
    project = get_project_for_element(element)

    if project:
        accessible = check_accessible_by_role(request, project, is_reader)
        accessible = admin_override(request, accessible)

    return response_handler(accessible, from_tag)


def can_update_project(request, project, from_tag=False):
    """
    Determines if a user can update a project.
    """
    accessible = project.type == "project" and check_accessible_by_role(
        request, project, is_manager
    )

    accessible = admin_override(request, accessible)

    return response_handler(accessible, from_tag)


def can_add_user_to_project_group(request, parent, from_tag=False):
    """
    Determines if a user can add another user to a project group.
    """
    project = get_project_for_element(parent)

    accessible = project and (
        project.in_managers_group(request.user) or project.owner == request.user
    )

    accessible = admin_override(request, accessible)

    return response_handler(accessible, from_tag)


def can_remove_user_from_project_group(request, parent, from_tag=False):
    """
    Determines if a user can remove another user from a project group.
    """
    project = get_project_for_element(parent)
    accessible = project and project.in_managers_group(request.user)
    accessible = admin_override(request, accessible)

    return response_handler(accessible, from_tag)


def can_read_project(request, parent, from_tag=False):
    """
    Determines if a user can read a project.
    """
    project = get_project_for_element(parent)

    accessible = project and (
        project.is_member(request.user) or project.visibility == "public"
    )

    accessible = admin_override(request, accessible)

    return response_handler(accessible, from_tag)


def can_deactivate_project(request, parent, from_tag=False):
    """
    Determines if a user can deactivate a project.
    """
    project = get_project_for_element(parent)
    accessible = project and project.owner == request.user
    accessible = admin_override(request, accessible)

    return response_handler(accessible, from_tag)
