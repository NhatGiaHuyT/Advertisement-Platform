import unittest
from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from domain.User.value_objects.created_at import CreatedAt


class TestCreatedAtValueObject(unittest.IsolatedAsyncioTestCase):
    async def test_created_at_cannot_be_none(self):
        with pytest.raises(ValueError):
            CreatedAt(value=None)

    async def test_created_at_must_be_timezone_aware(self):
        with pytest.raises(ValueError):
            CreatedAt(value=datetime.now(UTC).replace(tzinfo=None))

    async def test_created_at_is_immutable(self):
        created_at = CreatedAt(value=datetime.now(UTC))
        with pytest.raises(FrozenInstanceError):
            created_at.value = datetime.now(UTC)
