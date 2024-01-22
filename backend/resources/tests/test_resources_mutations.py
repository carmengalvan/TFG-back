import json

import pytest
from mixer.backend.django import mixer
from strawberry.django.views import GraphQLView

from backend.schema import schema
from base.factory_test_case import TestBase
from resources.errors import DATE_ERROR, EXISTING_RESOURCE, PAST_DATE
from resources.models import Resource
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

    def test_create_resource_past_date(self):
        variables = {
            "input": {
                "name": "test 1",
                "description": "test 1 description",
                "availableTime": 120,
                "startDate": "2022-02-22",
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

        assert data.get("errors")[0].get("message") == PAST_DATE

    def test_create_resource_date_error(self):
        variables = {
            "input": {
                "name": "test 1",
                "description": "test 1 description",
                "availableTime": 120,
                "startDate": "2024-02-22",
                "endDate": "2024-02-20",
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

        assert data.get("errors")[0].get("message") == DATE_ERROR

    def test_create_resource_existing_resource(self):
        mixer.blend(Resource, user=self.user, name="test 1")
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

        assert data.get("errors")[0].get("message") == EXISTING_RESOURCE
