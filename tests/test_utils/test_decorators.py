# using pytest and fixtures to test decorators

import pytest
from utils import sync_timed, async_timed

@pytest.fixture
def mock_sync_timed(monkeypatch):
    def mock_sync_timed(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    monkeypatch.setattr("utils.sync_timed", mock_sync_timed)

@pytest.fixture
def mock_async_timed(monkeypatch):
    def mock_async_timed(func):
        async def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    monkeypatch.setattr("utils.async_timed", mock_async_timed)

def test_sync_timed(mock_sync_timed):
    @sync_timed()
    def test():
        return True
    assert test() == True

def test_async_timed(mock_async_timed):
    @async_timed()
    async def test():
        return True
    assert test() == True
