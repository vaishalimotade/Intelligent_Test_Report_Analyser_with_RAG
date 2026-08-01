import pytest
from unittest.mock import patch
from backend.app.services.failure import get_failure_patterns
from backend.app.services.database import database

@pytest.mark.asyncio
async def test_get_failure_patterns_empty(monkeypatch):
    async def fake_fetch(query):
        return []
    monkeypatch.setattr(database, 'fetch_all', fake_fetch)
    result = await get_failure_patterns()
    assert result == []
