from django.test import TestCase

from apps.repo.models.element.folder import Folder
from apps.repo.tests.utils import get_test_document, get_test_folder, get_test_user
from apps.repo.utils.model import get_path_with_links
from apps.repo.utils.system.object import get_system_home_folder, get_system_root_folder


class FolderModelTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()

        self.test_folder = Folder.objects.create(
            name="Test folder",
            parent=get_system_home_folder(),
            owner=self.test_user,
        )

        self.test_subfolder = Folder.objects.create(
            name="Subfolder 1",
            parent=self.test_folder,
            owner=self.test_user,
        )

    def test_get_path_with_links(self):
        root_folder = get_system_root_folder()

        self.assertTrue(
            "ROOT"
            in get_path_with_links(
                root_folder,
                self.test_user,
            )
        )

    def test_str(self):
        self.assertTrue("Test folder" in self.test_folder.__str__())

    def test_has_children(self):
        self.assertTrue(self.test_folder.has_children())
        self.test_subfolder.delete()
        self.assertFalse(self.test_folder.has_children())


class FolderModelMethodsTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.parent_folder = get_test_folder(
            parent=self.test_user.profile.home_folder, owner=self.test_user
        )
        self.test_documents = []
        self.test_folders = []
        for i in range(3):
            self.test_folders.append(
                get_test_folder(
                    name=f"Folder {i}",
                    parent=self.parent_folder,
                )
            )
        for i in range(3):
            self.test_documents.append(
                get_test_document(
                    name=f"Document {i}",
                    parent=self.parent_folder,
                )
            )

    def test_get_children(self):
        self.assertEqual(len(self.test_documents), 3)
        self.assertEqual(len(self.test_folders), 3)
        children = self.parent_folder.get_children(search_term="1")
        self.assertEqual(len(children), 2)
