from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import Client, TestCase
from django.urls import reverse
from apps.projects.models import Project
from apps.repo.tests.utils import TEST_USER, get_test_project, get_test_user
from apps.repo.utils.system.object import get_admin_user
from apps.comms.models import Communication


User = get_user_model()


class ProjectsViewTest(TestCase):
    def setUp(self):
        self.admin_user = get_admin_user()
        self.test_user = get_test_user()
        self.client = Client()

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.get(reverse("repo:projects:index"))
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        self.client.login(username="admin", password="admin")

        # Test with admin user
        response = self.client.get(reverse("repo:projects:index"))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.post(
            reverse("repo:projects:index"),
            data={
                "name": "Example project",
                "visibility": "public",
            },
        )
        self.assertEqual(response.status_code, 302)
        project = Project.objects.get(name="Example project")
        self.assertTrue(project)
        self.assertTrue(project.is_active)

    def test_post_invalid_data(self):
        self.client.login(
            username=TEST_USER["username"],
            password=TEST_USER["password"],
        )
        response = self.client.post(
            reverse("repo:projects:index"),
            data={
                "name": "Example project",
            },
        )
        self.assertEqual(response.status_code, 200)


class ProjectDetailsViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.non_manager = get_test_user(username="testuser2")
        self.client = Client()
        self.test_project = Project.objects.create(
            name="Test project", owner=self.test_user, visibility="public"
        )

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.get(
            reverse(
                "repo:projects:project_details",
                args=[
                    self.test_project.pk,
                ],
            )
        )
        self.assertTrue(response.status_code, 200)

    def test_get_non_manager(self):
        self.client.login(username="testuser2", password=TEST_USER["password"])
        response = self.client.get(
            reverse(
                "repo:projects:project_details",
                args=[
                    self.test_project.pk,
                ],
            )
        )
        self.assertTrue(response.status_code, 200)


class UpdateProjectViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.client = Client()
        self.test_project = Project.objects.create(
            name="Test project",
            visibility="public",
            owner=self.test_user,
        )

    def test_get(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.get(
            reverse(
                "repo:update_element",
                args=[
                    "project",
                    self.test_project.pk,
                ],
            )
        )
        self.assertTrue(response.status_code, 200)

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.post(
            reverse(
                "repo:update_element",
                args=[
                    "project",
                    self.test_project.pk,
                ],
            ),
            data={
                "name": "Test project 1",
                "title": "Test project 1",
                "description": "Example description",
                "visibility": "private",
            },
        )
        self.assertTrue(response.status_code, 200)

    def test_post_invalid_data(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.post(
            reverse(
                "repo:update_element",
                args=[
                    "project",
                    self.test_project.pk,
                ],
            ),
            data={
                "title": "Test project 1",
                "description": "Example description",
                "visibility": "private",
            },
        )
        self.assertTrue(response.status_code, 200)

    def test_with_folder_as_project(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.get(
            reverse(
                "repo:update_element",
                args=[
                    "folder",
                    self.test_project.folder.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)


class AccessPublicProjectTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Test Public Project 2",
            visibility="public",
            owner=User.objects.get(username=TEST_USER["username"]),
        )
        self.non_member = User.objects.create(
            username="nonmember", email="nonmember@localhost"
        )
        self.non_member.set_password("testpass")
        self.non_member.save()
        self.client = Client()

    def test_get(self):
        self.client.login(username="nonmember", password="testpass")
        response = self.client.get(
            reverse("repo:folder", args=[self.project.folder.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_post_add_document_in_project(self):
        self.client.login(username="nonmember", password="testpass")
        test_content = b"Hello world"
        response = self.client.post(
            reverse(
                "repo:add_document",
                args=[
                    self.project.folder.id,
                ],
            ),
            data={
                "name": "TestDocument.txt",
                # "content_file": test_file,
                "content": test_content,
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_post_create_document_in_project(self):
        self.client.login(username="nonmember", password="testpass")
        test_content = b"Hello world"
        response = self.client.post(
            reverse(
                "repo:create_document",
                args=[
                    self.project.folder.id,
                ],
            ),
            data={
                "name": "TestDocument.txt",
                # "content_file": test_file,
                "content": test_content,
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_post_add_folder_in_project(self):
        self.client.login(username="nonmember", password="testpass")
        response = self.client.post(
            reverse(
                "repo:folder",
                args=[
                    self.project.folder.id,
                ],
            ),
            data={
                "name": "Test Folder",
            },
        )
        self.assertEqual(response.status_code, 404)


class AddUserToProjectViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_manager = get_test_user(username="testmanager2")
        self.client = Client()
        self.test_project = Project.objects.create(
            name="Test project",
            owner=self.test_user,
        )
        self.test_manager.groups.add(
            Group.objects.get(name="project_test-project_managers")
        )

    def test_post(self):
        group = Group.objects.get(name="project_test-project_readers")
        login_successful = self.client.login(
            username="testmanager2", password="testpass"
        )
        self.assertTrue(login_successful)
        response = self.client.post(
            reverse(
                "repo:projects:add_user_to_project",
                args=[
                    self.test_project.pk,
                    group.pk,
                ],
            ),
            data={"users": [self.test_user.pk]},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.test_project.in_readers_group(self.test_user))


class RemoveUserFromProjectGroupViewTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_manager = get_test_user(username="testmanager2")
        self.test_editor = get_test_user(username="testeditor2")
        self.client = Client()
        self.test_project = Project.objects.create(
            name="Test project",
            owner=self.test_user,
        )
        self.test_manager.groups.add(
            Group.objects.get(name="project_test-project_managers")
        )
        self.test_editor.groups.add(
            Group.objects.get(name="project_test-project_editors")
        )
        self.test_editor.groups.add(
            Group.objects.get(name="project_test-project_editors")
        )

    def test_post(self):
        group = Group.objects.get(name="project_test-project_readers")
        login_successful = self.client.login(
            username="testmanager2", password="testpass"
        )
        self.assertTrue(login_successful)
        response = self.client.post(
            reverse(
                "repo:projects:add_user_to_project",
                args=[
                    self.test_project.pk,
                    group.pk,
                ],
            ),
            data={"users": [self.test_user.pk]},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.test_project.in_readers_group(self.test_user))

        response = self.client.post(
            reverse(
                "repo:projects:remove_user_from_project_group",
                args=[
                    self.test_project.pk,
                    self.test_user.pk,
                    group.pk,
                ],
            ),
        )

        self.test_project.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.test_project.in_readers_group(self.test_user))


class ProjectCreationTest(TestCase):
    def setUp(self):
        self.test_user = get_test_user()
        self.test_project = Project.objects.create(
            name="Example project",
            owner=self.test_user,
        )

    def test_add(self):
        self.assertTrue(self.test_project)

    def test_update_project_name(self):
        self.test_project.name = "New name"
        self.test_project.save()
        self.test_project.refresh_from_db()
        self.assertEqual(self.test_project.name, "New name")


class RequestProjectJoinViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = get_test_user()
        self.project = Project.objects.create(
            name="Test Project", owner=self.test_user, visibility="public"
        )

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.post(
            reverse(
                "repo:projects:request_join",
                args=[
                    self.project.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Communication.objects.filter(msg_from=self.test_user))


class AddRequesterToProjectGroupViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = get_test_user()
        self.project = Project.objects.create(
            name="Test Project", owner=self.test_user, visibility="public"
        )

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.post(
            reverse(
                "repo:projects:request_join",
                args=[
                    self.project.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Communication.objects.filter(msg_from=self.test_user))

        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.post(
            reverse(
                "repo:projects:add_requester_to_project_group",
                args=[
                    self.project.pk,
                    self.test_user.pk,
                    "readers",
                ],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.project.in_readers_group(self.test_user))

        response = self.client.post(
            reverse(
                "repo:projects:add_requester_to_project_group",
                args=[
                    self.project.pk,
                    self.test_user.pk,
                    "editors",
                ],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.project.in_editors_group(self.test_user))

        response = self.client.post(
            reverse(
                "repo:projects:add_requester_to_project_group",
                args=[
                    self.project.pk,
                    self.test_user.pk,
                    "managers",
                ],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.project.in_managers_group(self.test_user))

        response = self.client.post(
            reverse(
                "repo:projects:add_requester_to_project_group",
                args=[
                    self.project.pk,
                    self.test_user.pk,
                    "unknown",
                ],
            )
        )
        self.assertEqual(response.status_code, 404)

        comm = Communication.objects.filter(msg_from=self.test_user)
        self.assertTrue(comm.count() < 1)


class RejectRequestJoinViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = get_test_user()
        self.project = Project.objects.create(
            name="Test Project", owner=self.test_user, visibility="public"
        )

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        response = self.client.post(
            reverse(
                "repo:projects:request_join",
                args=[
                    self.project.pk,
                ],
            )
        )

        comm = Communication.objects.get(msg_from=self.test_user)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(comm)

        response = self.client.post(
            reverse(
                "repo:projects:reject_join_request",
                args=[
                    comm.pk,
                ],
            )
        )

        comm = Communication.objects.filter(msg_from=self.test_user)
        self.assertTrue(comm.count() < 1)


class DeactivateProjectViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = get_test_user()
        self.test_user2 = get_test_user(username="testuser2")
        self.project = get_test_project()

    def test_post(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        self.client.post(
            reverse(
                "repo:projects:deactivate_project",
                args=[
                    self.project.pk,
                ],
            ),
            data={"deactivate": True},
        )
        project = Project.objects.get(name="Test Project")
        self.assertFalse(project.is_active)

    def test_post_no_deactivate_field(self):
        self.client.login(
            username=TEST_USER["username"], password=TEST_USER["password"]
        )
        self.client.post(
            reverse(
                "repo:projects:deactivate_project",
                args=[
                    self.project.pk,
                ],
            ),
        )
        project = Project.objects.get(name="Test Project")
        self.assertTrue(project.is_active)

    def test_post_invalid_user(self):
        self.client.login(username="testuser2", password="testpass")
        response = self.client.post(
            reverse(
                "repo:projects:deactivate_project",
                args=[
                    self.project.pk,
                ],
            )
        )
        self.assertEqual(response.status_code, 404)
        project = Project.objects.get(name="Test Project")
        self.assertTrue(project.is_active)
