import os
import shutil

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand


class ContentFileCheck:
    def __init__(self, app_name, model_name):
        self.app_name = app_name
        self.model_name = model_name

    def check(self, path):
        Model = apps.get_model(self.app_name, self.model_name)
        return Model.objects.filter(content_file__iexact=path)


class Command(BaseCommand):
    help = "Remove orphaned content from the database. These are content files that no longer have an associated document version or rendition (thumbnail or preview file)"

    def _handle_orphaned_files(self, relative_path, full_file_path):
        self.orphaned_files.append(relative_path)
        target_file_path = os.path.join(self.deleted_orphan_folder, relative_path)
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
        shutil.move(full_file_path, target_file_path)
        self.stdout.write(self.style.WARNING(f"Moved: {relative_path}"))

    def _get_matches(self, relative_path):
        checks = [
            ("repo", "version"),
            ("transformations", "thumbnail"),
            ("transformations", "preview"),
        ]

        return [ContentFileCheck(*check).check(relative_path) for check in checks]

    def _process_file(self, root, file):
        full_file_path = os.path.join(root, file)

        relative_path = os.path.normpath(
            os.path.relpath(full_file_path, self.media_root)
        )

        self.stdout.write(f"Checking file: {relative_path}")

        if any(self._get_matches(relative_path)):
            self.stdout.write(self.style.SUCCESS(f"Found in DB: {relative_path}"))
        else:
            self._handle_orphaned_files(relative_path, full_file_path)

    def handle(self, *args, **kwargs):
        self.media_root = settings.MEDIA_ROOT
        self.deleted_orphan_folder = settings.DELETED_ORPHAN_FOLDER

        if not os.path.isdir(self.media_root):
            self.stdout.write(self.style.ERROR("MEDIA_ROOT directory not found."))
            return

        if not os.path.exists(self.deleted_orphan_folder):
            os.makedirs(self.deleted_orphan_folder)

            self.stdout.write(
                self.style.SUCCESS(f"Created folder: {self.deleted_orphan_folder}")
            )

        self.stdout.write("Finding and moving orphaned files...")

        self.orphaned_files = []

        for root, _, files in os.walk(os.path.join(self.media_root, "content")):
            for file in files:
                self._process_file(root, file)

        self.stdout.write(f"Moved {len(self.orphaned_files)} orphaned files.")
        self.stdout.write("Done")
