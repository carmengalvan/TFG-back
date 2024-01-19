import strawberry

from base.constants import DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from base.models import OrderingChoice


@strawberry.input
class OrderByInput:
    field: str
    ordering: strawberry.enum(OrderingChoice)


@strawberry.input
class PaginationInput:
    page: int | None = DEFAULT_PAGE
    page_size: int | None = DEFAULT_PAGE_SIZE
    order_by: list[OrderByInput] | None = None
