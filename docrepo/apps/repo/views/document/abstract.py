from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from apps.core.views import View
from apps.repo import rules
from apps.repo.forms.element import AddDocumentForm, AddVersionForm
from apps.repo.models.element.document import Document
from apps.repo.models.element.folder import Folder
from apps.repo.utils.helpers import create_with_new_name
from apps.repo.utils.views import DocumentCreator


class BaseCreateDocumentView(DocumentCreator, View):
    """
    Base create document view for different create document view types (add, add_multi and create)
    """

    add_version_form = AddVersionForm()
    document_form = AddDocumentForm()
    has_document_errors = 0

    def _create_document(
        self,
        request,
        name,
        owner,
        parent,
        version_form,
        title=None,
        description=None,
    ):
        try:
            new_document = Document.objects.create(
                name=name,
                title=title,
                description=description,
                owner=owner,
                parent=parent,
            )
        except IntegrityError:  # pragma: no coverage
            new_document = create_with_new_name(
                model_type="document",
                name=name,
                owner=owner,
                parent=parent,
                title=title,
                description=description,
            )
        if new_document:
            self._create_version(new_document, version_form)
            messages.info(
                request,
                f'Document "{name}" was successfully created.',
            )
            return new_document

    def get(self, request, folder_id):
        """
        Base GET
        """
        parent = get_object_or_404(Folder, pk=folder_id)
        rules.can_create_document(request, parent)
        self.context = self._get_common_context(parent, request)
        self._set_extra_context()
        return render(request, "repo/create_document.html", self.context)

    def post(self, request, folder_id):
        """
        Base POST
        """
        parent = get_object_or_404(Folder, pk=folder_id)
        rules.can_create_document(request, parent)
        self.document_form = AddDocumentForm(request.POST)
        self._set_version_form(request)

        if self.document_form.is_valid() and self.version_form.is_valid():
            self._create_document(
                request,
                name=self.document_form.cleaned_data["name"],
                owner=request.user,
                parent=parent,
                version_form=self.version_form,
                title=self.document_form.cleaned_data.get("title"),
                description=self.document_form.cleaned_data.get(
                    "description",
                ),
            )

            if not self.has_document_errors:
                return HttpResponseRedirect(
                    reverse(
                        "repo:folder",
                        args=[parent.id],
                    )
                )

        self.context = self._get_common_context(parent, request)
        self._set_extra_context()
        return render(request, self.template_name, self.context)
