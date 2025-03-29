import logging

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from apps.core.views import View
from apps.repo.models.profile import Profile

from .models import Avatar


class UpdateAvatarView(View):
    def post(self, request, profile_id):  # pragma: no coverage
        log = logging.getLogger(__name__)
        profile = Profile.objects.get(pk=profile_id)
        avatar_file = request.FILES.get("avatar_image", None)

        if avatar_file:
            Avatar.objects.update_or_create(
                content_type=ContentType.objects.get_for_model(Profile),
                object_id=profile.id,
                defaults={"image_file": avatar_file},
            )
            log.debug(f"Avatar created for user {request.user.profile}")

        return render(
            request,
            "avatars/_avatar_image.html",
            {"profile": profile, "image_size": "100"},
        )
