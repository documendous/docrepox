from django.test import TestCase, Client
from django.urls import reverse

from apps.repo.tests.utils import (
    TEST_USER,
    get_test_document,
    get_test_folder,
    get_test_user,
)


class EmptyRecycleFolderViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.client = Client()
        self.test_folder = get_test_folder()
        self.test_document = get_test_document()
        self.recycle_folder = self.test_user.profile.recycle_folder
        self.test_folder.parent = self.recycle_folder
        self.test_folder.save()
        self.test_folder.refresh_from_db()

    def test_delete(self):
        self.assertEqual(self.recycle_folder.name, "Recycle")
        self.assertEqual(len(self.recycle_folder.get_children()), 1)
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.post(
            reverse(
                "repo:empty_recycle_folder",
                args=[
                    self.recycle_folder.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.recycle_folder.get_children(), [])

    def test_against_non_recycle_folder(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.post(
            reverse(
                "repo:empty_recycle_folder",
                args=[
                    self.test_folder.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 404)


class DeleteElementViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.client = Client()
        self.test_folder = get_test_folder()
        self.test_document = get_test_document()
        self.recycle_folder = self.test_user.profile.recycle_folder
        self.test_folder.parent = self.recycle_folder
        self.test_folder.save()
        self.test_folder.refresh_from_db()

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.post(
            reverse("repo:delete_element", args=["folder", self.test_folder.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.recycle_folder.get_children(), [])
