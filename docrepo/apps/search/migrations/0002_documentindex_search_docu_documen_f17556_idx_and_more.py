# Generated by Django 4.2.20 on 2025-03-12 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("search", "0001_initial"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="documentindex",
            index=models.Index(
                fields=["document"], name="search_docu_documen_f17556_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="documentindex",
            index=models.Index(
                fields=["is_indexed"], name="search_docu_is_inde_2433b6_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="documentindex",
            index=models.Index(
                fields=["last_indexed"], name="search_docu_last_in_792de2_idx"
            ),
        ),
    ]
