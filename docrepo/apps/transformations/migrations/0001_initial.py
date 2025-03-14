# Generated by Django 4.2.17 on 2024-12-10 22:50

import uuid

import django.db.models.deletion
from django.db import migrations, models

import apps.core.utils.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("repo", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Thumbnail",
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
                    "content_file",
                    models.FileField(
                        upload_to=apps.core.utils.storage.content_file_name
                    ),
                ),
                (
                    "version",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="repo.version"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Preview",
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
                    "content_file",
                    models.FileField(
                        upload_to=apps.core.utils.storage.content_file_name
                    ),
                ),
                (
                    "version",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="repo.version"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
