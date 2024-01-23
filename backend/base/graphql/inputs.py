import strawberry

from base.constants import DEFAULT_PAGE, DEFAULT_PAGE_SIZE


@strawberry.input
class PaginationInput:
    page: int | None = DEFAULT_PAGE
    page_size: int | None = DEFAULT_PAGE_SIZE
