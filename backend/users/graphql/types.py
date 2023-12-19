from datetime import datetime
from uuid import UUID

import strawberry


@strawberry.type
class UserType:
    id: UUID
    first_name: str
    last_name: str
    email: str
    public_name: str
    created: datetime


@strawberry.type
class UserTypeWeb:
    user: UserType
    token: str
    refresh_token: str
