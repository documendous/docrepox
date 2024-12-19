from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from apps.core.views import View
from apps.etags.models import Tag

from apps.projects.forms import UpdateProjectForm
from apps.projects.utils.project import is_a_project_folder
from apps.repo import rules
from apps.repo.forms.element import UpdateElementForm
from apps.repo.utils.static.lookup import get_model
from apps.repo.utils.system.object import get_system_root_folder


class UpdateElementDetailsView(View):
    """
    View for updating an element's (folder or document) details
    """

    template_name = "repo/update_element.html"

    def get_element_and_parent(self, element_id, element_type):  # pragma: no coverage
        Model = get_model(element_type)
        instance = Model.objects.get(pk=element_id)
        if element_type == "document":
            parent = instance.parent
        elif element_type == "folder":
            parent = instance
        elif element_type == "project":
            parent = instance.folder
        else:
            raise Http404("Element type is not found")
        return instance, parent

    def render_form(self, request, form, element, parent):
        path_with_links = parent.get_path_with_links(request.user)
        return render(
            request,
            self.template_name,
            {
                "element": element,
                "form": form,
                "home_folder_id": request.user.profile.home_folder.id,
                "path_with_links": path_with_links,
                "root_folder_id": get_system_root_folder().id,
            },
        )

    def get(self, request, element_id, element_type):
        element, parent = self.get_element_and_parent(element_id, element_type)
        if element.type == "project":
            rules.can_update_project(request, element)
        else:
            rules.can_update_element(request, element)
        if element_type == "folder" and is_a_project_folder(element):
            return HttpResponseRedirect(
                reverse(
                    "repo:update_element",
                    args=[
                        "project",
                        element.parent_project.pk,
                    ],
                )
            )

        existing_tags = (
            ", ".join([tag.name for tag in element.tags.all()])
            if element.tags.exists()
            else ""
        )

        form = (
            UpdateProjectForm(instance=element, initial={"tags": existing_tags})
            if element_type == "project"
            else UpdateElementForm(instance=element, initial={"tags": existing_tags})
        )

        return self.render_form(request, form, element, parent)

    def _handle_tags(self, updated_element, form):
        updated_element.tags.clear()
        tags_input = form.cleaned_data.get("tags", "")
        new_tag_names = [t.strip() for t in tags_input.split(",")] if tags_input else []

        for tag_name in new_tag_names:  # pragma: no coverage
            if tag_name:  # Ensure no empty strings are added
                tag, created = Tag.objects.get_or_create(name=tag_name)
                updated_element.tags.add(tag)

    def post(self, request, element_id, element_type):
        element, parent = self.get_element_and_parent(element_id, element_type)
        if element.type == "project":
            rules.can_update_project(request, element)
        else:
            rules.can_update_element(request, element)

        form = UpdateElementForm(request.POST, instance=element)
        if form.is_valid():
            updated_element = form.save(commit=False)
            updated_element.save()

            self._handle_tags(updated_element, form)

            messages.info(request, f'"{element.name}" details updated.')
            return HttpResponseRedirect(
                reverse("repo:update_element", args=[element.type, element.id])
            )

        return self.render_form(request, form, element, parent)
