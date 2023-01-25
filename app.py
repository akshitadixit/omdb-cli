from api import Request
from api import Response, ResponseHandler
from utils import sync_timed, Parser

params = Parser(prog="movie").parse()


@sync_timed()
def main():
    req = Request()
    res = req.get(params)
    if res is None:
        return
    res = ResponseHandler(Response(res, params))
    res.print()


if __name__ == "__main__":
    main()
