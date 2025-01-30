from django.test import Client, TestCase
from django.urls import reverse

from apps.repo.tests.utils import (
    TEST_USER,
    get_test_document,
    get_test_folder,
    get_test_project,
    get_test_user,
)
from apps.repo.utils.system.object import get_user_recycle_folder


class UpdateElementDetailsViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_user2 = get_test_user(username="Nonmember")
        self.client = Client()
        self.test_folder = get_test_folder()
        self.test_document = get_test_document()
        self.test_project = get_test_project()

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.get(
            reverse(
                "repo:update_element",
                args=[
                    self.test_folder.type,
                    self.test_folder.id,
                ],
            )
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse(
                "repo:update_element",
                args=[
                    self.test_document.type,
                    self.test_document.id,
                ],
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_get_non_project_member(self):
        self.client.login(
            username="Nonmember",
            password="testpass",
        )
        response = self.client.get(
            reverse(
                "repo:update_element",
                args=[
                    self.test_folder.type,
                    self.test_folder.id,
                ],
            )
        )
        self.assertEqual(response.status_code, 404)
        response = self.client.get(
            reverse(
                "repo:update_element",
                args=[
                    self.test_document.type,
                    self.test_document.id,
                ],
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_get_with_project(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.get(
            reverse(
                "repo:update_element",
                args=[
                    self.test_project.folder.type,
                    self.test_project.folder.id,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.post(
            reverse(
                "repo:update_element",
                args=[
                    self.test_folder.type,
                    self.test_folder.id,
                ],
            ),
            data={
                "name": "Example Folder Name",
                "title": "Example title",
                "description": "Example description",
            },
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.post(
            reverse(
                "repo:update_element",
                args=[
                    self.test_document.type,
                    self.test_document.id,
                ],
            ),
            data={
                "name": "ExampleDoc.docx",
                "title": "Example title",
                "description": "Example description",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_post_in_recycle_folder(self):
        recycle_folder = get_user_recycle_folder(user=self.test_user)
        self.test_folder.parent = recycle_folder
        self.test_folder.save()

        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.post(
            reverse(
                "repo:update_element",
                args=[
                    self.test_folder.type,
                    self.test_folder.id,
                ],
            ),
            data={
                "name": "Example Folder Name",
                "title": "Example title",
                "description": "Example description",
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_post_with_form_errors(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.post(
            reverse(
                "repo:update_element",
                args=[
                    self.test_folder.type,
                    self.test_folder.id,
                ],
            ),
            data={
                "title": "Example title",
                "description": "Example description",
            },
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse(
                "repo:update_element",
                args=[
                    self.test_document.type,
                    self.test_document.id,
                ],
            ),
            data={
                "title": "Example title",
                "description": "Example description",
            },
        )
        self.assertEqual(response.status_code, 200)
