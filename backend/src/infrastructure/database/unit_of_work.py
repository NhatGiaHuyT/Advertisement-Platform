from types import TracebackType
from typing import Any

from infrastructure.database.interfaces import IConnection, ICursor, IQueryBuilder, ITransactionManager, IUnitOfWork


class PostgresUnitOfWork(IUnitOfWork):
    def __init__(self, query: IQueryBuilder, connection: IConnection) -> None:
        self._query = query
        self._connection = connection
        self._pending_new: list[Any] = []
        self._pending_dirty: list[Any] = []
        self._pending_deleted: list[Any] = []
        self._tx_manager: ITransactionManager | None = None

    async def __aenter__(self):
        self._tx_manager = await self._connection.create_transaction()

        await self._tx_manager.__aenter__()
        return self

    async def execute(
        self,
        query: str,
    ) -> ICursor:
        cursor = await self._connection.create_cursor()
        await cursor.execute(query)
        return cursor

    def register_new(self, entity) -> None:
        self._pending_new.append(entity)

    def register_dirty(self, entity) -> None:
        self._pending_dirty.append(entity)

    def register_deleted(self, entity) -> None:
        self._pending_deleted.append(entity)

    def _clear(self) -> None:
        self._pending_new.clear()
        self._pending_dirty.clear()
        self._pending_deleted.clear()

    def rollback(self) -> None:
        self._clear()

    async def commit(self) -> None:
        if not self._pending_new and not self._pending_dirty and not self._pending_deleted:
            return

        await self._flush_new()
        await self._flush_dirty()
        await self._flush_deleted()

        self._clear()

    async def _flush_new(self) -> None:
        async with await self._connection.create_cursor() as cursor:
            for entity in self._pending_new:
                query = self._query.insert(entity).build()
                await cursor.execute(query)

    async def _flush_dirty(self) -> None:
        async with await self._connection.create_cursor() as cursor:
            for entity in self._pending_dirty:
                query = self._query.update(entity.id, entity).build()
                await cursor.execute(query)

    async def _flush_deleted(self) -> None:
        async with await self._connection.create_cursor() as cursor:
            for entity in self._pending_deleted:
                query = self._query.delete().where(id == entity.id).build()
                await cursor.execute(query)

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is not None:
                self._clear()

            elif self._tx_manager:
                await self.commit()
                await self._tx_manager.__aexit__(exc_type, exc_val, exc_tb)

        finally:
            self._tx_manager = None
            await self._connection.close()
