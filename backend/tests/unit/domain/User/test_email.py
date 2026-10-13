import pytest
from dataclasses import FrozenInstanceError
import unittest
from unittest.mock import AsyncMock

from domain.User.value_objects.email import Email

class TestEmailValueObject(unittest.IsolatedAsyncioTestCase):
    async def test_async_fetch_email(self):
        fake_email = Email(value="example@example.com")

        mock_fetch = AsyncMock(return_value=fake_email)

        result = await mock_fetch()

        self.assertEqual(result.value, "example@example.com")
        mock_fetch.assert_awaited_once()
    
    async def test_email_is_normalized(self):
        fake_email = Email(value="     Example@exampLe.cOm      ")

        mock_fetch = AsyncMock(return_value=fake_email)
        result = await mock_fetch()
        self.assertEqual(result.value, "example@example.com")

    async def test_email_empty_raises_error(self):
        with pytest.raises(ValueError, match="Email cannot be empty."):
            Email(value="")

    async def test_email_max_length_raises_error(self):
        make_email = lambda length: f"a@{'a' * (length - 6)}.com"
        with pytest.raises(ValueError, match="Email cannot be longer than 254 characters."):
            Email(value=make_email(255))

    async def test_email_regex_success(self):
        fake_email = Email(value="a@a.org")

        mock_fetch = AsyncMock(return_value=fake_email)
        result = await mock_fetch()

        self.assertEqual(result.value, "a@a.org")

    async def test_email_regex_raises_error(self):
        with pytest.raises(ValueError, match="Invalid email format."):
            Email(value="wafaf.dada@lol")

    async def test_email_is_immutable(self):
        fake_email = Email(value="a@a.com")
        mock_fetch = AsyncMock(return_value=fake_email)
        result = await mock_fetch()
        with pytest.raises(FrozenInstanceError, match="cannot assign to field 'value'"):
            result.value = "diff@diff.com"
            