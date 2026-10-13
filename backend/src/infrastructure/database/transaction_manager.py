from types import TracebackType

from psycopg import AsyncConnection

from infrastructure.database.interfaces import ITransactionManager


class PostgresTransactionManager(ITransactionManager):
    def __init__(self, connection: AsyncConnection):
        self._transaction = connection.transaction()

    async def __aenter__(self) -> "PostgresTransactionManager":
        await self._transaction.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._transaction.__aexit__(
            exc_type,
            exc_val,
            exc_tb,
        )
