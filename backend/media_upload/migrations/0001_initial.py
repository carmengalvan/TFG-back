# Generated by Django 3.0.6 on 2021-01-25 18:56

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UploadToken",
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
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="created date"
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="modified date"
                    ),
                ),
                ("token", models.CharField(max_length=255, null=True)),
            ],
            options={
                "ordering": ("-created",),
                "abstract": False,
            },
        ),
    ]
