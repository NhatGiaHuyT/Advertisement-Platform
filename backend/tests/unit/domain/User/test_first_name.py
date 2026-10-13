import pytest
from dataclasses import FrozenInstanceError
import unittest
from unittest.mock import AsyncMock

from domain.User.value_objects.first_name import FirstName

class TestFirstNameValueObject(unittest.IsolatedAsyncioTestCase):
    async def test_async_fetch_first_name(self):
        fake_first_name = FirstName(value="John")

        mock_fetch = AsyncMock(return_value=fake_first_name)

        result = await mock_fetch()

        self.assertEqual(result.value, "John")
        mock_fetch.assert_awaited_once()
    
    async def test_first_name_is_normalized(self):
        fake_username = FirstName(value="     John      ")

        mock_fetch = AsyncMock(return_value=fake_username)
        result = await mock_fetch()
        self.assertEqual(result.value, "John")

    async def test_first_name_regex_raises_error(self):
        with pytest.raises(ValueError, match="First name can only contain letters, spaces, hyphens, or apostrophes."):
            FirstName("J0hn")

    async def test_first_name_empty_raises_error(self):
        with pytest.raises(ValueError, match="First name cannot be empty."):
            FirstName(value="")

    async def test_first_name_max_length_raises_error(self):
        make_first_name = lambda length: f"{'a' * (length)}"
        with pytest.raises(ValueError, match="First name cannot be longer than 50 characters."):
            FirstName(value=make_first_name(51))

    async def test_first_name_is_immutable(self):
        fake_first_name = FirstName(value="John")
        mock_fetch = AsyncMock(return_value=fake_first_name)
        result = await mock_fetch()
        with pytest.raises(FrozenInstanceError, match="cannot assign to field 'value'"):
            result.value = "Jane"
            