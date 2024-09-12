import json


class StatsFilter:
    def __init__(self, id, value=None):
        self.json = {
            "disabled": False,
            "id": id
        }
        if value:
            self.json["value"] = value


class Query:
    def __init__(self):
        self.query = {
            "query": {
                "filters": {
                    "misc_filters": {
                        "disabled": False,
                        "filters": {
                            "ilvl": {"min": 0, "max": 100}
                        }
                    }
                },
                "stats": [
                    {
                        "filters": [],
                        "type": "and"
                    }
                ],
                "status": {"option": "online"}
            },
            "sort": {"price": "asc"}
        }
        with open("config.json") as f:
            self.config_data = json.load(f)

    def add_item_level(self, min=None, max=None):
        minmax = {}
        if min is not None:
            minmax["min"] = min
        if max is not None:
            minmax["max"] = max
        self.query["query"]["filters"]["misc_filters"]["filters"]["ilvl"] = minmax

    def add_stats_filter(self, id, value=None, index=0):
        self.query["query"]["stats"][index]["disabled"] = False
        self.query["query"]["stats"][index]["filters"].append(StatsFilter(id, value).json)
