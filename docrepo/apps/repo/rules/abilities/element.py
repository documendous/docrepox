from apps.projects.rules.utils import get_project_for_element
from apps.projects.utils.project import is_a_project_folder

from ..conditions import (
    is_a_home_folder,
    is_editor,
    is_manager,
    is_reader,
    is_undeletable_folder,
    is_unupdatable_folder,
)
from ..utils import admin_override, response_handler
from .document import can_create_document


def can_view_element_details(request, element, from_tag=False):
    """
    Determines if a user can view an element:
    - If the element is part of a project, the user can view it if they are in the project's readers group.
    - If the element is not part of a project, only the owner can view it.
    - Admins can always view if allowed by global settings.
    """
    accessible = False
    project = get_project_for_element(element)

    # Permission determinations
    if project:
        if is_reader(request, project):
            accessible = True

    else:
        if request.user == element.owner and not project:
            accessible = True

    # Explicit inclusions
    accessible = admin_override(request, accessible)

    return response_handler(accessible, from_tag)


def can_restore_element(request, element, from_tag=False):
    """
    Determines if a user can restore an element:
    - A user can restore if they can view the element and create documents in its original parent.
    - Elements in the recycle folder or outside the recycle path cannot be restored.
    """
    accessible = False
    orig_parent = getattr(element, "orig_parent", None)

    # Permission determinations:
    if can_view_element_details(request, element, from_tag=from_tag):
        if orig_parent:
            if can_create_document(request, orig_parent, from_tag=from_tag):
                accessible = True

    # Explicit exclusions:
    if element.is_recycle_folder():
        accessible = False

    if not element.is_in_recycle_path():
        accessible = False

    return response_handler(accessible, from_tag)


def can_update_element(request, element, from_tag=False):
    """
    Determines if a user can update an element:
    - A user can update if they are an editor in the project's editors group.
    - If the element is not part of a project, only the owner can update it.
    - Admins can update everything if allowed by global settings.
    - Certain folders are explicitly marked as not updatable and cannot be updated.
    """
    accessible = False
    project = get_project_for_element(element)

    # Permission determinations:
    if project:
        if is_editor(request, project):
            accessible = True

    else:
        if request.user == element.owner and not project:
            accessible = True

    # Explicit inclusions
    accessible = admin_override(request, accessible)

    # Explicit exclusions
    if is_unupdatable_folder(element):
        accessible = False

    return response_handler(accessible, from_tag)


def can_recycle_element(request, element, from_tag=False):
    """
    Determines if a user can recycle (delete) an element:
    - A user can recycle if they are a manager in the project's managers group.
    - If the element is not part of a project, the owner can recycle it if it is not already in the recycle path or a recycle folder.
    - Admins can recycle everything if allowed by global settings.
    - Certain elements cannot be recycled:
    - Undeletable folders.
    - Home folders.
    - Projects.
    """
    accessible = False
    project = get_project_for_element(element)

    # Permission determinations:
    if project:
        if is_manager(request, project):
            accessible = True

    else:
        if (
            not element.is_in_recycle_path()
            and not element.is_recycle_folder()
            and request.user == element.owner
        ):
            accessible = True

    # Explicit inclusions
    accessible = admin_override(request, accessible)

    # Explicit exclusions
    if is_undeletable_folder(request, element):
        accessible = False

    if element.type == "folder":
        if is_a_home_folder(element):
            accessible = False

    if element.type == "project":
        accessible = False

    return response_handler(accessible, from_tag)


def can_delete_element(request, element, from_tag=False):
    """
    Determines if a user can permanently delete an element:
    - A user can delete if they are a manager in the project's managers group.
    - If the element is not part of a project, the owner can delete it.
    - Admins can delete everything if allowed by global settings.
    - Certain elements cannot be deleted:
    - Undeletable folders.
    - Elements not in the recycle path.
    - Home folders.
    - Projects.
    """
    accessible = False
    project = get_project_for_element(element)

    # Permission determinations
    if project:
        if is_manager(request, project):
            accessible = True

    else:
        if request.user == element.owner and not project:
            accessible = True

    # Explicit inclusions
    accessible = admin_override(request, accessible)

    # Explicit exclusions
    if is_undeletable_folder(request, element):
        accessible = False

    if not element.is_in_recycle_path():
        accessible = False

    if element.type == "folder":
        if is_a_home_folder(element):
            accessible = False

    if element.type == "project":
        accessible = False

    return response_handler(accessible, from_tag)


def can_add_element_to_clipboard(request, element, from_tag=False):
    """
    A user can add an element to the clipboard if they can view its details,
    unless the element is in the recycle folder or recycle path.
    """
    accessible = False

    # Permission determinations
    if can_view_element_details(request, element, from_tag=from_tag):
        accessible = True

    # Explicit exclusions
    if element.is_recycle_folder():
        accessible = False

    if element.is_in_recycle_path():
        accessible = False

    return response_handler(accessible, from_tag)


def can_move_element(request, element, from_tag=False):
    """
    A user can move an element if:
    - They are a manager in the project's managers group or the owner of the element.
    - Admins can always move elements if allowed by global settings.

    Exceptions:
    - Projects and project folders cannot be moved.
    - Elements with a parent in the recycle path cannot be moved.
    """
    accessible = False
    parent = getattr(element, "parent", None)
    project = get_project_for_element(element)

    # Permission determinations
    if project:
        if is_manager(request, project):
            accessible = True
        elif request.user == element.owner:
            accessible = True
    else:
        if request.user == element.owner:
            accessible = True

    # Explicit inclusions
    accessible = admin_override(request, accessible)

    # Explicit exclusions
    if element.type == "project":
        accessible = False

    if is_a_project_folder(element):
        accessible = False

    if parent:
        if parent.is_in_recycle_path():
            accessible = False

    if is_undeletable_folder(request, element):
        accessible = False

    return response_handler(accessible, from_tag)


def can_copy_element(request, element, from_tag=False):
    """
    A user can copy an element if:
    - They are an editor in the project's editors group.
    - They are the owner of the element if it is not part of a project.
    - Admins can always copy elements if allowed by global settings.
    """
    accessible = False
    project = get_project_for_element(element)

    # Permission determinations
    if project:
        if is_editor(request, project):
            accessible = True
    else:
        if request.user == element.owner:
            accessible = True

    # Explicit inclusions
    accessible = admin_override(request, accessible)

    return response_handler(accessible, from_tag)


def can_bookmark(request, element, from_tag=False):
    accessible = False

    if element.type == "project":
        project = element
    else:
        project = element.parent_project

    if project:
        if not project.is_member(request.user):
            accessible = False
        else:
            accessible = True
    else:
        if element.owner != request.user:
            accessible = False
        else:
            accessible = True

    # if you turn this on, see Issue #668
    accessible = admin_override(request, accessible)

    return response_handler(accessible, from_tag)
