from django.conf import settings
from django.core.management.base import BaseCommand

from ...utils import index_documents


class Command(BaseCommand):
    help = "Runs the document indexing process for full text search"

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-reconcile-indexes",
            action="store_false",
            dest="reconcile_indexes",
            help="Disable index reconciliation during the indexing process.",
        )

    def handle(self, *args, **options):
        if settings.ENABLE_FULL_TEXT_SEARCH:
            reconcile_indexes = options.get("reconcile_indexes", True)

            self.stdout.write(self.style.SUCCESS("Starting indexing process..."))
            index_documents(reconcile_indexes=reconcile_indexes)
            self.stdout.write(self.style.SUCCESS("Indexing completed successfully!"))
        else:
            self.stdout.write(
                self.style.WARNING(
                    "ENABLE_FULL_TEXT_SEARCH must be set to True in order to index documents. Exiting."
                )
            )
