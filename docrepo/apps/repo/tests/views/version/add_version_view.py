from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from apps.repo.models.element.document import Document
from apps.repo.tests.utils import TEST_USER, get_test_folder, get_test_user


class AddVersionViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.client = Client()
        self.test_folder = get_test_folder()

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )

        # Create a document with new file content version
        test_content = b"Hello world"
        test_file = SimpleUploadedFile("TestDocument.txt", test_content)

        self.client.post(
            reverse(
                "repo:create_document",
                args=[
                    self.test_folder.id,
                ],
            ),
            data={
                "name": "TestDocument.txt",
                "content_file": test_file,
            },
        )

        document = Document.objects.get(name="TestDocument.txt")

        # Create a new version (minor: 1.1)
        test_new_content = b"Version 2"
        test_file2 = SimpleUploadedFile("TestDocument.txt", test_new_content)

        response = self.client.post(
            reverse(
                "repo:add_version",
                args=[
                    document.pk,
                ],
            ),
            data={
                "content_file": test_file2,
                "change_type": "Minor",
            },
        )

        self.assertEqual(response.status_code, 302)
        document.refresh_from_db()
        self.assertEqual(document.current_version_tag, "1.1")

        # Create a new version (major: 2.0)
        test_new_content = b"Version 3"
        test_file3 = SimpleUploadedFile("TestDocument.txt", test_new_content)

        response = self.client.post(
            reverse(
                "repo:add_version",
                args=[
                    document.pk,
                ],
            ),
            data={
                "content_file": test_file3,
                "change_type": "Major",
            },
        )

        self.assertEqual(response.status_code, 302)
        document.refresh_from_db()
        self.assertEqual(document.current_version_tag, "2.0")
