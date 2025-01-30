from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.projects.models import Project
from apps.repo.models.element.document import Document
from apps.repo.models.element.folder import Folder
from apps.repo.models.element.version import Version
from apps.repo.utils.system.object import (
    get_system_home_folder,
    get_user_recycle_folder,
)

TEST_USER = {
    "username": "testuser1",
    "password": "testpass",
}

User = get_user_model()


def get_test_user(username=None):
    test_user, created = User.objects.get_or_create(
        username=username if username else TEST_USER["username"],
    )
    if created:
        test_user.set_password(TEST_USER["password"])
        test_user.save()
    return test_user


def get_test_folder(name=None, parent=None):
    test_folder = Folder.objects.create(
        name="Test Folder" if not name else name,
        owner=get_test_user(),
        parent=parent if parent else get_system_home_folder(),
    )
    return test_folder


def get_test_document(name=None, parent=None, ext="txt"):
    test_document = Document.objects.create(
        name=f"TestDocument.{ext}" if not name else name,
        owner=get_test_user(),
        parent=parent if parent else get_system_home_folder(),
    )
    test_content = b"Hello world"
    test_file = SimpleUploadedFile(f"TestDocument.{ext}", test_content)
    Version.objects.create(parent=test_document, content_file=test_file)
    return test_document


def get_test_project(name=None, visibility="public"):
    test_project = Project.objects.create(
        name="Test Project", visibility=visibility, owner=get_test_user()
    )
    return test_project


def get_test_recycle_folder(user):
    return get_user_recycle_folder(user=user)
