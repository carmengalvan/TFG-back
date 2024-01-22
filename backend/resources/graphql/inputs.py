from datetime import date
from uuid import UUID

import strawberry


@strawberry.input
class ResourceInput:
    name: str
    description: str
    available_time: int
    start_date: date
    end_date: date
    location: str


@strawberry.input
class UpdateResourceInput:
    resource_id: UUID
    name: str | None = None
    description: str | None = None
    available_time: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    location: str | None = None
