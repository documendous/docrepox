# from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from apps.repo.settings import ADMIN_PASSWORD, ADMIN_USERNAME
from apps.repo.tests.utils import (
    TEST_USER,
    get_test_document,
    get_test_folder,
    get_test_user,
)
from apps.repo.models.element.folder import Folder
from apps.repo.utils.system.object import get_admin_user, get_system_projects_folder


User = get_user_model()


class FolderViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.admin_user = get_admin_user()
        self.shady_user = User.objects.create(username="shady_user")
        self.shady_user.set_password("shady_pass")
        self.shady_user.save()
        self.client = Client()
        self.test_folder = get_test_folder()
        self.test_document = get_test_document()
        self.projects_folder = get_system_projects_folder()

    def test_get_system_project_folder(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.get(
            reverse(
                "repo:folder",
                args=[
                    self.projects_folder.id,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.client.logout()

        self.client.login(
            username=ADMIN_USERNAME,
            password=ADMIN_PASSWORD,
        )
        response = self.client.get(
            reverse(
                "repo:folder",
                args=[
                    self.projects_folder.id,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.get(
            reverse(
                "repo:folder",
                args=[
                    self.test_folder.id,
                ],
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_get_with_sorting(self):
        self.test_document.parent = self.test_folder
        self.test_document.save()

        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.get(
            reverse(
                "repo:folder",
                args=[
                    self.test_folder.id,
                ],
            )
            + "?order_by=name"
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse(
                "repo:folder",
                args=[
                    self.test_folder.id,
                ],
            )
            + "?order_by=title"
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse(
                "repo:folder",
                args=[
                    self.test_folder.id,
                ],
            )
            + "?order_by=created"
        )
        self.assertEqual(response.status_code, 200)

    # def test_get_system_project_folder_with_admin_user(self):
    #     self.client.login(
    #         username=settings.ADMIN_USERNAME,
    #         password=settings.ADMIN_PASSWORD,
    #     )
    #     response = self.client.get(
    #         reverse(
    #             "repo:folder",
    #             args=[
    #                 self.projects_folder.id,
    #             ],
    #         )
    #     )
    #     self.assertEqual(response.status_code, 200)

    def test_get_nonowner_user(self):
        self.client.login(
            username="shady_user",
            password="shady_pass",
        )
        response = self.client.get(
            reverse(
                "repo:folder",
                args=[
                    self.test_folder.id,
                ],
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.post(
            reverse(
                "repo:folder",
                args=[
                    self.test_folder.id,
                ],
            ),
            data={
                "name": "Test Folder 2",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Folder.objects.get(name="Test Folder 2"))

    def test_post_invalid_data(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.post(
            reverse(
                "repo:folder",
                args=[
                    self.test_folder.id,
                ],
            ),
            data={},
        )
        self.assertEqual(response.status_code, 200)
