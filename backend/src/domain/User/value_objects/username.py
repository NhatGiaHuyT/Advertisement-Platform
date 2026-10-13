import re
from dataclasses import dataclass

_USERNAME_PATTERN = re.compile(
    r"^[a-zA-Z0-9](?!.*[._]{2})[a-zA-Z0-9._]*[a-zA-Z0-9]$"
)

@dataclass(frozen=True, slots=True)
class Username:
    value: str

    def __post_init__(self):
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("Username cannot be empty.")

        if(len(normalized) > 50):
            raise ValueError("Username cannot be longer than 50 characters.")

        if not _USERNAME_PATTERN.fullmatch(normalized):
            raise ValueError("Invalid username format.")

        object.__setattr__(self, "value", normalized)
