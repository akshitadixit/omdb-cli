import os
from utils import Table
from . import Request


class Response:
    def __init__(self, dict, params) -> None:
        self.flag = dict["Response"]
        self.len = dict["totalResults"]
        self.parameters = params
        self._results = dict["Search"]  # list of dicts

    def __str__(self) -> str:
        return str(vars(self))

    @property
    def table(self):
        table = [["Title", "Year", "Type", "imdb_id"]]
        if "imdbRating" in self.parameters:
            table[0].append("imdb_rating")
        if "Genre" in self.parameters:
            table[0].append("   genre     ")

        for result in self._results:
            temp = []
            temp.extend(list(result.values())[:4])
            temp[2], temp[3] = temp[3], temp[2]

            # TODO: make this more efficient to reduce api calls
            if "imdbRating" in self.parameters or "Genre" in self.parameters:
                req = Request()
                res = req.get({"i": result["imdbID"]})
                result = res
                if "imdbRating" in self.parameters:
                    temp.append(result["imdbRating"])
                if "Genre" in self.parameters:
                    temp.append(result["Genre"].replace(", ", ",  \n"))

            table.append(temp)
        return table

    def paginate(self, page):
        return self._results[(page - 1) * 10 : page * 10]

    @property
    def stats(self):
        return int(os.getenv("API_LIMIT"))


class ResponseHandler:
    def __init__(self, response) -> None:
        self.response = response

    def __str__(self) -> str:
        return str(vars(self))

    def _print(self):
        print("Response: ", self.response.flag)
        print("Total Results: ", self.response.len)
        print("Page: ", self.response.parameters["page"])

    def _print_table(self):
        table = Table(*self.response.table)
        table.print()

    def _print_stats(self):
        print(f"Requests left for the day: {self.response.stats}/1000")

    def print(self):
        self._print_table()
        if self.response.parameters["stats"] == True:
            self._print_stats()


if __name__ == "__main__":
    from request import Request

    req = Request()
    res = req.get({"s": "batman", "page": 1, "type": "movie", "i": None})
    res_handler = ResponseHandler(
        Response(
            res, {"s": "batman", "page": 1, "stats": True, "type": "movie", "i": None}
        )
    )
    res_handler.print()
