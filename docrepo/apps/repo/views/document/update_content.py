from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from apps.core.views import View
from apps.repo import rules

from ...forms.element import UpdateDocumentContentForm, UpdateDocumentForm
from ...models.element.document import Document
from ...utils.document import update_document_content
from ...utils.model import get_path_with_links
from ...utils.system.object import get_system_root_folder
from ...utils.version import get_content_from_version


class UpdateDocumentContentView(View):
    template_name = "repo/update_document.html"

    def _set_context(self):
        self.context = {
            "create_doc_as_rtf": settings.CREATE_DOC_AS_RTF,
            "document": self.document,
            "folder": self.document.parent,
            "home_folder_id": self.request.user.profile.home_folder.id,
            "path_with_links": get_path_with_links(
                self.document.parent,
                self.request.user,
            ),
            "root_folder_id": get_system_root_folder().id,
            "update_document_form": self.update_document_form,
            "update_content_form": self.update_content_form,
        }

    def get(self, request, document_id):
        self.document = Document.objects.get(pk=document_id)
        rules.can_update_content(request.user, element=self.document)
        current_version = self.document.current_version
        self.update_document_form = UpdateDocumentForm(instance=self.document)
        initial_content = get_content_from_version(version=current_version)

        self.update_content_form = UpdateDocumentContentForm(
            initial={"content": initial_content}
        )

        self._set_context()
        self.context["initial_content"] = initial_content

        return render(request, self.template_name, self.context)

    def post(self, request, document_id):
        self.document = Document.objects.get(pk=document_id)
        rules.can_update_content(request.user, element=self.document)
        current_version = self.document.current_version

        self.update_content_form = UpdateDocumentContentForm(
            request.POST, instance=current_version
        )

        self.update_document_form = UpdateDocumentForm(
            request.POST, instance=self.document
        )

        content = request.POST.get("content")

        if self.update_document_form.is_valid() and content:
            document = self.update_document_form.save()
            change_type = request.POST.get("change_type", "minor")

            update_document_content(
                document=document,
                content=content,
                files=request.FILES,
                change_type=change_type,
            )

            return HttpResponseRedirect(
                reverse(
                    "repo:folder",
                    args=[
                        self.document.parent.pk,
                    ],
                )
            )

        self._set_context()

        return render(request, self.template_name, self.context)
