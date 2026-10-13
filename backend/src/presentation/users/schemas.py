from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class CreateUserRequest(BaseModel):
    first_name: Annotated[str, Field(min_length=2, max_length=30)]
    last_name: Annotated[str, Field(min_length=2, max_length=30)]
    username: Annotated[str, Field(min_length=2, max_length=30)]
    email: Annotated[EmailStr, Field(min_length=2, max_length=30)]
    created_at: Annotated[datetime, Field(default_factory=lambda: datetime.now(UTC).replace(tzinfo=None))]
    updated_at: Annotated[datetime | None, Field(default=None)]
    deleted_at: Annotated[datetime | None, Field(default=None)]
    is_deleted: Annotated[bool, Field(default=False)]
    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=64,
            description=(
                "Password must be at least 8 characters long and include a number,"
                "uppercase letter, lowercase letter, and special character"
            ),
            examples=["Str1ngst!"],
            pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$",
        ),
    ]


# TODO: This is wrong, this should be a response from bounced back from later layers to the HTTP, solve this later
class CreateUserResponse(BaseModel):
    id: Annotated[UUID, Field(examples=["9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"])]
    first_name: Annotated[str, Field(min_length=2, max_length=30)]
    last_name: Annotated[str, Field(min_length=2, max_length=30)]
    username: Annotated[str, Field(min_length=2, max_length=30)]
    email: Annotated[EmailStr, Field(min_length=2, max_length=30)]
    is_active: Annotated[bool, Field(default=False)]
    created_at: Annotated[datetime, Field(default_factory=datetime.now)]
