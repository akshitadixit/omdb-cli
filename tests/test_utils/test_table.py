# test table module with pytest

import pytest
from utils import Table

@pytest.fixture
def mock_table(monkeypatch):
    def mock_table(self, data, headers):
        self.data = data
        self.headers = headers
    monkeypatch.setattr("utils.Table.__init__", mock_table)

def test_table(mock_table):
    table = Table(data=[["test"]], headers=["test"])
    assert table.data == [["test"]]
    assert table.headers == ["test"]

def test_table_with_headers(mock_table):
    table = Table(data=[["test"]], headers=["test"])
    assert table.table == "test"

def test_table_without_headers(mock_table):
    table = Table(data=[["test"]])
    assert table.table == "test"

def test_table_with_headers_and_data(mock_table):
    table = Table(data=[["test"]], headers=["test"])
    assert table.table == "test"

def test_table_without_headers_and_data(mock_table):
    table = Table()
    assert table.table == ""
