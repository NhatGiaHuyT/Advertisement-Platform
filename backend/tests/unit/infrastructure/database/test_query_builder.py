import unittest

from infrastructure.database.interfaces import IQueryBuilder
from infrastructure.database.query_builder import QueryBuilder


class TestQueryBuilder(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.builder = QueryBuilder(table_name="fake_user")

    async def test_query_builder_create_empty_table(self):
        query = self.builder.create_table()

        assert isinstance(query, IQueryBuilder)
        assert str(query) == 'CREATE TABLE "fake_user" ()'

    async def test_query_builder_create_table(self):
        query = self.builder.create_table("id", "first_name", "last_name")

        assert isinstance(query, IQueryBuilder)
        assert str(query) == 'CREATE TABLE "fake_user" ("id","first_name","last_name")'

    async def test_query_builder_drop_table(self):
        query = self.builder.drop_table()

        assert isinstance(query, IQueryBuilder)
        assert str(query) == 'DROP TABLE "fake_user"'

    async def test_query_builder_select_columns(self):
        query = self.builder.select(
            "id",
            "first_name",
            "last_name",
        )

        assert isinstance(query, IQueryBuilder)
        assert str(query) == 'SELECT "id","first_name","last_name" FROM "fake_user"'

    async def test_query_builder_select_all(self):
        query = self.builder.select()

        assert isinstance(query, IQueryBuilder)
        assert str(query) == 'SELECT * FROM "fake_user"'

    async def test_query_builder_insert(self):
        query = self.builder.insert(1, "email", "created_at")

        assert isinstance(query, IQueryBuilder)
        assert str(query) == "INSERT INTO \"fake_user\" VALUES (1,'email','created_at')"

    async def test_query_builder_update(self):
        query = self.builder.update("email", "new_email")
        assert isinstance(query, IQueryBuilder)

        assert str(query) == 'UPDATE "fake_user" SET "email"=\'new_email\''

        query = query.where(self.builder._table.id == 1)

        assert str(query) == 'UPDATE "fake_user" SET "email"=\'new_email\' WHERE "id"=1'

    async def test_query_builder_build(self):
        query = self.builder.insert(1, "email", "created_at").build()

        assert isinstance(query, str)
        assert str(query) == query
