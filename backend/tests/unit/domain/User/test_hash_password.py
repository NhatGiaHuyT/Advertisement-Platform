import unittest
from dataclasses import FrozenInstanceError

import pytest

from domain.User.value_objects.raw_password import RawPassword


class TestRawPasswordValidation(unittest.IsolatedAsyncioTestCase):
    def test_empty_password_raises_error(self):
        with pytest.raises(
            ValueError,
            match="Password cannot be empty.",
        ):
            RawPassword(value="")

    def test_password_with_whitespace_raises_error(self):
        with pytest.raises(
            ValueError,
            match="Password cannot have whitespaces.",
        ):
            RawPassword(value="password 123")

    def test_password_with_leading_whitespace_raises_error(self):
        with pytest.raises(
            ValueError,
            match="Password cannot have whitespaces.",
        ):
            RawPassword(value=" password123")

    def test_password_with_trailing_whitespace_raises_error(self):
        with pytest.raises(
            ValueError,
            match="Password cannot have whitespaces.",
        ):
            RawPassword(value="password123 ")

    def test_password_shorter_than_8_characters_raises_error(self):
        with pytest.raises(
            ValueError,
            match="Password must be at least 8 characters.",
        ):
            RawPassword(value="1234567")

    def test_password_of_exactly_8_characters_is_valid(self):
        password = RawPassword(value="12345678")

        assert password.value == b"12345678"

    def test_password_of_exactly_64_characters_is_valid(self):
        password = RawPassword(value="a" * 64)

        assert password.value == b"a" * 64

    def test_password_longer_than_64_characters_raises_error(self):
        with pytest.raises(
            ValueError,
            match="Password cannot be longer than 64 characters.",
        ):
            RawPassword(value="a" * 65)


class TestRawPasswordRepresentation(unittest.IsolatedAsyncioTestCase):
    def test_password_is_encoded_as_utf8(self):
        password = RawPassword(value="Pässword123")

        assert password.value == "Pässword123".encode()

    def test_unicode_password_is_validated_by_character_length(self):
        password = RawPassword(value="é" * 8)

        assert password.value == ("é" * 8).encode("utf-8")

    def test_password_value_is_bytes(self):
        password = RawPassword(value="password123")

        assert isinstance(password.value, bytes)

    def test_password_is_immutable(self):
        password = RawPassword(value="password123")

        with pytest.raises(
            FrozenInstanceError,
            match="cannot assign to field 'value'",
        ):
            password.value = b"different"
