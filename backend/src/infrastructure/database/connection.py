from typing import Any

from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool

from .interfaces import (
    IConnection,
    ICursor,
    ITransactionManager,
)
from .cursor import PostgresCursor
from .transaction_manager import PostgresTransactionManager


class PostgresConnection(IConnection):
    def __init__(
        self,
        connection: AsyncConnection,
        pool: AsyncConnectionPool,
    ):
        self._connection = connection
        self._pool = pool
        self._released = False

    async def ensure_connected(self) -> AsyncConnection:
        if self._connection is None:
            raise RuntimeError("Connection has already been released.")

        if self._connection.closed:
            raise RuntimeError("Database connection is closed.")

        return self._connection

    async def create_cursor(self) -> ICursor:
        connection = await self.ensure_connected()

        cursor = connection.cursor()

        return PostgresCursor(cursor)

    async def create_transaction(self) -> ITransactionManager:
        connection = await self.ensure_connected()

        return PostgresTransactionManager(connection)

    async def close(self) -> None:
        """
        Return the borrowed connection to the pool.

        This does NOT physically close the connection.
        """
        if self._released:
            return

        if self._connection is None:
            return

        await self._pool.putconn(self._connection)

        self._connection = None
        self._released = True