from apps.repo.utils.static.system import is_system_projects_folder


def has_public_access(folder):
    if is_system_projects_folder(folder):
        return True

    return False
