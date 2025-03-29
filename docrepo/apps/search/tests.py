from django.test import Client, TestCase
from django.urls import reverse

from apps.projects.models import Project
from apps.repo.tests.utils import TEST_USER, get_test_document, get_test_user
from apps.repo.utils.system.object import get_admin_user

from ..search.models import DocumentIndex
from ..search.utils import index_documents


class SearchProjectsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = get_test_user()
        self.admin_user = get_admin_user()

        self.test_project1 = Project.objects.create(
            name="Test Project 1", owner=self.test_user
        )

    def test_simple_search(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )

        response = self.client.post(
            reverse("repo:search:search_projects"), data={"search_term": "Test"}
        )

        self.assertTrue(b"Test Project 1" in response.content)

    def test_admin_user_search(self):
        self.client.login(username="admin", password="admin")

        response = self.client.post(
            reverse("repo:search:search_projects"), data={"search_term": "private"}
        )

        self.assertTrue(b"private" in response.content.lower())

    def test_no_search_term_search(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )

        response = self.client.post(
            reverse("repo:search:search_projects"), data={"search_term": ""}
        )

        self.assertTrue(b"Test Project 1" in response.content)


class SearchElementsViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()

        self.test_project1 = Project.objects.create(
            name="Test Project 1", owner=self.test_user, visibility="public"
        )

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )

        response = self.client.post(
            reverse(
                "repo:search:search_elements",
                args=[
                    self.test_user.profile.home_folder.pk,
                ],
            ),
            data={"search_term": "Test"},
        )

        self.assertEqual(response.status_code, 200)

    def test_post_with_project(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )

        response = self.client.post(
            reverse(
                "repo:search:search_elements",
                args=[
                    self.test_project1.folder.pk,
                ],
            ),
            data={"search_term": "Test"},
        )

        self.assertEqual(response.status_code, 200)

    def test_post_empty_search_term(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )

        response = self.client.post(
            reverse(
                "repo:search:search_elements",
                args=[
                    self.test_user.profile.home_folder.pk,
                ],
            ),
        )

        self.assertEqual(response.status_code, 200)

    def test_post_with_project_empty_search_term(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )

        response = self.client.post(
            reverse(
                "repo:search:search_elements",
                args=[
                    self.test_project1.folder.pk,
                ],
            ),
        )

        self.assertEqual(response.status_code, 200)

    def test_post_with_admin_user(self):
        self.client.login(username="admin", password="admin")

        response = self.client.post(
            reverse(
                "repo:search:search_elements",
                args=[
                    self.test_user.profile.home_folder.pk,
                ],
            ),
            data={"search_term": "Test"},
        )

        self.assertEqual(response.status_code, 200)


class IndexDocumentsTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_document = get_test_document(
            parent=self.test_user.profile.home_folder
        )

    def test_index_documents(self):
        self.assertFalse(DocumentIndex.objects.all())
        index_documents()
        self.assertTrue(DocumentIndex.objects.all())


class AdvancedSearchViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_document = get_test_document(
            parent=self.test_user.profile.home_folder
        )

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.get(reverse("repo:search:advanced_search"))
        self.assertEqual(response.status_code, 200)

    def test_get_metadata_search(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.get(
            reverse("repo:search:advanced_search")
            + "?query=TestDocument&multi_type=document&multi_type=folder",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"TestDocument.txt" in response.content)

    # def test_get_fulltext_search(self):
    #     self.client.login(
    #         username=TEST_USER["username"], password=TEST_USER["password"]
    #     )
    #     response = self.client.get(
    #         reverse("repo:search:advanced_search") + "?full_text=Hello",
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(b"TestDocument" in response.content)
