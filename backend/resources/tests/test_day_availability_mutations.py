import json

import pytest
from mixer.backend.django import mixer
from strawberry.django.views import GraphQLView

from backend.schema import schema
from base.factory_test_case import TestBase
from resources.errors import TIME_ERROR
from resources.models import DayAvailability, Resource
from resources.tests.requests.mutations import (
    CREATE_DAY_AVAILABILITY,
    DELETE_DAY_AVAILABILITY,
)
from users.models import User


@pytest.mark.django_db()
class TestDayAvailabilityMutations(TestBase):
    def test_create_day_availability(self):
        resource = mixer.blend(Resource)

        variables = {
            "resourceId": resource.id,
            "input": {
                "day": "2030-02-04",
                "startTime": "10:00:00",
                "endTime": "13:00:00",
            },
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": CREATE_DAY_AVAILABILITY,
                "variables": variables,
            },
            content_type="application/json",
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())

        day_availability = data.get("data")
        assert len(day_availability) == 1
        assert (
            day_availability.get("createDayAvailability").get("resource").get("name")
            == resource.name
        )

    def test_create_day_availability_time_error(self):
        resource = mixer.blend(Resource)

        variables = {
            "resourceId": resource.id,
            "input": {
                "day": "2030-02-04",
                "startTime": "10:00:00",
                "endTime": "09:00:00",
            },
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": CREATE_DAY_AVAILABILITY,
                "variables": variables,
            },
            content_type="application/json",
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())

        assert data.get("errors")[0].get("message") == TIME_ERROR

    def test_delete_day_availability(self):
        day_availability = mixer.blend(DayAvailability)
        variables = {
            "id": str(day_availability.id),
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": DELETE_DAY_AVAILABILITY,
                "variables": variables,
            },
            content_type="application/json",
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        day_availability = data.get("data").get("deleteDayAvailability")
        assert day_availability is True

    def test_delete_another_users_day_availability(self):
        user = mixer.blend(User)
        resource = mixer.blend(Resource, user=user)
        day_availability = mixer.blend(DayAvailability, resource=resource)
        variables = {
            "id": str(day_availability.id),
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": DELETE_DAY_AVAILABILITY,
                "variables": variables,
            },
            content_type="application/json",
        )
        request.user = self.user
        assert len(DayAvailability.objects.all()) == 1
