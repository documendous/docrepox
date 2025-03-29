from apps.core.utils.core import get_extension

from ..models.profile import Profile
from ..utils.document import UPDATEABLE_CONTENT_EXTENSIONS
from .utils import get_immutable_folders


def is_unupdatable_folder(element):
    if element in get_immutable_folders():
        return True
    elif element.is_recycle_folder():
        return True
    elif element.is_in_recycle_path():
        return True
    else:
        return False


def is_undeletable_folder(user, element):
    if element.type == "folder":
        folder = element
    elif element.type == "project":
        folder = element.folder
    else:
        folder = None

    if element in get_immutable_folders():
        return True
    elif element.is_recycle_folder():
        return True
    elif folder and is_a_home_folder(folder):
        return True
    else:
        return False


def is_a_home_folder(folder):
    """
    Checks if a given folder is a user's home folder efficiently.
    """
    return Profile.objects.filter(home_folder=folder).exists()


def is_editor(user, project):
    if project.in_editors_group(user):
        return True
    elif project.in_managers_group(user):
        return True
    return False


def is_manager(user, project):
    return True if project.in_managers_group(user) else False


def is_reader(user, project):
    return (
        True
        if project.in_readers_group(user)
        or project.in_editors_group(user)
        or project.in_managers_group(user)
        or project.visibility == "public"
        else False
    )


def content_file_is_updateable(document):
    if get_extension(file_name=document.name) in UPDATEABLE_CONTENT_EXTENSIONS:
        return True

    return False
