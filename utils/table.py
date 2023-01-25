# custom class to print a table in a pretty way
from prettytable import PrettyTable


class Table:
    def __init__(self, *args) -> None:
        self._table = PrettyTable()
        self._table.field_names = args[0]
        self._table.add_rows(args[1:])

    @property
    def table(self):
        return self._table

    def __str__(self) -> str:
        return str(vars(self))

    def _customize(self, **kwargs):
        # TODO: clean this up
        # TODO: add more customization options
        # TODO: add colors
        self._table._top_left_junction_char = kwargs["corners"][0]
        self._table._top_right_junction_char = kwargs["corners"][1]
        self._table._bottom_left_junction_char = kwargs["corners"][2]
        self._table._bottom_right_junction_char = kwargs["corners"][3]
        self._table._top_junction_char = "─"
        self._table._bottom_junction_char = "─"
        self._table._left_junction_char = "│"
        self._table._right_junction_char = "│"
        self._table._junction_char = "┼"
        self._table._horizontal_char = "─"
        self._table._vertical_char = "│"
        # self._table.header_style = "upper"
        self._table.header = True
        self._table.align = "c"
        self._table.border = True
        self._table.hrules = 1
        self._table.vrules = 1

    def print(self):
        self._customize(corners=["╭", "╮", "╰", "╯"])
        print(self._table)


if __name__ == "__main__":
    table = Table(
        ["Title", "Year", "imdbID", "Type", "imdbRating", "Genre"],
        [
            "The Shawshank Redemption",
            "1994",
            "tt0111161",
            "movie",
            "9.3",
            "Crime,  \nDrama",
        ],
        ["The Godfather", "1972", "tt0068646", "movie", "9.2", "Crime,  \nDrama"],
        [
            "The Godfather: Part II",
            "1974",
            "tt0071562",
            "movie",
            "9.0",
            "Crime,  \nDrama",
        ],
        [
            "The Dark Knight",
            "2008",
            "tt0468569",
            "movie",
            "9.0",
            "Action,  \nCrime,  \nDrama",
        ],
    )
    table.print()
