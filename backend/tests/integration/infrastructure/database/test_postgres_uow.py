import sys
import asyncio

import unittest

from infrastructure.database.unit_of_work import PostgresUnitOfWork
from infrastructure.database.connection_pool import PostgresConnectionPool
from infrastructure.database.query_builder import QueryBuilder
from common.configs import DatabaseConfig


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class TestPostgresUnitOfWorkIntegration(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        config = DatabaseConfig(
            host="localhost",
            port=5432,
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

        async with PostgresUnitOfWork(self.pool) as uow:
            await uow.execute("""
                CREATE TABLE IF NOT EXISTS test_users (
                    id UUID PRIMARY KEY,
                    username TEXT NOT NULL
                )
            """)

    async def asyncTearDown(self):
        async with PostgresUnitOfWork(self.pool) as uow:
            await uow.execute("""
                DROP TABLE IF EXISTS test_users
            """)

        await self.pool.close()

    async def test_real_transaction_commits(self):
        uow = PostgresUnitOfWork(self.pool)

        async with uow:
            await uow.execute(
                """
                INSERT INTO test_users (
                    id,
                    username
                )
                VALUES (%s, %s)
                """,
                (
                    "11111111-1111-1111-1111-111111111111",
                    "commit_user",
                ),
            )

        async with uow:
            await uow.execute(
                """
                SELECT username
                FROM test_users
                WHERE username = %s
                """,
                ("commit_user",),
            )

            result = await uow.fetch_one()

        self.assertIsNotNone(result)
        self.assertEqual(result["username"], "commit_user")

    async def test_real_transaction_rolls_back(self):
        uow = PostgresUnitOfWork(self.pool)

        with self.assertRaises(RuntimeError):
            async with uow:
                await uow.execute(
                    """
                    INSERT INTO test_users (
                        id,
                        username
                    )
                    VALUES (%s, %s)
                    """,
                    (
                        "22222222-2222-2222-2222-222222222222",
                        "rollback_user",
                    ),
                )

                raise RuntimeError("force rollback")

        async with uow:
            await uow.execute(
                """
                SELECT username
                FROM test_users
                WHERE username = %s
                """,
                ("rollback_user",),
            )

            result = await uow.fetch_one()

        self.assertIsNone(result)