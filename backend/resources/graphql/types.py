import uuid
from datetime import date

import strawberry

from base.graphql.types import PaginatedQueryType


@strawberry.type
class ResourceType:
    id: uuid.UUID
    name: str
    description: str
    available_time: int
    start_date: date
    end_date: date
    location: str


@strawberry.type
class PaginatedResourceType(PaginatedQueryType):
    edges: list[ResourceType]
