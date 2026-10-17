from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from uuid import UUID

from domain.User.user_model import User
from domain.User.value_objects.raw_password import RawPassword
from infrastructure.repositories.user_repository import IUserRepository
from infrastructure.security.password_hasher import IPasswordHasher


@dataclass(frozen=True)
class CreateUserCommand:
    organization_id: UUID
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    created_at: datetime


@dataclass(frozen=True)
class CreateUserOutput:
    id: UUID
    first_name: str
    last_name: str
    username: str
    email: str
    created_at: datetime
    user_status: str


class ICreateUser(Protocol):
    async def execute(self, command: CreateUserCommand) -> CreateUserOutput: ...


class CreateUser(ICreateUser):
    def __init__(self, user_repository: IUserRepository, password_hasher: IPasswordHasher):
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    async def execute(self, command: CreateUserCommand) -> CreateUserOutput:
        raw_password = RawPassword(command.password)
        password_hash = self._password_hasher.hash(raw_password)

        user = User.create(
            organization_id=command.organization_id,
            username=command.username,
            first_name=command.first_name,
            last_name=command.last_name,
            email=command.email,
            hash_password=str(password_hash),
        )

        await self._user_repository.persist(user)

        return CreateUserOutput(
            id=user.user_id,
            first_name=user.first_name.value,
            last_name=user.last_name.value,
            username=user.username.value,
            email=user.email.value,
            created_at=user.created_at.value,
            user_status=user.user_status.value,
        )
