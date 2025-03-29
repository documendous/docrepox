from django.urls import path

from .views import UpdateAvatarView

app_name = "avatars"


urlpatterns = [
    path(
        "update/<int:profile_id>/",
        UpdateAvatarView.as_view(),
        name="update_avatar_image",
    )
]
