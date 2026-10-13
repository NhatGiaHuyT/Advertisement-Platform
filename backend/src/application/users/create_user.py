from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from domain.User.model import User
from infrastructure.repositories.user_repository import IUserRepository
from infrastructure.security.password_hasher import IPasswordHasher


@dataclass(frozen=True)
class CreateUserCommand:
    first_name: str
    last_name: str
    username: str
    email: str
    created_at: datetime
    updated_at: datetime | None = None
    password: str


@dataclass(frozen=True)
class CreateUserOutput:
    first_name: str
    last_name: str
    username: str
    email: str


class ICreateUser(Protocol):
    async def execute(self, command: CreateUserCommand) -> CreateUserOutput: ...


class CreateUser(ICreateUser):
    def __init__(self, user_repository: IUserRepository, password_hasher: IPasswordHasher):
        self._user_repository = user_repository
        self.password_hasher = password_hasher

    async def execute(
        self,
        command: CreateUserCommand,
    ) -> CreateUserOutput:
        first_name = command.first_name
        last_name = command.last_name
        username = command.username
        email = command.email
        created_at = command.created_at
        password = command.password
        password_hash = self.password_hasher.hash(password)

        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            created_at=created_at,
            hash_password=password_hash,
        )

        return user
