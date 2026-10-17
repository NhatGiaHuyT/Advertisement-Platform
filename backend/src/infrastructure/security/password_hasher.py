from typing import Protocol

from argon2 import PasswordHasher

from domain.User.value_objects.hash_password import HashPassword
from domain.User.value_objects.raw_password import RawPassword


class IPasswordHasher(Protocol):
    def hash(self, value: RawPassword) -> HashPassword: ...

    def verify(
        self,
        value: RawPassword,
        hashed_value: HashPassword,
    ) -> bool: ...


class Argon2PasswordHasher(IPasswordHasher):
    def __init__(self) -> None:
        self._hasher = PasswordHasher()

    def hash(self, value: RawPassword) -> HashPassword:
        hashed_value = self._hasher.hash(value.value)
        return HashPassword(value=hashed_value)

    def verify(
        self,
        value: RawPassword,
        hashed_value: HashPassword,
    ) -> bool:
        return self._hasher.verify(
            hashed_value.value,
            value.value,
        )
