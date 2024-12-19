import logging
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest

from apps.comments.models import Comment
from apps.comms.models import Communication
from apps.projects.utils.project import is_a_project_folder
from apps.repo.utils.static.lookup import get_model
from apps.repo.utils.system.object import (
    get_system_home_folder,
    get_system_projects_folder,
    get_system_root_folder,
    get_system_sys_folder,
)


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


def get_immutable_folders():
    immutable_folders = (
        get_system_root_folder(),
        get_system_projects_folder(),
        get_system_home_folder(),
        get_system_sys_folder(),
    )
    return immutable_folders


def is_unupdatable_folder(element):
    if element in get_immutable_folders():
        return True
    elif element.is_recycle_folder():
        return True
    elif element.is_in_recycle_path():
        return True
    else:
        return False


def is_undeletable_folder(request, element):
    if element in get_immutable_folders():
        return True
    elif element.is_recycle_folder():
        return True
    else:
        return False


def is_editor(request, project):
    if project.in_editors_group(request.user):
        return True
    elif project.in_managers_group(request.user):
        return True
    return False


def is_manager(request, project):
    return True if project.in_managers_group(request.user) else False


def is_reader(request, project):
    return (
        True
        if project.in_readers_group(request.user)
        or project.in_editors_group(request.user)
        or project.in_managers_group(request.user)
        or project.visibility == "public"
        else False
    )


def can_view_folder(request, parent, from_tag=False):
    accessible = False
    project = getattr(parent, "parent_project", None)

    if project:
        if project.is_member(request.user) or project.visibility == "public":
            accessible = True
    else:
        if request.user == parent.owner and not project:
            accessible = True

    if parent == get_system_projects_folder():
        accessible = True

    return response_handler(accessible, from_tag)


def can_view_project_members(request, project, from_tag=False):
    accessible = False
    if project.type == "project":
        if project.is_member(request.user):
            accessible = True
    return response_handler(accessible, from_tag)


def can_create_folder_children(request, parent, from_tag=False):
    accessible = False
    project = getattr(parent, "parent_project", None)

    if project:
        if is_editor(request, project):
            accessible = True

    else:
        if request.user == parent.owner and not project:
            accessible = True

    return response_handler(accessible, from_tag)


def can_create_document(request, parent, from_tag=False):
    accessible = False
    project = getattr(parent, "parent_project", None)

    if project:
        if is_editor(request, project):
            accessible = True

    else:
        if request.user == parent.owner and not project:
            accessible = True

    if parent.is_recycle_folder() or parent.is_in_recycle_path():
        accessible = False

    return response_handler(accessible, from_tag)


def can_view_element_details(request, element, from_tag=False):
    accessible = False
    parent = getattr(element, "parent", None)
    orig_parent = getattr(element, "orig_parent", None)

    if parent:
        project = parent.parent_project
        if not project:
            project = getattr(orig_parent, "parent_project", None)
    elif element.type == "project":
        project = element
    else:
        project = None

    if project:
        if is_reader(request, project):
            accessible = True

    else:
        if request.user == element.owner and not project:
            accessible = True

    return response_handler(accessible, from_tag)


def can_view_project_details(request, element, from_tag=False):
    accessible = False
    project = None
    project = getattr(element, "parent_project", None)

    if project:
        if is_reader(request, project):
            accessible = True

    return response_handler(accessible, from_tag)


def can_restore_element(request, element, from_tag=False):
    accessible = False
    orig_parent = getattr(element, "orig_parent", None)

    if can_view_element_details(request, element, from_tag=from_tag):
        if orig_parent:
            if can_create_document(request, orig_parent, from_tag=from_tag):
                accessible = True

    if element.is_recycle_folder():
        accessible = False

    if not element.is_in_recycle_path():
        accessible = False

    return response_handler(accessible, from_tag)


def can_update_element(request, element, from_tag=False):
    accessible = False
    parent = getattr(element, "parent", None)
    if parent:
        project = parent.parent_project
    else:
        project = None

    if project:
        if is_editor(request, project):
            accessible = True

    else:
        if request.user == element.owner and not project:
            accessible = True

    if is_unupdatable_folder(element):
        accessible = False

    return response_handler(accessible, from_tag)


def can_update_project(request, project, from_tag=False):
    accessible = False
    if project.type == "project":
        if is_manager(request, project):
            accessible = True

    return response_handler(accessible, from_tag)


def can_recycle_element(request, element, from_tag=False):
    accessible = False
    parent = getattr(element, "parent", None)

    if parent:
        project = parent.parent_project
    else:
        project = None

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

    if element.type == "project":
        accessible = False

    return response_handler(accessible, from_tag)


