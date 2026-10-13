from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class HashPassword:
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Password hash cannot be empty.")