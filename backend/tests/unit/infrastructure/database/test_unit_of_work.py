import unittest
from unittest.mock import Mock

from domain.User.model import User
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
            )
        )
        self.uow = PostgresUnitOfWork(self.fake_query)

    async def rollback(self):
        self.uow.register_new(self.fake_user)
        self.uow.register_dirty(self.fake_user)
        self.uow.register_deleted(self.fake_user)

        self.assertEqual(len(self.uow._pending_new), 0)
        self.assertEqual(len(self.uow._pending_dirty), 0)
        self.assertEqual(len(self.uow._pending_deleted), 0)

    async def test_flush_new(self):
        expected_query = Mock(spec=QueryBuilder)

        self.fake_query.insert.return_value.build.return_value = expected_query

        self.uow.register_new(self.fake_user)

        query = await self.uow._flush_new()

        self.fake_query.insert.assert_called_once_with(self.fake_user)
        self.assertEqual(query, expected_query)
