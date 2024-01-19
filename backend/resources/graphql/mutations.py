from uuid import UUID

import strawberry
from django.core.exceptions import ValidationError
from strawberry.types import Info
from strawberry_django_jwt.decorators import login_required

from resources.errors import DATE_ERROR, EXISTING_RESOURCE
from resources.graphql.inputs import ResourceInput
from resources.graphql.types import ResourceType
from resources.models import Resource


@strawberry.type
class ResourceMutation:
    @strawberry.field(description="Creates a resource")
    @login_required
    def create_resource(self, input: ResourceInput, info: Info) -> ResourceType:
        user = info.context.request.user

        if input.start_date >= input.end_date:
            raise ValidationError(DATE_ERROR)

        existing_resource = Resource.objects.filter(user=user, name=input.name).first()
        if existing_resource:
            raise ValidationError(EXISTING_RESOURCE)

        resource = Resource.objects.create(
            user=user,
            name=input.name,
            description=input.description,
            available_time=input.available_time,
            start_date=input.start_date,
            end_date=input.end_date,
            location=input.location,
        )

        return resource

    @strawberry.field(description="Delete your resource")
    @login_required
    def delete_resource(self, id: UUID, info: Info) -> bool:
        user = info.context.request.user
        resource = Resource.objects.filter(id=id, user=user)
        if not resource:
            raise ValidationError(
                "Resource not found or you don't have permission to update it."
            )

        resource.delete()
        return True
