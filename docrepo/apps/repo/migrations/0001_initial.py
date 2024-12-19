# Generated by Django 4.2.16 on 2024-11-13 22:12

import apps.core.utils.storage
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid

from apps.repo.utils.system.main import setup_system


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("etags", "0001_initial"),
        ("comments", "0002_alter_comment_options"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Folder",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("title", models.CharField(blank=True, max_length=255, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("orig_name", models.CharField(max_length=255, blank=True, null=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("is_hidden", models.BooleanField(default=False)),
                ("comments", models.ManyToManyField(blank=True, to="comments.comment")),
                (
                    "orig_parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)s_orig_parent",
                        to="repo.folder",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="repo.folder",
                    ),
                ),
                ("tags", models.ManyToManyField(blank=True, to="etags.tag")),
            ],
            options={
                "verbose_name": "Folder",
                "verbose_name_plural": "Folders",
                "unique_together": {("name", "parent")},
            },
        ),
        migrations.CreateModel(
            name="Mimetype",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, unique=True)),
                ("extension_list", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bio", models.TextField(blank=True, max_length=500)),
                ("location", models.CharField(blank=True, max_length=30)),
                ("birth_date", models.DateField(blank=True, null=True)),
                (
                    "home_folder",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="repo.folder",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("title", models.CharField(blank=True, max_length=255, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("orig_name", models.CharField(max_length=255, blank=True, null=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("comments", models.ManyToManyField(blank=True, to="comments.comment")),
                (
                    "mimetype",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="repo.mimetype",
                    ),
                ),
                (
                    "orig_parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)s_orig_parent",
                        to="repo.folder",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="repo.folder",
                    ),
                ),
                ("tags", models.ManyToManyField(blank=True, to="etags.tag")),
            ],
            options={
                "verbose_name": "Document",
                "verbose_name_plural": "Documents",
                "unique_together": {("name", "parent")},
            },
        ),
        migrations.CreateModel(
            name="Version",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "tag",
                    models.CharField(
                        default="1.0", max_length=20, verbose_name="Version number"
                    ),
                ),
                (
                    "content_file",
                    models.FileField(
                        upload_to=apps.core.utils.storage.content_file_name
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="repo.document",
                    ),
                ),
            ],
            options={
                "verbose_name": "Document Version",
                "verbose_name_plural": "Document Versions",
                "unique_together": {("parent", "tag")},
            },
        ),
        migrations.AddIndex(
            model_name="document",
            index=models.Index(
                fields=["parent"], name="repo_docume_parent__11fcab_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="document",
            index=models.Index(
                fields=["mimetype"], name="repo_docume_mimetyp_dc4d2d_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="document",
            index=models.Index(
                fields=["created"], name="repo_docume_created_863120_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="document",
            index=models.Index(
                fields=["is_deleted"], name="repo_docume_is_dele_49b89e_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="folder",
            index=models.Index(
                fields=["parent"], name="repo_folder_parent__7f7d57_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="folder",
            index=models.Index(
                fields=["created"], name="repo_folder_created_30ecc3_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="folder",
            index=models.Index(
                fields=["is_deleted"], name="repo_folder_is_dele_f45eb8_idx"
            ),
        ),
        migrations.RunPython(setup_system),
    ]
