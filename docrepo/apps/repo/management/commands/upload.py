import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from apps.repo.models.element.folder import Folder
from apps.repo.utils.document import create_document


class Command(BaseCommand):
    help = "Uploads a directory structure into the repository"

    def add_arguments(self, parser):
        parser.add_argument("source", type=str, help="Source directory to upload")
        parser.add_argument("target", type=str, help="Target folder path in repository")
        parser.add_argument("--owner", type=str, default="admin", help="Owner username")

    def handle(self, *args, **options):
        source_dir = options["source"]
        target_path = options["target"]
        owner_username = options["owner"]

        if not os.path.isdir(source_dir):
            raise CommandError(f"Source directory '{source_dir}' does not exist.")

        try:
            owner = User.objects.get(username=owner_username)
        except User.DoesNotExist:
            raise CommandError(f"User '{owner_username}' does not exist.")

        target_folder = self.get_existing_folder(target_path, owner)
        self.upload_directory(source_dir, target_folder, owner)

    def get_existing_folder(self, path: str, owner: User) -> Folder | None:
        parts = path.strip("/").split("/")
        parent = None
        folder = None

        for part in parts:
            try:
                # Fetch the folder while ensuring correct parent hierarchy
                folder = Folder.objects.get(name=part, parent=parent)
            except Folder.DoesNotExist:
                raise CommandError(f"Required folder '{path}' does not exist.")

            parent = folder  # Move to the next level

        return folder

    def is_circular(self, parent: Folder, name: str, owner: User) -> bool:
        """
        Checks if creating a folder with the given name and parent would cause
        a circular relationship.
        """
        current = parent
        while current is not None:
            if current.name == name and current.owner == owner:
                return True
            current = current.parent
        return False

    def upload_directory(
        self, source_dir: str, target_folder: Folder, owner: User
    ) -> None:
        for root, dirs, files in os.walk(source_dir):
            relative_path = os.path.relpath(root, source_dir)
            current_folder = target_folder

            if relative_path != ".":
                for folder_name in relative_path.split(os.sep):
                    current_folder, created = Folder.objects.get_or_create(
                        name=folder_name, parent=current_folder, owner=owner
                    )
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Created subfolder: {current_folder.get_full_path()}"
                            )
                        )

            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    file_size = os.path.getsize(file_path)
                    if file_size > settings.MAX_BULK_UPLOAD_FILE_SIZE:
                        self.stderr.write(
                            self.style.WARNING(
                                f"File '{file_name}' exceeds the maximum allowed size and was skipped."
                            )
                        )
                        continue

                    with open(file_path, "rb") as file_content:
                        django_file = File(file_content)
                        document = create_document(
                            name=file_name,
                            owner=owner,
                            parent=current_folder,
                            content_file=django_file,
                        )
                        if document:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Uploaded document: {document.get_full_path()}"
                                )
                            )
                        else:
                            raise Exception("Document creation returned None.")
                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(
                            f"Error processing file '{file_name}': {str(e)}"
                        )
                    )
