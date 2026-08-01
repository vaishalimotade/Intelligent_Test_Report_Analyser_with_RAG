import pytest
from unittest.mock import patch
from backend.app.services.flaky import analyze_flaky_tests
from backend.app.services.database import database

@pytest.mark.asyncio
async def test_analyze_flaky_tests_empty(monkeypatch):
    async def fake_fetch(query):
        return []
    monkeypatch.setattr(database, 'fetch_all', fake_fetch)
    result = await analyze_flaky_tests()
    assert result == []
