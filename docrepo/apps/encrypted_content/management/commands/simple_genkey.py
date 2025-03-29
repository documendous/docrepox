from cryptography.fernet import Fernet
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generates a new encryption key for use with Fernet encryption."

    def handle(self, *args, **kwargs):
        key = Fernet.generate_key()
        self.stdout.write(
            self.style.SUCCESS(f"Generated Encryption Key: {key.decode()}")
        )
