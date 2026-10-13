from dataclasses import dataclass
import re


_EMAIL_PATTERN = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)

@dataclass(frozen=True, slots=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()

        if not normalized:
            raise ValueError("Email cannot be empty.")
        
        if len(normalized) > 254:
            raise ValueError("Email cannot be longer than 254 characters.")

        if not _EMAIL_PATTERN.fullmatch(normalized):
            raise ValueError("Invalid email format.")
        
        object.__setattr__(self, "value", normalized)