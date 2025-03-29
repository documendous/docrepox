import logging

from django.conf import settings
from django.contrib.auth import get_user_model

from apps.repo.models import Folder, Profile
from apps.repo.utils.system.object import get_admin_user, get_system_home_folder

User = get_user_model()


def create_admin_user(apps, schema):
    User.objects.create_superuser(
        username=settings.ADMIN_USERNAME,
        password=settings.ADMIN_PASSWORD,
        email=settings.ADMIN_EMAIL,
    )


def create_admin_user_profile(apps, schema):
    Profile.objects.create(user=get_admin_user())


def create_admin_home_folder(apps, schema):
    admin_user = get_admin_user()
    system_home_folder = get_system_home_folder()

    admin_home_folder = Folder.objects.create(
        name=admin_user.username,
        owner=admin_user,
        parent=system_home_folder,
    )

    admin_user.profile.home_folder = admin_home_folder
    admin_user.profile.save()
    create_recycle_folder(admin_user)  # must be last


def create_user_home_folder(user):
    log = logging.getLogger(__name__)
    home_folder = get_system_home_folder()

    user_home_folder = Folder.objects.create(
        name=user.username,
        title=f"{user.username} personal folder",
        description=f"Home folder for {user.username}",
        parent=home_folder,
        owner=user,
    )

    user.profile.home_folder = user_home_folder
    user.profile.save()
    create_recycle_folder(user)  # must be last
    log.debug(f"Created home folder for user: {user.username}")


def update_user_home_folder(user):  # pragma: no coverage
    user_home_folder = user.profile.home_folder

    if user_home_folder.name != user.username:
        user_home_folder.name = user.username
        user_home_folder.save()


def create_recycle_folder(user):
    Folder.objects.create(
        name="Recycle",  # Hard-coded purposely
        title=f"{user.username} recycle folder",
        description=f"Recycle folder for {user.username}",
        parent=user.profile.home_folder,
        owner=user,
        is_hidden=True,
    )
