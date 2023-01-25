# custom parser class for app.py

from argparse import Action, ArgumentParser
from typing import Any, Dict, Iterable, List, NoReturn, Optional, Union


class Parser(ArgumentParser):
    def __init__(self, *args, **kwargs) -> None:
        kwargs["description"] = "A simple CLI for the OMDB API"
        kwargs["epilog"] = "Source Code: https://github.com/akshitadixit/omdb-cli"
        super().__init__(*args, **kwargs)

    def parse(self, args: Optional[List[str]] = None) -> Dict[str, Union[str, bool]]:
        self.add_argument("-t", "--title")
        self.add_argument("-i", "--id")
        self.add_argument("-y", "--year")
        self.add_argument("--type")
        self.add_argument("-p", "--page", default="1")
        self.add_argument("-s", "--stats", default=False, action="store_true")
        self.add_argument(
            "-e",
            "--extra",
            choices=["imdb_rating", "genre"],
            action="append",
            default=[],
        )

        args = vars(self.parse_args(args))
        params: Dict[str, Union[str, bool]] = {}

        for key in args:
            match key:
                case "title":
                    params["s"] = args[key]
                case "id" | "year":
                    params[key[0]] = args[key]
                case "page" | "type" | "stats":
                    params[key] = args[key]
                case "extra":
                    for extra in args[key]:
                        match extra:
                            case "imdb_rating":
                                params["imdbRating"] = True
                            case "genre":
                                params["Genre"] = True

        parameters = {key: params[key] for key in params if params[key] is not None}
        return parameters

    def check_empty(self, args: Iterable[Any]) -> bool:
        return not any(args)
