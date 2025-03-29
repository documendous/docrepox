from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.core.views import View
from apps.repo import rules
from apps.repo.forms.element import UpdateVersionForm
from apps.repo.models.element.document import Document
from apps.repo.utils.version import update_version_tag


class AddVersionView(View):
    """
    View for adding a new version for a document
    """

    def post(self, request, document_id):
        document = Document.objects.get(pk=document_id)
        rules.can_add_document_version(request.user, document)
        update_version_form = UpdateVersionForm(request.POST, request.FILES)

        if update_version_form.is_valid():
            change_type = request.POST.get("change_type", "Minor")
            new_version = update_version_form.save(commit=False)

            new_version.tag = update_version_tag(
                change_type=change_type,
                document=document,
            )

            new_version.parent = document
            new_version.save()

        return HttpResponseRedirect(
            reverse(
                "repo:element_details",
                args=[
                    document.type,
                    document.pk,
                ],
            )
        )
