import requests
import json
import os
import dotenv
import requests_cache


class Request:
    def __init__(self) -> None:
        self.dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(self.dotenv_file)
        self._API_KEY = os.getenv("API_KEY")
        self.url = f"https://www.omdbapi.com/?apikey={self._API_KEY}"
        self._cache = requests_cache.install_cache(
            "movie_cache", backend="redis", expire_after=86400
        )

    def __str__(self) -> str:
        return str(vars(self))

    def _build(self, params):
        if "i" in params and params["i"] is not None:
            self.url += f"&i={params['i']}"
        else:
            self.url += f"&s={params['s']}"
            if "page" in params and params["page"]:
                self.url += f"&page={params['page']}"

        if "type" in params and params["type"]:
            self.url += f"&type={params['type']}"

    def _api_call(self, params):
        self._build(params)
        result = requests.get(url=self.url)
        data = json.loads(result.text)
        # TODO : run a cron job to reset api_limit to 1000 at 12:00 AM everyday
        api_limit = int(os.getenv("API_LIMIT"))
        if not result.from_cache:
            api_limit -= 1
            os.environ["API_LIMIT"] = str(api_limit)
            dotenv.set_key(self.dotenv_file, "API_LIMIT", os.environ["API_LIMIT"])
        if api_limit == 0:
            return {"Response": "False", "Error": "API limit exceeded"}
        return data

    def get(self, params):
        # if there are no params except stats, return the stats
        if len(params) == 2 and ("stats" in params and params["stats"] == True ):
            print(f"Requests left for the day: {os.getenv('API_LIMIT')}/1000")
            return None
        return self._api_call(params)
