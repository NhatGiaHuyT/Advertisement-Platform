from typing import Protocol


class IHasherEncoder(Protocol):
    async def hash(self, value: str) -> str:
        ...

    async def verify(self, value: str, hashed_value: str) -> bool:
        ...
