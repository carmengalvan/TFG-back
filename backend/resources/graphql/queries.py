import strawberry
from strawberry.types import Info
from strawberry_django_jwt.decorators import login_required

from base.graphql.inputs import OrderByInput, PaginationInput
from base.graphql.utils import get_paginator, order_queryset
from base.models import OrderingChoice
from resources.graphql.types import PaginatedResourceType
from resources.models import Resource


@strawberry.type
class ResourcesQuery:
    @strawberry.field(description="Returns a list of your resources.")
    @login_required
    def my_resources(
        self, info: Info, pagination: PaginationInput | None
    ) -> PaginatedResourceType:
        user = info.context.request.user
        order_by = pagination.order_by or [
            OrderByInput(field="created", ordering=OrderingChoice.DESC)
        ]
        query = Resource.objects.filter(user=user)

        query = order_queryset(query, order_by)

        return get_paginator(
            query,
            pagination.page_size,
            pagination.page,
            order_by,
            PaginatedResourceType,
        )