def can_delete_element(request, element, from_tag=False):
    accessible = False
    parent = getattr(element, "parent", None)
    orig_parent = getattr(element, "orig_parent", None)

    if parent:
        project = parent.parent_project
        if not project:
            project = getattr(orig_parent, "parent_project", None)
    else:
        project = None

    if project:
        if is_manager(request, project):
            accessible = True

    else:
        if request.user == element.owner and not project:
            accessible = True

    if is_undeletable_folder(request, element):
        accessible = False

    if not element.is_in_recycle_path():
        accessible = False

    if element.type == "project":
        accessible = False

    return response_handler(accessible, from_tag)


def can_add_document_version(request, document, from_tag=False):
    accessible = False
    parent = getattr(document, "parent", None)
    if parent:
        project = parent.parent_project
    else:
        project = None

    if project:
        if is_editor(request, project):
            accessible = True

    else:
        if request.user == parent.owner and not project:
            accessible = True

    return response_handler(accessible, from_tag)


def can_add_element_to_clipboard(request, element, from_tag=False):
    accessible = False

    if can_view_element_details(request, element, from_tag=from_tag):
        accessible = True

    if element.is_recycle_folder():
        accessible = False

    if element.is_in_recycle_path():
        accessible = False

    return response_handler(accessible, from_tag)


def can_move_element(request, element, from_tag=False):
    accessible = False
    parent = getattr(element, "parent", None)
    if parent:
        project = parent.parent_project
    else:
        project = None

    if project:
        if is_manager(request, project):
            accessible = True
        elif request.user == element.owner:
            accessible = True
    else:
        if request.user == element.owner:
            accessible = True

    if element.type == "project":
        accessible = False

    if is_a_project_folder(element):
        accessible = False

    if parent:
        if parent.is_in_recycle_path():
            accessible = False

    return response_handler(accessible, from_tag)


def can_copy_element(request, element, from_tag=False):
    accessible = False
    parent = getattr(element, "parent", None)
    if parent:
        project = parent.parent_project
    else:
        project = None

    if project:
        if is_editor(request, project):
            accessible = True
    else:
        if request.user == element.owner:
            accessible = True

    return response_handler(accessible, from_tag)


def can_add_comment(request, instance, from_tag=False):
    accessible = False
    user = request.user
    project = getattr(instance, "parent_project", None)

    if project:
        if project.is_member(user):
            return True

        if project.visibility == "public" and settings.ENABLE_PUBLIC_COMMENTS:
            return True

    else:
        if request.user == instance.owner:
            accessible = True

    if instance.type == "document" and not settings.ENABLE_DOCUMENT_COMMENTS:
        accessible = False

    elif instance.type == "folder" and not settings.ENABLE_FOLDER_COMMENTS:
        accessible = False

    elif instance.type == "project" and not settings.ENABLE_PROJECT_COMMENTS:
        accessible = False

    return response_handler(accessible, from_tag)


def can_delete_comment(
    request: HttpRequest,
    comment_id: int,
    element_type: str,
    element_id: int,
    from_tag=False,
) -> bool:
    accessible = False
    user = request.user
    Element = get_model(element_type=element_type)
    element = Element.objects.get(pk=element_id)
    project = getattr(element, "parent_project", None)
    comment = Comment.objects.get(pk=comment_id)

    if comment.author == user:
        accessible = True

    if element.owner == user:
        accessible = True

    if project:
        if is_manager(request, project):
            accessible = True

    return response_handler(accessible, from_tag)


def can_add_user_to_project_group(request, parent, from_tag=False):
    accessible = False
    project = getattr(parent, "parent_project", None)
    if project:
        if project.in_managers_group(request.user):
            accessible = True

    return response_handler(accessible, from_tag)


def can_remove_user_from_project_group(request, parent, from_tag=False):
    accessible = False
    project = getattr(parent, "parent_project", None)
    if project:
        if project.in_managers_group(request.user):
            accessible = True

    return response_handler(accessible, from_tag)


def can_read_project(request, parent, from_tag=False):
    accessible = False
    project = getattr(parent, "parent_project", None)

    if project:
        if project.is_member(request.user) or project.visibility == "public":
            accessible = True

    return response_handler(accessible, from_tag)


def has_project_membership(request, parent, from_tag=False):
    accessible = False
    project = getattr(parent, "parent_project", None)

    if project:
        if project.is_member(request.user):
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


def has_danger_privs_in_project(request, parent, from_tag=False):
    accessible = False
    project = getattr(parent, "parent_project", None)

    if project:
        if project.owner == request.user:
            accessible = True

    return response_handler(accessible, from_tag)


def has_boomark_access(request, element):
    log = logging.getLogger(__name__)
    project = element.parent_project
    log.debug(f"element in project: {project}")

    if project:
        if not project.is_member(request.user):
            log.debug(
                f"User: {request.user} is not a member of project: {project.name}"
            )
            raise Http404
        else:
            log.debug(f"User: {request.user} is a member of project: {project}")
    else:
        if element.owner != request.user:
            log.debug(f"User: {request.user} does not own element: {element.pk}")
            raise Http404
