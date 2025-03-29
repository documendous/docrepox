from apps.core.utils.handlers import response_handler

from ....repo.rules.conditions import is_manager, is_reader
from ....repo.rules.utils import admin_override


def get_project_for_element(element):
    """
    Retrieves the parent project for the given element, if available.
    """
    return getattr(element, "parent_project", None)


def check_accessible_by_role(user, project, role_check):
    """
    Checks if a user has access to a project based on a specific role.
    - `role_check` should be a callable (e.g., `is_reader`, `is_manager`).
    """
    return role_check(user, project) if project else False


def can_view_project_members(user, project, from_tag=False):
    """
    Determines if a user can view the members of a project.
    """
    accessible = project.type == "project" and project.is_member(user)

    return response_handler(accessible, from_tag)


def can_view_project_details(user, element, from_tag=False):
    """
    Determines if a user can view the details of a project.
    """
    accessible = False
    project = get_project_for_element(element)

    if project:
        accessible = check_accessible_by_role(user, project, is_reader)
        accessible = admin_override(user, accessible)

    return response_handler(accessible, from_tag)


def can_update_project(user, project, from_tag=False):
    """
    Determines if a user can update a project.
    """
    accessible = project.type == "project" and check_accessible_by_role(
        user, project, is_manager
    )

    accessible = admin_override(user, accessible)

    return response_handler(accessible, from_tag)


def can_add_user_to_project_group(user, parent, from_tag=False):
    """
    Determines if a user can add another user to a project group.
    """
    project = get_project_for_element(parent)

    accessible = project and (project.in_managers_group(user) or project.owner == user)

    accessible = admin_override(user, accessible)

    return response_handler(accessible, from_tag)


def can_remove_user_from_project_group(user, parent, from_tag=False):
    """
    Determines if a user can remove another user from a project group.
    """
    project = get_project_for_element(parent)
    accessible = project and project.in_managers_group(user)
    accessible = admin_override(user, accessible)

    return response_handler(accessible, from_tag)


def can_read_project(user, parent, from_tag=False):
    """
    Determines if a user can read a project.
    """
    project = get_project_for_element(parent)

    accessible = project and (project.is_member(user) or project.visibility == "public")

    accessible = admin_override(user, accessible)

    return response_handler(accessible, from_tag)


def can_deactivate_project(user, parent, from_tag=False):
    """
    Determines if a user can deactivate a project.
    """
    project = get_project_for_element(parent)
    accessible = project and project.owner == user
    accessible = admin_override(user, accessible)

    return response_handler(accessible, from_tag)
