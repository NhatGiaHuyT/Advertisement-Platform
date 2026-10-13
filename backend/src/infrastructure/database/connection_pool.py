from psycopg_pool import AsyncConnectionPool
from psycopg.errors import OperationalError
from psycopg_pool import PoolTimeout

from common.configs import DatabaseConfig
from .interfaces import IConnectionPool, IConnection
from .connection import PostgresConnection


class PostgresConnectionPool(IConnectionPool):
    def __init__(
        self,
        config: DatabaseConfig,
        min_size: int = 5,
        max_size: int = 20,
    ):
        self._config = config

        conninfo = (
            f"host={config.host} "
            f"port={config.port} "
            f"dbname={config.database} "
            f"user={config.user} "
            f"password={config.password}"
        )

        self._pool = AsyncConnectionPool(
            conninfo=conninfo,
            min_size=min_size,
            max_size=max_size,
            kwargs={
                "autocommit": False,
            },
            open=False
        )

    async def open(self) -> None:
        await self._pool.open()

    async def wait_until_ready(self) -> None:
        await self._pool.wait()

    async def acquire(self) -> IConnection:
        try:
            raw_connection = await self._pool.getconn()

            return PostgresConnection(
                connection=raw_connection,
                pool=self._pool,
            )

        except (OperationalError, PoolTimeout) as exc:
            raise RuntimeError(
                "Unable to acquire a database connection."
            ) from exc

    async def release(self, connection: IConnection) -> None:
        await connection.close()

    async def close(self) -> None:
        await self._pool.close()