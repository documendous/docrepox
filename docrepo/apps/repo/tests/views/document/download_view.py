from django.test import TestCase, Client
from django.urls import reverse
from apps.repo.tests.utils import (
    TEST_USER,
    get_test_user,
    get_test_document,
)


class RetrieveDocumentViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.client = Client()
        self.test_document = get_test_document()

    def test_get_as_download(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )

        response = self.client.get(
            reverse(
                "repo:retrieve_document",
                args=[
                    self.test_document.id,
                ],
            )
            + "?action=attachment"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Hello world" in response.content)

    def test_get_as_preview(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )

        response = self.client.get(
            reverse(
                "repo:retrieve_document",
                args=[
                    self.test_document.id,
                ],
            )
        )

        self.assertEqual(response.status_code, 200)
