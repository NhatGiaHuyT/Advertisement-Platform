import unittest
from dataclasses import FrozenInstanceError
from unittest.mock import AsyncMock

import pytest

from domain.User.user_model import User


class TestUserModel(unittest.IsolatedAsyncioTestCase):
    def setup(self):
        fake_user = User(
            user_id=1,
            organization_id=2,
            first_name="John",
            last_name="Doe",
            username="johndoe",
            created_at="2023-01-01T00:00:00Z",
            email="johndoe@example.com",
            user_status="active",
            hash_password="hashedpassword123",
        )
        return fake_user

    async def test_create_user(self):
        user = self.setup()
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.organization_id, 2)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.username, "johndoe")
        self.assertEqual(user.email, "johndoe@example.com")
        self.assertEqual(user.user_status, "active")
        self.assertEqual(user.hash_password, "hashedpassword123")
        self.assertEqual(user.created_at, "2023-01-01T00:00:00Z")

    async def test_async_fetch_user(self):
        mock_fetch = AsyncMock(return_value=self.setup())
        result = await mock_fetch()
        self.assertEqual(result, self.setup())
        mock_fetch.assert_awaited_once()

    async def test_user_is_immutable(self):
        mock_fetch = AsyncMock(return_value=self.setup())
        result = await mock_fetch()
        with pytest.raises(FrozenInstanceError, match="cannot assign to field 'first_name'"):
            result.first_name = "Jane"
