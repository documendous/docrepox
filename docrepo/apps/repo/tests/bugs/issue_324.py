from django.test import Client, TestCase
from django.urls import reverse

from apps.projects.models import Project
from apps.repo.models.element.document import Document
from apps.repo.tests.utils import get_test_user


class ProjectOwnerCannotAddTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_user2 = get_test_user(username="testuser2")
        self.client = Client()
        self.client.login(username="testuser1", password="testpass")

    def test_issue(self):
        self.client.post(
            reverse("repo:projects:index"),
            data={
                "name": "Test Project",
                "visibility": "public",
            },
        )

        project = Project.objects.get(name="Test Project")
        self.assertTrue(project)

        response = self.client.get(
            reverse(
                "repo:folder",
                args=[
                    project.folder.pk,
                ],
            )
        )

        # Expect actions to show
        self.assertTrue(
            b"Upload one or more documents in this space" in response.content
        )

        response = self.client.post(
            reverse(
                "repo:create_document",
                args=[
                    project.folder.pk,
                ],
            ),
            data={
                "content": "sample text",
                "name": "Test.txt",
            },
        )

        # Expect document to be created
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Document.objects.get(name="Test.txt"))

        self.client.logout()

        # Expect non-member cannot create a document here
        self.client.login(username="testuser2", password="testpass")

        response = response = self.client.post(
            reverse(
                "repo:create_document",
                args=[
                    project.folder.pk,
                ],
            ),
            data={
                "content": "sample text",
                "name": "Test2.txt",
            },
        )

        self.assertEqual(response.status_code, 404)

        with self.assertRaises(Document.DoesNotExist):
            Document.objects.get(name="Test2.txt")
