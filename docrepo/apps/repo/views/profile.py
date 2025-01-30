import logging

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from apps.core.views import MultipleFormView
from apps.repo.forms.user import UpdateProfileForm, UpdateUserForm
from apps.repo.models.profile import Profile
from apps.repo.settings import UPDATE_MODEL_ERROR_MSG, UPDATE_MODEL_SUCCESS_MSG
from apps.repo.utils.system.object import get_system_root_folder


class UpdateProfileView(MultipleFormView):
    """
    View for updating a user profile
    """

    template_name = "ui/update_profile.html"
    log = logging.getLogger(__name__)

    def _get_common_context(
        self, profile, request, update_profile_form, update_user_form
    ):
        return {
            "cancel_url": reverse("repo:index"),
            "profile": profile,
            "update_profile_form": update_profile_form,
            "update_user_form": update_user_form,
            "home_folder_id": request.user.profile.home_folder.id,
            "root_folder_id": get_system_root_folder().id,
        }

    def get(self, request):
        profile = get_object_or_404(Profile, pk=request.user.profile.pk)
        update_profile_form = UpdateProfileForm(instance=profile)
        update_user_form = UpdateUserForm(instance=profile.user)
        context = self._get_common_context(
            profile, request, update_profile_form, update_user_form
        )
        return render(request, self.template_name, context)

    def post(self, request):
        profile = get_object_or_404(Profile, pk=request.user.profile.pk)
        update_profile_form = UpdateProfileForm(request.POST, instance=profile)
        update_user_form = UpdateUserForm(request.POST, instance=profile.user)

        if update_profile_form.is_valid() and update_user_form.is_valid():
            self._save_multi_forms(
                forms=[update_profile_form, update_user_form],
                success_msg=UPDATE_MODEL_SUCCESS_MSG,
                error_msg=UPDATE_MODEL_ERROR_MSG,
            )
            return HttpResponseRedirect(reverse("repo:update_profile"))

        context = self._get_common_context(  # pragma: no coverage
            profile, request, update_profile_form, update_user_form
        )
        return render(
            request,
            self.template_name,
            context,
        )  # pragma: no coverage
