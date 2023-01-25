# test ResponseHandler and Response classes

import pytest
from ...api.request import Request
from ...api.response import Response, ResponseHandler

params = {
    "s": "batman",
    "page": 1,
    "type": "movie",
}

@pytest.fixture
def mock_api_call(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        match args[0]:
            case "https://www.omdbapi.com/?apikey=12345&s=shawshank&page=1&type=movie":
                return MockResponse(
                    {
                        "Search": [
                            {
                                "Title": "The Shawshank Redemption",
                                "Year": "1994",
                                "imdbID": "tt0111161",
                                "Type": "movie",
                                "Poster": "N/A",
                            },
                            {
                                "Title": "The Shawshank Redemption",
                                "Year": "2017",
                                "imdbID": "tt5290382",
                                "Type": "movie",
                                "Poster": "N/A",
                            },
                        ],
                        "totalResults": "2",
                        "Response": "True",
                    },
                    200,
                )
            case _:
                return MockResponse(
                    {
                        "Search": [
                            {
                                "Title": "The Shawshank Redemption",
                                "Year": "2017",
                                "imdbID": "tt5290382",
                                "Type": "movie",
                                "Poster": "N/A",
                            }
                        ],
                        "totalResults": "1",
                        "Response": "True",
                    },
                    200,
                )

    monkeypatch.setattr("requests.get", mock_get)

@pytest.fixture
def mock_api_call_error(monkeypatch):
    # error response
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(
            {"Response": "False", "Error": "API limit exceeded"}, 200
        )

    monkeypatch.setattr("requests.get", mock_get)

@pytest.fixture
def mock_api_call_timeout(monkeypatch):
    # timeout response
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse({"Response": "False", "Error": "Timeout"}, 200)

    monkeypatch.setattr("requests.get", mock_get)


def test_getResponseFlag(mock_api_call):
    req = Request()
    res = req.get(params)
    res_handler = ResponseHandler(res)
    assert res_handler.get_response_flag() == True

def test_buildTable(mock_api_call):
    req = Request()
    res = req.get(params)
    res_handler = ResponseHandler(res)
    table = res_handler.build_table()
    assert table[0][0] == "Title"
    assert table[0][1] == "Year"
    assert table[0][2] == "imdb_id"
    assert table[0][3] == "Type"

def test_get(mock_api_call):
    req = Request()
    res = req.get(params)
    res_handler = ResponseHandler(res)
    assert res_handler.get() == 2

def test_paginate(mock_api_call):
    req = Request()
    res = req.get(params)
    res_handler = ResponseHandler(res)
    assert len(res_handler.paginate(1)) == 10

def test_stats():
    req = Request()
    res = req.get(params)
    res_handler = ResponseHandler(res)
    assert res_handler.stats() == 1000

def test_getError(mock_api_call_error):
    req = Request()
    res = req.get(params)
    res_handler = ResponseHandler(res)
    assert res_handler.get() == 0

def test_responseHandler():
    res = Response()
    res_handler = ResponseHandler(res)
    assert res_handler.get_response_flag() == False

