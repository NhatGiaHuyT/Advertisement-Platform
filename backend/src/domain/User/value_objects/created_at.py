from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True, slots=True)
class CreatedAt:
    value: datetime

    def __post_init__(self) -> None:
        if self.value is None:
            raise ValueError("CreatedAt cannot be None.")

        if self.value.utcoffset() is None:
            raise ValueError(
                "CreatedAt must be a timezone-aware datetime."
            )

        object.__setattr__(self, "value", self.value.astimezone(timezone.utc))