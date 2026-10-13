from uuid import UUID
from typing import Protocol

from ...domain.User.model import User


class IUserRepository(Protocol):
    async def create(self, user: User) -> None:
        ...

    async def get_by_id(self, user_id: UUID) -> User | None:
        ...

    async def get_by_email(self, email: str) -> bool: 
        ...

class PostgresUserRepository(IUserRepository):
    