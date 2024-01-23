from uuid import UUID

import strawberry
from django.core.exceptions import ValidationError
from django.utils import timezone
from strawberry.types import Info
from strawberry_django_jwt.decorators import login_required

from resources.errors import DATE_ERROR, EXISTING_RESOURCE, PAST_DATE, PERMISION_ERROR
from resources.graphql.inputs import ResourceInput, UpdateResourceInput
from resources.graphql.types import ResourceType
from resources.models import Resource


@strawberry.type
class ResourceMutation:
    @strawberry.field(description="Creates a resource")
    @login_required
    def create_resource(self, input: ResourceInput, info: Info) -> ResourceType:
        user = info.context.request.user
        if input.start_date < timezone.now().date():
            raise ValidationError(PAST_DATE)

        if input.start_date >= input.end_date:
            raise ValidationError(DATE_ERROR)

        existing_resource = Resource.objects.filter(
            user=user,
            name=input.name,
            start_date=input.start_date,
            end_date=input.end_date,
            available_time=input.available_time,
        ).first()
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
        Resource.objects.filter(id=id, user=user).delete()
        return True

    @strawberry.field(description="Updates a resource")
    @login_required
    def update_resource(self, input: UpdateResourceInput, info: Info) -> ResourceType:
        user = info.context.request.user
        resource = Resource.objects.filter(user=user, id=input.resource_id).first()
        if not resource:
            raise ValidationError(PERMISION_ERROR)

        updated_fields = {
            "name": input.name or resource.name,
            "description": input.description or resource.description,
            "available_time": input.available_time or resource.available_time,
            "start_date": input.start_date or resource.start_date,
            "end_date": input.end_date or resource.end_date,
            "location": input.location or resource.location,
        }

        if input.start_date:
            if input.start_date < timezone.now().date():
                raise ValidationError(PAST_DATE)
            if input.end_date:
                if input.start_date >= input.end_date:
                    raise ValidationError(DATE_ERROR)
            elif input.start_date >= resource.end_date:
                raise ValidationError(DATE_ERROR)

        existing_resource = Resource.objects.filter(
            user=user,
            name=input.name,
            start_date=input.start_date,
            end_date=input.end_date,
            available_time=input.available_time,
        ).first()
        if existing_resource:
            raise ValidationError(EXISTING_RESOURCE)

        Resource.objects.filter(id=input.resource_id).update(**updated_fields)
        updated_resource = Resource.objects.get(id=input.resource_id)

        return updated_resource
