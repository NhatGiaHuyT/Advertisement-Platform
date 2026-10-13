import pytest
from dataclasses import FrozenInstanceError
import unittest
from unittest.mock import AsyncMock

from domain.User.value_objects.username import Username

class TestUsernameValueObject(unittest.IsolatedAsyncioTestCase):
    async def test_async_fetch_username(self):
        fake_username = Username(value="example")

        mock_fetch = AsyncMock(return_value=fake_username)

        result = await mock_fetch()

        self.assertEqual(result.value, "example")
        mock_fetch.assert_awaited_once()
    
    async def test_username_is_normalized(self):
        fake_username = Username(value="     example      ")

        mock_fetch = AsyncMock(return_value=fake_username)
        result = await mock_fetch()
        self.assertEqual(result.value, "example")

    async def test_username_empty_raises_error(self):
        with pytest.raises(ValueError, match="Username cannot be empty."):
            Username(value="")

    async def test_username_max_length_raises_error(self):
        make_email = lambda length: f"{'a' * (length)}"
        with pytest.raises(ValueError, match="Username cannot be longer than 50 characters."):
            Username(value=make_email(51))

    async def test_username_is_immutable(self):
        fake_username = Username(value="example")
        mock_fetch = AsyncMock(return_value=fake_username)
        result = await mock_fetch()
        with pytest.raises(FrozenInstanceError, match="cannot assign to field 'value'"):
            result.value = "helloworld"
            