from typing import Any

from psycopg import AsyncCursor
from psycopg.rows import dict_row

from infrastructure.database.interfaces import ICursor


class PostgresCursor(ICursor):
    def __init__(self, cursor: AsyncCursor):
        self._cursor = cursor
        self._cursor.row_factory = dict_row

    async def execute(
        self,
        query: str,
        params: tuple | dict | None = None,
    ) -> None:
        await self._cursor.execute(query, params)

    async def fetch_many(self, size: int) -> list[dict[str, Any]]:
        return await self._cursor.fetchmany(size)

    async def fetch_one(self) -> dict[str, Any] | None:
        return await self._cursor.fetchone()

    async def close(self) -> None:
        if not self._cursor.closed:
            await self._cursor.close()
