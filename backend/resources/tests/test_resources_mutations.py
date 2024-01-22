import json

import pytest
from strawberry.django.views import GraphQLView

from backend.schema import schema
from base.factory_test_case import TestBase
from resources.tests.requests.mutations import CREATE_RESOURCE
from users.models import User


@pytest.mark.django_db()
class TestResourcesMutations(TestBase):
    def test_create_resource(self):
        variables = {
            "input": {
                "name": "test 1",
                "description": "test 1 description",
                "availableTime": 120,
                "startDate": "2024-02-22",
                "endDate": "2024-02-27",
                "location": "Sevilla",
            }
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": CREATE_RESOURCE,
                "variables": variables,
            },
            content_type="application/json",
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        user = User.objects.get(id=self.user.id)

        resource = data.get("data")
        assert len(resource) == 1
        assert resource.get("createResource").get("user").get("email") == user.email
