from django.conf import settings

from apps.repo.utils.mock import create_testusers
from apps.repo.utils.system.mimetype.setup import add_mimetypes
from apps.repo.utils.system.setup import create_system_folders
from apps.repo.utils.system.user import (
    create_admin_home_folder,
    create_admin_user,
    create_admin_user_profile,
)


def setup_system(apps, schema):
    create_admin_user(apps, schema)
    create_admin_user_profile(apps, schema)
    create_system_folders(apps, schema)
    create_admin_home_folder(apps, schema)

    if settings.ADD_TEST_OBJECTS:
        create_testusers(apps, schema)

    add_mimetypes()
