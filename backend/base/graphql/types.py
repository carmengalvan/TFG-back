import strawberry


@strawberry.type
class PageInfoType:
    page: int
    pages: int
    has_next: bool
    has_prev: bool
    total_results: int
    order_by: str


@strawberry.type
class PaginatedQueryType:
    page_info: PageInfoType
