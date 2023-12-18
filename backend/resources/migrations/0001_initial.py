# Generated by Django 4.2.8 on 2023-12-18 18:11

import datetime
import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DayAvailability",
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
                ("day", models.DateField(verbose_name="day")),
                ("start_time", models.TimeField(verbose_name="start_time")),
                ("end_time", models.TimeField(verbose_name="end_time")),
            ],
            options={
                "verbose_name": "availability",
                "verbose_name_plural": "availabilities",
                "ordering": ("day",),
            },
        ),
        migrations.CreateModel(
            name="Resource",
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
                ("name", models.CharField(max_length=30, verbose_name="name")),
                (
                    "description",
                    models.CharField(max_length=100, verbose_name="description"),
                ),
                (
                    "available_time",
                    models.IntegerField(
                        help_text="The time in which the resource will be available for reservation. In minutes",
                        verbose_name="available_time",
                    ),
                ),
                (
                    "start_date",
                    models.DateField(
                        default=datetime.date.today, verbose_name="start_date"
                    ),
                ),
                ("end_date", models.DateField(verbose_name="end_date")),
            ],
            options={
                "verbose_name": "resource",
                "verbose_name_plural": "resources",
                "ordering": ("start_date",),
            },
        ),
    ]
