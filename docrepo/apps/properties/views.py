from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from apps.core.views import View
from apps.repo.utils.model import get_path_with_links
from apps.repo.utils.static.lookup import get_model
from apps.repo.utils.system.object import get_system_root_folder

from .forms import UpdatePropertyForm
from .models import Property


class AddElementPropertiesView(View):
    template_name = "properties/add_properties.html"

    def get(self, request, element_type, element_id):
        Model = get_model(element_type)
        element = get_object_or_404(Model, pk=element_id)
        path_with_links = get_path_with_links(element, request.user)

        return render(
            request,
            self.template_name,
            {
                "element": element,
                "home_folder_id": request.user.profile.home_folder.id,
                "path_with_links": path_with_links,
                "root_folder_id": get_system_root_folder().id,
            },
        )

    def post(self, request, element_type, element_id):
        Model = get_model(element_type)

        keys = request.POST.getlist("key[]")
        values = request.POST.getlist("value[]")
        types = request.POST.getlist("type[]")
        descriptions = request.POST.getlist("description[]")

        content_type = ContentType.objects.get_for_model(Model)

        for key, value, prop_type, description in zip(
            keys, values, types, descriptions
        ):
            Property.objects.create(
                content_type=content_type,
                object_id=element_id,
                key=key,
                description=description,
                value=value,
                type=prop_type,
            )

        return HttpResponseRedirect(
            reverse("repo:element_details", args=[element_type, element_id])
        )


class DeleteElementPropertyView(View):
    def post(self, request, property_id):  # pragma: no coverage
        property = Property.objects.get(pk=property_id)
        property.delete()
        return_url = request.META["HTTP_REFERER"]
        return HttpResponseRedirect(return_url)


class UpdateElementPropertyView(View):
    def get(self, request, property_id):
        property = Property.objects.get(pk=property_id)
        element = property.content_object
        form = UpdatePropertyForm(instance=property)
        path_with_links = get_path_with_links(element, request.user)

        return render(
            request,
            "properties/update_property.html",
            {
                "property": property,
                "form": form,
                "home_folder_id": request.user.profile.home_folder.id,
                "path_with_links": path_with_links,
                "root_folder_id": get_system_root_folder().id,
                "element": element,
            },
        )

    def post(self, request, property_id):
        property = Property.objects.get(pk=property_id)
        element = property.content_object
        form = UpdatePropertyForm(request.POST, instance=property)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse("repo:element_details", args=[element.type, element.id])
            )

        path_with_links = get_path_with_links(element, request.user)

        return render(
            request,
            "properties/update_property.html",
            {
                "property": property,
                "form": form,
                "home_folder_id": request.user.profile.home_folder.id,
                "path_with_links": path_with_links,
                "root_folder_id": get_system_root_folder().id,
                "element": element,
            },
        )
