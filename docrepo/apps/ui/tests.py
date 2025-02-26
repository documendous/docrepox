from django.test import Client, TestCase
from django.urls import reverse

from apps.repo.tests.utils import TEST_USER, get_test_user

from .models import Setting


class ModifySettingsViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.client = Client()

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )

        response = self.client.get(
            reverse("ui:modify_setting", args=["show_welcome", "true"]),
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Setting.objects.get(key="show_welcome", user=self.test_user, value="true")
        )

    def test_get_with_next(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )

        response = self.client.get(
            reverse("ui:modify_setting", args=["show_welcome", "true"]) + "?next=index",
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Setting.objects.get(key="show_welcome", user=self.test_user, value="true")
        )
