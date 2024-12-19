from django.test import TestCase
from apps.projects.models import Project
from apps.projects.templatetags.project_tags import is_a_project_folder
from apps.repo.tests.utils import get_test_document, get_test_folder, get_test_user


class ProjectTagsTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_folder = get_test_folder()
        self.test_document = get_test_document()
        self.test_project = Project.objects.create(
            name="test project",
            visibility="public",
            owner=self.test_user,
        )

    def test_is_a_project_folder(self):
        self.assertTrue(is_a_project_folder(self.test_project.folder))

    def test_is_not_a_project_folder(self):
        self.assertFalse(is_a_project_folder(self.test_folder))

    def test_is_a_project_folder_project_type(self):
        self.assertTrue(is_a_project_folder(self.test_project))

    def test_is_a_project_folder_document_type(self):
        self.assertFalse(is_a_project_folder(self.test_document))
