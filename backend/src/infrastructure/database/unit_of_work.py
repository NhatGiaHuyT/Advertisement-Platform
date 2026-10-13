from .interfaces import IUnitOfWork, IQueryBuilder

class PostgresUnitOfWork(IUnitOfWork):
    def __init__(self, query: IQueryBuilder):
        self._query = query
        self._pending_new = []
        self._pending_dirty = []
        self._pending_deleted = []
    
    def register_new(self, entity) -> None:
        self._pending_new.append(entity)

    def register_dirty(self, entity) -> None:
        self._pending_dirty.append(entity)

    def register_deleted(self, entity) -> None:
        self._pending_deleted.append(entity)

    async def commit(self) -> None:
        if not self._pending_new and not self._pending_dirty and not self._pending_deleted:
            return

        await self._flush_new()
        await self._flush_dirty()
        await self._flush_deleted()

        self._clear()

    async def _flush_new(self) -> None:
        for entity in self._pending_new:
            query = self._query.insert(entity).build()
            return query
        
    async def _flush_dirty(self) -> None:
        for entity in self._pending_dirty:
            query, params = self._query.update(entity).where(id=entity.id).build()
            return query, params

    async def _flush_deleted(self) -> None:
        for entity in self._pending_deleted:
            query, params = self._query.delete(entity).where(id=entity.id).build()
            return query, params

    def _clear(self) -> None:
        self._pending_new.clear()
        self._pending_dirty.clear()
        self._pending_deleted.clear()

    async def rollback(self) -> None:
        self._clear()
