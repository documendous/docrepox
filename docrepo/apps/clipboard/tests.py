from django.test import Client, TestCase
from django.urls import reverse

from apps.repo.models.element.document import Document

from .models import Clipboard  # , PastedDocument, PastedFolder
from apps.repo.models.element.folder import Folder
from apps.repo.tests.utils import (
    TEST_USER,
    get_test_document,
    get_test_folder,
    get_test_user,
)
from apps.repo.utils.system.object import get_system_root_folder


class AddElementClipboardViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.client = Client()
        self.test_folder = get_test_folder()
        self.test_document = get_test_document()
        self.target_folder = Folder.objects.create(
            name="target",
            owner=self.test_user,
            parent=get_system_root_folder(),
        )
        self.test_sub_document = get_test_document(name="Random1.txt")
        self.test_sub_document.parent = self.test_folder
        self.test_sub_document.save()
        self.test_sub_folder = get_test_folder(name="Random11")
        self.test_sub_folder.parent = self.test_folder
        self.test_sub_folder.save()

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

    # def test_copy_in_same_parent(self):
    #     clipboard = Clipboard.objects.create(user=self.test_user)
    #     parent = self.test_document.parent
    #     pasted_document = PastedDocument.objects.create(document=self.test_document)
    #     pasted_folder = PastedFolder.objects.create(folder=self.test_folder)
    #     clipboard.documents.add(pasted_document)
    #     clipboard.folders.add(pasted_folder)

    #     self.client.login(
    #         username=TEST_USER["username"], password=TEST_USER["password"]
    #     )
    #     response = self.client.post(
    #         reverse(
    #             "repo:clipboard:paste_copy_elements",
    #             args=[
    #                 parent.pk,
    #             ],
    #         )
    #     )

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
