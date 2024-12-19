from itertools import chain
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from apps.core.utils.htmx import htmx_redirect
from apps.projects.models import Project
from apps.projects.utils.project import get_viewable_project_list
from apps.repo.utils.system.object import get_admin_user
from apps.repo.models.element.document import Document
from apps.repo.models.element.folder import Folder


class SearchProjectsView(View):
    """
    Project search view. Returns only projects a user has initial access to.
    Non-admin user should be able to see all public and managed projects.
    Admin user should be able to see all projects (public, managed, private)
    """

    def post(self, request):
        search_term = request.POST.get("search_term", None)

        if search_term:
            if request.user == get_admin_user():
                projects = Project.objects.filter(
                    name__icontains=search_term, is_active=True
                )
            else:
                projects = Project.objects.filter(
                    Q(name__icontains=search_term)
                    & (
                        Q(visibility="public")
                        | Q(visibility="managed")
                        | (
                            Q(visibility="private")
                            & Q(
                                id__in=[
                                    project.id
                                    for project in Project.objects.all()
                                    if project.is_member(request.user)
                                ]
                            )
                        )
                    ),
                    is_active=True,
                )
        else:
            projects = get_viewable_project_list(request)

        return render(
            request,
            "projects/partials/_project_children_table_data.html",
            {"projects": projects},
        )


class SearchElementsView(View):
    """
    Element search view (folders and documents). Returns only elements a user has initial access to.
    Non-admin user should be able to see all folders and documents they own or have read access to.
    Admin user should be able to see all projects (public, managed, private)
    """

    def _get_default_children(self, parent):
        documents = Document.objects.filter(parent=parent)
        folders = Folder.objects.filter(parent=parent, is_hidden=False)
        return (
            documents,
            folders,
        )

    def post(self, request, folder_id):
        parent = Folder.objects.get(pk=folder_id)
        project = parent.parent_project
        search_term = request.POST.get("search_term", None)
        pagination_enabled = False

        if project:
            if project.is_member(request.user) or project.visibility == "public":
                if search_term:
                    documents = Document.objects.filter(
                        name__icontains=search_term,
                        parent=parent,
                    )
                    folders = Folder.objects.filter(
                        name__icontains=search_term,
                        parent=parent,
                        is_hidden=False,
                    )
                else:
                    documents, folders = self._get_default_children(parent)
                    pagination_enabled = True

        else:
            if search_term:
                if request.user == get_admin_user():
                    documents = Document.objects.filter(
                        parent=parent, name__icontains=search_term
                    )
                    folders = Folder.objects.filter(
                        parent=parent, name__icontains=search_term, is_hidden=False
                    )
                else:
                    documents = Document.objects.filter(
                        Q(name__icontains=search_term) & (Q(owner=request.user)),
                        parent=parent,
                    )
                    folders = Folder.objects.filter(
                        Q(name__icontains=search_term) & (Q(owner=request.user)),
                        parent=parent,
                        is_hidden=False,
                    )
            else:
                documents, folders = self._get_default_children(parent)
                pagination_enabled = True

        children = list(chain(folders, documents))

        if pagination_enabled:
            url = reverse(
                "repo:folder",
                args=[
                    folder_id,
                ],
            )
            return htmx_redirect(url)

        return render(
            request,
            "repo/partials/_folder_children_table_data.html",
            {
                "children": children,
                "scope": "full",
                "pagination_enabled": pagination_enabled,
            },
        )
