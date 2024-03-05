from collections import defaultdict

import strawberry
from strawberry.types import Info
from strawberry_django_jwt.decorators import login_required

from base.graphql.inputs import PaginationInput
from base.graphql.utils import get_paginator
from resources.graphql.inputs import MonthInput
from resources.graphql.types import DayAvailabilityGroupType, PaginatedResourceType
from resources.models import DayAvailability, Resource


@strawberry.type
class ResourcesQuery:
    @strawberry.field(description="Returns a list of your resources.")
    @login_required
    def my_resources(
        self, info: Info, pagination: PaginationInput | None = None
    ) -> PaginatedResourceType:
        if pagination is None:
            pagination = {}
        user = info.context.request.user
        query = Resource.objects.filter(user=user).order_by("-created")

        return get_paginator(
            query,
            pagination.page_size,
            pagination.page,
            PaginatedResourceType,
        )

    @strawberry.field(description="Returns a list of your daily availabilities.")
    @login_required
    def my_daily_availability(
        self, info: Info, input: MonthInput
    ) -> list[DayAvailabilityGroupType]:
        user = info.context.request.user
        resources = Resource.objects.filter(user=user)
        query = DayAvailability.objects.filter(
            resource__in=resources, day__year=input.year, day__month=input.month
        ).order_by("day", "start_time")

        availability_groups = defaultdict(list)
        for availability in query:
            availability_groups[availability.day].append(availability)

        result = []
        for day, availabilities in availability_groups.items():
            day_availability_group = DayAvailabilityGroupType(
                day=day, availabilities=availabilities
            )
            result.append(day_availability_group)

        return result
