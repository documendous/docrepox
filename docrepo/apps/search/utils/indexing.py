import logging
from io import BytesIO

import fitz
from django.conf import settings
from django.utils.timezone import now

from apps.encrypted_content.utils import get_encrypted_file_handler
from apps.repo.models.element.document import Document
from apps.repo.utils.model import get_current_version
from apps.transformations.core import generate_pdf_file
from apps.transformations.models import Preview

from ..models import DocumentIndex


def clean_extracted_text(extracted_text: str | bytes) -> str:  # pragma: no coverage
    if isinstance(extracted_text, bytes):
        content = extracted_text.decode("utf-8", errors="replace").replace(
            "\x00", "\ufffd"
        )
    else:
        content = extracted_text.replace("\x00", "\ufffd")

    return content


def index_documents(reconcile_indexes=True):
    if reconcile_indexes:
        reconcile_missing_indexes()

    indexes = DocumentIndex.objects.all()

    for index in indexes:
        index_document(index)


def index_document(index):
    log = logging.getLogger(__name__)
    document = index.document
    version = document.current_version

    log.debug(f"Getting preview for document: {document}|{version}")

    try:
        preview = Preview.objects.get(version=version)
    except Preview.DoesNotExist:
        log.debug(
            f"Preview does not exist for document: {document}|{version}. Creating one."
        )

        current_version = get_current_version(document)
        generate_pdf_file(current_version)

        try:
            preview = Preview.objects.get(version=current_version)
        except Preview.DoesNotExist:  # pragma: no coverage
            return

    file_path = preview.content_file.path
    log.debug(f"Extracting text from: {file_path}")
    extracted_text = extract_pdf_text(pdf_path=file_path)

    if extracted_text:
        log.debug(f"Updating index for document: {document}")
        index.content = clean_extracted_text(extracted_text)
        index.is_indexed = True
        index.last_indexed = now()
        index.save()

        log.debug(f"Indexed {file_path} successfully")

    else:  # pragma: no coverage
        log.warning(f"Unable to successfully index {file_path}")


def extract_pdf_text(pdf_path):  # pragma: no coverage
    """Extract text from a PDF file using PyMuPDF."""
    log = logging.getLogger(__name__)

    try:
        if settings.ENCRYPT_CONTENT:
            encrypted_file_handler = get_encrypted_file_handler(pdf_path)

            if isinstance(encrypted_file_handler, BytesIO):
                doc = fitz.open(
                    stream=encrypted_file_handler, filetype="pdf"
                )  # Read from decrypted stream

            else:
                log.error("Decryption failed or returned an invalid file handler")
                return None

        else:
            doc = fitz.open(pdf_path)

        return "\n".join([page.get_text("text") for page in doc])

    except Exception as e:  # pragma: no coverage
        log.error(f"Error extracting text: {e}")
        return None


def reconcile_missing_indexes():  # pragma: no coverage
    log = logging.getLogger(__name__)
    log.debug("Reconciling missing indexes ...")

    [
        DocumentIndex.objects.get_or_create(document=document)
        for document in Document.objects.all()
    ]

    log.debug("Done.")
