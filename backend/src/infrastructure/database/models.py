from dataclasses import dataclass
import datetime

@dataclass
class BaseEntity:
    id: str
    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None