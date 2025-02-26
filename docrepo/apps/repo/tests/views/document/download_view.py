from django.test import Client, TestCase
from django.urls import reverse

from apps.repo.tests.utils import TEST_USER, get_test_document, get_test_user


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
        streamed_content = b"".join(response.streaming_content)
        self.assertTrue(b"Hello world" in streamed_content)

    def test_get_as_nontrans_nonprev(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )

        test_document = get_test_document(ext="dll")

        response = self.client.get(
            reverse(
                "repo:retrieve_document",
                args=[
                    test_document.id,
                ],
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response["Content-Disposition"], 'attachment; filename="TestDocument.dll"'
        )

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
