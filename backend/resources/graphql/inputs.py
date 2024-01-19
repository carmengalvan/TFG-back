from datetime import date

import strawberry


@strawberry.input
class ResourceInput:
    name: str
    description: str
    available_time: int
    start_date: date
    end_date: date
    location: str
