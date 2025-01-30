from ..conditions import is_editor
from ..utils import admin_override, response_handler


def can_create_document(request, parent, from_tag=False):
    """
    Determines if a user can create a document:
    - A user can create a document if they are an editor in the associated project.
    - If the parent is not part of a project, only the owner can create a document.
    - Admins can create documents if allowed by global admin settings.
    - Documents cannot be created in recycle folders or in elements within the recycle path.
    """
    accessible = False
    project = getattr(parent, "parent_project", None)

    # Permssion determinations
    if project:
        if is_editor(request, project):
            accessible = True

    else:
        if request.user == parent.owner and not project:
            accessible = True

    # Explicit inclusions
    accessible = admin_override(request, accessible)

    # Explicit exclusions
    if parent.is_recycle_folder() or parent.is_in_recycle_path():
        accessible = False

    return response_handler(accessible, from_tag)


def can_add_document_version(request, document, from_tag=False):
    """
    Determines if a user can add a version to a document:
    - A user can add a document version if they are an editor in the associated project.
    - If the document's parent is not part of a project, only the parent owner can add a version.
    - Admins can add document versions if allowed by global admin settings.
    """
    accessible = False
    parent = getattr(document, "parent", None)

    if parent:
        project = parent.parent_project
    else:
        project = None

    # Permssion determinations
    if project:
        if is_editor(request, project):
            accessible = True

    else:
        if request.user == parent.owner and not project:
            accessible = True

    # Explicit inclusions
    accessible = admin_override(request, accessible)

    return response_handler(accessible, from_tag)
