import asyncio
import sys
import unittest

from common.configs import DatabaseConfig
from infrastructure.database.connection_pool import PostgresConnectionPool
from infrastructure.database.query_builder import QueryBuilder
from infrastructure.database.unit_of_work import PostgresUnitOfWork

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class TestPostgresUnitOfWorkIntegration(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        config = DatabaseConfig(
            host="localhost",
            port="5432",
            database="postgres",
            user="postgres",
            password="password",
        )

        self.pool = PostgresConnectionPool(
            config=config,
            min_size=1,
            max_size=2,
        )

        await self.pool.open()
        await self.pool.wait_until_ready()

        self.query_builder = QueryBuilder(table_name="test_users")

        async with await self._create_uow() as uow:
            cursor = await uow.execute(
                """
                CREATE TABLE IF NOT EXISTS test_users (
                    id UUID PRIMARY KEY,
                    username TEXT NOT NULL
                )
                """
            )
            await cursor.close()

    async def asyncTearDown(self):
        async with await self._create_uow() as uow:
            cursor = await uow.execute(
                """
                DROP TABLE IF EXISTS test_users
                """
            )
            await cursor.close()

        await self.pool.close()

    async def _create_uow(self) -> PostgresUnitOfWork:
        connection = await self.pool.acquire()
        return PostgresUnitOfWork(self.query_builder, connection)

    async def test_real_transaction_commits(self):
        # Transaction 1: Insert and let it auto-commit on clean context exit
        async with await self._create_uow() as uow:
            cursor = await uow.execute(
                """
                INSERT INTO test_users (id, username)
                VALUES ('11111111-1111-1111-1111-111111111111', 'commit_user')
                """
            )
            await cursor.close()

        # Transaction 2: Read it back using a completely fresh UoW instance
        async with await self._create_uow() as uow:
            cursor = await uow.execute(
                """
                SELECT username FROM test_users WHERE username = 'commit_user'
                """
            )
            result = await cursor.fetch_one()
            await cursor.close()

        self.assertIsNotNone(result)
        self.assertEqual(result["username"], "commit_user")

    async def test_real_transaction_rolls_back(self):
        # Transaction 1: Force an exception to test psycopg's automatic rollback
        with self.assertRaises(RuntimeError):
            async with await self._create_uow() as uow:
                cursor = await uow.execute(
                    """
                    INSERT INTO test_users (id, username)
                    VALUES ('22222222-2222-2222-2222-222222222222', 'rollback_user')
                    """
                )
                await cursor.close()
                raise RuntimeError("force rollback")

        # Transaction 2: Verify the user DOES NOT exist using a fresh UoW
        async with await self._create_uow() as uow:
            cursor = await uow.execute(
                """
                SELECT username FROM test_users WHERE username = 'rollback_user'
                """
            )
            result = await cursor.fetch_one()
            await cursor.close()

        self.assertIsNone(result)
