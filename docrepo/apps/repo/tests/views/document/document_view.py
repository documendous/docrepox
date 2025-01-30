from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from apps.repo.models.element.document import Document
from apps.repo.models.element.version import Version
from apps.repo.tests.utils import TEST_USER, get_test_folder, get_test_user


class DocumentViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.client = Client()
        self.test_folder = get_test_folder()

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        test_content = b"Hello world"
        test_file = SimpleUploadedFile("TestDocument.txt", test_content)
        response = self.client.post(
            reverse(
                "repo:add_document",
                args=[
                    self.test_folder.id,
                ],
            ),
            data={
                "name": "TestDocument.txt",
                "content_file": test_file,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.test_document = Document.objects.get(
            name="TestDocument.txt",
        )
        self.assertTrue(self.test_document)
        self.assertTrue(Version.objects.get(parent=self.test_document))

    def test_post_invalid_data(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.post(
            reverse(
                "repo:add_document",
                args=[
                    self.test_folder.id,
                ],
            ),
            data={},
        )
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Document.DoesNotExist):
            Document.objects.get(
                name="TestDocument.txt",
            )
