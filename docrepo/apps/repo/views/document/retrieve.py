import logging
import pathlib
from urllib.parse import quote

from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse, HttpResponseServerError

from apps.core.views import View
from apps.repo.settings import DEFAULT_MIMETYPE
from apps.repo.utils.model import get_current_version_tag
from apps.repo.utils.views import DocumentRetriever
from apps.transformations.core import generate_pdf_file
from apps.transformations.models import Preview


class DocumentRetrieverView(DocumentRetriever, View):
    """
    DocumentRetrieverView

    A Django class-based view for retrieving and serving documents for download or preview.
    It extends DocumentRetriever and View and processes HTTP GET requests to fetch a document
    based on document_id.

    Flow of Execution:
    1. Initialize Logging
    - Sets up a logger for document retrieval operations.

    2. Retrieve Document and File Path
    - Calls _get_file(request, document_id) to fetch the document instance and its file path.
    - Logs the original file path.

    3. Determine Download Action
    - Uses get_action_type(request) to decide if the document should be streamed or downloaded as an attachment.
    - If ?action=attachment is present, sets action to "attachment; ", otherwise remains None.

    4. Handle Preview Generation (For Transformable Files)
    - If action is None, attempts to generate a preview:
        - Retrieves current_version_tag using get_current_version_tag(document). Returns 500 Server Error if no version exists.
        - If the document's extension is in settings.TRANSFORMABLE_TYPES, tries to retrieve an existing Preview.
        - If no preview exists, attempts to generate a PDF using generate_pdf_file(current_version_tag). Logs warnings and returns 404 Not Found if transformation fails.
        - If successful, updates file_path and sets content_type to application/pdf, then serves the file response.

    5. Serve the File
    - If no preview is required:
        - Ensures unsupported preview types are downloaded as attachments.
        - Determines content_type from document.mimetype or DEFAULT_MIMETYPE.
        - Calls file_response(file_path, content_type, file_name, action) to return the document.

    6. Error Handling
    - Returns 500 Server Error if an IOError occurs while accessing the file.

    Helper Methods:
    - file_response(file_path, content_type, file_name, action): Reads the file and returns it as a FileResponse with appropriate headers.
    - get_action_type(request): Determines if the document should be streamed or downloaded as an attachment.

    Expected Outcomes:
    - 200 OK with the document file (either as an attachment or inline preview).
    - 404 Not Found if no versions exist and transformation fails.
    - 500 Server Error if the document cannot be accessed due to file I/O errors.
    """

    def file_response(
        self, file_path: pathlib.Path, content_type: str, file_name: str, action: str
    ) -> HttpResponse:
        response = FileResponse(open(file_path, "rb"), content_type=content_type)
        quoted_file_name = quote(file_name)
        response["Content-Disposition"] = f'{action}filename="{quoted_file_name}"'
        response["X-Frame-Options"] = "SAMEORIGIN"
        response["Content-Security-Policy"] = "frame-ancestors 'self';"

        return response

    def get_action_type(self, request: HttpRequest) -> str | None:
        """
        Determine download as stream or as attachment
        """
        if request.GET.get("action", None) == "attachment":
            return "attachment; "

        return None

    def _get_preview(self, version_tag):
        log = logging.getLogger(__name__)

        try:  # pragma: no coverage
            """Getting a preview and file_path"""
            preview = Preview.objects.get(version=version_tag)
            file_path = preview.content_file.path
            log.debug("Preview generated")

        except Preview.DoesNotExist:
            """The preview does not exist -- then we will create one"""
            log.warning("Preview and file_path do not exist. Retrying generate preview")

            try:
                generate_pdf_file(version_tag)
                preview = Preview.objects.get(version=version_tag)
                file_path = preview.content_file.path
                log.debug("Preview generated")

            except Exception as err:  # pragma: no coverage
                """Having an issue creating a preview and cannot create one"""
                log.warning(f"Error during transformation: {err}")
                log.warning("No preview exists or can be created.")
                preview = None
                file_path = None

        return preview, file_path

    def get(self, request, document_id):
        log = logging.getLogger("__name__")

        document, file_path = self._get_file(request, document_id)
        action = self.get_action_type(request)
        document_ext = pathlib.Path(document.name).suffix.lower()

        log.debug(f"Orig file path: {file_path}")

        if not action:
            """We are expecting a preview and not an attachment"""
            current_version_tag = get_current_version_tag(document)

            if not current_version_tag:  # pragma: no coverage
                """The document must have a current version tag"""
                return HttpResponseServerError(
                    "Error accessing file. No version exists.",
                )

            if document_ext in settings.TRANSFORMABLE_TYPES:
                """The document must be of a transformable type"""
                preview, file_path = self._get_preview(version_tag=current_version_tag)

                if preview:
                    """We have a preview and will show it in the browser"""
                    content_type = "application/pdf"

                    return self.file_response(
                        file_path=file_path,
                        content_type=content_type,
                        file_name=document.name,
                        action=None,
                    )

                # Else we continue on and look for a way to retrieve for the user

        try:
            """
            Some document extensions are not transformable but the browser will allow us to
            see them there (like jpg, png, gif etc.). We can also get here if we were
            unable to show a preview but there are no real issues besides being able to
            generate a preview (for this, we fall back to downloading as attachment).
            """
            if not action and document_ext not in settings.ALLOWED_PREVIEW_TYPES:
                """
                But we must define which ones are previable in the browser nonetheless
                else no matter what we will deliver them as an attachment.
                """
                log.debug("Setting retrieval as attachment")
                action = "attachment; "

            content_type = (
                document.mimetype.name
                if hasattr(document.mimetype, "name")
                else DEFAULT_MIMETYPE
            )

            log.debug("Downloading as attachment")

            return self.file_response(
                file_path=file_path,
                content_type=content_type,
                file_name=document.name,
                action=action,
            )

        except IOError as e:  # pragma: no coverage
            """All IO type errors will end here"""
            err_msg = ("Error accessing file: {}".format(e),)
            log.error(err_msg)

            return HttpResponseServerError(err_msg)
