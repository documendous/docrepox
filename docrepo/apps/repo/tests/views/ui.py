from django.test import Client, TestCase
from django.urls import reverse

from apps.repo.tests.utils import TEST_USER, get_test_user


class IndexViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.client = Client()

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.get(reverse("repo:index"))
        self.assertTrue(response.status_code, 200)
