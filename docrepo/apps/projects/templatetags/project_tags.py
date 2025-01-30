"""
Template tags for project functionality
"""

from django import template

from apps.projects import rules
from apps.projects.utils import project as project_utils

register = template.Library()


@register.simple_tag
def is_a_project_folder(folder) -> bool:
    """
    Returns True if this folder is actually the main folder for an existing project
    """
    return project_utils.is_a_project_folder(folder)


@register.simple_tag
def can_view_project_details(request, element) -> bool:
    return rules.can_view_project_details(request, element, from_tag=True)


@register.simple_tag
def can_view_project_members(request, element) -> bool:
    return rules.can_view_project_members(request, element, from_tag=True)


@register.simple_tag
def can_add_user_to_project_group(request, parent) -> bool:
    return rules.can_add_user_to_project_group(request, parent, from_tag=True)


@register.simple_tag
def can_remove_user_from_project_group(request, parent) -> bool:
    return rules.can_remove_user_from_project_group(request, parent, from_tag=True)


@register.simple_tag
def can_read_project(request, parent) -> bool:
    return rules.can_read_project(request, parent, from_tag=True)


@register.simple_tag
def has_project_membership(request, parent) -> bool:
    return rules.has_project_membership(request, parent, from_tag=True)


@register.simple_tag
def is_membership_pending(request, parent) -> bool:
    return rules.is_membership_pending(request, parent)


@register.simple_tag
def can_deactivate_project(request, parent) -> bool:
    return rules.can_deactivate_project(request, parent, from_tag=True)


@register.simple_tag
def can_update_project(request, project) -> bool:
    return rules.can_update_project(request, project, from_tag=True)


@register.simple_tag
def get_role_display(request, project) -> str:
    return project.get_role_display(user=request.user)
