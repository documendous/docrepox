from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from apps.projects.models import Project

from .users import users_data

User = get_user_model()


def create_projects(apps, schema):

    users = {}
    for user_data in users_data:
        user = User.objects.create(
            username=user_data["username"], email=user_data["email"]
        )
        user.set_password(user_data["password"])
        user.save()
        users[user_data["username"]] = user

    projects_data = [
        {
            "name": "Test Public Project",
            "title": "The Test Public Project",
            "description": "This is the test public project",
            "visibility": "public",
            "owner": users["testmanager"],
        },
        {
            "name": "Test Managed Project",
            "title": "The Test Managed Project",
            "description": "This is the test managed project",
            "visibility": "managed",
            "owner": users["testmanager"],
        },
        {
            "name": "Test Private Project",
            "title": "The Test Private Project",
            "description": "This is the test private project",
            "visibility": "private",
            "owner": users["testmanager"],
        },
    ]

    for project_data in projects_data:
        project = Project.objects.create(**project_data)
        managers_group = Group.objects.get(name=project.managers_group)
        editors_group = Group.objects.get(name=project.editors_group)
        readers_group = Group.objects.get(name=project.readers_group)

        managers_group.user_set.add(users["testmanager"])
        editors_group.user_set.add(users["testeditor"])
        readers_group.user_set.add(users["testreader"])

        managers_group.save()
        editors_group.save()
        readers_group.save()


def setup_test_projects(apps, schema):  # pragma: no coverage
    if settings.ADD_TEST_PROJECTS:
        create_projects(apps, schema)
