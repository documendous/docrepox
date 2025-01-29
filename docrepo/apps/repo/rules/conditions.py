from apps.repo.models.profile import Profile

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


def is_undeletable_folder(request, element):
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
