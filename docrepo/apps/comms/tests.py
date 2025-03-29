from django.test import TestCase
from django.urls import reverse

from apps.repo.tests.utils import TEST_USER, get_test_user


class CommListViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.get(reverse("repo:comms:comm_list"))
        self.assertEqual(response.status_code, 200)
