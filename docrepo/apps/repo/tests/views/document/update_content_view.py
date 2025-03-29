from django.test import TestCase
from django.urls import reverse

from ....tests.utils import TEST_USER, get_test_document, get_test_user


class UpdateDocumentContentViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_document = get_test_document(
            parent=self.test_user.profile.home_folder
        )

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )

        response = self.client.get(
            reverse("repo:update_document_content", args=[self.test_document.pk])
        )

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )

        response = self.client.post(
            reverse("repo:update_document_content", args=[self.test_document.pk]),
            data={
                "name": "Test.txt",
                "content": "new content to go here",
                "change_type": "minor",
            },
        )

        self.assertEqual(response.status_code, 302)

    def test_post_invalid(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )

        response = self.client.post(
            reverse("repo:update_document_content", args=[self.test_document.pk]),
            data={
                "content": "new content to go here",
                "change_type": "minor",
            },
        )

        self.assertEqual(response.status_code, 200)
