from typing import Protocol
from uuid import UUID

from domain.User.user_model import User


class IUserRepository(Protocol):
    async def persist(self, user: User) -> None: ...

    async def get_by_id(self, user_id: UUID) -> User | None: ...

    async def get_by_email(self, email: str) -> bool: ...


class PostgresUserRepository(IUserRepository):
    pass
