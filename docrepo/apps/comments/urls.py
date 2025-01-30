from django.urls import path

from apps.comments.views import AddCommentView, DeleteCommentView

app_name = "comments"


urlpatterns = [
    path(
        "<str:element_type>/<uuid:element_id>/",
        AddCommentView.as_view(),
        name="add_comment",
    ),
    path(
        "<int:comment_id>/<str:element_type>/<uuid:element_id>/delete/",
        DeleteCommentView.as_view(),
        name="delete_comment",
    ),
]
