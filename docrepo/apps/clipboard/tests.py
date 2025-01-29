from django.test import Client, TestCase
from django.urls import reverse

from apps.clipboard.utils.clipboard import is_in_clipboard
from apps.repo.models.element.document import Document
from apps.repo.models.element.folder import Folder
from apps.repo.tests.utils import (
    TEST_USER,
    get_test_document,
    get_test_folder,
    get_test_user,
)

from .models import (  # , PastedDocument, PastedFolder
    Clipboard,
    PastedDocument,
    PastedFolder,
)


class AddElementClipboardViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.client = Client()
        self.test_folder = get_test_folder(parent=self.test_user.profile.home_folder)
        self.test_document = get_test_document()
        self.target_folder = Folder.objects.create(
            name="target",
            owner=self.test_user,
            parent=self.test_user.profile.home_folder,
        )
        self.test_sub_document = get_test_document(name="Random1.txt")
        self.test_sub_document.parent = self.test_folder
        self.test_sub_document.save()
        self.test_sub_folder = get_test_folder(name="Random11")
        self.test_sub_folder.parent = self.test_folder
        self.test_sub_folder.save()

    def test_post_paste_move_to_same_parent(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.post(
            reverse(
                "repo:clipboard:add_element_to_clipboard",
                args=[
                    "folder",
                    self.test_folder.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            reverse(
                "repo:clipboard:paste_move_elements",
                args=[self.test_folder.pk],
            )
        )

        self.test_folder.refresh_from_db()
        self.assertEqual(self.test_folder.parent, self.test_user.profile.home_folder)

    def test_post_paste_copy_to_same_parent(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.post(
            reverse(
                "repo:clipboard:add_element_to_clipboard",
                args=[
                    "folder",
                    self.test_folder.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            reverse(
                "repo:clipboard:paste_copy_elements",
                args=[self.test_folder.pk],
            )
        )

        self.test_folder.refresh_from_db()
        self.assertEqual(self.test_folder.parent, self.test_user.profile.home_folder)
        self.assertFalse(self.target_folder.get_children())

    def test_post_paste_move(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.post(
            reverse(
                "repo:clipboard:add_element_to_clipboard",
                args=[
                    "document",
                    self.test_document.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            reverse(
                "repo:clipboard:add_element_to_clipboard",
                args=[
                    "folder",
                    self.test_folder.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)

        clipboard = Clipboard.objects.get(user=self.test_user)
        self.assertTrue(clipboard.documents.all())
        self.assertTrue(clipboard.folders.all())

        response = self.client.post(
            reverse(
                "repo:clipboard:paste_move_elements",
                args=[self.target_folder.pk],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.test_document.refresh_from_db()
        self.test_folder.refresh_from_db()
        self.assertEqual(self.test_document.parent, self.target_folder)
        self.assertEqual(self.test_folder.parent, self.target_folder)

    def test_post_paste_copy(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.post(
            reverse(
                "repo:clipboard:add_element_to_clipboard",
                args=[
                    "document",
                    self.test_document.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            reverse(
                "repo:clipboard:add_element_to_clipboard",
                args=[
                    "folder",
                    self.test_folder.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)

        clipboard = Clipboard.objects.get(user=self.test_user)
        self.assertTrue(clipboard.documents.all())
        self.assertTrue(clipboard.folders.all())

        response = self.client.post(
            reverse(
                "repo:clipboard:paste_copy_elements",
                args=[self.target_folder.pk],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.test_document.refresh_from_db()
        self.test_folder.refresh_from_db()
        self.assertTrue(Document.objects.filter(parent=self.target_folder.pk))
        self.assertTrue(Folder.objects.filter(parent=self.target_folder.pk))

    def test_post_dup_document(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.post(
            reverse(
                "repo:clipboard:add_element_to_clipboard",
                args=[
                    "document",
                    self.test_document.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.post(
            reverse(
                "repo:clipboard:add_element_to_clipboard",
                args=[
                    "document",
                    self.test_document.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)

    def test_post_dup_folder(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )

        response = self.client.post(
            reverse(
                "repo:clipboard:add_element_to_clipboard",
                args=[
                    "folder",
                    self.test_folder.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            reverse(
                "repo:clipboard:add_element_to_clipboard",
                args=[
                    "folder",
                    self.test_folder.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)


class RecycleElementViewTestWithClipboardTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.home_user_folder = self.test_user.profile.home_folder
        self.test_document = get_test_document(parent=self.home_user_folder)
        self.test_folder = get_test_folder(parent=self.home_user_folder)
        self.clipboard, _ = Clipboard.objects.get_or_create(user=self.test_user)
        pasted_document = PastedDocument.objects.create(document=self.test_document)
        pasted_folder = PastedFolder.objects.create(folder=self.test_folder)
        self.clipboard.documents.add(pasted_document)
        self.clipboard.folders.add(pasted_folder)

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )

        response = self.client.post(
            reverse(
                "repo:recycle_element",
                args=[self.test_folder.type, self.test_folder.id],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.test_folder.refresh_from_db()
        self.assertFalse(is_in_clipboard(self.test_user, element=self.test_folder))

        response = self.client.post(
            reverse(
                "repo:recycle_element",
                args=[self.test_document.type, self.test_document.id],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.test_document.refresh_from_db()
        self.assertFalse(is_in_clipboard(self.test_user, element=self.test_document))
