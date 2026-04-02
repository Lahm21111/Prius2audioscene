import os
from typing import Dict

from utils.utils import generate_token

from .table import Table
from .map import Map

schema = {
    "type": "object",
    "properties": {
        "token": {"type": "string"},
        "logfile": {"type": "string"},
        "vehicle": {"type": "string"},
        "date_captured": {"type": "string"},
        "location": {"type": "string"},
    },
    "required": [
        "token",
        "logfile",
        "vehicle",
        "date_captured",
        "location",
    ],
}


class Log(Table):

    def __init__(self) -> None:
        super().__init__()
        self._schema = schema
        self._path = os.path.join(self._path, "log.json")

    def create_record(self, map: Map) -> str:
        token = generate_token()
        data = {
            "token": token,
            "logfile": token,
            "vehicle": "EDGAR",
            "date_captured": "2024-01-01",
            "location": map.name,
        }
        map.add_log(token)
        super().create_record(data)
        return token
