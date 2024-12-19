from django.urls import path

from apps.projects.views import (
    AddRequesterToProjectGroupView,
    AddUserToProjectView,
    DeactivateProjectView,
    ProjectDetailsView,
    ProjectsView,
    RejectRequestJoinView,
    RemoveUserFromProjectGroupView,
    RequestProjectJoinView,
)


app_name = "projects"


urlpatterns = [
    path(
        "<uuid:project_id>/request/join/",
        RequestProjectJoinView.as_view(),
        name="request_join",
    ),
    path(
        "<uuid:project_id>/add/requester/<int:user_id>/<str:group_type>/",
        AddRequesterToProjectGroupView.as_view(),
        name="add_requester_to_project_group",
    ),
    path(
        "project/join/<int:req_join_id>/",
        RejectRequestJoinView.as_view(),
        name="reject_join_request",
    ),
    path(
        "<uuid:project_id>/details/",
        ProjectDetailsView.as_view(),
        name="project_details",
    ),
    path(
        "<uuid:project_id>/users/add/<int:group_id>/",
        AddUserToProjectView.as_view(),
        name="add_user_to_project",
    ),
    path(
        "<uuid:project_id>/users/remove/<int:user_id>/<int:group_id>/",
        RemoveUserFromProjectGroupView.as_view(),
        name="remove_user_from_project_group",
    ),
    path(
        "",
        ProjectsView.as_view(),
        name="index",
    ),
    path(
        "deactivate/<uuid:project_id>/",
        DeactivateProjectView.as_view(),
        name="deactivate_project",
    ),
]
