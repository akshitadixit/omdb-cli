# use pytest to write unit tests for Request module
# use fixtures to mock api calls

import pytest
from ...api import Request
from ...api import Response, ResponseHandler
from ...utils import Parser

params = Parser(prog="movie").parse()


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


def test_createRequestObject():
    req = Request()
    assert req is not None

def test_createResponseObject():
    res = Response()
    assert res is not None

def test_createResponseHandlerObject():
    res = ResponseHandler()
    assert res is not None

def test_getResponseFlag(mock_api_call):
    req = Request()
    res = req.get(params)
    res = ResponseHandler(Response(res, params))
    assert res.response.flag == "True"

def test_buildTable(mock_api_call):
    req = Request()
    res = req.get(params)
    res = ResponseHandler(Response(res, params))
    table = res.response.table
    assert table[0][0] == "Title"
    assert table[0][1] == "Year"
    assert table[0][2] == "imdb_id"
    assert table[0][3] == "Type"

def test_get(mock_api_call):
    req = Request()
    res = req.get(params)
    res = ResponseHandler(Response(res, params))
    assert res.response.len == "2"

def test_paginate(mock_api_call):
    req = Request()
    res = req.get(params)
    res = ResponseHandler(Response(res, params))
    assert len(res.response.paginate(1)) == 10

def test_stats():
    req = Request()
    res = req.get(params)
    res = ResponseHandler(Response(res, params))
    assert res.response.stats == 1000

def test_getError(mock_api_call_error):
    req = Request()
    res = req.get(params)
    res = ResponseHandler(Response(res, params))
    assert res.response.flag == "False"

def test_getTimeout(mock_api_call_timeout):
    req = Request()
    res = req.get(params)
    res = ResponseHandler(Response(res, params))
    assert res.response.flag == "False"

