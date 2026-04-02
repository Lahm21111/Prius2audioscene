import os

from .table import Table

schema = {
    "type": "object",
    "properties": {
        "category": {"type": "string"},
        "filename": {"type": "string"},
        "log_tokens": {"type": "array"},
        "token": {"type": "string"},
    },
    "required": ["category", "filename", "log_tokens", "token"],
}


class Map(Table):

    def __init__(self) -> None:
        super().__init__()
        self._schema = schema
        self._path = os.path.join(self._path, "map.json")
        self.name = "Munich"

        data = {
            "category": "IMS",
            "filename": "wiesn_map.png",
            "log_tokens": [],
            "token": "ed816fb25c16886c9232debb9b63b6a9",
        }

        self.create_record(data)

    def add_log(self, log_token: str):
        self.records[-1]["log_tokens"].append(log_token)
