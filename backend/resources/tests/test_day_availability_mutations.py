import json

import pytest
from mixer.backend.django import mixer
from strawberry.django.views import GraphQLView

from backend.schema import schema
from base.factory_test_case import TestBase
from resources.errors import TIME_ERROR
from resources.models import Resource
from resources.tests.requests.mutations import CREATE_DAY_AVAILABILITY


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
        print("DATA", data)

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
