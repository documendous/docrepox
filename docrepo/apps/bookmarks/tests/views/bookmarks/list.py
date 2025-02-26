from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from apps.bookmarks.models import Bookmark
from apps.repo.models.element.folder import Folder
from apps.repo.utils.system.object import get_system_home_folder

User = get_user_model()


class BookmarkListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create(username="testuser")
        self.test_user.set_password("testpass")
        self.test_user.save()
        home_folder = get_system_home_folder()
        self.folder = Folder.objects.create(
            name="Test Folder", parent=home_folder, owner=self.test_user
        )
        Bookmark.objects.create(
            owner=self.test_user,
            content_object=self.folder,
        )

    def test_get(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(
            reverse(
                "repo:bookmarks:bookmark_list",
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Test Folder" in response.content)
