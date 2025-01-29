from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TestCase

from apps.repo.models.element.folder import Folder
from apps.repo.tests.utils import get_test_user
from apps.repo.utils.validation import has_duplicate_peers


class DuplicateTopLevelPeerTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_folder = Folder.objects.create(
            name="Folder 1",
            owner=self.test_user,
            parent=self.test_user.profile.home_folder,
        )

    def test_create_duplicate_root_peer(self):
        with self.assertRaises(ValidationError):
            Folder.objects.create(
                name="Peer",
                owner=self.test_user,
                parent=None,
            )

    def test_create_duplicate_peers(self):
        with self.assertRaises(IntegrityError):
            Folder.objects.create(
                name="Folder 1",
                owner=self.test_user,
                parent=self.test_user.profile.home_folder,
            )

    def test_has_duplicate_peers(self):
        self.subfolder = Folder.objects.create(
            name="Folder 2",
            owner=self.test_user,
            parent=self.test_user.profile.home_folder,
        )
        self.assertTrue(
            has_duplicate_peers(
                self.test_user.profile.home_folder,
                "Folder 2",
            )
        )
        self.assertFalse(
            has_duplicate_peers(
                self.test_user.profile.home_folder,
                "Folder 3",
            )
        )
