from django.test import Client, TestCase
from django.urls import reverse

from apps.comments.models import Comment
from apps.projects.models import Project
from apps.repo.tests.utils import (
    TEST_USER,
    get_test_document,
    get_test_folder,
    get_test_user,
)


class AddCommentViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_document = get_test_document()
        self.test_folder = get_test_folder()
        self.test_project = Project.objects.create(
            name="Test project", owner=self.test_user, visibility="public"
        )

    def test_post_document(self):
        self.client.login(username="testuser1", password="testpass")
        response = self.client.post(
            reverse(
                "repo:comments:add_comment",
                args=[
                    "document",
                    self.test_document.pk,
                ],
            ),
            data={
                "content": "Example content",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"testuser1" in response.content)
        self.assertTrue(b"Example content" in response.content)

    def test_post_folder(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.post(
            reverse(
                "repo:comments:add_comment",
                args=[
                    "folder",
                    self.test_folder.pk,
                ],
            ),
            data={
                "content": "Example content",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"testuser1" in response.content)
        self.assertTrue(b"Example content" in response.content)

    def test_post_project(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.post(
            reverse(
                "repo:comments:add_comment",
                args=[
                    "project",
                    self.test_project.pk,
                ],
            ),
            data={
                "content": "Example content",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"testuser1" in response.content)
        self.assertTrue(b"Example content" in response.content)


class DeleteCommentViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_document = get_test_document()
        self.test_folder = get_test_folder()
        self.test_project = Project.objects.create(
            name="Test project", owner=self.test_user, visibility="public"
        )
        self.client = Client()

    def test_post_with_document(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        self.client.post(
            reverse(
                "repo:comments:add_comment",
                args=[
                    "document",
                    self.test_document.pk,
                ],
            ),
            data={
                "content": "Example content",
            },
        )
        comment = Comment.objects.get(content="Example content", author=self.test_user)
        self.client.post(
            reverse(
                "repo:comments:delete_comment",
                args=[
                    comment.pk,
                    "document",
                    self.test_document.pk,
                ],
            )
        )
        with self.assertRaises(Comment.DoesNotExist):
            comment = Comment.objects.get(
                content="Example content", author=self.test_user
            )

    def test_post_with_folder(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        self.client.post(
            reverse(
                "repo:comments:add_comment",
                args=[
                    "folder",
                    self.test_folder.pk,
                ],
            ),
            data={
                "content": "Example content",
            },
        )
        comment = Comment.objects.get(content="Example content", author=self.test_user)
        self.client.post(
            reverse(
                "repo:comments:delete_comment",
                args=[
                    comment.pk,
                    "folder",
                    self.test_folder.pk,
                ],
            )
        )
        with self.assertRaises(Comment.DoesNotExist):
            comment = Comment.objects.get(
                content="Example content", author=self.test_user
            )

    def test_post_with_project(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        self.client.post(
            reverse(
                "repo:comments:add_comment",
                args=[
                    "folder",
                    self.test_project.folder.pk,
                ],
            ),
            data={
                "content": "Example content",
            },
        )
        comment = Comment.objects.get(content="Example content", author=self.test_user)
        self.client.post(
            reverse(
                "repo:comments:delete_comment",
                args=[
                    comment.pk,
                    "folder",
                    self.test_project.folder.pk,
                ],
            )
        )
        with self.assertRaises(Comment.DoesNotExist):
            comment = Comment.objects.get(
                content="Example content", author=self.test_user
            )
