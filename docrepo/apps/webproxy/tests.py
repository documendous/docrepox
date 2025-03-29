from django.test import TestCase
from django.urls import reverse

from apps.repo.tests.utils import TEST_USER, get_test_document, get_test_user

from .models import ProxiedDocument


class DownloadProxiedDocumentViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_document = get_test_document(
            parent=self.test_user.profile.home_folder
        )

    def _set_proxy(self):
        self.proxied_document = ProxiedDocument.objects.create(
            document=self.test_document, manager=self.test_user
        )

    def test_get(self):
        """Should not need a login"""
        # no proxy:
        response = self.client.get(
            reverse(
                "repo:webproxy:download_proxied_document",
                args=[self.test_document.pk],
            )
        )
        self.assertEqual(response.status_code, 404)

        self._set_proxy()

        response = self.client.get(
            reverse(
                "repo:webproxy:download_proxied_document",
                args=[self.test_document.pk],
            )
        )

        self.assertEqual(response.status_code, 200)
        streamed_content = b"".join(response.streaming_content)
        self.assertTrue(b"Hello world" in streamed_content)


class AddProxiedDocumentViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_document = get_test_document(
            parent=self.test_user.profile.home_folder
        )

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.get(
            reverse("repo:webproxy:add_webproxy_document", args=[self.test_document.pk])
        )
        self.assertEqual(response.status_code, 302)

        self.assertTrue(ProxiedDocument.objects.get(document=self.test_document))


class RemoveProxiedDocumentView(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_document = get_test_document(
            parent=self.test_user.profile.home_folder
        )

    def _set_proxy(self):
        self.proxied_document = ProxiedDocument.objects.create(
            document=self.test_document, manager=self.test_user
        )

    def test_get(self):
        self._set_proxy()

        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.get(
            reverse(
                "repo:webproxy:remove_webproxy_document", args=[self.test_document.pk]
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            ProxiedDocument.objects.filter(
                document=self.test_document, manager=self.test_user
            ).exists()
        )


class ProxiedDocumentListViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        for i in range(3):
            self.test_document = get_test_document(
                name=f"ExampleDoc{i}.txt", parent=self.test_user.profile.home_folder
            )
            self.proxied_document = ProxiedDocument.objects.create(
                document=self.test_document, manager=self.test_user
            )

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.get(reverse("repo:webproxy:proxied_document_list"))
        self.assertEqual(response.status_code, 200)
