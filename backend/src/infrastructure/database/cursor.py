from types import TracebackType
from typing import Any

from psycopg import AsyncCursor
from psycopg.rows import DictRow, dict_row

from infrastructure.database.interfaces import ICursor


class PostgresCursor(ICursor):
    def __init__(self, cursor: AsyncCursor[DictRow]):
        self._cursor = cursor
        self._cursor.row_factory = dict_row

    async def __aenter__(self) -> "PostgresCursor":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def execute(
        self,
        query: str,
    ) -> None:
        await self._cursor.execute(query)

    async def fetch_many(self, size: int) -> list[dict[str, Any]]:
        return await self._cursor.fetchmany(size)

    async def fetch_one(self) -> dict[str, Any] | None:
        return await self._cursor.fetchone()

    async def close(self) -> None:
        if not self._cursor.closed:
            await self._cursor.close()
