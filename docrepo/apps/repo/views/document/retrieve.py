import logging
import pathlib
from urllib.parse import quote
from django.conf import settings
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseServerError,
)
from apps.core.views import View
from apps.repo.utils.model import get_current_version_tag
from apps.transformations.core import generate_pdf_file
from apps.transformations.models import Preview
from apps.repo.settings import DEFAULT_MIMETYPE
from apps.repo.utils.views import DocumentRetriever


class DocumentRetrieverView(DocumentRetriever, View):
    """
    View for retrieving documents via download
    """

    def file_response(
        self, file_path: pathlib.Path, content_type: str, file_name: str, action: str
    ) -> HttpResponse:
        with open(file_path, "rb") as fh:
            response = HttpResponse(
                fh.read(),
                content_type=content_type,
            )
            quoted_file_name = quote(
                file_name
            )  # handles chars unexpected for Content-Disposition
            response["Content-Disposition"] = f'{action}filename="{quoted_file_name}"'
        return response

    def get_action_type(self, request: HttpRequest) -> str | None:
        """
        Determine download as stream or as attachment
        """
        if request.GET.get("action", None) == "attachment":
            return "attachment; "
        return None

    def get(self, request, document_id):
        log = logging.getLogger("__name__")
        document, file_path = self._get_file(request, document_id)
        log.debug(f"Orig file path: {file_path}")

        action = self.get_action_type(request)
        preview = None

        if not action:  # pragma: no coverage
            current_version_tag = get_current_version_tag(document)

            if not current_version_tag:
                return HttpResponseServerError(
                    "Error accessing file. No version exists.",
                )

            document_ext = pathlib.Path(document.name).suffix.lower()
            if document_ext in settings.TRANSFORMABLE_TYPES:
                try:
                    preview = Preview.objects.get(version=current_version_tag)
                    file_path = preview.content_file.path
                except Preview.DoesNotExist:
                    try:
                        generate_pdf_file(current_version_tag)
                        preview = Preview.objects.get(version=current_version_tag)
                        file_path = preview.content_file.path

                    except Exception as err:
                        log.warning(f"Error during transformation: {err}")
                        log.warning(
                            "No preview exists or can be created. Downloading file."
                        )
                        preview = None
                        file_path = None
                        return HttpResponseNotFound(
                            "No versions available for this document."
                        )

                if preview:
                    content_type = "application/pdf"
                    return self.file_response(
                        file_path=file_path,
                        content_type=content_type,
                        file_name=document.name,
                        action=action,
                    )

        try:
            content_type = (
                document.mimetype.name
                if hasattr(document.mimetype, "name")
                else DEFAULT_MIMETYPE
            )
            return self.file_response(
                file_path=file_path,
                content_type=content_type,
                file_name=document.name,
                action=action,
            )
        except IOError as e:  # pragma: no coverage
            return HttpResponseServerError(
                "Error accessing file: {}".format(e),
            )
