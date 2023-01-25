# writing tests for app.py

import pytest
from app import App

@pytest.fixture
def mock_app(monkeypatch):
    def mock_app(self):
        self.args = {"movie": "test"}
    monkeypatch.setattr("app.App.__init__", mock_app)

def test_app(mock_app):
    app = App()
    assert app.args == {"movie": "test"}

def test_app_with_args(mock_app):
    app = App()
    assert app.args == {"movie": "test"}

def test_app_with_args_and_search(mock_app):
    app = App()
    assert app.search() == "test"
