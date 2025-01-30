from django.test import Client, TestCase
from django.urls import reverse

from apps.repo.models.element.document import Document
from apps.repo.models.element.version import Version
from apps.repo.tests.utils import TEST_USER, get_test_folder, get_test_user


class AddDocumentViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.client = Client()
        self.test_folder = get_test_folder()

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.get(
            reverse(
                "repo:add_document",
                args=[
                    self.test_folder.id,
                ],
            ),
        )
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        test_content = b"Hello world"
        response = self.client.post(
            reverse(
                "repo:create_document",
                args=[
                    self.test_folder.id,
                ],
            ),
            data={
                "name": "TestDocument.txt",
                # "content_file": test_file,
                "content": test_content,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.test_document = Document.objects.get(
            name="TestDocument.txt",
        )
        self.assertTrue(self.test_document)
        self.assertTrue(Version.objects.get(parent=self.test_document))


class CreateDocumentViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.client = Client()
        self.test_folder = get_test_folder()

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.get(
            reverse(
                "repo:create_document",
                args=[
                    self.test_folder.id,
                ],
            ),
        )
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        test_content = b"Hello world"
        response = self.client.post(
            reverse(
                "repo:create_document",
                args=[
                    self.test_folder.id,
                ],
            ),
            data={
                "name": "TestDocument.txt",
                # "content_file": test_file,
                "content": test_content,
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
        test_content = b"Hello world"
        response = self.client.post(
            reverse(
                "repo:create_document",
                args=[
                    self.test_folder.id,
                ],
            ),
            data={
                # "name": "TestDocument.txt",
                # "content_file": test_file,
                "content": test_content,
            },
        )
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Document.DoesNotExist):
            self.test_document = Document.objects.get(
                name="TestDocument.txt",
            )
