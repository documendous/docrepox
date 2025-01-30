from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase
from django.urls import reverse

from apps.bookmarks.models import Bookmark
from apps.repo.models.element.folder import Folder
from apps.repo.tests.utils import get_test_document, get_test_project, get_test_user
from apps.repo.utils.system.object import get_system_home_folder

User = get_user_model()


class RemoveBookmarkViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create(username="testuser")
        self.test_user.set_password("testpass")
        self.test_user.save()
        home_folder = get_system_home_folder()
        self.folder = Folder.objects.create(
            name="Test Folder", parent=home_folder, owner=self.test_user
        )

    def test_post(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            reverse(
                "repo:bookmarks:set_bookmark",
                args=[
                    self.folder.type,
                    self.folder.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)
        content_type = ContentType.objects.get_for_model(self.folder)
        self.assertTrue(
            Bookmark.objects.get(
                owner=self.test_user,
                content_type=content_type,
                object_id=self.folder.id,
            )
        )

        response = self.client.post(
            reverse(
                "repo:bookmarks:remove_bookmark",
                args=[
                    self.folder.type,
                    self.folder.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)
        content_type = ContentType.objects.get_for_model(self.folder)
        with self.assertRaises(Bookmark.DoesNotExist):
            Bookmark.objects.get(
                owner=self.test_user,
                content_type=content_type,
                object_id=self.folder.id,
            )

    def test_post_with_project_document(self):
        project = get_test_project()
        test_document = get_test_document()
        test_user = get_test_user()
        test_document.parent = project.folder
        test_document.save()
        self.client.login(username="testuser1", password="testpass")
        response = self.client.post(
            reverse(
                "repo:bookmarks:set_bookmark",
                args=[
                    test_document.type,
                    test_document.pk,
                ],
            )
        )

        self.assertTrue(Bookmark.objects.get(owner=test_user))

        get_test_user(username="testuser2")
        self.client.login(username="testuser2", password="testpass")

        response = self.client.post(
            reverse(
                "repo:bookmarks:remove_bookmark",
                args=[
                    test_document.type,
                    test_document.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 404)

        content_type = ContentType.objects.get_for_model(test_document)
        self.assertTrue(
            Bookmark.objects.get(
                owner=test_user,
                content_type=content_type,
                object_id=test_document.id,
            )
        )

    def test_post_not_owner(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            reverse(
                "repo:bookmarks:set_bookmark",
                args=[
                    self.folder.type,
                    self.folder.pk,
                ],
            )
        )

        get_test_user(username="testuser2")
        self.client.login(username="testuser2", password="testpass")
        response = self.client.post(
            reverse(
                "repo:bookmarks:remove_bookmark",
                args=[
                    self.folder.type,
                    self.folder.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 404)
        content_type = ContentType.objects.get_for_model(self.folder)
        self.assertTrue(
            Bookmark.objects.get(
                owner=self.test_user,
                content_type=content_type,
                object_id=self.folder.id,
            )
        )
