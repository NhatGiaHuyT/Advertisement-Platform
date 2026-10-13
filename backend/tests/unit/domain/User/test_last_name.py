import unittest
from dataclasses import FrozenInstanceError
from unittest.mock import AsyncMock

import pytest

from domain.User.value_objects.last_name import LastName


class TestLastNameValueObject(unittest.IsolatedAsyncioTestCase):
    async def test_async_fetch_last_name(self):
        fake_last_name = LastName(value="Doe")

        mock_fetch = AsyncMock(return_value=fake_last_name)

        result = await mock_fetch()

        self.assertEqual(result.value, "Doe")
        mock_fetch.assert_awaited_once()

    async def test_last_name_is_normalized(self):
        fake_username = LastName(value="     Doe      ")

        mock_fetch = AsyncMock(return_value=fake_username)
        result = await mock_fetch()
        self.assertEqual(result.value, "Doe")

    async def test_last_name_regex_raises_error(self):
        with pytest.raises(ValueError, match="Last name can only contain letters, spaces, hyphens, or apostrophes."):
            LastName("D0e")

    async def test_last_name_empty_raises_error(self):
        with pytest.raises(ValueError, match="Last name cannot be empty."):
            LastName(value="")

    async def test_last_name_max_length_raises_error(self):
        def make_last_name(length):
            return f"{'a' * (length)}"

        with pytest.raises(ValueError, match="Last name cannot be longer than 50 characters."):
            LastName(value=make_last_name(51))

    async def test_last_name_is_immutable(self):
        fake_last_name = LastName(value="Doe")
        mock_fetch = AsyncMock(return_value=fake_last_name)
        result = await mock_fetch()
        with pytest.raises(FrozenInstanceError, match="cannot assign to field 'value'"):
            result.value = "Jane"
