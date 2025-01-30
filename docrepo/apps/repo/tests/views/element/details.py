from django.test import Client, TestCase
from django.urls import reverse

from apps.repo.tests.utils import (
    TEST_USER,
    get_test_document,
    get_test_folder,
    get_test_user,
)


class ElementDetailsViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.client = Client()
        self.test_folder = get_test_folder()
        self.test_document = get_test_document()

    def test_get_folder(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.get(
            reverse(
                "repo:element_details",
                args=[
                    self.test_folder.type,
                    self.test_folder.id,
                ],
            )
        )
        self.assertTrue(response.status_code, 200)

    def test_get_document(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.get(
            reverse(
                "repo:element_details",
                args=[
                    self.test_document.type,
                    self.test_document.id,
                ],
            )
        )
        self.assertTrue(response.status_code, 200)
