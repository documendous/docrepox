from django.conf import settings
from django.contrib.auth import get_user_model
from apps.repo.models import Folder


User = get_user_model()


def get_admin_user():
    return User.objects.get(username=settings.ADMIN_USERNAME)


def get_system_root_folder():
    return Folder.objects.get(
        name="ROOT",
        parent=None,
        owner=get_admin_user(),
    )


def get_system_home_folder():
    return Folder.objects.get(
        name="Home",
        parent=get_system_root_folder(),
        owner=get_admin_user(),
    )


def get_system_projects_folder():
    return Folder.objects.get(
        name="Projects",
        parent=get_system_root_folder(),
        owner=get_admin_user(),
    )


def get_system_sys_folder():
    return Folder.objects.get(  # pragma: no coverage
        name="System",
        parent=get_system_root_folder(),
        owner=get_admin_user(),
    )


def get_user_recycle_folder(user):
    return Folder.objects.get(
        name="Recycle", owner=user, parent=user.profile.home_folder
    )
