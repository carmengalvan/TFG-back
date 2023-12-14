from datetime import date

from django.db import models

from base.models import SimpleModel


class Resource(SimpleModel):
    user = models.ForeignKey(
        "users.User",
        verbose_name="user",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name="name",
        max_length=30,
        null=False,
    )
    description = models.CharField(
        verbose_name="description",
        max_length=100,
        null=False,
    )
    available_time = models.TimeField(
        verbose_name="available_time",
        null=False,
        help_text="Time resource is available for reservation",
    )
    start_date = models.DateField(
        verbose_name="start_date",
        null=False,
        default=date.today,
    )
    end_date = models.DateField(
        verbose_name="end_date",
        null=False,
    )

    class Meta:
        verbose_name = "resource"
        verbose_name_plural = "resources"
        ordering = ("start_date",)


class DayAvailability(SimpleModel):
    resource = models.ForeignKey(
        Resource,
        verbose_name="resource",
        on_delete=models.CASCADE,
    )

    day = models.DateField(
        verbose_name="day",
        null=False,
    )

    start_time = models.TimeField(
        verbose_name="start_time",
        null=False,
    )

    end_time = models.TimeField(
        verbose_name="end_time",
        null=False,
    )

    class Meta:
        verbose_name = "availability"
        verbose_name_plural = "availabilities"
        ordering = ("day",)
