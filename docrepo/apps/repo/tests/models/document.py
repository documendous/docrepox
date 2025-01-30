from django.test import TestCase

from apps.repo.models.element.version import Version
from apps.repo.tests.utils import get_test_document, get_test_user


class DocumentModelTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_document = get_test_document()
        test_versions = Version.objects.filter(parent=self.test_document).order_by(
            "-created"
        )
        self.test_latest_version = test_versions[0]

    def test_document_size(self):
        self.assertEqual(
            self.test_latest_version.content_file.size,
            self.test_document.document_size(),
        )
