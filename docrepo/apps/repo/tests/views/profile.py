from django.test import Client, TestCase
from django.urls import reverse

from apps.repo.tests.utils import TEST_USER, get_test_user


class UpdateProfileViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.client = Client()

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )

        response = self.client.get(reverse("repo:update_profile"))
        self.assertTrue(response.status_code, 200)

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )

        response = self.client.post(
            reverse("repo:update_profile"),
            data={
                "bio": "Example bio",
            },
        )

        self.assertTrue(response.status_code, 302)

    def test_post_no_login(self):
        response = self.client.post(
            reverse("repo:update_profile"),
            data={
                "bio": "Example bio",
            },
        )

        self.assertTrue(response.status_code, 302)
