from django.conf import settings
from django.core.files.base import ContentFile
from apps.repo.forms.element import AddVersionForm
from apps.repo.views.document.abstract import BaseCreateDocumentView


class CreateDocumentView(BaseCreateDocumentView):
    """
    View for creating document from text
    """

    has_create_document_errors = 0
    template_name = "repo/create_document.html"

    def _create_content_file_from_content(self, request, content):
        file_name = request.POST.get("name", None)
        if file_name:
            content_file = ContentFile(content.encode("utf-8"), name=file_name)
            files_data = request.FILES.copy()
            files_data["content_file"] = content_file
            return AddVersionForm(request.POST, files_data)

    def _set_extra_context(self):
        self.context.update(
            {
                "add_version_form": self.add_version_form,
                "create_doc_as_rtf": settings.CREATE_DOC_AS_RTF,
                "editor_font_size": settings.EDITOR_FONT_SIZE,
            }
        )

    def _set_version_form(self, request):
        content = request.POST.get("content", None)
        if content:
            self.version_form = self._create_content_file_from_content(
                request,
                content,
            )
        else:
            self.version_form = AddVersionForm(request.POST, request.FILES)
