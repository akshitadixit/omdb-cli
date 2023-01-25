# test the parser class

import argparse
import pytest
from utils import Parser

@pytest.fixture
def mock_parser(monkeypatch):
    def mock_parser(self, prog, description, usage):
        self.parser = argparse.ArgumentParser(prog=prog, description=description, usage=usage)
        self.parser.add_argument("movie", help="Movie to search for")
        self.parser.add_argument("-y", "--year", help="Year of release")
        self.parser.add_argument("-t", "--type", help="Type of media")
        self.parser.add_argument("-p", "--page", help="Page number")
        self.parser.add_argument("-r", "--rating", help="IMDB rating")
        self.parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
        self.parser.add_argument("-d", "--debug", help="Debug output", action="store_true")
    monkeypatch.setattr("utils.Parser.__init__", mock_parser)

def test_parser(mock_parser):
    parser = Parser(prog="movie")
    assert parser.parse() == {'movie': 'movie', 'year': None, 'type': None, 'page': None, 'rating': None, 'verbose': False, 'debug': False}

def test_parser_with_args(mock_parser):
    parser = Parser(prog="movie")
    assert parser.parse(["-y", "2020"]) == {'movie': 'movie', 'year': '2020', 'type': None, 'page': None, 'rating': None, 'verbose': False, 'debug': False}

def test_parser_wrong_args(mock_parser):
    parser = Parser(prog="movie")
    with pytest.raises(SystemExit):
        parser.parse(["-y", "2020", "-y", "2021"])

def test_parser_with_unknown_args(mock_parser):
    parser = Parser(prog="movie")
    with pytest.raises(SystemExit):
        parser.parse(["-y", "2020", "-z", "2021"])

def test_parser_with_help(mock_parser):
    parser = Parser(prog="movie")
    with pytest.raises(SystemExit):
        parser.parse(["-h"])
