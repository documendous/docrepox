from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase
from django.urls import reverse

from apps.bookmarks.models import Bookmark
from apps.repo.models.element.folder import Folder
from apps.repo.tests.utils import (
    TEST_USER,
    get_test_document,
    get_test_folder,
    get_test_recycle_folder,
    get_test_user,
)

User = get_user_model()


class RecycleElementFlowTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.client = Client()
        self.user_home_folder = self.test_user.profile.home_folder
        self.test_folder = get_test_folder(parent=self.user_home_folder)
        self.test_document = get_test_document(parent=self.user_home_folder)

    def test_post_recycle_element_folder(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )

        response = self.client.post(
            reverse(
                "repo:recycle_element",
                args=[
                    "folder",
                    self.test_folder.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.test_folder.refresh_from_db()
        self.assertEqual(self.test_folder.parent.name, "Recycle")

        response = self.client.post(
            reverse(
                "repo:restore_element",
                args=[
                    "folder",
                    self.test_folder.pk,
                ],
            )
        )

        self.test_folder.refresh_from_db()
        self.assertEqual(self.test_folder.parent, self.user_home_folder)

        response = self.client.post(
            reverse(
                "repo:recycle_element",
                args=[
                    "folder",
                    self.test_folder.pk,
                ],
            )
        )

        self.client.post(
            reverse(
                "repo:delete_element",
                args=[
                    "folder",
                    self.test_folder.pk,
                ],
            )
        )

        with self.assertRaises(self.test_folder.DoesNotExist):
            self.test_folder.refresh_from_db()

    def test_delete_without_recycle(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )

        response = self.client.post(
            reverse(
                "repo:delete_element",
                args=[
                    "folder",
                    self.test_folder.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 404)

        response = self.client.post(
            reverse(
                "repo:delete_element",
                args=[
                    "document",
                    self.test_document.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_restore_without_recycle(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )

        response = self.client.post(
            reverse(
                "repo:restore_element",
                args=[
                    "folder",
                    self.test_folder.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 404)

        response = self.client.post(
            reverse(
                "repo:restore_element",
                args=[
                    "document",
                    self.test_document.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_post_recycle_element_document(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )

        response = self.client.post(
            reverse(
                "repo:recycle_element",
                args=[
                    "document",
                    self.test_document.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.test_document.refresh_from_db()
        self.assertEqual(self.test_document.parent.name, "Recycle")

        response = self.client.post(
            reverse(
                "repo:restore_element",
                args=[
                    "document",
                    self.test_document.pk,
                ],
            )
        )

        self.test_document.refresh_from_db()
        self.assertEqual(self.test_document.parent, self.user_home_folder)

        response = self.client.post(
            reverse(
                "repo:recycle_element",
                args=[
                    "document",
                    self.test_document.pk,
                ],
            )
        )

        self.client.post(
            reverse(
                "repo:delete_element",
                args=[
                    "document",
                    self.test_document.pk,
                ],
            )
        )

        with self.assertRaises(self.test_document.DoesNotExist):
            self.test_document.refresh_from_db()

    def test_with_wrong_user(self):
        self.client.login(
            username="testuser2",
            password=TEST_USER["password"],
        )

        response = self.client.post(
            reverse(
                "repo:recycle_element",
                args=[
                    "document",
                    self.test_document.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 404)


class RestoreElementsViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.user_home_folder = self.test_user.profile.home_folder
        self.recycle_folder = self.test_user.profile.recycle_folder
        self.test_document = get_test_document(parent=self.user_home_folder)
        self.test_folder = get_test_folder(parent=self.user_home_folder)

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        self.client.post(
            reverse("repo:recycle_elements", args=[self.user_home_folder.pk])
        )
        self.test_folder.refresh_from_db()
        self.assertEqual(self.test_folder.parent.name, "Recycle")
        self.test_document.refresh_from_db()
        self.assertEqual(self.test_document.parent.name, "Recycle")

        response = self.client.post(
            reverse("repo:restore_elements", args=[self.recycle_folder.pk])
        )
        self.assertEqual(response.status_code, 302)

        self.test_folder.refresh_from_db()
        self.assertEqual(self.test_folder.parent.name, "testuser1")
        self.test_document.refresh_from_db()
        self.assertEqual(self.test_document.parent.name, "testuser1")


class RecycleElementsViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.home_folder = self.test_user.profile.home_folder
        self.test_folder = get_test_folder(
            name="Example Folder", parent=self.home_folder
        )
        self.test_document = get_test_document(
            name="Example.txt", parent=self.home_folder
        )

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.post(
            reverse("repo:recycle_elements", args=[self.home_folder.id])
        )
        self.assertEqual(response.status_code, 302)
        self.test_folder.refresh_from_db()
        self.assertEqual(self.test_folder.parent.name, "Recycle")
        self.test_document.refresh_from_db()
        self.assertEqual(self.test_document.parent.name, "Recycle")


class RecycleFolderActionTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.client = Client()
        self.test_recycle_folder = get_test_recycle_folder(user=self.test_user)

    def test_restore(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )

        response = self.client.post(
            reverse(
                "repo:restore_element",
                args=[
                    self.test_recycle_folder.type,
                    self.test_recycle_folder.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )

        response = self.client.post(
            reverse(
                "repo:recycle_element",
                args=[
                    self.test_recycle_folder.type,
                    self.test_recycle_folder.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_perma_delete(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )

        response = self.client.post(
            reverse(
                "repo:delete_element",
                args=[
                    self.test_recycle_folder.type,
                    self.test_recycle_folder.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 404)


class RemoveBookmarkFromRecycledElementTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create(username="testuser")
        self.test_user.set_password("testpass")
        self.test_user.save()

        self.folder = Folder.objects.create(
            name="Test Folder",
            parent=self.test_user.profile.home_folder,
            owner=self.test_user,
        )

    def test_post(self):
        self.client.login(username="testuser", password="testpass")

        response = self.client.post(
            reverse(
                "repo:bookmarks:add_bookmark",
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
                "repo:recycle_element",
                args=[
                    "folder",
                    self.folder.pk,
                ],
            ),
            data={
                "element_type": "folder",
                "element_id": self.folder.pk,
            },
        )

        with self.assertRaises(Bookmark.DoesNotExist):
            Bookmark.objects.get(
                owner=self.test_user,
                content_type=content_type,
                object_id=self.folder.id,
            )
