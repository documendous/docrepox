from django.test import TestCase
from django.urls import reverse

from apps.core.utils.htmx import ALLOWED_HEADERS, htmx_redirect, hx_response
from apps.repo.tests.utils import get_test_user


class HTMXRedirectTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_folder = self.test_user.profile.home_folder

    def test_htmx_redirect(self):
        """Test that HTMX redirect sets correct headers and status code."""
        url_name = "repo:folder"

        url_args = [
            self.test_folder.pk,
        ]

        response = htmx_redirect(reverse(url_name, args=url_args))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["HX-Redirect"], reverse(url_name, args=url_args))
        self.assertEqual(response["Content-Type"], "text/html")
        self.assertEqual(response.content.decode("utf-8"), "")

    def test_hx_response_invalid_header(self):
        """Test that hx_response raises ValueError for invalid headers."""
        invalid_header = "HX-Invalid-Header"

        with self.assertRaises(ValueError) as context:
            hx_response(
                status_code=200,
                content="Test Content",
                **{invalid_header: "some_value"},
            )

        expected_message = (
            f"Header '{invalid_header}' is not allowed. "
            f"Allowed headers are: {', '.join(ALLOWED_HEADERS)}."
        )

        self.assertEqual(str(context.exception), expected_message)
