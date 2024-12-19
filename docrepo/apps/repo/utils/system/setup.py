from apps.repo.models import Folder
from apps.repo.utils.system.object import get_admin_user


def create_system_folders(apps, schema):
    admin_user = get_admin_user()
    root_folder = Folder.objects.create(
        name="ROOT",
        owner=admin_user,
    )
    Folder.objects.create(
        name="Home",
        owner=admin_user,
        parent=root_folder,
    )
    Folder.objects.create(
        name="System",
        owner=admin_user,
        parent=root_folder,
    )
    Folder.objects.create(
        name="Projects",
        owner=admin_user,
        parent=root_folder,
    )
