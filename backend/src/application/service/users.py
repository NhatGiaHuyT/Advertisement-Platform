from typing import Protocol
from uuid import UUID
from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=True)
class CreateUserInput:
    first_name: str
    last_name: str
    username: str
    email: str
    password: str

@dataclass(frozen=True)
class CreateUserDTO:
    first_name: str
    last_name: str
    username: str
    email: str

#TODO: integrate later once other layers are established
@dataclass(frozen=True)
class CreateUserOutput:
    id: UUID
    first_name: str
    last_name: str
    username: str
    email: str
    created_at: datetime
    is_active: bool

class UserService(Protocol):
    async def create_user(self, input: CreateUserInput) -> CreateUserDTO:
        pass
