import unittest
from unittest.mock import AsyncMock, Mock

from domain.User.user_model import User
from infrastructure.database.query_builder import QueryBuilder
from infrastructure.database.unit_of_work import PostgresUnitOfWork


class TestUnitOfWork(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.fake_query = Mock(spec=QueryBuilder(table_name="fake_user"))
        self.fake_user = Mock(
            spec=User(
                user_id=1,
                organization_id=2,
                first_name="John",
                last_name="Doe",
                username="johndoe",
                created_at="2023-01-01T00:00:00Z",
                email="johndoe@example.com",
                user_status="active",
                hash_password="hashed_password",
            ),
        )

        self.fake_cursor = AsyncMock()
        self.fake_cursor.__aenter__.return_value = self.fake_cursor

        self.fake_connection = AsyncMock()
        self.fake_connection.create_cursor.return_value = self.fake_cursor

        self.uow = PostgresUnitOfWork(self.fake_query, self.fake_connection)

    async def test_register_new_adds_to_pending(self):
        self.uow.register_new(self.fake_user)
        self.assertEqual(len(self.uow._pending_new), 1)
        self.assertEqual(len(self.uow._pending_dirty), 0)
        self.assertEqual(len(self.uow._pending_deleted), 0)

    async def test_register_dirty_adds_to_pending(self):
        self.uow.register_dirty(self.fake_user)
        self.assertEqual(len(self.uow._pending_new), 0)
        self.assertEqual(len(self.uow._pending_dirty), 1)
        self.assertEqual(len(self.uow._pending_deleted), 0)

    async def test_register_deleted_adds_to_pending(self):
        self.uow.register_deleted(self.fake_user)
        self.assertEqual(len(self.uow._pending_new), 0)
        self.assertEqual(len(self.uow._pending_dirty), 0)
        self.assertEqual(len(self.uow._pending_deleted), 1)

    async def test_flush_new(self):
        expected_query = "INSERT INTO fake_user VALUES param"
        self.fake_query.insert.return_value.build.return_value = expected_query

        self.uow.register_new(self.fake_user)
        await self.uow._flush_new()

        self.fake_query.insert.assert_called_once_with(self.fake_user)
        self.fake_cursor.execute.assert_awaited_once_with(
            expected_query,
        )

    async def test_commit_with_no_pending_entities_does_not_flush(self):
        await self.uow.commit()
        self.fake_cursor.execute.assert_not_awaited()

    async def test_commit_flushes_and_clears_pending(self):
        expected_query = "INSERT INTO fake_user VALUES param"
        self.fake_query.insert.return_value.build.return_value = expected_query

        self.uow.register_new(self.fake_user)
        await self.uow.commit()

        self.fake_cursor.execute.assert_awaited_once_with(expected_query)
        self.assertEqual(len(self.uow._pending_new), 0)

    async def test_rollback_clears_pending(self):
        self.uow.register_new(self.fake_user)
        self.uow.register_dirty(self.fake_user)
        self.uow.register_deleted(self.fake_user)
        self.uow.rollback()
        self.assertEqual(len(self.uow._pending_new), 0)
        self.assertEqual(len(self.uow._pending_dirty), 0)
        self.assertEqual(len(self.uow._pending_deleted), 0)
