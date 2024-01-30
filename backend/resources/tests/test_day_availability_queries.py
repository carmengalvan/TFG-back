import json

import pytest
from mixer.backend.django import mixer

from base.factory_test_case import TestBase
from resources.models import DayAvailability, Resource
from resources.tests.requests.queries import DAY_AVAILABILITY_ITEMS


@pytest.mark.django_db()
class TestResourcesQueries(TestBase):
    def test_my_daily_availabilities(self):
        resource = mixer.blend(Resource, user=self.user)
        mixer.blend(
            DayAvailability,
            resource=resource,
            day="2030-02-02",
            start_time="09:00:00",
            end_time="13:00:00",
        )
        mixer.blend(
            DayAvailability,
            resource=resource,
            day="2030-02-10",
            start_time="09:00:00",
            end_time="14:00:00",
        )
        mixer.blend(
            DayAvailability,
            resource=resource,
            day="2030-02-20",
            start_time="08:00:00",
            end_time="13:00:00",
        )

        variables = {
            "pagination": {
                "page": 1,
                "pageSize": 5,
            },
        }

        response = self.post(
            query=DAY_AVAILABILITY_ITEMS, user=self.user, variables=variables
        )

        data = json.loads(response.content.decode())
        resources = data.get("data").get("myDailyAvailability").get("edges")
        assert len(resources) == 3

        assert resources[0].get("day") == "2030-02-20"
        assert resources[1].get("startTime") == "09:00:00"
        assert resources[2].get("endTime") == "13:00:00"

    def test_my_daily_availabilities_without_pagination(self):
        resource = mixer.blend(Resource, user=self.user)
        mixer.blend(
            DayAvailability,
            resource=resource,
            day="2030-02-02",
            start_time="09:00:00",
            end_time="13:00:00",
        )
        mixer.blend(
            DayAvailability,
            resource=resource,
            day="2030-02-10",
            start_time="09:00:00",
            end_time="14:00:00",
        )
        mixer.blend(
            DayAvailability,
            resource=resource,
            day="2030-02-20",
            start_time="08:00:00",
            end_time="13:00:00",
        )

        variables = {}

        response = self.post(
            query=DAY_AVAILABILITY_ITEMS, user=self.user, variables=variables
        )

        data = json.loads(response.content.decode())
        assert data.get("data") is None
