import pytest
from dataclasses import FrozenInstanceError
import unittest
from datetime import datetime, timezone

from domain.User.value_objects.created_at import CreatedAt

class TestCreatedAtValueObject(unittest.IsolatedAsyncioTestCase):
    async def test_created_at_cannot_be_none(self):
        with pytest.raises(ValueError):
            CreatedAt(value=None)
    
    async def test_created_at_must_be_timezone_aware(self):
        with pytest.raises(ValueError):
            CreatedAt(value=datetime.now(timezone.utc).replace(tzinfo=None))

    async def test_created_at_is_immutable(self):
        created_at = CreatedAt(value=datetime.now(timezone.utc))
        with pytest.raises(FrozenInstanceError):
            created_at.value = datetime.now(timezone.utc)