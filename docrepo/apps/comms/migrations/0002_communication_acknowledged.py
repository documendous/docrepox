# Generated by Django 4.2.17 on 2025-01-02 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comms", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="communication",
            name="acknowledged",
            field=models.BooleanField(default=False),
        ),
    ]
