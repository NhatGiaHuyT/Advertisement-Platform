from dataclasses import dataclass
from uuid import UUID

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

