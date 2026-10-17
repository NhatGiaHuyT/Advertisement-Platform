from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from domain.User.user_status import UserStatus
from domain.User.value_objects.created_at import CreatedAt
from domain.User.value_objects.email import Email
from domain.User.value_objects.first_name import FirstName
from domain.User.value_objects.hash_password import HashPassword
from domain.User.value_objects.last_name import LastName
from domain.User.value_objects.username import Username


@dataclass(frozen=True, slots=True)
class User:
    user_id: UUID
    organization_id: UUID
    username: Username
    first_name: FirstName
    last_name: LastName
    created_at: CreatedAt
    email: Email
    user_status: UserStatus
    hash_password: HashPassword

    @classmethod
    def create(
        cls,
        organization_id: UUID,
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        hash_password: str,
    ) -> "User":
        return cls(
            user_id=uuid4(),
            organization_id=organization_id,
            username=Username(username),
            first_name=FirstName(first_name),
            last_name=LastName(last_name),
            created_at=CreatedAt(datetime.now()),
            email=Email(email),
            user_status=UserStatus.ACTIVE,
            hash_password=HashPassword(hash_password),
        )
