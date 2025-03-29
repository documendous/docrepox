# Generated by Django 4.2.18 on 2025-01-16 17:12

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("repo", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DocumentIndex",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("content", models.TextField(blank=True, null=True)),
                ("is_indexed", models.BooleanField(default=False)),
                ("last_indexed", models.DateTimeField(blank=True, null=True)),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="repo.document"
                    ),
                ),
            ],
            options={
                "verbose_name": "Document Index",
                "verbose_name_plural": "Document Indexes",
            },
        ),
    ]
